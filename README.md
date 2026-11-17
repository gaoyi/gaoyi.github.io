# gaoyi.github.io — 维护说明

新版个人主页（2026-11 重构）。**纯静态、零运行时依赖**：系统字体（大标题 Georgia/宋体 + 正文苹方/微软雅黑系统栈）、单一样式表（`assets/css/main.css`）、无 JavaScript、无外部 CDN——任何网络环境（包括国内）都能正常渲染。

**设计语言**：编辑排版风格——深海军蓝（#06101b）+ 青色点缀（#80d6ef）、衬线大标题配无衬线正文、eyebrow 眉标 + 数字编号（01/02/03）、明暗分带（深色 hero/页头 → 浅色内容带 → 深色页脚）。改样式只动 `assets/css/main.css`。

## 页面结构

| 文件 | 内容 |
|------|------|
| `index.html` / `indexCN.html` | 首页：深色 hero、数据带、简介与新闻、代表性成果、研究方向卡 |
| `research.html` / `researchCN.html` | 板块一·Research 总览：banner 内两排导航胶囊（按应用/按方法），全部卡片可点击进入子页面 |
| `research/*.html` / `research/*CN.html` | 10 个子领域页面（**由脚本生成，不要手改**）：顶部综述卡 + 胶囊导航 + 每篇论文一张带图卡片 |
| `software.html` / `softwareCN.html` | 板块二·Open Science and Software：开源社区贡献与六个软件项目 |
| `publications.html` / `publicationsCN.html` | 论文列表（**由脚本生成，不要手改**） |
| `data/publications.json` | 论文数据（完整列表的唯一维护入口） |
| `data/areas.json` | 子领域数据（各领域的代表论文、要点、图片；**改这里再跑 build_areas.py**） |
| `tools/build_pubs.py` | 论文列表页生成脚本 |
| `tools/build_areas.py` | 子领域页面生成脚本 |
| `tools/extract_pubs.py` | 一次性迁移工具（从旧版 HTML 提取，平常不用） |
| `images/areas/` | 子领域论文配图（现为占位 SVG，可替换） |

**信息架构**：两大并列板块——①Research（banner 两排胶囊分别导航"按应用"5 个子页与"按方法"5 个子页；应用讲临床问题与落地成效，方法讲算法技术贡献）②Open Science and Software。

## 子领域论文配图（替换占位图）

每篇论文卡片当前用自动生成的占位图（深色 + 期刊年份标注）。换成真实图形摘要：
1. 把图片放到 `images/areas/`，文件名 = 论文 id（如 `ajr-2024.png`，支持 png/jpg/webp）；
2. 重新运行 `python tools/build_areas.py`；
3. 脚本自动优先使用同名真实图片，占位图保留但不引用。

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

直接编辑对应 HTML，双语页面（`xxx.html` 与 `xxxCN.html`）记得同步修改。

### 换图片

- 个人照片：替换 `images/photo-placeholder.svg` 为真实照片（如 `images/photo.jpg`），并修改 `index.html` / `indexCN.html` 中的 `<img src>`。
- ABUS 成果图：替换 `images/feature-placeholder.svg`。
- 建议每张图压到 300KB 以内。

## 旧版备份

旧版完整备份在 `D:/usr/10-work/gaoyi.github.io-v1-backup/`（2026-11-12 下载自 GitHub main 分支）。

## 设计约束（改动时请保持）

1. **不引入任何运行时外部依赖**：不加载 Google Fonts、不挂 CDN 上的 JS/CSS 库、不加统计脚本（除非确认国内可达性）。
2. 中英文是两套独立页面，用纯链接切换，不需要 JS。
3. 论文页面只通过 `tools/build_pubs.py` 生成。
