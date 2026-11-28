# -*- coding: utf-8 -*-
"""ZNKernel-II bench-v0 verifier: recompute input SHA256 and verdicts.

Usage:
  python verify.py --cli <znk2_cli.exe> [--dir .] [--license <lic>]
Exit 0 = all pass; 1 = any mismatch; 2 = setup error.
"""
import argparse, hashlib, json, os, subprocess, sys


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def summary3(vs):
    vs = vs or {}
    return {k: vs.get(k) for k in ("allow", "reject", "cannot_judge")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cli", required=True)
    ap.add_argument("--dir", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--license", default=os.environ.get("ZNK2_LICENSE_FILE"))
    a = ap.parse_args()
    root = a.dir
    exp = json.load(open(os.path.join(root, "expected.json"), encoding="utf-8"))
    env = os.environ.copy()
    if a.license:
        env["ZNK2_LICENSE_FILE"] = a.license
    fails, n = [], 0
    for c in exp["public_cases"]:
        n += 1
        cid = c["id"]
        inp = os.path.join(root, c["input"])
        if not os.path.exists(inp):
            print("FAIL", cid, "missing input", inp)
            fails.append(cid)
            continue
        got = sha(inp)
        if got != c["input_sha256"]:
            print("FAIL", cid, "sha", got[:16], "!=", c["input_sha256"][:16])
            fails.append(cid)
            continue
        if c.get("request"):
            req = json.load(open(os.path.join(root, c["request"]), encoding="utf-8"))
            p = subprocess.run([a.cli, "--json", "-"], input=json.dumps(req).encode(),
                               cwd=root, env=env, capture_output=True, timeout=900)
        else:
            p = subprocess.run([a.cli, "adjudicate", "--file", c["input"]],
                               cwd=root, env=env, capture_output=True, timeout=900)
        raw = p.stdout.decode("utf-8-sig", "replace")
        try:
            d = json.loads(raw)
        except Exception as e:
            print("FAIL", cid, "parse", e, raw[:120])
            fails.append(cid)
            continue
        body = d.get("result", d)
        e = c["expected"]
        if c["kind"] == "na-counterexample":
            res = (body.get("results") or [{}])[0]
            ok = (res.get("verdict") == e["verdict"]
                  and res.get("applicability") == e["applicability"]
                  and summary3(body.get("verdict_summary")) == summary3(e["verdict_summary"]))
            got_s = "%s/%s" % (res.get("verdict"), res.get("applicability"))
        else:
            rules = {r.get("id"): r.get("verdict") for r in body.get("results", [])}
            exp_rules = {r["id"]: r["verdict"] for r in e["rules"]}
            ok = (summary3(body.get("verdict_summary")) == summary3(e["verdict_summary"])
                  and rules == exp_rules)
            got_s = str(summary3(body.get("verdict_summary")))
        print(("PASS" if ok else "FAIL"), cid, got_s, "rc=%s" % p.returncode)
        if not ok:
            fails.append(cid)
    print("SUMMARY", "PASS" if not fails else "FAIL", "%d/%d" % (n - len(fails), n),
          ("fail=%s" % ",".join(fails)) if fails else "")
    return 0 if not fails else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("ERROR", type(e).__name__, e)
        sys.exit(2)
