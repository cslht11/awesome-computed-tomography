<a id="top"></a>
<div align="center">

<img src="assets/logo.svg" width="88" alt="">

# Awesome Computed Tomography

**一份经过核验的 CT 重建研究精选列表**——涵盖 CT、CBCT 与显微 CT 的论文、工具包、数据集与基准。

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![Website](https://img.shields.io/badge/网站-computedtomography.org-3f51b5?style=flat-square)](https://computedtomography.org/) [![Papers](https://img.shields.io/badge/论文-546-555?style=flat-square)](#论文) [![License](https://img.shields.io/badge/许可-CC%20BY--NC--SA%204.0-555?style=flat-square)](#许可)

**[网站](https://computedtomography.org/)** · [论文](#论文) · [工具包与库](#工具包与库) · [数据集](#数据集) · [基准与挑战赛](#基准与挑战赛) · [学习资源](#学习资源) · [研究团队](#研究团队) · [知识图谱](#知识图谱)

</div>

[EN](README.md) · **中文**

<div align="center">

| 546 篇论文 | 52 个工具包 | 79 个数据集 | 19 个基准 | 更新于 2026-10-24 |
| :-: | :-: | :-: | :-: | :-: |

</div>

覆盖稀疏视角、有限角、低剂量、金属伪影、能谱、锥束与 4D CT——从 FBP 与迭代求解器，到展开式网络、扩散先验、神经场与高斯溅射。每条论文链接均对照 Crossref、arXiv 或出版方记录核验。检索与筛选请使用 **[网站](https://computedtomography.org/)**。

## 论文

| | | |
| --- | --- | --- |
| [综述与回顾](https://computedtomography.org/zh/?tab=papers&topic=survey) <sub>25</sub> | [经典与迭代重建](https://computedtomography.org/zh/?tab=papers&topic=classical) <sub>98</sub> | [稀疏视角 CT](https://computedtomography.org/zh/?tab=papers&topic=sparse-view) <sub>186</sub> |
| [有限角层析](https://computedtomography.org/zh/?tab=papers&topic=limited-angle) <sub>52</sub> | [低剂量 CT 去噪](https://computedtomography.org/zh/?tab=papers&topic=low-dose) <sub>94</sub> | [金属伪影校正](https://computedtomography.org/zh/?tab=papers&topic=metal-artifact) <sub>51</sub> |
| [能谱与双能 CT](https://computedtomography.org/zh/?tab=papers&topic=spectral) <sub>22</sub> | [锥束 CT](https://computedtomography.org/zh/?tab=papers&topic=cbct) <sub>89</sub> | [动态与 4D CT](https://computedtomography.org/zh/?tab=papers&topic=dynamic) <sub>26</sub> |
| [散射校正](https://computedtomography.org/zh/?tab=papers&topic=scatter) <sub>12</sub> | [几何标定与运动补偿](https://computedtomography.org/zh/?tab=papers&topic=geometry) <sub>30</sub> | [深度展开与基于模型的学习](https://computedtomography.org/zh/?tab=papers&topic=unrolling) <sub>73</sub> |
| [自监督与免训练方法](https://computedtomography.org/zh/?tab=papers&topic=self-supervised) <sub>43</sub> | [扩散与生成式先验](https://computedtomography.org/zh/?tab=papers&topic=diffusion) <sub>71</sub> | [隐式神经表示](https://computedtomography.org/zh/?tab=papers&topic=inr) <sub>30</sub> |
| [高斯溅射](https://computedtomography.org/zh/?tab=papers&topic=gaussian) <sub>29</sub> | [其他主题](https://computedtomography.org/zh/?tab=papers&topic=other) <sub>64</sub> |  |

## 工具包与库

[在网站上浏览全部 52 条](https://computedtomography.org/zh/?tab=toolkits)

## 数据集

[在网站上浏览全部 79 条](https://computedtomography.org/zh/?tab=datasets)

## 基准与挑战赛

[在网站上浏览全部 19 条](https://computedtomography.org/zh/?tab=benchmarks)

## 学习资源

[在网站上浏览全部 29 条](https://computedtomography.org/zh/?tab=learning)

## 研究团队

[在网站上浏览全部 20 条](https://computedtomography.org/zh/?tab=teams)

## 知识图谱

把整个库画成一张关系网，按类拆成加载很快的小页：团队骨架、数据集与使用它们的论文，以及每个主题一张图——共 1,004 个节点、6,677 条关系，全部由上面的条目投影生成，并以 OpenAlex 的作者与引用数据富集。[打开知识图谱](https://computedtomography.org/zh/graph/)

## 联系方式

本列表由作者策展并维护，不接受拉取请求。如有疑问、勘误，或希望增删某篇论文，请提交 [issue](https://github.com/cslht11/awesome-computed-tomography/issues) 或发送邮件至 **[heitieya@163.com](mailto:heitieya@163.com)**。

## 许可

内容（`data/`、本 README 与生成的页面）采用 [CC BY-NC-SA 4.0](LICENSE-content) 许可：

- **署名**：使用时请注明出处。
- **非商业性使用**：不得用于商业用途，如需商用请先联系。
- **相同方式共享**：改编作品须以相同许可发布。

代码（`scripts/`、`web/`、`.github/`、`assets/`、`site.config.yml`）采用 [MIT](LICENSE) 许可，其中构建时复制进 `site/` 的前端脚本同样属于 MIT。表格中的许可列描述的是**那些项目自身**而非本列表；每条条目都只是指向论文的链接，从不复制论文内容。
