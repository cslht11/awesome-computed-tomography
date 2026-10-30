# 更新日志（中文译文）

本文件是 `CHANGELOG.md` 的中文译文，供网站 `/zh/changelog/` 页面使用；英文原文是唯一的事实来源，两者有出入时以英文为准。

每个条目的标题与英文条目同一日期，标题下第一行用 `<!-- en: 英文标题 -->` 注明它对应的英文条目——构建时按“日期 + 英文标题”配对，所以两个文件的顺序不必一致。还没有译文的英文条目在中文页面上以英文显示；如果某条译文对应的英文条目已不存在（例如英文标题被改了），构建会失败，以免过时的译文无声地留在页面上。改动英文条目的标题时，请同步修改这里的 `en:` 注释。

段落与列表项一律写在一行内：中文句子中间的换行会被当成空格。运行 `python scripts/changelog.py --status CHANGELOG.zh-CN.md` 可以列出尚未翻译的条目。

## 2026-10-30 — 为新增的 25 篇论文补上作者与引用
<!-- en: Authors and citations for the 25 new papers -->

### 新增

- **今天新增的 25 篇论文现已进入知识图谱**，附 OpenAlex 作者信息与 459 条库内引用连线；Siddon 投影算法、OS-EM、DPS 等经典工作被库中大量论文引用。其中 CT 金属伪影挑战赛报告上的一处作者“Jianhua Ma”，OpenAlex 指向的是一位无关的纺织化学研究者；按身份规则，它不与南方医科大学的同名研究者合并。

## 2026-10-30 — 新增 25 篇论文：奠基工作、挑战赛报告、扩散模型基线、能谱 CT
<!-- en: 25 papers: foundations, challenge reports, diffusion baselines, spectral CT -->

### 新增

从审查报告中经过核实的缺失清单新增 25 篇论文（653 → 678），每篇都回读了 Crossref 或 arXiv 记录，并配有中英文原创简介：

- **奠基工作与投影算法：**Hounsfield 1973 年的 EMI 扫描仪论文；OS-EM（Hudson 与 Larkin）及面向透射 CT 的有序子集方法（Erdogan 与 Fessler）；Thibault 等人面向螺旋 CT 的三维统计重建；PI 线精确重建（Zou 与 Pan）；Joseph、Siddon 与距离驱动投影算法。
- **挑战赛与数据集报告：**2016 年 AAPM–Mayo 低剂量 CT 大挑战结果、Mayo 低剂量 CT 图像与投影数据集论文，以及 AAPM 稀疏视角、能谱与金属伪影挑战赛报告。前三篇现在作为"如何引用"显示在对应的基准与数据集页面上。
- **学习型与扩散方法：**GloReDi、RegFormer、用于医学反问题的分数先验（Song 等）、MCG、DPS 与 DDS，以及在 LoDoPaB 与苹果 CT 数据上比较学习型方法的研究（Leuschner 等）。
- **能谱 CT 与观点文章：**两篇光子计数综述、统计多材料分解（Long 与 Fessler）、Wang 的《A Perspective on Deep Imaging》以及 2018 年 TMI 专刊社论。

## 2026-10-30 — 说明论文简介的用途与来源，并署名维护者
<!-- en: What the paper summaries are, and who maintains the list -->

### 变更

