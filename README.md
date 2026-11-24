# step-inspect · ZNGL 几何体检落地页

一个**纯静态、零依赖**的营销落地页：向客户说明「打开 STEP，先看清再谈打印」的
几何体检服务，并附一页脱敏样例报告。

- 页面只含截图、说明、报价与 `mailto:` 表单；**不提供任何软件下载**。
- **不含** ZNGL `dist/`、引擎、ZNKernel-II 内核、SDK、许可逻辑或密钥。
- **不收集数据**：无第三方脚本、无 cookie、无统计；表单只在本机生成邮件草稿。

## 目录结构

| 路径 | 作用 |
|---|---|
| `index.html` | 落地页（单文件，内联 CSS + 约 40 行表单脚本） |
| `sample-report.html` | 1 页样例报告（脱敏，虚构客户；A4 打印 1 页） |
| `img/` | 三张真机截图 + `SHA256SUMS.txt` |
| `manifest.json` | 发布清单：文件、字节、SHA256、验证记录 |
| `README-DEPLOY.md` | 部署说明（GitHub Pages / Gitee Pages / 阿里云 OSS） |
| `README.md` | 本文件 |

## 本地起（零构建）

直接双击 `index.html` 即可：页面不 `fetch` 任何资源，`file://` 下可用。

需要 HTTP 环境时（例如检查相对路径），任选一种：

```powershell
# Python 3
python -m http.server 8080
# 或 Node（一次性）
npx --yes serve . -l 8080
```

然后打开 <http://127.0.0.1:8080/>，样例报告在 `/sample-report.html`。

上线后 5 分钟自检与三种部署方案见 [`README-DEPLOY.md`](README-DEPLOY.md)。

## License

**MIT 只覆盖代码/页面；营销文案与图片保留版权。** 详见 [`LICENSE`](LICENSE)。

| 范围 | 是否 MIT | 说明 |
|---|---|---|
| `index.html`、`sample-report.html` 的 HTML/CSS/JS 源码 | 是 | 可复用、修改、再分发 |
| 页面里的营销文案（服务描述、报价、交付口径、FAQ、社交链接区） | 否 | © 2026 haidi-ai（ZNGL），保留所有权利 |
| 样例报告文字 | 否 | 同上（客户为虚构） |
| `img/` 截图与图片 | 否 | 同上，仅用于展示本页 |
| `README*.md`、`manifest.json`、`SHA256SUMS.txt` 文本 | 否 | 供参考与部署，可链接/署名引用 |
| ZNGL 引擎 / `dist/` / ZNKernel-II 内核 / 许可逻辑 | 不在本仓库 | 不随本仓库授权 |

可以自由链接本仓库或线上页面；简短引用并署名（评论、评测）无需许可。

## 边界（诚实清单）

- 报价与交期为展示口径，**不构成承诺**。
- 页面未接表单服务、未接统计；`mailto:` 收件箱为公开业务邮箱。
- 部署方案为步骤说明，具体条款/配额以各平台当前官方公告为准。
