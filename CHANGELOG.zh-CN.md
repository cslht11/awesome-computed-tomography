# 更新日志（中文译文）

本文件是 `CHANGELOG.md` 的中文译文，供网站 `/zh/changelog/` 页面使用；英文原文是唯一的事实来源，两者有出入时以英文为准。

每个条目的标题与英文条目同一日期，标题下第一行用 `<!-- en: 英文标题 -->` 注明它对应的英文条目——构建时按“日期 + 英文标题”配对，所以两个文件的顺序不必一致。还没有译文的英文条目在中文页面上以英文显示；如果某条译文对应的英文条目已不存在（例如英文标题被改了），构建会失败，以免过时的译文无声地留在页面上。改动英文条目的标题时，请同步修改这里的 `en:` 注释。

段落与列表项一律写在一行内：中文句子中间的换行会被当成空格。运行 `python scripts/changelog.py --status CHANGELOG.zh-CN.md` 可以列出尚未翻译的条目。

## 2026-10-18 — 苹果、黏土与珊瑚数据集及 PFITRE 的中文说明
<!-- en: Chinese notes for the Apple / Play-Doh / coral datasets and PFITRE -->

### 修复

- `2f27bbb` 新增的三个数据集与一个工具包（Apple CT 仿真数据、Play-Doh 黏土加石子、深海竹珊瑚、PFITRE）只带英文说明，中文站因此整段显示英文——构建报告 `4 of 173 table notes still fall back to English`。现在四条都有中文说明，计数回到 `0 of 173`。

## 2026-10-17 — 35 个新数据集的中文说明
<!-- en: Chinese notes for the 35 new datasets -->

### 修复

- 2026-10-16 新增的 35 条数据集（26 条来自 Zenodo，9 条来自 FIPS）只带英文说明，中文站会整段回落英文——构建报告 `35 of 169 table notes still fall back to English`。现在 35 条都有中文说明，计数回到 `0 of 169`；中文数据集列表恢复为全中文。

## 2026-10-16 — 作者规则纳入 CI 强制
<!-- en: The authorship rule is enforced in CI -->

### 新增

- **当推送范围内的提交被归属到 cslht11 之外的账号时，`validate` 会失败。** GitHub 按提交上的邮箱归属作者，而贡献者图只统计默认分支——因此一笔带着他人账号地址的提交会永久变成第二个“作者”，这也是本仓库不得不在 2026-10-12 重建的原因。
- `hooks/pre-push` 已在本地执行同一规则，且刻意检查提交本身而非 `user.email`。但 `hooks/` 里的钩子要等有人运行 `scripts/install-hooks.sh` 才会启用，所以**全新克隆一开始完全没有闸门**——2026-10-15 那批带个人邮箱的提交就是这样进到 `main` 的。放到 CI 里堵上了这个缺口：它无法被跳过，而且会在运行记录里留痕。
- `actions/checkout` 现在使用 `fetch-depth: 0`，以便检查推送范围而不只是末端提交。

### 修复

- 检查接受**两个**地址而非一个：`cslht11@users.noreply.github.com`（本地提交）与 `heitieya@163.com`（通过 GitHub Contents API 的提交，即连接器推送；GitHub 用账号主邮箱署名，且该端点没有作者参数，地址并非调用方可选）。第一版只钉住 noreply 地址，会把所有连接器推送判为失败、却仍放行本地提交。规则是“作者为 cslht11”，不是“某个精确字符串”；`MAINTENANCE.md` 现在用表格写明这一点以及两个地址各自合法的原因。

## 2026-10-16 — 首页链接到数据集、基准和指南页面
<!-- en: Homepage links to the dataset, benchmark and guide pages -->

### 变更

- 首页的**数据集**和**基准与挑战赛**标签页中，21 个数据集和 11 个基准凡有单独页面的，名称现在都链接到该页面（`/datasets/<slug>/`、`/benchmarks/<slug>/`；中文首页链接到 `/zh/...`）。官方网站仍可一键到达：名称旁另有一个单独的 `[官网]` 链接。没有单独页面的条目保持不变。
- **学习资源**标签页顶部新增一个小的**指南**分组，列出三篇指南，并附有 `/guides/` 索引页的链接。
- `tests/test_seo.js` 现在检查首页恰好链接到这些页面（每个数据集与基准页面、三篇指南和 `/guides/`），且每个链接都指向已生成的页面；`tests/test_site_dom.js` 检查渲染后的标签页。

### 修复

- 网站页脚中的“更新于”日期现在使用 Asia/Shanghai 时区的日期，而不是构建服务器的 UTC 日期，清晨构建时不再显示前一天。

## 2026-10-16 — 新增数据集与基准页面，以及三篇指南
<!-- en: Dataset and benchmark pages, and three guides -->

### 新增

