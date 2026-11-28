# ZNKernel-II 判定基准集 v0（公开件）

可复算的判定基准：每件给出**输入件 + 2.40 实测期望 + 复算命令 + SHA256**。
目的不是让人“相信”结论，而是让人用同一 CLI 跑出同一个结果。

## 版本

- 内核 **ZNKernel-II 2.40.0**；CLI `znk2_cli.exe`，SHA256 `5bc7a310f4aa7992549218d7028069140fdbbba75ead669532232cae3be9cce1`。
- 运行需 `ZNK2_LICENSE_FILE`（内部许可）。未设许可时 CLI 会拒绝运行，这是预期行为。

## 件数：6（全部自建，无客户数据）

| id | 件 | 规则 | 2.40 期望 |
|---|---|---|---|
| NA01 | draft-0p5 | `manufacturing/draft_angle` | **reject**（minDraftDeg≈0.5 < 1.0） |
| NA02 | interference | `assembly/interference` | **reject**（interferenceVolume=1000 > 0） |
| NA03 | blind-hole-ld | `manufacturing/hole_depth_ratio` | **reject**（L/D=7.5 > 5.0） |
| NA04 | wall-uneven | `manufacturing/wall_thickness_uniformity` | **reject**（variation=0.75 > 0.25） |
| NA05 | opening-transition | `quality/opening_radius` | **reject**（openingRadius=0.1 < 0.2） |
| C01 | flange | 全 20 规则 | allow 15 / reject 0 / cannot_judge 5（5 条 CJ 均 not_applicable） |

`cannot_judge` 是**未决**，不是通过；超时、非 0 退出同样不是通过。

## 复算

```powershell
$cli = 'E:\ai-crew-assets\ZNKernel-II\dist-2.40\znk2_cli.exe'
$env:ZNK2_LICENSE_FILE = 'E:\ai-crew-assets\ZNKernel-II\licenses\internal\znk2-internal.lic'
cd bench
Get-Content requests/NA01.json -Raw | & $cli --json -    # 单规则
& $cli adjudicate --file inputs/C01-flange.step           # 全 20 规则
python verify.py --cli $cli                               # 一键逐件校验
```

## 目录

```
bench/
  README.md          本文件
  expected.json      6 条公开：输入 SHA256 + 期望 verdict + 复算命令
  MANIFEST.sha256    逐文件 SHA256（sha256sum -c 可校验）
  verify.py          复算校验器（SHA + verdict）
  inputs/            6 件输入（STEP + 自建 recipe）
  requests/          NA01–05 的 CLI stdin JSON
  verdicts/          上述命令的 2.40 原始响应
```

## 边界

- 本仓只含自建件，不含任何客户件；客户件经授权仅限内部验证，绝不入公开仓。
- 每件可复算；输入 SHA256 不符即视为基准失效。
- 本基准集不覆盖装配体多 body、NURBS 多轮廓、torus 一般布尔等范围外场景。