- **"关于"页面现在说明了一句话简介的用途和来源。**鼠标停在标题上时出现的简介，是为了帮助判断论文是否值得点开原文；其中不少引用了论文自身的摘要。此前页面写的是条目"绝不是其副本"，与这些引用不符。`LICENSE-content` 现在写明：被引用的摘要文字与论文标题仍归作者与出版方所有，不在本站许可之内；CC 许可涵盖的是本项目自己的遴选、组织、说明与原创简介。
- **署名维护者：**"关于"、"联系"、"隐私"页面与 README 现在写明由 [cslht11](https://github.com/cslht11) 维护，而不是"作者"。

## 2026-10-30 — 每个栏目都有供搜索引擎收录的独立页面
<!-- en: Every section has its own page for search engines -->

### 新增

- **工具包、基准、学习资源、研究团队的独立页面**（`/toolkits/`、`/benchmarks/`、`/learning/`、`/teams/`），与已有的数据集（`/datasets/`）和知识图谱（`/graph/`）一致。首页标签页的地址（`?tab=…`）在搜索引擎看来就是首页本身，所以这几个栏目此前没有可被搜到的独立页面。每个页面都以同样的开头区域开始，完整表格直接写在页面里，并有各自的中英文标题与描述。导航仍是即时切换的标签页；这些页面通过每页页脚新增的一行链接进入，并列入站点地图。

### 修复

- **页脚的"更新于"日期现在与数字栏一致。**此前显示的是构建日期，这也让每天的构建都把所有页面判定为"有变化"。
- **每周链接检查不再把 3D Slicer 与 MosMedData 报为故障。**这两个网站拒绝自动程序访问，但在浏览器中可以正常打开（MosMedData 条目另附有可用的镜像）。

## 2026-10-30 — 知识图谱与其他六个栏目一样成为首页标签页
<!-- en: The Knowledge Graph is a homepage tab like the other six -->

### 变更

- **知识图谱现在是首页的第七个标签页**（`?tab=graph`），与论文、工具包、数据集、基准、学习资源、研究团队一样即时切换，标题样式、版面宽度与语言切换也都一致。此前它是一个独立页面，切换过去或回来都要重新加载网站，会闪一下。
- 每个具体图谱（骨架图、数据集图、各主题图与谱系树）仍是独立页面，就像"数据集"标签下每个数据集都有自己的页面；这些页面上的"← 全部图谱分类"链接，以及各页面导航里的"知识图谱"，现在都回到这个标签页。
- **`/graph/` 地址保留**为独立页面，供搜索引擎收录和已有链接使用，与标签页由同一段代码生成。
- **页面之间的跳转更平滑：**在支持的浏览器中，进入或离开独立页面（具体图谱、数据集页、关于页）时会淡入淡出，而不是白屏闪一下。

## 2026-10-30 — 知识图谱页与其他栏目布局一致；首次访问时导航不再闪动
<!-- en: Knowledge Graph laid out like the other sections; no nav flash on a first visit -->

### 变更

- **知识图谱页现在与其他六个栏目外观一致。**它以同样的开头区域（Logo、标题、统计数字）开始，内容标题与版面宽度也相同，不再是一个窄栏的文字页。两个页面的开头区域由同一份模板生成，不会彼此走样。
- **每个页面的页头都有搜索框。**在首页以外的页面，搜索会跳转到首页的论文列表（按"/"即可聚焦搜索框）。

### 修复

- **首次（无缓存）访问时，切换语言不再先闪到"论文"标签。**此前导航栏的下划线先停在"论文"上，等页面脚本下载完才移到目标栏目；现在导航栏一出现就标好当前栏目。

## 2026-10-29 — 首页开头恢复大气的居中样式，不再重复数字
<!-- en: The homepage intro is big and centred again, without repeating the figures -->

### 变更

- **首页开头恢复为完整的居中样式：**Logo 在上，下面是大标题、一句简介，以及带分隔线的数字栏。简介不再重复数字栏已经给出的数量（"653 篇论文、52 个工具包……"）；数字栏新增"学习资源"一项，此前只有简介里提到它。手机上数字栏分两列显示。

### 修复

- **中文首页的"工具包""数据集""基准与挑战赛""学习资源"标签页，标题此前显示为英文。**现在显示中文。

## 2026-10-29 — 切换语言保持当前标签页；首页开头居中
<!-- en: Language switch keeps the tab you are on; centred homepage intro -->

### 修复

- **切换语言时保留所选的标签页和筛选条件。**语言链接只带着页面打开时的网址，所以在页面里点了某个标签页（比如"数据集"）之后再切换语言，会落到另一种语言的"论文"页。现在它在被点击时读取当前网址，连谱系树卡片这样的 #锚点也会保留。全部 212 个页面和首页的每个标签页都已在两种语言下逐一核验。
- **网址里带主题（?topic=…）时，主题按钮现在会显示为选中。**此前列表已经筛选，按钮却没有亮起。

### 变更

- **首页开头区域居中并放大：**Logo 与标题在同一行，简介与统计数字（论文、工具包、数据集、基准、更新日期）居中排在下方。手机上 Logo 在标题上方。下方的列表仍是居中的版面、文字左对齐。

## 2026-10-29 — 切换标签页与语言不再跳动；导航栏居中
<!-- en: No more jumps on tab and language switches; centred section links -->

### 修复

- **切换语言时不再先闪出"论文"页。**打开带标签页参数的页面（切换语言正是如此）时，浏览器先显示论文列表，等页面脚本运行后才跳到目标标签页。现在在第一帧之前就应用了标签页。
- **切换标签页时页面不再上下跳动。**此前除"论文"外的标签页都会隐藏开头区域，每次切换页面都会跳动一个开头区域的高度；现在所有标签页都保留开头区域。
- **在首页与其他页面之间切换时，页头不再左右移动**：各页面的页头宽度统一（此前只有首页更宽）。

### 变更

- **栏目导航（论文 … 知识图谱）在单独一行中居中显示**，不再从左边开始排列。

## 2026-10-29 — 又为三篇论文补上作者与引用
<!-- en: Authors and citations for three more papers -->

### 新增

- **EFMCT、SR4ZCT 与多阶段平行束伪影校正论文现在在知识图谱中有了作者与引用**（新增 10 条库内引用连线）。上次抓取图谱数据时，OpenAlex 尚未收录它们。其作者被拆分的 OpenAlex 身份（Jiayang Shi；以两种写法出现的 K. Joost Batenburg）按与其他作者相同的证据规则合并。仍有五篇论文没有 OpenAlex 记录：三篇 CVPR 2026、一篇 ICLR 2026 与一篇未发表稿件。

## 2026-10-29 — 论文年份统一为一条规则，每周与 Crossref 核对
<!-- en: One year rule for papers, checked weekly against Crossref -->

### 修复

- **24 篇论文的年份改为遵循同一条规则。**期刊论文按其所在期次的年份标注（即参考文献的通常写法）；尚未分配期次的在线优先或 IEEE Early Access 论文，先用上线年份，分配期次后再更新；会议论文用会议年份。533 篇带 DOI 的论文中已有 507 篇如此。其余 24 篇（多为按 Early Access 年份标注的 IEEE 论文）现改为期次或会议年份：例如 Momentum-Net 为 TPAMI 2023（Early Access 为 2020）；其中 8 篇此前标为 2025 年，实际在 2026 年发表。
- **ADMM 专著**（Boyd 等）此前写的是期刊名，链接的却是 2010 年的图书版；现改为链接期刊文章（Foundations and Trends in Machine Learning 3(1)，2011）。

### 新增

- **每周一次的 Crossref 回读**（`scripts/check_years.py`）：按 DOI 核对每篇论文的年份与标题，随每周链接检查一起运行。这样，把 arXiv 链接升级为 DOI 却没有回读记录的情况，一周之内就能被发现。

## 2026-10-29 — 知识图谱：一人一个节点，团队负责人按身份锁定
<!-- en: Knowledge graph: one node per person, team leads pinned by identity -->

### 修复

- **被 OpenAlex 拆成多个身份的作者现在合并为一个节点。**例如 Jiliu Zhou、Cynthia McCollough、Yang Chen 与 Qiegen Liu 都被 OpenAlex 拆成了多个作者 ID，他们的论文因此分散在重复的节点上。新文件 `data/graph/author_overrides.yaml` 把 43 个这样的 ID 合并到 56 位作者名下。只有在有证据时才合并，并在旁边注明证据：相同的 ORCID、库内至少三位共同作者，或同一机构且至少一位共同作者。
- **团队负责人按身份关联，而不是按姓名。**此前凡是与团队负责人同名的作者都会得到一条"负责"连线，于是五个不同的"Yang Chen"记录都成了东南大学团队的负责人，其中一个是电网工程师的档案。现在每个团队的负责人都锁定到经过核实的 OpenAlex ID；例如 LLNL 的 Hyojin Kim 现在链接到 LLNL 的档案，而不是被 OpenAlex 与一位眼科医生混在一起的那个档案。

## 2026-10-29 — 数据与图谱修正：真正的 CBCT 数据集、主题调整、2016 年 Mayo 挑战赛数据、谱系连线的性质
<!-- en: Data and graph corrections: a real CBCT dataset, topic fixes, the 2016 Mayo challenge data, editorial lineage links -->

### 修复

- **替换了"Cone-Beam CT (CBCT) Head & Neck"。**它声称提供配对的计划 CT 与机载 CBCT，链接的却是 TCIA 的 Head-Neck-Cetuximab 数据集，其中根本没有 CBCT。改为收录 **Pancreatic-CT-CBCT-SEG**（TCIA，CC BY 4.0）：40 例患者，每例含一次计划 CT 与两次 CBCT，两类图像上都有危及器官轮廓。原页面 `/datasets/cbct-head-and-neck/` 已删除。
- **18 个基于学习的方法移出了"经典与迭代重建"**（该主题的定义是手工设计的正则项）。展开网络（FISTA-Net、Momentum-Net、iRadonMAP 等）、可学习的滤波器与正则项，以及嵌入迭代循环的扩散先验，现在归入各自的方法主题；该主题现有 80 篇论文。
- **2016 年 Mayo 挑战赛数据单独成为一个数据集。**2017 年以来有 29 篇论文写明使用的是"2016 年 AAPM–Mayo 低剂量 CT 大挑战"的数据，图谱却把它们记在 TCIA 的 LDCT-and-Projection-data 名下——那是更晚（2020 年 12 月）发布的数据集，只包含挑战赛 30 例中的 13 例。新增数据集条目 **2016 Low Dose CT Grand Challenge data**，链接到完整的 30 例重新发布版，这些使用关系现在指向它。确实使用 TCIA 数据库的两篇论文保持不变。

### 变更

- **新增主题"相关工作：重建之外"**（25 篇）：CT 基础模型、分析与生成模型（Merlin、CT-CLIP、MAISI、GenerateCT 等），跨成像模态训练的一体化复原模型，一个 MRI 方法（Deep ADMM-Net），以及重建工作所依赖的通用网络（CycleGAN、Noise2Noise、MSD-Net）。它们仍作为背景收录，排在最后，没有主题页，也不再挤占"其他主题"（现为 54 篇）。MAINTENANCE.md 写明了收录范围规则以及"经典"一词的含义。
- **谱系树说明了连线的含义。**31 条连线中只有 4 条是引用关系（后一篇论文引用了前一篇），其余是策展人对研究脉络的解读。现在引用关系画成实线，其余画成虚线，并配有分别计数的图例。

## 2026-10-29 — 首页布局：紧凑的开头、主题侧栏、固定的筛选栏、年份标题
<!-- en: Homepage layout: compact header, topic sidebar, sticky filters, year headings -->

### 变更

- **列表从更靠上的位置开始。**开头区域（Logo、标题、简介与数字）此前约 600 px 高，笔记本屏幕上第一篇论文在 y = 974 处，手机上则在首屏之外。现在它是一个紧凑的区块，笔记本屏幕上第一篇论文出现在 y ≈ 500 处。手机上隐藏了数字一行，因为上方的简介已给出全部数量。
- **宽屏上的主题侧栏。**屏幕宽度不小于 1080 px 时，17 个主题改放在列表左侧的一栏，不再在列表上方排成四五行标签；滚动时这一栏保持可见。宽屏上首页的版面也更宽（最宽 1280 px）。
- **筛选栏随手可用。**桌面端滚动论文列表时，筛选栏（状态、有代码、年份、排序与结果数）固定在页头下方。
- **开头区域只在"论文"标签页显示。**其他标签页直接从表格开始。

### 新增

- **论文列表按年份分组的标题**，并注明该年的篇数；只要列表按年份排序就会显示。它们是真正的标题元素，读屏用户可以逐年跳转。按标题排序或按搜索相关度排序时不显示。

## 2026-10-29 — 首页减重、图谱库的许可声明、每周链接检查
<!-- en: Lighter homepage, licence notices for the graph libraries, weekly link check -->

### 变更

- **首页轻了约四分之一**（1.33 MB → 1.02 MB；压缩后 308 → 228 KB）。每篇论文的一句话简介此前在页面里存了两份，现在只存一份，由页面脚本读回。列出全部论文的结构化数据已删除：其中每一项都指向站外，没有任何搜索功能使用它，而且它是所有标题的第三份拷贝。`data.json` 不变。
- **IndexNow 只推送有变化的页面。**此前每次部署都把全部 210 个网址提交给搜索引擎；现在只提交自上次部署以来内容有变化的页面。

### 新增

- **sigma.js 与 graphology 的许可声明。**网站提供的这两个图谱库副本开头现在附有各自的 MIT 许可全文，仓库中库文件旁也放了许可文件。
- **每周链接检查。**每周一检查数据中的全部网址（论文、工具包、数据集、基准、学习资源与团队）；发现失效链接会自动开一个 issue。

## 2026-10-29 — 网站修复：深色模式可读、换行、斜体、无障碍、/topics/
<!-- en: Site fixes: readable dark mode, wrapping, emphasis, accessibility, /topics/ -->

### 修复

- **深色模式：**每篇带代码的论文旁的"code"按钮此前是浅靛蓝底白字（对比度 2.49:1），现改为深色文字（7.45:1）。新增的 `--on-accent` 颜色变量在两种主题下分别给出合适的取值。
- **手机上的更新日志页：**行内 `code` 此前禁止换行，长文件路径把 375 px 宽的屏幕撑到 560 px，手机因此把整页缩小显示。现在行内代码在必要时会换行。
- **许可证列：**许可证此前沿用数字列的样式，永不换行：手机上长许可证被截断，宽屏上许可证列比"说明"列还宽。现在可以换行（工具包与数据集表）。
- **斜体可以显示了：**`*text*` 与 `_text_` 此前原样显示（例如 `*why*`、`_preprint_`）。构建端与浏览器端的 Markdown 渲染现在都支持斜体，而且只在词边界生效、规则一致，所以 `snake_case` 名称与网址不受影响。
- **图例与网站一致：**论文图例此前仍在描述旧版 README（"同一主题内""以斜体给出"）；数据集图例提到网站上并不存在的"数据"列。两段都已重写（中英文）。
- **无障碍（axe-core 检查：首页、关于页、主题索引、谱系页与更新日志页现均为 0 违规）：**论文标题不再共用同一个 ARIA 标签——此前读屏软件会把 653 篇论文读成同一句话；标签列表里只放标签（抽屉标题、图谱与 GitHub 链接移到其旁边）；搜索框声明为 combobox；手机上文字被隐藏的 Logo 与 GitHub 链接有了名称；谱系画布为卡片补上了一级标题。
- **谱系画布：**此前打开时约为 12% 的缩放（卡片文字约 2 px）。现在从根卡片开始、以可读的比例打开，双击仍可查看全图。普通鼠标滚轮会滚动页面，不再被画布拦截；按住 Ctrl/⌘ 再滚动或双指捏合即可缩放。
- **主题图谱页**各自有了独立的页面描述（此前 17 页共用一条）。

### 新增

- **`/topics/`**（以及 `/zh/topics/`）列出全部主题页及其论文数与一句话说明；此前该地址是 404。每个主题页的"主题"面包屑现在链接到它。
- `tests/test_seo.js` 检查站点地图中每个页面的描述在同一语言内不重复，并检查 `/topics/` 链接了每个主题页。

## 2026-10-29 — 部署须等校验通过；静态资源带版本号；last_updated 受检查
<!-- en: Deploys wait for validation; cache-busted assets; a guarded last_updated -->

### 变更

- **网站只在 `validate` 通过后才更新。** 此前 `deploy.yml` 在每次推送时与 `validate.yml` 并行触发，因此一次校验失败的推送（README 过期、提交者不是本账号、jsdom 测试失败）照样会上线。现在它通过 `workflow_run` 在 `validate` 于 `main` 推送上成功之后运行，并且构建的正是 validate 检查过的那个提交。从 Actions 页手动部署仍然可用。
- **每个页面的样式表和脚本都带上内容哈希**（`styles.css?v=…`、`app.js?v=…` 等），与图谱页和谱系页的资源一致。GitHub Pages 会把文件缓存十分钟，否则访客可能拿到新页面配旧脚本。`tests/test_seo.js` 发现任何未带版本号的引用都会失败。
- **站点地图的 `<lastmod>` 改用内容日期**（`data/meta.yaml` 的 `last_updated`），不再用构建日期，因此不改数据的重新构建不会再把全部 208 个页面标为"已修改"。

### 新增

- `scripts/check_last_updated.py`，由 `validate` 运行：当 `data/` 在 `last_updated` 之后又有改动时报错。`last_updated` 是首页、两份 README、JSON-LD、`llms.txt` 和站点地图共同读取的唯一手写日期。提交本身的日期或其上海时区日期任一满足即可，所以在任一时区深夜提交都不会误报。
- MAINTENANCE.md：仓库结构图涵盖分片后的论文与摘要、图谱、团队、主题、指南和谱系；CI 一节列出 `validate` 现在检查的内容；**"Checklist: adding one paper"** 列出新增一篇论文会涉及的全部文件——两份摘要、`last_updated`、OpenAlex 步骤（它从 GitHub 读取数据，所以是第二次提交）以及谱系简介里手写的论文数量。SITE.md 说明了部署链路、静态资源版本号和站点地图日期。

## 2026-10-29 — 修正外部审查发现的条目错误
<!-- en: Corrected records found by an outside review -->

### 修复

- **数据集、基准与学习资源。**《Foundations of Image Science》此前链接的 DOI 实际指向 Wiley 的另一本书（Spall《Introduction to Stochastic Search and Optimization》），现改为 Barrett & Myers 这本书的 Wiley 页面。**CT-RATE** 此前链接的 Zenodo 6406114 实为 RAD-ChestCT，现改为 Hugging Face 上的数据集，并补上其许可（CC BY-NC-SA 4.0）。**2DeteCT** 此前链接的 Zenodo 6984866 是一份医学病例报告，现改为该数据集在 *Scientific Data* 上的数据描述论文。**STOIC 2021** 此前链接的 IDC 页面会落到集合索引页，且写成 10,735 例、CC BY-NC 3.0；公开发布的是 AWS Open Data 上的 2,000 例，许可为 CC BY-NC 4.0。**AAPM 2016 低剂量 CT 大挑战**的说明（以及低剂量指南的问答）称其确立了"1/4 剂量 / 10% / 5% 协议"；实际该挑战只用了 1/4 剂量数据，共 30 例腹部病例（10 例训练、20 例测试）。**SPARE 挑战赛**的年份是 2018，不是 2024。
- **论文。**《Learned denoising with simulated and experimental low-dose CT data》是 Sci Rep 2025（2025-12-04 在线发表），不是 2026；其代码链接指向一个不存在的仓库，已删除。DDDM 改为链接 IEEE SPL 正式论文，不再链接 TechRxiv 预印本。三个条目改用正式发表版本的题名与年份（作者与预印本相同）：MedIA 上的扩散模型综述（2023）、ProCT（《Universal Pre-training for Generalizable Incomplete-View CT Reconstruction》）以及 4D-CBCT 高斯论文（《Dynamic Cone Beam CT Reconstruction via Spatiotemporal Gaussian Neural Representation》）。三个代码链接改为仓库更名后的地址（DiffusionMBIR、MAGIC、SparseViewCT-TCI），三处期刊名统一为"TRPMS"，与其余十六处一致。
- **中文首页。**/zh/ 首屏的导语此前以英文标语开头；现在 `{tagline}` 按语言填充，DOM 测试也会检查这一点。

## 2026-10-28 — 4D-Lung 数据集
<!-- en: 4D-Lung dataset -->

### 新增

- **4D-Lung**（TCIA，CC BY 3.0）：20 例肺癌患者放化疗期间的四维扇束 CT 与四维锥束 CT，附轮廓标注；只有图像，没有原始投影。PRIOR 在该数据上训练和测试，已记为一条经过核实的数据集使用关系。数据集 79 → 80。

## 2026-10-27 — 新增三篇论文，arXiv 审核后撤下三篇
<!-- en: Three papers added, three withdrawn after an arXiv audit -->

### 新增

- Jiayang Shi 等人的三篇论文：**EFMCT**（MICCAI 2026）、**Multi-stage deep learning artifact reduction for parallel-beam CT**（J. Synchrotron Radiat. 2025）与 **SR4ZCT**（MLMI 2023），并附六条经过核实的数据集使用关系。

### 移除

- 对仅有 arXiv 版本的论文审核后，撤下三条：`baggagect`、`temporal-ct-per-bundle` 与 `care-ct-foundation`（最后一条原是收录范围的例外，且没有正式发表的论文）。论文数回到 653 篇。

### 修复

- 审核后续：一篇论文的期刊与年份改为 TMI 2026；为两篇论文补上代码链接；两条说明改为描述其代码仓库的当前状态。

## 2026-10-26 — 11 篇原预印本补上正式发表的期刊/会议；13 条数据集使用关系
<!-- en: Published venues for 11 former preprints; 13 dataset-usage links -->

### 变更

- **11 篇原标为预印本的论文补上了正式发表的期刊或会议**（依据 DOI 记录）：PMB 2026、Off-Grid Workshop 2026、Fully3D 2025、BMVC 2026、NeurIPS 2025、TMI 2026、MICCAI 2025、CVPR 2026、MIDL 2025、WACV 2025 与 ECCV 2024，年份改为正式发表的卷期年份。

### 新增

- 知识图谱中新增 **13 条人工核实的数据集使用关系**（分五批，33 → 46），每条都引用论文自身实验部分的原文。

## 2026-10-25 — 团队梳理完成；图谱数据更新
<!-- en: Team sweeps complete; graph data refreshed -->

### 新增

- **来自"团队"目录中最后六个课题组的 41 篇论文**（团队梳理第 15–20 批），另有 GeoAtt 改为指向其真正对应的论文，以及谱系树中新增的 CNN-inverse 卡片。论文从 611 篇增至 653 篇。
- **图谱数据更新**：为 10 月 22 日以来新增的 116 篇论文补上 OpenAlex 作者信息，以及 1,110 条库内引用连线。

### 修复

- 内部重建（interior tomography）论文的年份：依据其 DOI 应为 2022（PMB），而不是 2025。

## 2026-10-24 — 团队梳理：来自各课题组的 65 篇论文
<!-- en: Team sweeps: 65 papers from the research groups -->

### 新增

- **来自"团队"目录中各课题组的 65 篇论文**（团队梳理第 3–14 批）：JHU 6 篇、Fessler（密歇根）4 篇、Mayo Clinic 23 篇、UW–Madison 5 篇、Purdue 2 篇、LLNL 1 篇、Argonne 2 篇、FAU Erlangen 6 篇、剑桥 4 篇、CWI 4 篇、安特卫普 2 篇、KTH 6 篇。论文从 546 篇增至 611 篇。

## 2026-10-24 — 图谱索引把谱系树并入总览
<!-- en: Graph index folds lineages into Overview -->

### 变更

- **/graph/ 索引现在是两个小标题，不再是三个。**此前手工策展的谱系树单独占一个"经典脉络"标题、下面只有一张卡，页面显得零散。现在它并入总览，和团队骨架、数据集两张卡排在一行，顺序不变；"按主题"仍单独成节，因为 17 张主题卡会淹没 3 张总览卡。索引导语里也补上了谱系树。

## 2026-10-24 — 中文图谱主题名修复，测试门关上
<!-- en: Chinese graph topic labels, and the test gate closes -->

### 修复

- **中文图谱页的主题名现在是中文了。**此前图谱构建用的数据没有经过主题名翻译，所以 /zh/graph/ 的画布节点全是英文，而旁边的索引卡片却是中文。主题名现在直接在数据里翻译，构建时还会断言翻译后的切片主题节点必须带翻译标签，缺了就失败。
- **页面脚本语法错误现在会让构建失败。**此前 CI 从不执行网站自己的脚本，app.js / graph.js / lineage.js 写坏了也能全绿上线。构建现在会对 6 个页面脚本跑 `node --check`，两个流程都跑构建，所以两边都会拦住。
- **渲染页测试覆盖了谱系树、每种语言各一张图谱切片和抽屉。**直接断言 pointer 捕获规则（只按下不捕获、真拖拽才捕获）、干净点击能到达卡片链接、图谱回退列表正常且主题名语言正确、抽屉开关正常。把它接进 CI 需要改 workflow 文件，仓库的 App 连接推不上去，补丁另外交接。

## 2026-10-24 — 子页面导航标出当前栏目
<!-- en: Sub-page nav marks the current section -->

### 修复

- **子页面的导航现在也会给当前栏目加下划线，和首页标签一样。**此前子页面导航只是普通链接，没有任何当前状态，所以在 /graph/（以及每个数据集、基准、指南、主题页）上所有标签都没有下划线，知识图谱那一项看起来像是坏的。现在共享模板生成的页面都会标出自己的栏目（图谱、数据集、基准、指南归入学习资源、主题归入论文）；没有对应栏目的页面（更新日志、关于、联系、隐私）则诚实地什么都不标。子页面导航还补上了缺失的研究团队链接，终于和首页一样是七个栏目。SEO 检查会对 sitemap 中的每一页断言这个标记。

## 2026-10-24 — 工具包页按类别分组，组内按星标排序
<!-- en: Toolkits tab groups by category, stars within each group -->

### 变更

- **工具包页现在先按类别分组，组内再按星标排序。**此前是整表按星标排，MONAI、3D Slicer、pydicom 这类通用大库永远霸占前面，CT 专属工具被埋在很后面，而且手机上星标列要横滑才看得到，顺序看起来毫无根据。九个分组就是数据文件本来就有的分节（重建引擎、可微 / 学习、仿真与物理、I/O 框架、经典 / 统计、参考实现、数据增强与仿真、平台与查看器、算子 / 物理与同步辐射）。星标快照也刷新到了今天；ESRF 的 pyHST2 因 GitLab 项目这边测不到，仍显示无星标。

## 2026-10-24 — 谱系树卡片链接可以点了
<!-- en: Lineage tree card links are clickable -->

### 修复

- **谱系树卡片上的链接（标题、Paper、Code）现在能点开了。**此前画布控制器在每次按下时就捕获指针，Chrome 里这会把随后的点击重定向到画布本身，所以卡片上的任何链接都点不开——画布下方的阅读清单链接不受影响，这也是这个问题长期没被发现的原因。现在捕获只在手势真正变成拖拽（或第二根手指加入捏合）时才生效，装饰性的连线也不再拦截指针事件，点击和轻触都能落到下面的链接上。拖拽后的点击屏蔽逻辑不变。视口适配也加了防护：拒绝样式表生效前的畸形测量值，并在文档加载完成后重新适配一次，堵上慢网络下树被甩出可视区的竞态窗口。

## 2026-10-24 — 语言切换停留在当前页
<!-- en: Language switcher stays on the page -->

### 修复

- **中文/EN 切换现在切的是你正在看的这一页。**此前切换链接是按语言从语言根目录统一生成的，所以在任何子页面——图谱页与谱系树、更新日志、主题页、数据集与指南页、独立页面——点切换都会落到另一种语言的首页，而不是当前页的对应语言版本。现在切换链接按页生成，指向该页自身的 hreflang 对应页，SEO 检查也会对 sitemap 中的每一页断言这个目标。

## 2026-10-23 — 经典脉络：一张画布上的谱系树
<!-- en: Curated lineages: the family tree on one canvas -->

### 变更

- **第一条经典脉络改版为一张可平移缩放画布上的分叉谱系树。**脉络页（`/graph/lineage/fbp-to-foundation/`）不再把故事画成纵向单链：画布上是 29 篇论文加两个分支分组框（学表示本身、基础模型）的手工策展树，从解析重建的根 FDK 出发，分叉经过全变分、即插即用先验、双域网络、隐式与显式表示、生成先验，最终汇入基础模型。布局在构建时算好——卡片定位、正交连线、每一步一条点明步子的短标签——画布可平移缩放（拖拽、滚轮、双指捏合、键盘），打开时先 fit 全景，并支持以 `#<论文 id>` 深链直达某张卡片。策展长文移到画布下方的阅读清单，按深度优先顺序排列，页面全文不依赖画布也能读完。`data/lineages.yaml` 改存树本身（单亲链接、画布标签、分组框），构建时按树校验：有且只有一个根、无环无孤点、每条根路径年份不递减。图谱索引卡改为只数论文里程碑（"29 个里程碑 · 1984–2026"）。

## 2026-10-23 — 经典脉络：从 FBP 到基础模型
<!-- en: Curated lineages: from FBP to foundation models -->

### 新增

- **知识图谱下新增一类页面：经典脉络**（`/graph/lineage/fbp-to-foundation/`，中文版 `/zh/graph/lineage/fbp-to-foundation/`）。一条脉络是少量手工挑选的论文连成的一个故事，按纵向时间线渲染成卡片链：每一步都有一句策展说明，讲清它为什么是里程碑；每两步之间都有一段文字，写明上一步卡在哪里、下一步的想法从何而来。第一条脉络《从 FBP 到基础模型》用十一篇论文从 FDK（1984）走到 TAMP（2026），追踪一条主线——先验住在哪里：固定滤波器、手写的稀疏假设、可插拔的去噪器、学习型网络、生成式扩散模型，直到预训练基础模型。脉络数据放在新文件 `data/lineages.yaml` 里，构建时按其他策展栏目同样的标准校验：引用的每篇论文必须在库中存在、两种语言必须齐全、链条必须按时间顺序；而卡片本身的标题、年份、发表出处与链接都取自论文条目，因此条目的更正会自动反映到卡片上。图谱索引新增"经典脉络"一节，链向每条脉络页。与图谱的分类页不同，脉络页从头到尾是静态 HTML：没有切片数据、没有 JavaScript，也不存在画布空白那类故障。

## 2026-10-22 — README 新增知识图谱一节
<!-- en: README: Knowledge Graph section -->

### 新增

- **两版 README 现在都链到知识图谱。** 图谱在网站上早已上线，但 GitHub 首页一直没有提它：顶部快速导航与章节列表都止于研究团队一节。现在 `README.md` 与 `README.zh-CN.md` 在研究团队之后新增"知识图谱"一节——由 `scripts/build.py` 依新的 `graphHeading`/`graphBody` 文案生成——链到 computedtomography.org/graph/ 的分类图谱索引（中文版 /zh/graph/），导航行也加上同一链接。

## 2026-10-22 — 知识图谱：拆成分类小图谱
<!-- en: Knowledge Graph: split into small per-category graphs -->

### 变更

- **单一图谱页改为一个索引加每个分类一张小图。** 此前 1,004 个节点的页面要求每位读者的浏览器一次性加载并绘制整张图，在普通硬件上太大、太慢，无法使用。现在 `/graph/` 是分类索引：团队骨架（92 个节点：团队、主题、工具包、指南）、数据集关系（138 个节点：全部数据集与基准，加上使用它们的论文），以及每个主题一张图（每张至多 250 个节点）。每个分类页只加载自己的切片——节点、边与预计算位置打包在一个小文件里（5–76 KB），由新的构建步骤（`scripts/graph_slices.py`）在构建时生成——详情面板、邻居高亮与搜索保持不变。全图模式随之取消，单一大文件 `graph.json` 也不再存在：现在分类本身就是筛选。

## 2026-10-22 — 知识图谱：预计算布局与单一快速渲染器
<!-- en: Knowledge Graph: precomputed layout, one fast renderer -->

### 变更

- **图谱页改为在构建时完成布局，并由单一 WebGL 渲染器绘制。** 节点位置由新的构建步骤（`scripts/graph_layout.py`，带 Barnes–Hut 斥力的 Fruchterman–Reingold 布局）离线算好，随 `graph.json` 一起发布；浏览器不再运行任何力导向模拟。渲染改用自托管的 sigma.js + graphology（批量 WebGL 程序），取代此前的两个视图：Cytoscape 2D 视图（每次交互都要重跑 cose 布局）与 3d-force-graph 3D 视图（three.js 逐对象渲染，在这个规模下明显卡顿；且两者切换需要整页刷新、会丢失读者当前的位置）。交互方式不变——骨架优先、点击展开、自我网络、搜索、类型/主题/地区过滤、全图模式与同一个详情面板——只是现在快了，标签也随缩放层级显隐，不再在任何距离上互相重叠。

## 2026-10-22 — 知识图谱：3D 视图
<!-- en: Knowledge Graph: a 3D view -->

### 新增

- **图谱页新增 3D 视图**（`/graph/`，中文版 `/zh/graph/`），由自托管的 3d-force-graph 库渲染。它使用同一份 `graph.json`，交互模型与 2D 版一致——团队/主题/工具包骨架、点选展开邻居、搜索时镜头飞向目标节点、按类型/主题/地区筛选、全图模式——场景可旋转、缩放和拖动。工具栏有 2D/3D 切换按钮，可切回 Cytoscape 视图（选择会被记住）；WebGL 或库文件不可用时，页面照旧由 2D 视图提供。为保证场景可读，常驻标签只给团队、主题和高度数枢纽节点，且一律显示完整文字；其余节点由悬停提示给出名称。

## 2026-10-22 — 知识图谱：目录中一切条目的关系网
<!-- en: Knowledge Graph: how everything in the directory connects -->

### 新增

- **网站新增知识图谱页（`/graph/`，中文版 `/zh/graph/`）。** 本目录的全部条目及它们之间的关系——上线时共 1,004 个节点、6,603 条边。图谱在构建时由与网站其余部分相同的数据生成（`graph.json`），因此永远不会与目录脱节。打开时默认显示 20 个团队、17 个主题与 52 个工具包组成的骨架；点选任意节点即可展开它的邻居网络，另提供搜索、按类型/主题/地区筛选与全图模式。
- **新增图谱侧数据集（`data/graph/`），带来作者与引用关系。** 已从 OpenAlex 为全部 537 篇论文拉取作者名单与参考文献：531 篇匹配成功（413 篇按 DOI、116 篇按 arXiv 号、2 篇按标题），得到 3,341 对库内引用关系（引用双方都在库中）。这些数据只存在于图谱数据里——文库条目本身没有改动，论文数据仍然不带 authors 字段。作者节点只收录在库论文不少于 3 篇的作者以及 20 个团队的负责人（共 189 位）；负责人与团队之间只在姓名精确一致时才连边（20 个团队中 19 个）。在库论文不少于 2 篇的发表出处（59 个）也成为节点。
- 构建会像校验其他分区一样校验图谱：`data/graph/` 引用的每个论文 id 必须存在，引用对不得重复、不得自引，生成的图谱节点计数必须与目录各表对得上。

## 2026-10-20 — 研究团队：20 个 CT 重建团队的目录
<!-- en: Research Teams: a directory of 20 CT reconstruction groups -->

### 新增

- **网站新增"研究团队"标签页，数据来自新文件 `data/teams.yaml`。** 收录本库所收论文、工具与数据的 20 个研究团队——北美 9 个、欧洲 7 个、亚洲 4 个——每条给出所在机构、负责人、研究方向、简短的双语事实介绍，以及该团队已被本库收录的代表作链接。构建会像其他表一样校验这一分区：每个被引用的论文 id、工具包、数据集与基准都必须能解析到真实条目，每个方向标签都必须是合法的主题 id。
- README 新增**研究团队**一节，指向该标签页；五格统计条保持不变。

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
