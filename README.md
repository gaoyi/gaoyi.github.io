# gaoyi.github.io — 维护说明

新版个人主页（2026-11 重构）。**纯静态、零运行时依赖**：系统字体（大标题 Georgia/宋体 + 正文苹方/微软雅黑系统栈）、单一样式表（`assets/css/main.css`）、无 JavaScript、无外部 CDN——任何网络环境（包括国内）都能正常渲染。

**设计语言**：编辑排版风格——深海军蓝（#06101b）+ 青色点缀（#80d6ef）、衬线大标题配无衬线正文、eyebrow 眉标 + 数字编号（01/02/03）、明暗分带（深色 hero/页头 → 浅色内容带 → 深色页脚）。改样式只动 `assets/css/main.css`。

## 页面结构

| 文件 | 内容 |
|------|------|
| `index.html` / `indexEN.html` | 首页（**`index.html` 为中文，是默认落地页**；`indexEN.html` 为英文）：深色 hero、数据带、简介与新闻、代表性成果、研究方向卡 |
| `research.html` / `researchCN.html` | 板块一·Research 总览：banner 内两排导航胶囊（按应用/按方法），全部卡片可点击进入子页面 |
| `research/*.html` / `research/*CN.html` | 10 个子领域页面（**由脚本生成，不要手改**）：顶部综述卡 + 胶囊导航 + 每篇论文一张带图卡片 |
| `software.html` / `softwareCN.html` | 板块二·Open Science and Software：开源社区贡献与六个软件项目 |
| `publications.html` / `publicationsCN.html` | 论文列表（**由脚本生成，不要手改**） |
| `data/publications.json` | 论文数据（完整列表的唯一维护入口） |
| `data/areas.json` | 子领域数据（各领域的代表论文、要点、图片；**改这里再跑 build_areas.py**） |
| `tools/build_pubs.py` | 论文列表页生成脚本 |
| `tools/build_areas.py` | 子领域页面生成脚本 |
| `tools/build_figures.py` | ABUS 检出率对比柱状图生成脚本，产出 `images/fig-abus-cdr-cn.svg` / `-en.svg` |
| `tools/render_paper_shots.py` | 批量把论文 PDF 首页渲染成卡片截图（`images/areas/<id>.jpg`） |
| `tools/extract_pubs.py` | 一次性迁移工具（从旧版 HTML 提取，平常不用） |
| `images/areas/` | 子领域论文配图（现为占位 SVG，可替换） |

**信息架构**：两大并列板块——①Research（banner 两排胶囊分别导航"按应用"5 个子页与"按方法"5 个子页；应用讲临床问题与落地成效，方法讲算法技术贡献）②Open Science and Software。

## 子领域论文配图

每张论文卡片使用该文 PDF 首页的截图（`images/areas/<论文id>.jpg`），卡片内按 640×300 顶部裁切显示刊名、标题与作者：

1. 生成/更新截图：`python tools/render_paper_shots.py`（映射表在脚本内，源 PDF 在 `D:\usr\01_work\06_gth818nWrite\manuscript\40_published`）；
2. 重新运行 `python tools/build_areas.py`，脚本自动优先使用同名真实图片（jpg/png/webp），缺图时退回占位 SVG。
3. 裁切规则在 `assets/css/main.css` 的 `.card .card-img img.paper`。

**未发表不显示**：`tools/build_areas.py` 的 `is_published()` 会过滤掉 `"type": "project"`（进行中）与 `venue` 含 `in press`／`在刊` 的条目——数据仍留在 `data/areas.json`，见刊后把 `type` 改成 `paper`、`venue` 写成正式卷期或补 DOI，重跑脚本即可上站。

## ABUS 检出率柱状图

首页第一张成果卡与乳腺子页（`research/breastCN.html` / `research/breast.html`）综述卡共用同一张图，中英各一版：

1. 数据维护在 `tools/build_figures.py`：`ROWS`（中）/ `ROWS_EN`（英）每根柱为 `标签, 副标, 数值, 显示值, 分组, 引文编号`；`TEXT` 里是标题、副标题、脚注与图例。跑 `python tools/build_figures.py` 生成两张 SVG。
2. 接入位置由 `data/areas.json` 中 breast 领域的 `figure_cn` / `figure_en` 指定；`tools/build_areas.py` 把它注入综述卡（`{figure_html}`）。首页两处 `<img src>` 手工指向同名 SVG。
3. **配色约定（勿改回同色系）**：暖琥珀橙 = 我们的研究（与站点 navy/cyan 互补，专门做高亮）；青蓝 = 日韩 / 外部 AI 基准；灰 = 中国既往筛查基准。改动时保持三组色系区分。
4. 检出率单位为每千名筛查女性（‰），脚注 [1]–[7] 逐条给出出处，含 Sun W, et al. *iScience* 2026;29:118186（ABUS 3.08‰ vs 手持 1.22‰）。跨研究比较受年龄结构、首筛比例与随访完整性影响，图下已注明。

## 日常维护

### 加一篇论文

1. 打开 `data/publications.json`，在对应板块（`journals` / `conferences` 等）的 `items` **最前面**加一条，照抄现有条目格式：

```json
"张三, <b>高毅*</b>, <i>\"论文标题\"</i>, 期刊名, 2027, DOI: 10.xxxx/xxxxx"
```

   - `<b>高毅</b>`：加粗自己名字；`*` 表示通讯作者
2. 运行：

```
python tools/build_pubs.py
```

3. `publications.html` 和 `publicationsCN.html` 会同时重新生成，提交推送即可。

### 改首页 / 研究页 / 软件页

首页、研究总览、软件页直接编辑对应 HTML，双语页面记得同步修改：`index.html`（中）↔ `indexEN.html`（英）、`researchCN.html` ↔ `research.html`、`softwareCN.html` ↔ `software.html`。

**语言与链接约定**：`index.html` 是中文首页（默认落地页）；中文页面的所有导航一律指向 `*CN.html`，英文页面指向英文页，语言切换按钮负责跨语言跳转。`tools/build_areas.py`、`tools/build_pubs.py` 的模板里已按此约定写死。

### 换图片

- 个人照片：替换 `images/photo-placeholder.svg` 为真实照片（如 `images/photo.jpg`），并修改 `index.html` / `indexEN.html` 中的 `<img src>`。
- ABUS 检出率柱状图：改 `tools/build_figures.py` 的 `ROWS` / `ROWS_EN` 与 `TEXT` 脚注，跑 `python tools/build_figures.py` 重新生成两张 SVG；首页与乳腺子页会自动引用（不要手改 SVG）。
- 建议每张图压到 300KB 以内。

## 旧版备份

旧版完整备份在 `D:/usr/10-work/gaoyi.github.io-v1-backup/`（2026-11-12 下载自 GitHub main 分支）。

## 设计约束（改动时请保持）

1. **不引入任何运行时外部依赖**：不加载 Google Fonts、不挂 CDN 上的 JS/CSS 库、不加统计脚本（除非确认国内可达性）。
2. 中英文是两套独立页面，用纯链接切换，不需要 JS。
3. 论文页面只通过 `tools/build_pubs.py` 生成。