- **`/datasets/<slug>/` 与 `/benchmarks/<slug>/`**（中英文）：为目录中内容充实的 21 个数据集和 11 个基准各建一个页面——即有描述、有官方链接，并且目录中至少有一个主题页或一篇论文用到它们。每个页面列出该条目提供的数据（按其备注所述，投影和／或图像）、成像方式、任务、数据集本身的许可、官方链接和记录中已有的 DOI、描述它的论文、目录中提到或链接它的论文、相关主题页、相关条目和指南。每个页面都有自己的标题、描述、canonical URL、hreflang 互链、一个 `BreadcrumbList`，以及一个与页面可见内容出自同一记录的 schema.org `Dataset` 块。其余 28 个条目（多为目录中尚无相关重建主题或论文的分割与检测数据集）仍保留在目录表格中；`build_site.py` 会逐一打印被跳过的条目及原因。哪些条目建页、它们的 URL slug，以及用来查找使用它们的论文的别名，都写在新文件 `data/resources.yaml` 中。
- **`/datasets/`**：列出所有数据集与基准页面的索引页。
- **`/guides/` 下的三篇指南**及 `/guides/` 索引页：[稀疏视角 CT 重建](https://computedtomography.org/zh/guides/sparse-view-ct-reconstruction/)、[低剂量 CT 去噪](https://computedtomography.org/zh/guides/low-dose-ct-denoising/) 和 [如何选择 CT 重建数据集](https://computedtomography.org/zh/guides/choosing-a-ct-reconstruction-dataset/)。每篇开头先给出答案，用由目录数据生成的表格比较各种选择（方法族、数据集、基准、工具库、入门论文），标明最近更新日期，最后附一组简短的常见问题，其 `FAQPage` JSON-LD 由页面上可见的文字生成。正文写在 `data/guides.yaml` 中，其中所有数字都由实时数据填入。
- 主题页现在会链接到它所列出的数据集与基准页面（官方网站仍保留一键可达的链接）以及涵盖该主题的指南；“关于”页面链接到 `/datasets/`、`/guides/` 和每篇指南。所有新页面都收录在 `sitemap.xml` 和 `llms.txt` 中。首页没有任何变化。
- 如果新页面缺少 canonical、hreflang、面包屑或 JSON-LD，未收录在 sitemap 中，没有任何页面链接到它，或某篇指南链接了一个不会生成的页面，`build_site.py` 会构建失败。`tests/test_seo.js` 还会检查每个 `Dataset` 块与页面上可见的名称、描述、许可、DOI 和引用一致，以及每篇指南的常见问题和最近更新日期与其 JSON-LD 一致。

### 修复

- 以缩写加逗号开头的论文标题（LoDoPaB-CT）在主题页上不再显示成“LoDoPaB-CT: , a benchmark …”。

## 2026-10-16 — 新增更新日志页面，首页以数据目录的形式描述
<!-- en: A changelog page, and the homepage described as a data catalog -->

### 新增

- **`/changelog/` 与 `/zh/changelog/`**：每次构建时由 `scripts/changelog.py` 从 `CHANGELOG.md` 生成，列出全部带日期的条目，按日期从新到旧排列（同一天的条目保持它们在文件中的顺序）。中文版用中文显示每一条，译文取自 `CHANGELOG.zh-CN.md`，按日期和标题与英文原文配对；尚未翻译的条目以英文显示、标注 `lang="en"`，页面上也会注明。两个版本各有自己的标题、描述、canonical URL、hreflang 互链和 `BreadcrumbList`；两者都收录在 `sitemap.xml` 和 `llms.txt` 中，并从“关于”页面和页脚链接过去。`CHANGELOG.md` 中出现没有日期的 `##` 标题，或日期比构建时间超前一天以上时，构建会失败。
- **首页 JSON-LD 新增一个 `DataCatalog` 块**（英文版和中文版），与原有的 Organization、WebSite 和 ItemList 并列。它列出首页展示的三张表——论文、数据集、基准——数量取自实时数据，`dateModified` 取自 `data/meta.yaml` 中的 `last_updated`，并以该 Organization 为创建者和发布者。如果目录中的数量或日期与 `data.json` 不一致，`build_site.py` 会拒绝写出。
- `tests/test_seo.js` 检查以上两项，不依赖任何软件包，并在 `validate.yml` 中运行。

## 2026-10-15 — 每个主题都有了主题页，“关于”页面新增常见问题
<!-- en: Topic pages for every topic, and an FAQ on the About page -->

以 #2 合并（squash 提交 `3459829`）。

### 新增

- **`/topics/<id>/` 与 `/zh/topics/<id>/`**：为 `data/meta.yaml` 中的 16 个主题（除 `other` 外的全部主题）各建一个中英文主题页。每页包含手写的简介、由维护者挑选的简短“从这里开始”阅读清单、该主题最新的 30 篇论文、相关的数据集、基准与工具包，以及指向其他主题的链接。编辑性文字放在新文件 `data/topics.yaml` 中；论文表、数量和相关资源都是生成的，因此不会过时。每个页面都有自己的 canonical URL、`hreflang` 互链（en、zh-Hans、x-default）、一个 `BreadcrumbList` 和一个 `CollectionPage` 块，并收录在 `sitemap.xml` 和 `llms.txt` 中。
- **“关于”页面（中英文）新增“按主题浏览”和六个常见问题**：稀疏视角 CT 适合用哪些数据集、低剂量 CT 研究常用哪些工具包、条目如何核实、列表多久更新一次、如何引用本列表，以及如何推荐论文或报告错误。`FAQPage` JSON-LD 由页面上可见的问答文本生成，因此两者不会不一致。
- `build_site.py` 会检查 `data/topics.yaml` 中每个 `start` id 和 `also` 名称都确实存在，每个主题页都带有 canonical、hreflang、JSON-LD 和 sitemap 条目，并且“关于”页面链接了每一个主题页。

## 2026-10-15 — 在 Google Search Console 和 Bing Webmaster Tools 完成站点所有权验证
<!-- en: Ownership verified with Google Search Console and Bing Webmaster Tools -->

### 新增

- `site.config.yml` 中新增 `google_site_verification` 和 `bing_site_verification`。`build_site.py` 把它们写成首页（中英文）`<head>` 中的 `google-site-verification` 和 `msvalidate.01` meta 标签。两个服务都会重新检查这个标签，因此删掉任何一个都会使站点失去验证；配置文件的注释里写明了这一点。

## 2026-10-15 — 新增 llms.txt，每次部署后推送 IndexNow
<!-- en: llms.txt, and IndexNow pings after each deploy -->

以 #1 合并（squash 提交 `6736652`）。现有页面、样式和数据均未改动。

### 新增

- **`/llms.txt`**：一份给 AI 问答引擎看的纯 Markdown 站点地图（llmstxt.org 提案），说明列表涵盖什么，并链接两个语言版本、“关于”和“联系”页面、两份 `data.json` 导出，以及每个主题及其论文数。数量和主题取自与页面相同的数据，因此不会过时。添加它几乎没有成本；是否真有程序读取它，尚未得到证实。
- **IndexNow。** `site.config.yml` 中新增 `indexnow_key`；构建时在站点根目录写出密钥文件 `site/<key>.txt`，`deploy.yml` 新增一个作业，在每次部署之后把 `sitemap.xml` 中的全部 URL 提交给 `api.indexnow.org`（Bing、Yandex 及其他支持 IndexNow 的搜索引擎）。这一步尽力而为——推送失败从不会让部署失败。Google 不使用 IndexNow，它读取的是在 Search Console 中提交的 sitemap。

## 2026-10-15 — 撰写简介后的清理
<!-- en: Clean-up after the blurb work -->

### 移除

- `TODO-summaries.md`：记录仍缺少简介的论文的清单。中英文简介的覆盖率都已达到 401/401，这个文件只会招来已经不存在的工作。

### 修复

- `tests/test_site_dom.js` 曾断言至少有一篇论文**没有**简介，用来证明这样的标题保持不可交互。覆盖率一达到 100%，这个前提就失效了，断言悄无声息地变成了永远失败的误报。现在它检查真正必须成立的事情——`has-blurb` 与 `data-blurb` 一致，因此没有简介的标题永远不会出现悬停效果。

## 2026-10-15 — README 改为落地页，完整列表放在网站上
<!-- en: README is a landing page; the full lists live on the website -->

### 变更

- README 保持原有结构——页眉、统计条、论文、工具包、数据集、基准、学习资源、联系方式、许可——但不再逐条展开条目。论文部分改为主题网格，每个格子链接到已选好该主题的网站页面；其他四个部分各自链接到网站上对应的标签页。条目备注和数据集图例仍在网站上显示，网站才是完整的列表。
- `scripts/build.py` 不再包含逐条渲染函数（`render_papers`、`render_toolkits`、`render_datasets`、`render_benchmarks`、`render_learning`）；只有这些函数使用的 i18n 键也一并删除。

## 2026-10-15 — 统计信息显示最后更新日期，而不是论文年份跨度
<!-- en: Stats show the last-updated date, not the paper-year span -->

### 变更

- README 统计条、网站统计行和覆盖率说明现在显示“更新于 2026-10-15”（取自 `data/meta.yaml` 中新增的 `last_updated` 字段），而不是论文年份跨度“1917–2026”，让访问者一眼就能看出列表是否仍在维护。每次内容变动时都要更新 `last_updated`；如果它缺失或不是 YYYY-MM-DD 格式的日期，`scripts/build.py --check` 会失败。

## 2026-10-12 — DC-PnPDP 可以按名称搜到了
<!-- en: DC-PnPDP findable by its name -->

### 修复

- **DC-PnPDP**（ICML 2026）早已收录，但只有完整标题，所以搜索“DC-PnPDP”找不到它。现在它带上了这个缩写、项目主页，以及其 CT 实验所涵盖的稀疏视角和有限角度主题（SVCT-20、LACT-90）。

## 2026-10-12 — 接入 Cloudflare Web Analytics，并在隐私页面中说明
<!-- en: Cloudflare Web Analytics, and the privacy page that says so -->

### 变更

- `site.config.yml` 中的 `analytics_token` 现已设置，因此列表页面（中英文）会加载 Cloudflare Web Analytics 的统计脚本。本域名并未经 Cloudflare 代理，这就是区域面板显示零访客的原因；JS 统计脚本则不受此影响，照常计数。它不设置 cookie，也不使用本地存储。
- 隐私页面（中英文，以及 `web/pages/privacy.html` 中的维护者副本）：“统计分析：无”一节现在说明了这个统计脚本、Cloudflare 会收到哪些信息，以及我们只能看到汇总数字。页面按其事先承诺，在任何改动之前更新，更新日期为 2026 年 10 月 12 日。

## 2026-10-14 — 中英双语的悬停简介，以及根据外部审阅所做的更正
<!-- en: Bilingual hover blurbs, and corrections from an outside review -->

### 新增

- **论文标题悬停即可看到说明。** 标题原先是一个 `<a>`，指向与旁边 `paper` 链接相同的 URL，点哪个都去同一个地方。现在它是纯文本；对于我们有简介的论文，在鼠标悬停、轻触或键盘聚焦时会弹出一张卡片显示简介。没有额外的页面——下面的链接才是出口。没有简介的论文保持不可交互，`title=` 属性则为关闭了 JavaScript 的读者保留一个后备。
- `data/summaries.yaml`：为 **399 篇论文中的 256 篇** 提供一段式简介，每段都由官方摘要中的**原句**组成（压缩步骤只挑选句子，从不改写），因此简介可能不完整，但绝不会是编造的。分两轮获取：先按 id 从 arXiv 获取（158/158），再按 DOI 从 Crossref 获取（237 篇中得到 47 篇——大多数出版商不向 Crossref 提供摘要），最后按标题在 arXiv 中检索，并以相似度 ≥0.90 作为门槛（又得到 51 篇）。
- `scripts/oneoff/fetch_summaries.py` 和 `fetch_summaries_by_title.py`，两者都有限速和缓存（`--offline` 可以从缓存重新生成）。
- **简介是双语的。** `data/summaries.zh.yaml` 提供全部 256 段简介的中文版，因此中文网站显示中文，英文网站显示英文。它们单独成文件，而不是放进 `data/i18n/zh.yaml`——后者是精心维护的覆盖层，几百条机器长度的条目会把它淹没；`scripts/export_site_data.py` 会选用与所构建语言相匹配的文件，未翻译的内容回落到英文，因此缺口表现为看得见的英文，而不是一张空卡片。
- `scripts/oneoff/translate_summaries.py`：应用一批译文，并报告还缺哪些（`--status`）。
- `TODO-summaries.md`：仍没有简介的 143 篇论文，附简短的操作说明。这些论文本身没有任何问题，只是不显示卡片。

### 修复

一次对网站的外部审阅发现了一批真实存在的错误。每一处在应用之前都对照一手来源重新核实过：

- **八篇被归为预印本的论文其实早已发表**：CTO（ECCV 2026）、NAB-GS（MICCAI 2026）、PMF-STGR（PMB 70(16):165011）、DREME-adapt（Med Phys 52(11):e70119）、加速 INR 那篇论文（ISBI 2025）、EAGLE（J. Med. Imaging 12(1):014001）、DDDM（IEEE SPL 31:1279–1283）和 UncertaINR（TMLR 2023）。预印本数量从 67 降到 59。注意 EAGLE 的 arXiv 页面仍写着“Preprint”——以期刊页面为准。
- 五处标题笔误：“Denosing” → “Denoising”、“Low-Dose Ct” → “Low-Dose CT”、“HorusEye: a …” → “HorusEye: A …”、“multi-domain … swin transformer” → “Multi-domain … Swin Transformer”、“for Cone beam CT” → “for cone-beam CT”。
- 二十四篇标题已经以“缩写: …”开头的论文没有填写 `abbr`，因此网站上没有显示开头的标签，这一列看起来参差不齐。现已补上——这同时也让这些缩写可以被搜索到。
- 有一段简介仍带着某出版商 Crossref 记录中原始的 `&lt;p&gt;` 标记；已反转义并去除。

### 有意未改

- 审阅中被认为重复的 TomoPhantom 和 LoDoPaB-CT 条目是有意为之：两者互相引用，LoDoPaB 那一条是该数据集的引用文献，而不是数据集的第二份副本。
- 审阅中所说中英文网站内容已经不一致，无法复现——两者都提供 399 篇论文，构建日期也相同。

## 2026-10-13 — 一轮 arXiv 检索带来的七篇论文和一个工具包
<!-- en: Seven papers and one toolkit from an arXiv sweep -->

按最新优先的顺序，在 arXiv 上检索了 `computed tomography`、`sparse-view`、`limited-angle`、`CT reconstruction`、`cone-beam` 和 `low-dose CT`，收录了属于本列表范围的工作。

### 新增

- **PhyDiCT**（MICCAI 2026）：从少量 X 射线投影进行免训练的即插即用 CT 重建。一个可微的 Beer–Lambert 前向模型通过 Split Gibbs 采样引导文本条件扩散先验，联合优化投影保真度与图像先验。属于稀疏视角，附代码。
- **OX-NeRF**：从超稀疏视角（10 个或更少）进行 X 射线断层成像，将跨场景的特征学习与逐场景的多分辨率哈希网格结合起来。
- **基于梯度的稀疏视角 CBCT 轨迹优化**：每个射线源位姿都成为一个连续变量，在扫描机的运动学流形上通过梯度上升联合移动，因此扫描路径是设计出来的，而不是从固定的候选池中挑选的。
- **高斯材料场**：用共享的各向异性三维高斯基元配合各材料独立的系数，进行多能 CT 的材料分解。
- **LINGO**：在三维高斯泼溅框架下，通过潜在初始化与梯度优化，实现稀疏视角 X 射线新视角合成与 CT 重建。
- **考虑随视角变化的探测器位移的基于模型的迭代重建**：把实测的探测器运动纳入 CBCT 前向模型，而不是把几何当作标称值。
- **Deep Pseudo-Proximal Map**：一个自监督的数据拟合智能体，在迭代重建循环中代替近端映射。
- **CTrex**（工具包）：一个面向研究的 GPU 框架，把投影—校正—反投影流程开放到单个 CUDA kernel 的粒度，使非理想采集效应可以直接写进算子，而不是作为校正事后附加；几何由逐投影的齐次视图矩阵描述，因此 kernel 对圆轨道、螺旋、偏置和传送带等轨迹一视同仁。目前通过其预印本收录：论文未公布代码仓库，一旦出现仓库，条目会改为指向它。

### 修复

- **Geometry-Aware Diffusion Approximate Posterior Sampling** 原先只归在 `limited-angle` 下，但它的标题和方法都同样涵盖稀疏视角 CT。已补上 `sparse-view`——这和前一天导致 DC-PnPDP 无法按缩写搜到的，是同一类标签缺失。

### 有意未收录

检索过但未收录：**CPF-DDNM**（一个通用的扩散后验采样器，摘要中从未提到 CT）、随机批采样坐标下降（纯优化理论）、**EviDent-CBCT**（基于牙科 CBCT 生成报告，不是重建）、一种可变形 CT–超声配准方法，以及当前一批面向一般场景的三维高斯泼溅与 NeRF 论文——那些属于计算机视觉中的视角合成，不是断层成像。

## 2026-10-12 — 搜索、排序与语言切换的修复
<!-- en: Search, sorting and language-switch fixes -->

### 修复

- **在搜索框中输入 arXiv id 不会再跳到错误的页面。** 工具包、数据集、基准和学习资源记录曾把整个 URL 编入索引，于是 URL 中的每个数字都成了可搜索的词元，一个 id 可能匹配到不相关的记录。现在它们只索引主机名，这正是代码一直声称的行为。裸的 arXiv id 单独编入索引——151 篇论文链接了 arXiv id——因此搜索 `2607.14415` 会找到它所属的论文 `$K$-NeAS`，而不是某个 URL 里恰好含有 `2607` 的数据集。
- **按 Enter 之前必须有真正的命中。** 以前在没有论文匹配时，按 Enter 会打开排名第一的结果，无论它多弱。现在只有得分达到 2 或以上（名称或元数据命中才有这个分数）才会打开；单个弱的正文命中（约 0.7）只会过滤列表，因此误按一个键不会把人带出站外。
- **按标题排序时 `$K$-NeAS` 不再排在第一。** 排序用的是原始标题，而 `$` 排在所有数字和字母之前；现在按显示出来的标题排序，并去掉行内 TeX 定界符。比较函数在键相等时也会返回 0，而只返回 `-1/1` 的比较函数从来做不到这一点。
- **年份筛选的“及以后”标签已翻译。** 它原先是硬编码的英文字符串；现在读取已有的 `yearAndLater` 键，中文覆盖层早已提供了这个键。
- **切换语言会保留筛选条件。** 切换链接在构建时写出，不带查询字符串，所以从 `/zh/?tab=datasets&q=…` 切换语言时会丢掉所有筛选。`web/lang.js` 在页面加载时把当前查询字符串附加上去一次；两个模板都加载了它。

### 文档

- `SITE.md` 仍把搜索描述为“边输入边过滤……多个词按 AND 组合”，自从排序取代严格的 AND 以来，这已不再正确。现在它描述的是“先下拉、再按 Enter”的行为，以及 Enter 为什么有阈值。

## 2026-10-12 — 更正两项挑战赛描述和两条数据集记录
<!-- en: Corrected two challenge descriptions and two dataset records -->

### 修复

- **AAPM DL-Sparse-View CT Challenge**（及其数据集条目）：这是 2021 年的挑战赛，不是 2022 年；它要求从理想、无噪声的 **128 视角**扇形束数据中恢复模拟的二维乳腺 CT 体模（4,000 对训练数据，100 个测试病例）。原先的描述是对 2016 年临床队列进行 2/4/8/16/32/64 视角的重投影，那并不是该挑战赛提供的内容。数据集的模态和许可证现在以 AAPM 页面和 Zenodo 记录为准（CC BY 4.0）。
- **Helsinki Tomography Challenge 2022**：冠军是一个在合成数据上训练的纯学习网络；唯一基于模型的参赛方案（CIL）排名第三。原来的备注把这一点说反了。
- **LDCT-and-Projection-data** 的许可证：TCIA 第 7 版以 CC BY 4.0 开放了胸部和腹部扫描；头部扫描仍属于 NIH 受控访问。原先记录为 CC BY-NC 4.0。

## 2026-10-12 — 三个 CT 基础模型，以及 CT-RATE 数据集
<!-- en: Three CT foundation models, and the CT-RATE dataset -->

### 新增

- **TAMP**、**DeepSparse** 和 **LCTfound**。三者在写入之前都对照 Crossref 做了核对——标题匹配度均为 1.000——而不是直接取自它们被采集时所在的 PDF，因为这些 PDF 转出的 markdown 里带的是*参考文献*的 arXiv id，而不是论文本身的。TAMP（Nat Commun 2026）用一个主干网络同时处理低剂量、稀疏视角和有限角度问题；DeepSparse（TMI 2026）针对稀疏视角 CBCT；LCTfound（Nat Commun 2025）涵盖八项任务，其中 CT 图像增强和稀疏视角重建与重建相关。
- **CT-RATE**，归入数据集中图像域的那一半：50,188 个重建好的三维胸部 CT 体数据，每个都配有一份放射学报告。它没有投影标记——没有原始正弦图——在拿它来测试前向模型之前，这一点值得知道。它的着陆页没有写明许可证，因此记录为 `see source`，而不是凭猜测填写。
- `scripts/oneoff/verify_foundation_papers.py` 及其输出，让这批条目的来源记录与它们产生的条目一起留在仓库中。

### 修复

- **HorusEye 之前没有代码链接。** 现已记录其代码仓库。

### 有意未收录

同一批中还有三篇论文**没有**收录：CT-RATE 本身的论文（CT-CLIP / CT-CHAT）、Merlin 和 TAP-CT。三者都是 CT 基础模型，但它们的贡献在于视觉—语言检索、报告生成和冻结特征分类，而不是重建。`MAINTENANCE.md` 中的门槛是*关于 CT 重建*的论文，为重建方法而来的读者只会觉得它们是噪声。在此记录，而不是悄悄略去。

## 2026-10-12 — 贡献者图表重新只剩 cslht11
<!-- en: The contributor graph is cslht11-only again -->

### 修复（署名）

- **一个已合并的 Dependabot pull request 让 `dependabot[bot]` 出现在贡献者图表中。** squash 合并会把新提交署名给 pull request 的作者，于是 `main` 上多了一个由 `dependabot[bot]` 署名的提交——它以一个提交排在第二位，紧挨着 cslht11 的十四个提交。该提交已改写为 cslht11 的提交；它所携带的改动（PyYAML 的版本下限）原样保留。
- **删除了 `.github/dependabot.yml`。** `refs/pull/N/head` 引用无法删除——API 的回答是 `refs/pull/* is read-only`（HTTP 422）——所以从 Dependabot 打开 pull request 的那一刻起，它的作者就永久留在图表里，无论该 pull request 是被合并、关闭还是一直开着。没有任何设置能把图表限定为单一作者。今后版本升级一律由 cslht11 手动提交。Dependabot 的**安全警报**是另一项设置，不需要配置文件，继续保持开启。

### 新增（作者身份守卫）

- **`hooks/` 和 `scripts/install-hooks.sh`。** 防止此事再次发生的两个守卫原先只存在于某一个克隆的 `.git/hooks/` 里，也就是说，只要重新克隆一次它们就不复存在。现在两者都放进了仓库，用一条命令即可安装；仓库地图里也写明了克隆后要运行它。
  - `hooks/pre-commit`：拒绝 `user.email` 不是 cslht11 的提交。
  - `hooks/pre-push`：拒绝任何包含非 cslht11 作者提交的推送。能挡住 `dependabot[bot]` 的正是这一个：squash 合并使用的是 pull request 作者的身份，本地的 `git config` 根本看不到，所以任何 `pre-commit` 钩子都抓不住它。

## 2026-10-12 — 许可证表述精确化，结构写成文档，数据体积缩小 16%
<!-- en: Licences made precise, structure written down, payload 16% smaller -->

### 修复（许可）

- **内容与代码的边界有两处划错了。** `LICENSE-content` 把 `site/` 列为内容，但构建会把 `web/*.js` 和 `web/*.css` 原样复制进去——于是同样的字节同时被两个许可证声明。它还完全漏掉了 `data/i18n/*.yaml`（`data/*.yaml` 不匹配子目录），而所有翻译过的文字都在那里。现在两个文件都明确列出各自的路径，包括 `site/*.js` 和 `site/*.css` 这一例外。
- `MAINTENANCE.md` 解释了**为什么代码不使用与内容相同的许可证**——CC 自己就不建议把它的许可证用于软件：它们对专利、对源代码与目标代码的区别只字未提；NonCommercial 不是开源许可（OSI 和 DFSG 都不接受它）；ShareAlike 对代码具有传染性。NC 带来的后果也直接写明，而不是留给读者去推断。

### 新增（结构）

- **`MAINTENANCE.md` 中的仓库地图**：列出每个目录和文件，外加一张“要改 X，就编辑 Y，然后运行 Z”的表格。它是为毫无背景、初次接手的人写的，这正是这个文件的用途。
- **`tests/` 放进了仓库。** 搜索测试原先放在一个私有的运维目录里；不和被测代码放在一起的测试，迟早会失效。`tests/test_search.js` 不需要任何软件包，现在在 `validate.yml` 中于站点构建之后运行；`tests/test_site_dom.js` 用 jsdom 驱动真实页面，并且有意保留为本地的推送前检查——一个会因为软件包仓库连不上而变红的工作流，只会让人学会无视红色，这与 `SITE.md` 中不让部署工作流在 pull request 上运行的理由是同一个。

### 变更（维护）

- **GitHub Actions 升级到当前的主版本**：`checkout` v4 → v7、`setup-python` v5 → v7、`upload-pages-artifact` v3 → v5、`deploy-pages` v4 → v5。部署日志一直在警告 `deploy-pages@v4` 仍以 Node 20 为目标。
- `requirements.txt` 把 PyYAML 固定在 `>=6.0.3,<7`。下限是第一个修补了加载器的 6.x 版本；上限确保主版本升级是一次经过测试的主动改动，而不是 CI 在某个夜里自动拉取的东西。

### 变更（数据体积）

- **去掉了 `_q` 搜索字符串**（数据格式版本 1 → 2）。它是把标题、缩写、出处、主题名、备注和链接主机名转成小写后拼接起来的字符串，好让客户端在一个字符串里做子串匹配。`web/search.js` 现在改为在浏览器中根据结构化字段构建加权索引，所以这个字符串只是重复的内容，已经没有任何读取者——光它就约有 68,000 个字符。`index.html` 541 KB → **472 KB**，`data.json` 263 KB → **192 KB**，整个站点 868 KB → **727 KB**，还少了一个需要保持同步的派生字段。

## 2026-10-12 — 网站搜索终于真正可用，也不再报错
<!-- en: The site's search actually works now, and stops throwing -->

两处名字冲突让网站的 JavaScript 出错。两者都早已存在，在服务端渲染的 HTML 中都看不出来，而合在一起，正好解释了为什么搜索框毫无反应。

- **`renderPapers` 声明了 `var t = titleParts(p)`**，遮蔽了几行之后要用的 i18n 辅助函数 `t()`。由此产生的 `TypeError` 在每次渲染时都会触发，在 `init()` 接好搜索框之前就把它中止了——所以在筛选框里打字从来没有任何作用。
- **`renderToolkits` 用 `function (t)` 作为 `map` 的回调**，是同样的冲突，对 14 个带有 `homepage` 的工具包都会报错。
- **顶栏搜索框为它的防抖定时器声明了 `var t`**，遮蔽了它自己的 `t()`：第一次按键就把 `t` 变成了定时器 id，下一次渲染随即报错。现在下拉框在多次按键之后依然正常。
- `debounce` 和 `/` 键聚焦的处理函数也有同样的遮蔽结构，只是没有调用 `t()`，所以只是碰巧能用；在修复其他问题时一并改了名。

### 新增：真正的搜索核心（`web/search.js`）

旧的搜索只是在一个扁平字符串上做不区分大小写的子串测试，采用严格的 AND 语义，也不排序——所以查询必须是一个精确的子串，多一个词列表就会变空，结果则保持数据原有的顺序。

- **CJK 分词。** 中文不以空格分词，因此一串汉字会同时按单字和相邻的二字组合编入索引：「稀疏视角」变成 稀 疏 视 角 + 稀疏 疏视 视角。现在「稀疏重建」能找到标题为「稀疏视角 … 重建」的记录，即使用户输入的两个词在标题中从未相邻。
- **字段加权。** 每条记录一张加权词元表（标题 5、缩写 4、元数据 2、其余 1），每个词元保留最高权重，因此标题中的命中排在备注深处同一个词的命中之前。
- **排序。** 词元权重按查询覆盖率缩放，再加上查询原样出现时的加分。完全不匹配的记录会被剔除，但部分匹配不再被丢掉：排序是在用户自己的排序之后进行的稳定排序，因此得分相同的结果保持用户所选的顺序。
- **拉丁字母词元的子串回退。** 只做精确的词元相等会丢掉 “mamba” → DenoMamba 和 “splat” → Splatting 这类结果，而旧的子串搜索能找到它们。因此，没有精确对应键的查询词元会回退到包含它的索引键，并打一个折扣。
- **该高亮的地方都有高亮**：结果、下拉框，以及每行论文的主题行（中文查询通常匹配的是主题而不是英文标题，不高亮的话，结果看起来就像什么都没匹配上）。
- **顶栏搜索框会搜索全部五个部分**，而不仅仅是论文；只有当查询确实找到论文时，按 Enter 才会过滤论文列表，否则会打开最佳匹配。
- 由两套测试验证（核心逻辑 54 条断言，用 jsdom 驱动构建后页面的 23 条），其中包括“任何渲染都不抛出异常”——这一项本可以发现上面那些冲突。

### 变更

- **不使用网页字体，并写明了原因。** 系统 UI 字体加上平台自带的中文字体在这里更快、也更好看，还让页面不产生任何第三方请求，也不涉及任何字体许可问题。字体栈加入了 `system-ui` 和更完整的中文回退链，让 macOS、Windows 和 Linux 的显示一致；这个决定写在做出它的地方。
- LoDoPaB-CT 论文标题不再重复“(Scientific Data)”——出处一栏已经写了。

## 2026-10-12 — 逐条处理三份外部审计，并清理贡献者名单
<!-- en: Three external audits worked through, and the contributor list cleaned up -->

对仓库的三份独立审计——涵盖数据、i18n、链接、CI 和文档——是逐条核对的，而不是照单全收。每一处修复在动手之前都从 Crossref、出版方记录或项目自己的一手来源重新推导过；有几条审计意见被证明是错的，因而被舍弃或收窄（见下文）。

### 修复（论文与数据集记录）

- **四处错误的年份或出处**，每处都对照 DOI 所指向的记录确认过：LoDoPaB-CT 2017 → **2021**（Scientific Data）、MAP-NN 2021 → **2019**（Nat Mach Intell）、DL-PICCS 2019 → **2021**（Med Phys）、DREAM-Net TMI 2022 → **JBHI 2023**——这个错误其实早被 DOI 自身的前缀 `10.1109/jbhi...` 否定了。DenoMamba 2025 → **2026**，遵循其他 IEEE 条目使用的卷/期惯例。
- **LoDoPaB-CT 的标题里残留着一段 markdown**（`(**Scientific Data**) -->`），来自一个被手工删除的链接；`FSTensor` 的标题缺少分隔符（“FSTensorFull-spectrum…”，现为“FSTensor: Full-spectrum…”）。
- **删除两对重复条目**，每对都保留经过同行评审的那一条：CasRedSCAN 的 2020 年预印本与其 TMI 2021 论文，以及 CAIP 2025 的配准论文与它早先以研讨会标题发布的 arXiv 版本。论文数 391 → 389。
- **数据集信息对照一手来源更正。** LDCT-and-Projection-data 曾声称有“四个剂量水平（全剂量 / 四分之一 / 10% / 5%）”；实际上该挑战赛发布的是常规剂量加*一个*模拟的降剂量版本，TCIA 写明头部/腹部为 25%、胸部为 10%。VerSe 曾声称有“3,741 例 CT/CBCT 脊柱扫描”——实际是**来自 355 名患者的 374 例 CT 扫描**，没有 CBCT。Medical Segmentation Decathlon 有**六项** CT 任务，而不是四项。KiTS23 有 **599** 例扫描（489 例训练 + 110 例测试），而不是“三届”合计 489 例。RibFrac 的两个数字**写反了**：660 例扫描，约 5,000 处标注。STOIC 2021 是 **10,735 例法国第一波疫情**期间的扫描，而不是“23,000+ 例多中心”。LUNGx 是一项诊断分类任务，不是结节检测。CHAOS 的 CT 是门静脉期增强扫描，不是低剂量。AutoPET 到 2025 年共举办了**四届**，而不是三届。
- **`sigpy` 不包含 Radon 相关的基本运算**，**RadIO 也不是 Radon/FBP 软件包**——两条备注现在描述的是代码实际包含的内容。**LEAP** 的全称原先是编造的（实为 LivermorE AI Projector for Computed Tomography）。**libcbct** 采用 CC BY-NC-SA 4.0，而 GitHub 的 API 报告为“Other”。**CBCT Scatter Correction Tool** 的仓库里没有源代码——它提供的是一个 Windows 可执行文件——因此不再声称使用某种编程语言。
- **两篇基于泼溅的 CBCT 金属伪影论文都予以保留，而不是合并。** 两者都真实存在，也都经过同行评审（CVPR 2026 和 Computer Graphics Forum 45(2) 2026，出自同一课题组）；现在每条都附有说明，让几乎相同的标题被理解为一对论文，而不是重复录入的错误。
- **`generative-modeling-in-sinogram-domain`** 现在链接到其已发表的 TRPMS DOI（10.1109/trpms.2023.3309474），而不是 arXiv 版本；另有两篇 Transformer 论文和两篇纯学习方法论文去掉了与其内容不符的主题标签。
- **中文文字**：修正错字“高斯泼澅”，并统一了“Gaussian splatting”此前互相竞争的三种译法。

### 修复（构建与渲染）

- **`paper_head()` 把任何只是以缩写*开头*的标题都当作前缀匹配**，因此像“A”这样的缩写会把“A benchmark …”弄乱。现在它要求缩写*就是*第一个词，并会去掉标题末尾括号中重复出现的缩写。`web/app.js` 镜像实现了这两条规则，两处实现互相注明对方，避免各自走样。
- **数据集标记清除逻辑只认英文句号**，所以 ToothFairy2 的中文备注——它把标记本身也翻译了——会把同一句话同时打印在“数据”列和“描述”列。现在标记和其他地方一样保持英文。
- **覆盖层可以重命名一行**，而不仅仅是翻译它的备注。`learning."CT Principles and Algorithms".name` 原本就是为此而设，但这个键一直无声地失效；现在站点数据保留英文名称作为稳定键，并把译名作为 `label` 携带。
- **`tableDescription` 放在 `readme:` 部分，却是通过 `ov.ui()` 读取的**，因此永远找不到，中文 README 打印出的是英文表头“Description”。现已在两个语言文件中移到 `ui:` 下，同时移动的还有十个既不进入 README 也不进入网站的 `readme:` 键——其中两个具有实际的误导性：`licenseBody1` 写的是允许商业再利用的 CC BY 4.0（实际许可证是 CC BY-NC-SA 4.0），`contributing*` 链接到已于 2026-10-10 删除的 CONTRIBUTING.md。
- **README 中的网站 URL 不再硬编码。** `build.py` 从 `site.config.yml` 读取站点地址——文档承诺它只存放在这一个地方——因此更换域名时，README 徽章不会再指向旧地址。
- **创建了 `new entry` 标签。** issue 表单引用了它，但它并不存在——GitHub 会无声地丢弃未知标签，所以收到的建议都没有标签。

### 变更

- **期刊出处字符串统一**：TNS、TIT、TSP、SPM 和 JSAIT 去掉了 `IEEE ` 前缀，与其他地方使用的简写保持一致（IEEE Access 保留前缀，因为这就是期刊的正式名称）；`MedIA` → `Med Image Anal`。
- **中文术语统一**（同行评审、工具包、出版方），并修正了措辞：“on-board imaging”应译为机载成像而不是在轨成像，“beam hardening”全文统一为射束硬化；`topics.diffusion` 的描述改为涵盖一般的生成式先验——它自己的名称（“Diffusion & Generative Priors”）早已这样声称。
- 三本中文书籍和 XDesign 条目现在链接或描述的是来源的真实情况：两本书补上了出版社页面，1992 年那本注明没有出版社页面（因此链接到书名检索），Kak & Slaney 的备注改为“分章 PDF”而不是“Free PDF”，XDesign 按其 README 所述描述为体模与采集模拟软件包，而不是“可微分的”。
- `validate.yml` 增加了 `permissions: contents: read`；`check_links.py` 关闭证书校验这一点现在有文档说明和理由，而不是悄无声息。
- 更正了 **SITE.md** 对 CI 行为的描述：README 是否最新的检查在 `validate.yml` 中，在 pull request 上也会运行；而 `deploy.yml` 只在推送到 `main` 时运行。同一天的两个 `2026-10-10` 条目也分别取了不同的标题。

### 有意未改

- **研讨会出处**（“SC Workshops”、“NeurIPS Workshop”、“Off-Grid Workshop”）是三个不同的研讨会，而不是同一个名称的三种写法；强行统一成一个字符串会丢失信息。
- **17 个被截断的 `id`**（例如 `…-for-low-`）保持原样：`id` 是永久的 `/p/<id>` 键，所以修正的是生成器，而不是数据。
- **`oneoff/` 中 2.2 MB 的采集 JSON** 保留：它是来源记录，使每个条目都能追溯到它是如何被找到的，而且 `check_links.py` 仍会向其中写入。

## 2026-10-11 — 新增 102 篇论文，整个列表有了中文版，并搬进新家
<!-- en: 102 more papers, the whole list in Chinese, and a new home -->

迄今为止规模最大的一次新增。列表搬进了自己独立的仓库，并且从头到尾实现了双语。

### 内容

- **391 篇论文**（原为 289 篇），时间跨度 **1917–2026**（原为 1976 年起），分属 17 个主题；另有 **44 个工具包**（原为 43 个）、**40 个数据集**（原为 34 个）、19 个基准/挑战赛和 29 项学习资源。**391 篇中有 328 篇（84%）**带有同行评审的出处。
- 新增 **Radon 1917**：提出这一变换的论文，本列表中每一种解析方法所求逆的正是它，发表时间比第一台 CT 扫描机早 54 年。原文没有 DOI，因此该条目链接到 P. C. Parks 在 IEEE TMI（1986）上发表的英译本，并把原文的莱比锡出版信息记为出处。
- 57 篇论文来自 Web of Science 导出结果，只保留了经 Crossref 确认为期刊论文、且属于重建方法（而不是仅仅使用 CT 的应用）的工作。另外 44 篇来自对一篇综述稿参考文献的交叉核对。

### 语言

- 列表、网站界面、静态页面和两份 README 现在都有中英文两个版本。界面文字放在 `data/i18n/` 中；英文是事实来源，其他语言都是在其之上的覆盖层，缺失时回落到英文。
- `/zh/` 提供中文网站，有自己的 canonical URL、`hreflang` 互链和 sitemap 条目。

### 网站

- **`description` 现在在构建时填充。** 它原先直接写着“289 papers”，一加论文就过时了——而这正是搜索引擎展示的文字。
- 修复了明暗主题切换：`app.js` 和 `chrome.js` 里各有一个监听器，所以点一次会切换两次主题。现在它只存在于 `<head>` 中的一段内联脚本里，在首次绘制之前就应用已保存的选择，按钮显示的是它将要切换到的主题的图标。
- EN / 中文 切换从页脚移到了页眉，放在主题切换按钮旁边。
- 网站由 `computedtomography.org` 提供，现在从本仓库发布。
- **条目备注现在会被翻译。** 132 条备注（以及 Radon 条目的备注）在中文网站上都以英文显示，即使已有译文也是如此，因为站点导出直接读取英文字段，从不查询覆盖层。现在每种语言构建自己的数据，如果某条已翻译的备注没有进入该语言的 `data.json`，`build_site.py` 会失败。

## 2026-10-10 — 静态页面、非商业内容许可，不再接受 pull request
<!-- en: Static pages, a non-commercial content licence, and no more pull requests -->

### 新增（“关于”“联系”和“隐私”页面）

- 新增静态页面 `/about/`、`/contact/` 和 `/privacy/`（收录范围与核实方法、如何推荐或更正条目、网站收集和不收集哪些信息）。
- 每个页面都有简洁的页脚链接到它们；保留许可证说明。
- `build_site.py` 从 `web/pages/` 渲染这些页面，并把它们加入 sitemap。

### 变更（维护）

- 列表只由其作者维护，不再接受 pull request。`CONTRIBUTING.md` 和 pull request 模板已删除。条目的数据格式和核实规则现在写在 `MAINTENANCE.md#adding-entries` 中。建议通过 issue 或电子邮件提交。

### 变更（许可）

- **内容现在采用 CC BY-NC-SA 4.0**（原为 CC BY 4.0）；代码仍为 MIT。维护者希望列表得到署名、保持非商业用途，并且改编作品以相同方式共享。`LICENSE-content` 收录了完整、未经修改的法律文本。此变更不溯及既往：此前已按 CC BY 4.0 获得的副本仍保留该许可。
- README 和网站页脚新增联系邮箱：heitieya@163.com。

**列表现已上线：<https://computedtomography.org/>**，每次推送到 `main` 时网站都会重新发布。

## 2026-10-10 — 首次公开发布
<!-- en: First public release -->

首次公开的状态。列表已足够稳定，可以引用。

### 内容

- **289 篇论文**，时间跨度 **1976–2026**，分属 **17 个主题**；另有 **43 个工具包**、**34 个数据集**、**19 个基准/挑战赛**和 **29 项学习资源**。
- 每个论文链接都对照 Crossref、arXiv 或出版方自己的记录解析过，每个 URL 都检查过。
- **289 篇中有 226 篇（78%）**带有同行评审的出处。没有出处的条目以斜体显示为 `preprint year`，因此评审与未评审的区别在 README 中一目了然，而不必让读者去猜。

### 新增

- **三个最薄弱部分的奠基性论文。** 能谱、散射和动态/4D 三个部分分别只有 6、6 和 9 篇，而其他部分有 45–62 篇——原因是缺少这些子领域赖以建立的工作，而不是相关工作本身很少。补回 17 篇论文，使这三部分分别达到 12、11 和 15 篇：Alvarez & Macovski 1976（能谱 CT 的奠基论文）、Roessl & Proksa 2007 和 Schlomka 2008（光子计数 K 边成像）、Elbakri & Fessler 2002 和 De Man 2001（多能谱统计重建）、Siewerdsen & Jaffray 2001 和 Zhu 2006（CBCT 散射的经典参考文献）、Sonke 2005（4D-CBCT 的奠基论文）、Chen 2008（PICCS）、Leng 2008、Rit 2009、Bergner 2010 和 Gao 2012。
- 2025–2026 年的前沿：94 个条目，侧重扩散先验、高斯泼溅、隐式神经表示和动态/4D CBCT。
- `MAINTENANCE.md`、本更新日志、`.editorconfig`，以及 issue/PR 模板。
- **网站源代码，把同一套数据渲染成一个可搜索的单页。** `web/`（模板、样式表、客户端脚本）、`site.config.yml`（标题，以及推导所有绝对地址的唯一 `url`）和 `scripts/build_site.py` 生成 `site/` 目录；`scripts/export_site_data.py` 单独生成 JSON 数据，供任何需要以程序方式获取数据的用途使用。构建读取 `data/*.yaml` 并调用 `build.py` 自己的校验器，因此页面和 README 不可能不一致，而且它不引入任何依赖。`site/` 被 git 忽略，每次重新生成。

  它**已经部署**：<https://computedtomography.org/>，由 `.github/workflows/deploy.yml` 在每次推送到 `main` 时发布。这个工作流最初有意设为只能手动触发——Pages 关闭时 `actions/deploy-pages` 会失败，而一个因与所审改动无关的原因变红的工作流，只会让人学会无视红色——等 Pages 启用后才加上推送触发。`SITE.md` 记录了文件结构、复现这套设置需要在 Settings 中完成的四个步骤、DNS 记录、只需改一行的域名切换方法，以及编写过程中遇到的各种故障情形。`CONTRIBUTING.md` 和 `MAINTENANCE.md` 在撰写时都指向它；`CONTRIBUTING.md` 当天就被删除，README 也没有链接它，所以实际上 `MAINTENANCE.md` 是保留下来的入口。

- **页面本身：一个首屏区、六个统计卡片和一个带边框的检索面板。** 统计卡片读取的是与 README 覆盖率说明相同的计数（`{{N_PAPERS}}`、`{{PEER_PCT}}`……），而不是硬编码数字，因此不会与 `data/` 不一致。卡片和首屏按钮上的 `data-goto` 链接会切换到对应的标签页；关闭 JavaScript 时，它们退化为普通的 `#tabs` / `#q` 锚点。
- **第二轮采集：与两个私人论文笔记合集交叉核对，找回 32 篇论文。** 两个文件合计包含 43 项工作（39 ∪ 34，其中 30 项重合）；10 项已在列表中，33 项是新的。收录了 32 项——第 33 项是一篇不带论文链接的纯学习理论论文，因超出范围而未收录。新增内容偏重最新的会议（CVPR / ICCV / ECCV / ICLR / ICML / NeurIPS / AAAI / ICASSP 2024–2026，另有一篇期刊论文），因为这两个合集在这些会议上最为密集。
- **四个条目的 `paper` 链接既不是 arXiv id 也不是 DOI**——列表中首次出现这种情况。三篇 CVPR 2026 论文（`CryoDeRec`、`Exact-GS`、`GH-NAF`）既没有 arXiv 版本，也没有注册 DOI，因此链接到它们的 CVF OpenAccess 页面；`MedGMAE`（ICLR 2026）链接到它的 OpenReview 讨论页。每一个都对照页面自身的 `citation_title` 元数据或会议的官方列表核实过，README 中的覆盖率说明现在也如实写明了这一点，而不再声称每个链接都来自 Crossref 或 arXiv。

### 修复

- **`scatter-rev` 指向了一对论文中错误的那一篇。** 该条目用的是第 1 部分的标题，却配着第 2 部分的 DOI（`10.1118/1.3589140`），所以链接通向的论文与标题所说的不同。现在两部分都已收录，各自指向自己的 DOI；两个副标题（“Scatter compensation approaches” / “Scatter estimation approaches”）也写进了标题，以便区分。
- **删除 88 个重复条目。** 一轮采集把已在列表中的论文以不同的 `id` 又追加了一遍：已有条目使用简短的缩写 id（`lpd`、`dip`、`super`），采集来的条目使用标题生成的 slug，两者从不冲突，而按 `id` 比较的重复检测因此什么也没发现。现在重复检测使用规范身份（arXiv id、DOI，或规范化标题加年份），同一项工作出现两次时，`build.py` 会让 CI 失败。
- **规范化出处字符串**：85 种不同写法合并为 70 种。这修复了在来源处就被截断的字符串（`the Journal of Machine Learning for Biomedical Imaging (MELB` → `MELBA`）、未转义的 HTML 实体（`Physics in Medicine &amp` → `PMB`）、同义写法的分裂（`IEEE Transactions on Medical Imaging` 与 `TMI`）、重复写在出处里的年份（生成的 README 会把它打印两次），以及六个把预印本服务器（`arXiv`、`TechRxiv`）当作出处的条目。
- **更正了年份**：有些条目记录的是 arXiv 发布年份而不是会议/期刊的年份，还有一个条目的年份和出处是从一篇恰好使用相同短 id 的无关论文那里继承来的。
- 找回 14 个缺失的出处：11 个来自来源记录，另外 3 个——`Epi-NAF` → ISBI 2025、`Generative Modeling in Sinogram Domain` → TRPMS 2024、`CoCoDiff` → SPIE 2022——是在 Crossref 中逐个核对候选 DOI 得到的。其中两个还暴露出任何基于标题的检查都发现不了的年份错误。
- 修复了 8 个失效的目录链接和一个损坏的徽章。
- **两个错误的出处和一个不够精确的出处，都是从来源笔记中继承来的。** `Regularizing INR with Diffusion Prior … Neutron CT` 被记为 CVPR 2025——实际是 **ICASSP 2026**（`10.1109/ICASSP55912.2026.11464479`，第 21947–21951 页，巴塞罗那）；`Variational Garrote for Sparse Inverse Problems` 被记为 CVPR 2025——实际是 **Journal of Computational Science** 2026 年第 100 卷，文章号 102980（`10.1016/j.jocs.2026.102980`）。`Modeling X-ray Photon Pile-up with a Normalizing Flow` 被记为 NeurIPS 2025，这并不算错——它是 **NeurIPS 2025 ML4PS 研讨会**论文，只是需要写得更精确。

  这两处 CVPR 的说法并不是简单地被一个更好的来源推翻；“先有会议版本、后有期刊版本”的解释也被明确排除了，因为那样的话笔记就是对的而不是错的。两篇论文在任何地方都没有 CVPR 记录：CVPR 2025 主会论文集（2,871 篇）中没有，当年 52 卷 CVF 研讨会论文集中也没有；CVPR 2026（4,042 篇 / 86 卷研讨会论文集）和 ICCV 2025（2,701 / 76）中同样没有——而同时收录期刊、会议*和*研讨会的 OpenAlex 为第一篇论文只列出两项作品（ICASSP 2026 + arXiv），为第二篇只列出三项（J. Comput. Sci. + SNU 机构库 + arXiv），Crossref 中也没有登记任何预印本与会议论文之间的关联。“CVPR 2025”这个标签来自那些笔记网站本身，它们把这个标签前后不一地标在一个 2026 年 3 月的 arXiv id 旁边，而且至少有三个网站逐字照搬。

  没有任何出处信息是未经核实就沿用的：每一条都从 arXiv 的 `comment` 字段重新推导，并在 Crossref、OpenAlex 或 dblp 中再次确认。每个 arXiv id 也都通过 arXiv API 回读，而不是按印刷出来的样子直接信任：26 个中有 25 个与条目标题的相似度为 1.000，最后一个只是措辞不同（“neutron computed tomography data”与“neutron CT data”）。
- **`MedGMAE` 收录时没有论文链接。** 它是一篇已被接收的 **ICLR 2026 poster**；OpenReview 记录和会议列表都已找到。
- **新增链接中有一个一上线就是失效的，链接巡检发现了它。** `Efficient Unrolled Networks` 指向 `github.com/romainvo/efficientunrolling`（404）；正确的仓库是 `romainvo/efficient-unrolling`。这正说明了为什么任何导入之后都要跑一遍巡检，而不是信任来源给出的 URL。

### 变更

- **内容现在采用 CC BY 4.0 许可；代码仍为 MIT。** 仓库原先用一个 MIT 许可证覆盖所有内容，这对内容部分来说是错误的许可证：awesome 规范明确说明代码许可证不适用于列表内容（*“We strongly recommend the CC0 license, but any Creative Commons license will work. Code licenses like MIT, BSD, Apache, GPL, etc, are not acceptable.”*）。`LICENSE-content` 现在收录完整、未经修改的 CC BY 4.0 法律文本，覆盖 `data/`、`README.md` 和生成的网站；`LICENSE` 继续覆盖 `scripts/`、`web/` 和 `.github/`。这一划分在 README、网站页脚、JSON-LD 的 `license` 字段、一个 `<link rel="license">` 标签和 CONTRIBUTING.md 中都有说明。

  之所以选它而不是 CC0，是因为列表希望得到署名；之所以不选某个同类项目使用的 CC BY-NC-SA，是因为 NC 会把最需要这份列表的工业 CT 和医疗器械领域的读者排除在外，而 ShareAlike 会阻止任何人把这些条目并入采用宽松许可的项目。此变更不溯及既往：此前已按 MIT 发布的内容，对已经获得它的人仍是 MIT。

- 澄清了工具包和数据集表格中的 `License` 一列描述的是**那些项目本身**，而不是本列表。还检查了 `data/` 中是否有源自其他列表备注的文字——没有；其中唯一的非 ASCII 文字是九处中文作者姓名（庄天戈、张朝宗），论文记录不包含 `authors`、摘要，也没有超过 300 个字符的字段。
- `README.md` 现在由 `data/*.yaml` 生成。如果提交的版本与重新构建的结果不同，CI 会失败，因此 README 不会再与数据不一致。
- 没有出处的条目以斜体显示为 `preprint 2025`，而不是一个孤零零的年份，覆盖率说明也会报告评审与预印本的比例。（后来措辞缩短为斜体中只有年份；见 2026-10-11 条目。）
- 仓库更名为 `awesome-computed-tomography`，并重写了描述、主题标签和 README 中的范围说明，使人们能用这个领域的术语找到本项目，而不只是靠项目名称。
- **GitHub 主题标签现在根据实际测得的仓库数量来选择**，而不是凭关键词猜测。只有一颗星的情况下，只有仓库数远少于约 100 个的主题标签才可能让本仓库出现在第一页，因此加入了列表所涵盖的六个小众标签（`spectral-ct`、`dual-energy-ct`、`limited-angle`、`4d-ct`、`scatter-correction`、`ct-imaging`），去掉了六个无法上榜或重复的标签，尤其是 `medical-image-processing`（931 个仓库，与 `medical-imaging` 含义相同）和 `awesome`（11,730 个，与 `awesome-list` 重复）。有两种写法因为匹配到*零*个仓库而被放弃：`limited-angle-tomography` 和 `dynamic-ct`。
