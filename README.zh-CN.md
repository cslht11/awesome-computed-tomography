<a id="top"></a>
<div align="center">

<img src="assets/logo.svg" width="88" alt="">

# Awesome Computed Tomography

**一份经过核验的 CT 重建研究精选列表**——涵盖 CT、CBCT 与显微 CT 的论文、工具包、数据集与基准。

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![Website](https://img.shields.io/badge/网站-computedtomography.org-3f51b5?style=flat-square)](https://computedtomography.org/) [![Papers](https://img.shields.io/badge/论文-391-555?style=flat-square)](#论文) [![License](https://img.shields.io/badge/许可-CC%20BY--NC--SA%204.0-555?style=flat-square)](#许可)

**[网站](https://computedtomography.org/)** · [论文](#论文) · [工具包与库](#工具包与库) · [数据集](#数据集) · [基准与挑战赛](#基准与挑战赛) · [学习资源](#学习资源)

</div>

[EN](README.md) · **中文**

| 391 篇论文 | 84% 同行评议 | 87 项附代码 | 44 个工具包 | 40 个数据集 | 19 个基准 | 1917–2026 |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |

覆盖稀疏视角、有限角、低剂量、金属伪影、能谱、锥束与 4D CT——从 FBP 与迭代求解器，到展开式网络、扩散先验、神经场与高斯溅射。每条论文链接均对照 Crossref、arXiv 或出版方记录核验。检索与筛选请使用 **[网站](https://computedtomography.org/)**。

## 论文

| | | |
| --- | --- | --- |
| [综述与回顾](#综述与回顾) <sub>23</sub> | [经典与迭代重建](#经典与迭代重建) <sub>70</sub> | [稀疏视角 CT](#稀疏视角-ct) <sub>133</sub> |
| [有限角层析](#有限角层析) <sub>44</sub> | [低剂量 CT 去噪](#低剂量-ct-去噪) <sub>57</sub> | [金属伪影校正](#金属伪影校正) <sub>21</sub> |
| [能谱与双能 CT](#能谱与双能-ct) <sub>17</sub> | [锥束 CT](#锥束-ct) <sub>66</sub> | [动态与 4D CT](#动态与-4d-ct) <sub>21</sub> |
| [散射校正](#散射校正) <sub>11</sub> | [几何标定与运动补偿](#几何标定与运动补偿) <sub>26</sub> | [深度展开与模型驱动学习](#深度展开与模型驱动学习) <sub>72</sub> |
| [自监督与免训练方法](#自监督与免训练方法) <sub>32</sub> | [扩散与生成式先验](#扩散与生成式先验) <sub>56</sub> | [隐式神经表示](#隐式神经表示) <sub>24</sub> |
| [高斯溅射](#高斯溅射) <sub>25</sub> | [其他主题](#其他主题) <sub>28</sub> |  |

同一主题内按最新在前排列。每条条目以斜体给出出处与年份；_预印本_ 表示该工作尚未（或还未）发表于同行评审的会议或期刊，年份取首次公开的时间。

### 综述与回顾

<sub>概述性论文、教程与对比研究 · 23 篇论文</sub>

- **DM4CT: Benchmarking Diffusion Models for CT Reconstruction** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2602.18589) · [代码](https://github.com/DM4CT/DM4CT)
- **Are Pixel-Wise Metrics Reliable for Sparse-View Computed Tomography Reconstruction?** — _NeurIPS 2025_ · [论文](https://arxiv.org/abs/2506.02093) · [代码](https://github.com/MrGiovanni/CARE)
- **Synthetic CT image generation from CBCT: A Systematic Review** — _TRPMS 2025_ · [论文](https://arxiv.org/abs/2501.13972)
- **A Review of Deep Learning CT Reconstruction From Incomplete Projection Data** — _TRPMS 2024_ · [论文](https://doi.org/10.1109/trpms.2023.3316349)
- **DiffRecon: Diffusion Models for Medical Image Reconstruction** — _BJR|AI 2024_ · [论文](https://doi.org/10.1093/bjrai/ubae013)
- **Machine learning in industrial X-ray computed tomography - a review** — _CIRP JMST 2024_ · [论文](https://doi.org/10.1016/j.cirpj.2024.05.004)
- **DiffMed: Diffusion Models for Medical Image Analysis: A Comprehensive Survey** — _预印本 2022_ · [论文](https://arxiv.org/abs/2211.07804)
- **Review of high energy x-ray computed tomography for non-destructive dimensional metrology of large metallic advanced manufactured components** — _RoPP 2022_ · [论文](https://doi.org/10.1088/1361-6633/ac43f6)
- **A review on deep learning in medical image reconstruction** — _JORSC 2020_ · [论文](https://arxiv.org/abs/1906.10643)
- **DL-CT-Rev: Deep Learning for Tomographic Image Reconstruction** — _Nat Mach Intell 2020_ · [论文](https://doi.org/10.1038/s42256-020-00273-z)
- **DL-InvProb: Deep Learning Techniques for Inverse Problems in Imaging** — _IEEE JSAIT 2020_ · [论文](https://arxiv.org/abs/2005.06001)
- **Sparsity2DL: Image Reconstruction: From Sparsity to Data-Adaptive Methods and Machine Learning** — _Proc. IEEE 2020_ · [论文](https://doi.org/10.1109/JPROC.2019.2936204)
- **CT-Evolution: The Evolution of Image Reconstruction for CT: From Filtered Back Projection to Artificial Intelligence** — _Eur Radiol 2019_ · [论文](https://doi.org/10.1007/s00330-018-5810-7)
- **DataDriven: Solving Inverse Problems Using Data-Driven Models** — _Acta Numerica 2019_ · [论文](https://doi.org/10.1017/S0962492919000059)
- **Applications of nonlocal means algorithm in low-dose X-ray CT image processing and reconstruction: A review** — _Med Phys 2017_ · [论文](https://doi.org/10.1002/mp.12097)
- **CNN-InvRev: Convolutional Neural Networks for Inverse Problems in Imaging: A Review** — _IEEE SPM 2017_ · [论文](https://doi.org/10.1109/MSP.2017.2739299)
- **MAR-4Dec: Metal Artifact Reduction in CT: Where Are We After Four Decades?** — _IEEE Access 2016_ · [论文](https://doi.org/10.1109/ACCESS.2016.2608621)
- **Dual- and Multi-Energy CT: Principles, Technical Approaches, and Clinical Applications** — _Radiology 2015_ · [论文](https://doi.org/10.1148/radiol.2015142631)
- **A General Framework and Review of Scatter Correction Methods in Cone-Beam CT: Part 2 — Scatter Estimation Approaches** — _Med Phys 2011_ · [论文](https://doi.org/10.1118/1.3589140)
- **Scatter-Rev: A General Framework and Review of Scatter Correction Methods in X-Ray Cone-Beam CT: Part 1 — Scatter Compensation Approaches** — _Med Phys 2011_ · [论文](https://doi.org/10.1118/1.3599033)
- **Task-based performance analysis of FBP, SART and ML for digital breast tomosynthesis using signal CNR and Channelised Hotelling Observers** — _Med Image Anal 2011_ · [论文](https://doi.org/10.1016/j.media.2010.07.004)
- **Tomographic Reconstruction in the 21st Century** — _IEEE SPM 2010_ · [论文](https://doi.org/10.1109/msp.2010.936743)
- **Why do commercial CT scanners still employ traditional, filtered back-projection for image reconstruction?** — _Inverse Problems 2009_ · [论文](https://doi.org/10.1088/0266-5611/25/12/123009)

### 经典与迭代重建

<sub>解析法（FBP/FDK）与迭代法（SART/SIRT/CGLS），以及手工设计的正则项（TV、TGV、非局部） · 70 篇论文</sub>

- **Complex Wavelet-Based Sinogram Segmentation for Metal Artifact Reduction in Cone-Beam CT** — _PMB 2026_ · [论文](https://arxiv.org/abs/2602.14315)
- **Computed Tomography Reconstruction Algorithm Using Markov Random Field Model** — _J. Phys. Soc. Jpn. 2026_ · [论文](https://arxiv.org/abs/2605.11637)
- **Cross-Distribution Diffusion Priors-Driven Iterative Reconstruction for Sparse-View CT** — _TMI 2026_ · [论文](https://arxiv.org/abs/2509.13576)
- **H3D-MarNet: Wavelet-Guided Dual-Path Learning for Metal Artifact Suppression and CT Modality Transformation for Radiotherapy Workflows** — _ICPR 2026_ · [论文](https://arxiv.org/abs/2605.12252)
- **Plug-and-Play Diffusion Meets ADMM: Dual-Variable Coupling for Robust Medical Image Reconstruction** — _ICML 2026_ · [论文](https://arxiv.org/abs/2602.23214) · [代码](https://github.com/duchenhe/DC-PnPDP)
- **Robustness and Stability Analysis of Differentiable Shift-Variant FBP for Cone-Beam CT under Challenging Acquisition Settings** — _MELBA 2026_ · [论文](https://arxiv.org/abs/2607.09828) · [项目页](https://melba-journal.org/2026:014)
- **Variational Garrote for Sparse Inverse Problems** — _J. Comput. Sci. 2026_ · [论文](https://doi.org/10.1016/j.jocs.2026.102980)
- **An Iterative Reconstruction Method for Dental Cone-Beam Computed Tomography with a Truncated Field of View** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.07618)
- **CoCo-PnP: Learning Cocoercive Conservative Denoisers via Helmholtz Decomposition for Poisson Inverse Problems** — _NeurIPS 2025_ · [论文](https://arxiv.org/abs/2505.08909) · [代码](https://github.com/FizzzFizzz/CoCo-PnP)
- **Learning Wavelet-Sparse FDK for 3D Cone-Beam CT Reconstruction** — _Fully3D 2025_ · [论文](https://arxiv.org/abs/2505.13579)
- **MONSTR: Model-Oriented Neutron Strain Tomographic Reconstruction** — _预印本 2025_ · [论文](https://arxiv.org/abs/2505.22187)
- **SDB: System-Embedded Diffusion Bridge Models** — _NeurIPS 2025_ · [论文](https://arxiv.org/abs/2506.23726) · [代码](https://github.com/sobieskibj/sdb)
- **Data-Driven Filter Design in FBP: Transforming CT Reconstruction with Trainable Fourier Series** — _预印本 2024_ · [论文](https://arxiv.org/abs/2401.16039)
- **How auto-differentiation can improve CT workflows: classical algorithms in a modern framework** — _Opt. Express 2024_ · [论文](https://doi.org/10.1364/oe.502920)
- **IRDS: Iterative reconstruction of low-dose CT based on differential sparse** — _BSPC 2023_ · [论文](https://doi.org/10.1016/j.bspc.2022.104204)
- **EASEL: Iterative Reconstruction for Low-Dose CT using Deep Gradient Priors of Generative Model** — _TRPMS 2022_ · [论文](https://doi.org/10.1109/trpms.2022.3148373) · [代码](https://github.com/yqx7150/EASEL)
- **ALPD: Adversarially learned iterative reconstruction for imaging inverse problems** — _SSVM 2021_ · [论文](https://arxiv.org/abs/2103.16151) · [代码](https://github.com/Subhadip-1/adversarial_primal_dual_tomography)
- **FISTA-Net: Learning a Fast Iterative Shrinkage Thresholding Network for Inverse Problems in Imaging** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3054167) · [代码](https://github.com/jinxixiang/FISTA-Net)
- **Limited-Angle CT Reconstruction via the L1/L2 Minimization** — _SIAM J. Imaging Sci. 2021_ · [论文](https://doi.org/10.1137/20m1341490)
- **Tensor-Net: Learning to Reconstruct CT Images From the VVBP-Tensor** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3090257)
- **FSTensor: Full-spectrum-knowledge-aware tensor model for energy-resolved CT iterative reconstruction** — _TMI 2020_ · [论文](https://doi.org/10.1109/tmi.2020.2976692)
- **iRadonMAP: Radon Inversion via Deep Learning** — _TMI 2020_ · [论文](https://arxiv.org/abs/1808.03015)
- **Learned convex regularizers for inverse problems** — _预印本 2020_ · [论文](https://arxiv.org/abs/2008.02839)
- **Momentum-Net: Fast and convergent iterative neural network for inverse problems** — _TPAMI 2020_ · [论文](https://doi.org/10.1109/tpami.2020.3012955)
- **Moreau-envelope-enhanced nonlocal shearlet transform and total variation for sparse-view CT reconstruction** — _Meas. Sci. Technol. 2020_ · [论文](https://doi.org/10.1088/1361-6501/aba282)
- **Sparsity2DL: Image Reconstruction: From Sparsity to Data-Adaptive Methods and Machine Learning** — _Proc. IEEE 2020_ · [论文](https://doi.org/10.1109/JPROC.2019.2936204)
- **TVWFR: Sparse View CT Image Reconstruction Based on Total Variation and Wavelet Frame Regularization** — _IEEE Access 2020_ · [论文](https://doi.org/10.1109/access.2020.2982229)
- **CT-Evolution: The Evolution of Image Reconstruction for CT: From Filtered Back Projection to Artificial Intelligence** — _Eur Radiol 2019_ · [论文](https://doi.org/10.1007/s00330-018-5810-7)
- **DataDriven: Solving Inverse Problems Using Data-Driven Models** — _Acta Numerica 2019_ · [论文](https://doi.org/10.1017/S0962492919000059)
- **DL-PICCS: Accurate and robust sparse-view angle CT image reconstruction using deep learning and prior image constrained compressed sensing (DL-PICCS)** — _Med Phys 2019_ · [论文](https://doi.org/10.1002/mp.15183)
- **PDE: A regional adaptive variational PDE model for computed tomography image reconstruction** — _PR 2019_ · [论文](https://doi.org/10.1016/j.patcog.2019.03.009)
- **PSRV: Patient-specific reconstruction of volumetric computed tomography images from a single projection view via deep learning** — _Nat Biomed Eng 2019_ · [论文](https://doi.org/10.1038/s41551-019-0466-4)
- **SISVM: Learning to Reconstruct Computed Tomography Images Directly From Sinogram Data Under A Variety of Data Acquisition Conditions** — _TMI 2019_ · [论文](https://doi.org/10.1109/tmi.2019.2910760)
- **VVBP-tSVD: VVBP-Tensor in the FBP Algorithm: Its Properties and Application in Low-Dose CT Reconstruction** — _TMI 2019_ · [论文](https://doi.org/10.1109/tmi.2019.2935187)
- **An Image Reconstruction Method Based on Total Variation and Wavelet Tight Frame for Limited-Angle CT** — _IEEE Access 2018_ · [论文](https://doi.org/10.1109/access.2017.2779148)
- **AUTOMAP: Image reconstruction by domain-transform manifold learning** — _Nature 2018_ · [论文](https://doi.org/10.1038/nature25988)
- **PTPN: Intelligent Parameter Tuning in Optimization-Based Iterative CT Reconstruction via Deep Reinforcement Learning** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2823679)
- **RAD: Regularization analysis and design for prior-image-based X-ray CT reconstruction** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2847250)
- **Statistical Image Reconstruction Using Mixed Poisson-Gaussian Noise Model for X-Ray CT** — _预印本 2018_ · [论文](https://arxiv.org/abs/1801.09533)
- **An improved statistical iterative algorithm for sparse-view and limited-angle CT image reconstruction** — _Sci. Rep. 2017_ · [论文](https://doi.org/10.1038/s41598-017-11222-z)
- **Edge-preserving reconstruction from sparse projections of limited-angle computed tomography using L0-regularized gradient prior** — _Rev. Sci. Instrum. 2017_ · [论文](https://doi.org/10.1063/1.4981132)
- **ReATV: Reweighted Anisotropic Total Variation Minimization for Limited-Angle CT Reconstruction** — _IEEE TNS 2017_ · [论文](https://doi.org/10.1109/tns.2017.2750199)
- **SENP: Low‐dose CT reconstruction using spatially encoded nonlocal penalty** — _Med Phys 2017_ · [论文](https://doi.org/10.1002/mp.12523)
- **Image reconstruction from few views by L0-norm optimization** — _Chinese Phys. B 2014_ · [论文](https://doi.org/10.1088/1674-1056/23/7/078703)
- **TGV: Sparse-view x-ray CT reconstruction via total generalized variation regularization** — _PMB 2014_ · [论文](https://doi.org/10.1088/0031-9155/59/12/2997)
- **TV-Stokes: Total Variation-Stokes Strategy for Sparse-View X-ray CT Image Reconstruction** — _TMI 2014_ · [论文](https://doi.org/10.1109/tmi.2013.2295738)
- **ATV: A limited-angle CT reconstruction method based on anisotropic TV minimization** — _PMB 2013_ · [论文](https://doi.org/10.1088/0031-9155/58/7/2119)
- **Feature constrained compressed sensing CT image reconstruction from incomplete data via robust principal component analysis of the database** — _PMB 2013_ · [论文](https://doi.org/10.1088/0031-9155/58/12/4047)
- **Image reconstruction based on total-variation minimization and alternating direction method in linear scan computed tomography** — _Chinese Phys. B 2013_ · [论文](https://doi.org/10.1088/1674-1056/22/7/078701)
- **Iterative CT Reconstruction Using Shearlet-Based Regularization** — _IEEE TNS 2013_ · [论文](https://doi.org/10.1109/tns.2013.2275994)
- **Iterative Image Reconstruction for Sparse-View CT Using Normal-Dose Image Induced Total Variation Prior** — _PLoS One 2013_ · [论文](https://doi.org/10.1371/journal.pone.0079709)
- **Sparse Tomography** — _SIAM J. Sci. Comput. 2013_ · [论文](https://doi.org/10.1137/120876277)
- **AWTV: Adaptive-weighted total variation minimization for sparse data toward low-dose x-ray computed tomography image reconstruction** — _PMB 2012_ · [论文](https://doi.org/10.1088/0031-9155/57/23/7923)
- **Few-view image reconstruction with dual dictionaries** — _PMB 2012_ · [论文](https://doi.org/10.1088/0031-9155/57/1/173)
- **Low-Dose X-ray CT Reconstruction via Dictionary Learning** — _TMI 2012_ · [论文](https://doi.org/10.1109/tmi.2012.2195669)
- **Task-based performance analysis of FBP, SART and ML for digital breast tomosynthesis using signal CNR and Channelised Hotelling Observers** — _Med Image Anal 2011_ · [论文](https://doi.org/10.1016/j.media.2010.07.004)
- **Compressed sensing based cone-beam computed tomography reconstruction with a first-order method** — _Med Phys 2010_ · [论文](https://doi.org/10.1118/1.3481510)
- **Few-View Projection Reconstruction With an Iterative Reconstruction-Reprojection Algorithm and TV Constraint** — _IEEE TNS 2009_ · [论文](https://doi.org/10.1109/tns.2008.2009990)
- **Why do commercial CT scanners still employ traditional, filtered back-projection for image reconstruction?** — _Inverse Problems 2009_ · [论文](https://doi.org/10.1088/0266-5611/25/12/123009)
- **Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization** — _PMB 2008_ · [论文](https://doi.org/10.1088/0031-9155/53/17/021)
- **Compressed sensing** — _IEEE TIT 2006_ · [论文](https://doi.org/10.1109/tit.2006.871582)
- **K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation** — _IEEE TSP 2006_ · [论文](https://doi.org/10.1109/tsp.2006.881199)
- **Robust uncertainty principles: exact signal reconstruction from highly incomplete frequency information** — _IEEE TIT 2006_ · [论文](https://doi.org/10.1109/tit.2005.862083)
- **ROF: Nonlinear total variation based noise removal algorithms** — _Physica D 1992_ · [论文](https://doi.org/10.1016/0167-2789(92)90242-f)
- **FDK: Practical cone-beam algorithm** — _JOSA A 1984_ · [论文](https://doi.org/10.1364/JOSAA.1.000612)
- **SART: Simultaneous Algebraic Reconstruction Technique (SART): A superior implementation of the ART algorithm** — _Ultrasonic Imaging 1984_ · [论文](https://doi.org/10.1016/0161-7346(84)90008-7)
- **MLEM: Maximum Likelihood Reconstruction for Emission Tomography** — _TMI 1982_ · [论文](https://doi.org/10.1109/tmi.1982.4307558)
- **Shepp-Logan: The Fourier reconstruction of a head section** — _IEEE TNS 1974_ · [论文](https://doi.org/10.1109/tns.1974.6499235)
- **Three-dimensional Reconstruction from Radiographs and Electron Micrographs: Application of Convolutions instead of Fourier Transforms** — _PNAS 1971_ · [论文](https://doi.org/10.1073/pnas.68.9.2236)
- **Über die Bestimmung von Funktionen durch ihre Integralwerte längs gewisser Mannigfaltigkeiten** — _Ber. Verh. Sächs. Akad. Wiss. Leipzig, Math.-Phys. Kl. 1917_ · [论文](https://doi.org/10.1109/TMI.1986.4307775)

### 稀疏视角 CT

<sub>投影角度数量不足时的重建 · 133 篇论文</sub>

- **3D Field of Junctions: A Noise-Robust, Training-Free Structural Prior for Volumetric Inverse Problems** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2603.02149) · [代码](https://github.com/voilalab/3D-Field-of-Junctions)
- **CG-GLORE: A Conjugate Gradient-Based Global-Local Regularization Network for Sparse-View CT Reconstruction** — _BMVC 2026_ · [论文](https://arxiv.org/abs/2608.15246)
- **Conditional Diffusion Posterior Alignment for Sparse-View CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2604.21960)
- **Continuity-driven Synergistic Diffusion with Neural Priors for Ultra-Sparse-View CBCT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.07980)
- **Cross-Distribution Diffusion Priors-Driven Iterative Reconstruction for Sparse-View CT** — _TMI 2026_ · [论文](https://arxiv.org/abs/2509.13576)
- **DiffNR: Diffusion-Enhanced Neural Representation Optimization for Sparse-View 3D Tomographic Reconstruction** — _AAAI 2026_ · [论文](https://arxiv.org/abs/2604.21518) · [项目页](https://ooonesevennn.github.io/DiffNR/)
- **Efficient Unrolled Networks for Large-Scale 3D Inverse Problems** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2601.02141) · [代码](https://github.com/romainvo/efficient-unrolling)
- **Event-Based Sparse-View Background-Oriented Schlieren Tomography** — _ECCV 2026_ · [论文](https://doi.org/10.1007/978-3-032-37335-9_18)
- **From Sparse X-rays to 3D CT: Training-Free Reconstruction with Diffusion Priors** — _DGM4MICCAI 2026_ · [论文](https://arxiv.org/abs/2606.20763) · [代码](https://github.com/Fredy-Zhang/TF-PRDiT)
- **GR-Gaussian: Graph-Based Radiative Gaussian Splatting for Sparse-View Tomography** — _TCI 2026_ · [论文](https://doi.org/10.1109/TCI.2026.3701585)
- **ILV: Iterative Latent Volumes for Fast and Accurate Sparse-View CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2603.14915) · [项目页](https://sngryonglee.github.io/ILV/)
- **ISCS: Improving 2D Diffusion Models for 3D Medical Imaging with Inter-Slice Consistent Stochasticity** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2602.04162) · [代码](https://github.com/duchenhe/ISCS)
- **KLIP: Localized Distribution Shift Detection via KL-Divergence with Diffusion Priors in Inverse Problems** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2605.31596) · [代码](https://github.com/voilalab/KLIP)
- **Learning Where and What to Lift for Bi-planar X-ray-to-CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2608.17255)
- **LUCID: Learned Undersampling-Adaptive Consistency-Guided Inference with Deterministic Flow Matching for Sparse-View CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2606.16212)
- **NAB: Neural Adaptive Binning for Sparse-View CT Reconstruction** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2602.02356) · [代码](https://github.com/Wangduo-Xie/NAB_CT_reconstruction)
- **Projection-Volume Fidelity Divergence: Diagnosing and Controlling Optimization Drift in Sparse-View 3D Gaussian Tomography** — _预印本 2026_ · [论文](https://arxiv.org/abs/2606.22525)
- **Revisiting Pose Sensitivity in Splat-based Computed Tomography under Sparse-view Reconstruction** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2608.04752)
- **Shape-guided Gaussian Splatting for Sparse-View X-ray 3D Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2609.10376) · [代码](https://github.com/polyshape-lab/ShapeGuidedGaussian)
- **Tomographic Sparse View Selection Using the View Covariance Loss** — _TPAMI 2026_ · [论文](https://doi.org/10.1109/TPAMI.2025.3600072)
- **Towards reconstructing experimental sparse-view X-ray CT data with diffusion models** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.12755)
- **Variational Garrote for Sparse Inverse Problems** — _J. Comput. Sci. 2026_ · [论文](https://doi.org/10.1016/j.jocs.2026.102980)
- **XDen-1K: A Density Field Dataset of Real-World Objects** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2512.10668)
- **A CT Geometry With Multiple Centers Of Rotation For Solving Sparse View Problem** — _预印本 2025_ · [论文](https://arxiv.org/abs/2502.06125)
- **Adaptive Diffusion Models for Sparse-View Motion-Corrected Head Cone-beam CT** — _TRPMS 2025_ · [论文](https://arxiv.org/abs/2504.14033) · [项目页](https://antoinedepaepe.github.io/jrm-adm-io/)
- **An unsupervised sparse-view CT reconstruction framework using combination of iterative deep image prior and ADMM** — _Med Phys 2025_ · [论文](https://doi.org/10.1002/mp.17933)
- **Are Pixel-Wise Metrics Reliable for Sparse-View Computed Tomography Reconstruction?** — _NeurIPS 2025_ · [论文](https://arxiv.org/abs/2506.02093) · [代码](https://github.com/MrGiovanni/CARE)
- **CvG-Diff: Cross-View Generalized Diffusion Model for Sparse-View CT Reconstruction** — _MICCAI 2025_ · [论文](https://doi.org/10.1007/978-3-032-05325-1_14) · [代码](https://github.com/xmed-lab/CvG-Diff)
- **Investigating the effects of machine learning generalization for enhancing accuracy in fast X-ray computed tomography for industrial metrology** — _CIRP Annals 2025_ · [论文](https://doi.org/10.1016/j.cirp.2025.04.025)
- **Latent Space Consistency for Sparse-View CT Reconstruction** — _预印本 2025_ · [论文](https://arxiv.org/abs/2507.11152)
- **MInDI-3D: Iterative Deep Learning in 3D for Sparse-view Cone Beam Computed Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.09616)
- **Mitigating Data Consistency Induced Discrepancy in Cascaded Diffusion Models for Sparse-View CT Reconstruction** — _TMI 2025_ · [论文](https://doi.org/10.1109/tmi.2025.3557243)
- **Neural Discrete Representation Learning for Sparse-View CBCT Reconstruction: From Algorithm Design to Prospective Multicenter Clinical Evaluation** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.00873)
- **Ordered-subsets Multi-diffusion Model for Sparse-view CT Reconstruction** — _预印本 2025_ · [论文](https://arxiv.org/abs/2505.09985)
- **Recover Biological Structure from Sparse-View Diffraction Images with Neural Volumetric Prior** — _ICCV 2025_ · [论文](https://arxiv.org/abs/2510.16391)
- **Resolution-Agnostic Neural Operators for Multi-Rate Sparse-View CT** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.12236) · [代码](https://github.com/neuraloperator/sparse_ct)
- **Semantic contrastive learning for orthogonal X-ray computed tomography reconstruction** — _Fully3D 2025_ · [论文](https://arxiv.org/abs/2512.22674)
- **Spener: Unsupervised Self-Prior Embedding Neural Representation for Sparse-View CT Reconstruction** — _AAAI 2025_ · [论文](https://doi.org/10.1609/aaai.v39i7.32794) · [代码](https://github.com/MeijiTian/Spener)
- **Steerable Conditional Diffusion for Out-of-Distribution Adaptation in Medical Image Reconstruction** — _TMI 2025_ · [论文](https://doi.org/10.1109/tmi.2024.3524797)
- **Swap-Net: A Memory-Efficient 2.5D Network for Sparse-View 3D Cone Beam CT Reconstruction to ICF Applications** — _TCI 2025_ · [论文](https://doi.org/10.1109/tci.2025.3572699)
- **When are Diffusion Priors Helpful in Sparse Reconstruction? A Study with Sparse-view CT** — _ISBI 2025_ · [论文](https://arxiv.org/abs/2502.02771)
- **X-GRM: Large Gaussian Reconstruction Model for Sparse-view X-rays to Computed Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2505.15235) · [代码](https://github.com/CUHK-AIM-Group/X-GRM)
- **XGenRecon: A New Perspective in Ultrasparse Volumetric CBCT Reconstruction Through Geometry-Controlled X-Ray Projection Generation** — _TRPMS 2025_ · [论文](https://doi.org/10.1109/trpms.2024.3420742)
- **A Review of Deep Learning CT Reconstruction From Incomplete Projection Data** — _TRPMS 2024_ · [论文](https://doi.org/10.1109/trpms.2023.3316349)
- **BaggageCT: Fan-Beam CT Reconstruction for Unaligned Sparse-View X-Ray Baggage Data** — _预印本 2024_ · [论文](https://arxiv.org/abs/2412.03036)
- **DIF-Gaussian: Learning 3D Gaussians for Extremely Sparse-View Cone-Beam CT Reconstruction** — _MICCAI 2024_ · [论文](https://doi.org/10.1007/978-3-031-72104-5_41) · [代码](https://github.com/xmed-lab/DIF-Gaussian)
- **Generative Modeling in Sinogram Domain for Sparse-view CT Reconstruction** — _TRPMS 2024_ · [论文](https://arxiv.org/abs/2211.13926)
- **INR-Joint: Implicit Neural Representations for Robust Joint Sparse-View CT Reconstruction** — _TMLR 2024_ · [论文](https://arxiv.org/abs/2405.02509) · [代码](https://github.com/jiayangshi/INR4JointCTRecon)
- **Machine learning based sinogram interpolation for X-ray computed tomography validated on experimental data** — _Precis. Eng. 2024_ · [论文](https://doi.org/10.1016/j.precisioneng.2024.02.020)
- **Neural Field Regularization by Denoising for 3D Sparse-View X-Ray Computed Tomography** — _3DV 2024_ · [论文](https://doi.org/10.1109/3dv62453.2024.00094)
- **Plug-and-Play Learned Proximal Trajectory for 3D Sparse-View X-Ray Computed Tomography** — _ECCV 2024_ · [论文](https://doi.org/10.1007/978-3-031-72761-0_13)
- **R2-Gaussian: Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction** — _NeurIPS 2024_ · [论文](https://arxiv.org/abs/2405.20693) · [代码](https://github.com/Ruyi-Zha/r2_gaussian)
- **RBP-DIP: Residual back projection with deep image prior for ill-posed CT reconstruction** — _Neural Netw. 2024_ · [论文](https://doi.org/10.1016/j.neunet.2024.106740)
- **SAX-NeRF: Structure-Aware Sparse-View X-Ray 3D Reconstruction** — _CVPR 2024_ · [论文](https://doi.org/10.1109/cvpr52733.2024.01062) · [代码](https://github.com/caiyuanhao1998/SAX-NeRF)
- **SWORD: Stage-by-Stage Wavelet Optimization Refinement Diffusion Model for Sparse-View CT Reconstruction** — _TMI 2024_ · [论文](https://doi.org/10.1109/tmi.2024.3355455) · [代码](https://github.com/yqx7150/SWORD)
- **Two-View Industrial CT Reconstruction Based on a Multiscale Conditional Latent Diffusion Network** — _TIM 2024_ · [论文](https://doi.org/10.1109/TIM.2024.3476543)
- **Wavelet-Improved Score-Based Generative Model for Medical Imaging** — _TMI 2024_ · [论文](https://doi.org/10.1109/tmi.2023.3325824)
- **DDDM: Dual-Domain Diffusion Model for Sparse-View CT Reconstruction** — _预印本 2023_ · [论文](https://doi.org/10.36227/techrxiv.23726703) · [代码](https://github.com/YC-Markus/code-for-DDDM)
- **DEAR: Deep Embedding-Attention-Refinement for Sparse-View CT Reconstruction** — _TIM 2023_ · [论文](https://doi.org/10.1109/tim.2022.3221136)
- **Fast algorithms based on Empirical Interpolation Methods for selecting best projections in Sparse-View X-ray Computed Tomography using a priori information** — _NDT&E Int. 2023_ · [论文](https://doi.org/10.1016/j.ndteint.2022.102768)
- **FreeSeed: Frequency-Band-Aware and Self-Guided Network for Sparse-View CT Reconstruction** — _MICCAI 2023_ · [论文](https://doi.org/10.1007/978-3-031-43999-5_24) · [代码](https://github.com/Masaaki-75/freeseed)
- **LEARN++: Recurrent Dual-Domain Reconstruction Network for Compressed Sensing CT** — _TRPMS 2023_ · [论文](https://doi.org/10.1109/trpms.2022.3222213)
- **MDST: multi-domain sparse-view CT reconstruction based on convolution and swin transformer** — _PMB 2023_ · [论文](https://doi.org/10.1088/1361-6560/acc2ab)
- **PINER: Prior-Informed Implicit Neural Representation Learning for Test-Time Adaptation in Sparse-View CT Reconstruction** — _WACV 2023_ · [论文](https://doi.org/10.1109/wacv56688.2023.00197) · [代码](https://github.com/efzero/PINER)
- **Sparse-View Cone Beam CT Reconstruction Using Data-Consistent Supervised and Adversarial Learning From Scarce Training Data** — _TCI 2023_ · [论文](https://doi.org/10.1109/TCI.2022.3225680)
- **SPIE-DIR: Self-Prior Information Enhanced Deep Iterative Reconstruction Using Two Complementary Limited-Angle Scans for DECT** — _TIM 2023_ · [论文](https://doi.org/10.1109/tim.2022.3227549)
- **The realisation of fast X-ray computed tomography using a limited number of projection images for dimensional metrology** — _NDT&E Int. 2023_ · [论文](https://doi.org/10.1016/j.ndteint.2023.102852)
- **An Educated Warm Start for Deep Image Prior-Based Micro CT Reconstruction** — _TCI 2022_ · [论文](https://doi.org/10.1109/tci.2022.3233188)
- **DDCL: Dual domain closed-loop learning for sparse-view CT reconstruction** — _ICIFXCT 2022_ · [论文](https://doi.org/10.1117/12.2646639)
- **DREAM-Net: Deep Residual Error Iterative Minimization Network for Sparse-View CT Reconstruction** — _TMI 2022_ · [论文](https://doi.org/10.1109/jbhi.2022.3225697)
- **DuDoDR-Net: Dual-domain data consistent recurrent network for simultaneous sparse view and metal artifact reduction in computed tomography** — _MedIA 2022_ · [论文](https://doi.org/10.1016/j.media.2021.102289)
- **DuDoTrans: Dual-Domain Transformer for Sparse-View CT Reconstruction** — _MLMIR 2022_ · [论文](https://doi.org/10.1007/978-3-031-17247-2_9) · [代码](https://github.com/cewang-sysu/DuDoTrans)
- **NAF: Neural Attenuation Fields for Sparse-View CBCT Reconstruction** — _MICCAI 2022_ · [论文](https://arxiv.org/abs/2209.14540) · [代码](https://github.com/Ruyi-Zha/naf_cbct)
- **PLANet: Learning Projection Views for Sparse-View CT Reconstruction** — _ACM MM 2022_ · [论文](https://doi.org/10.1145/3503161.3548204)
- **SNAF: Sparse-View CBCT Reconstruction with Neural Attenuation Fields** — _预印本 2022_ · [论文](https://arxiv.org/abs/2211.17048)
- **UNDIP: Sparse-view and limited-angle CT reconstruction with untrained networks and deep image prior** — _CMPB 2022_ · [论文](https://doi.org/10.1016/j.cmpb.2022.107167)
- **CD-Net: Comprehensive Domain Network With Spectral Complementary for DECT Sparse-View Reconstruction** — _TCI 2021_ · [论文](https://doi.org/10.1109/tci.2021.3070184)
- **DRONE: Dual-Domain Residual-Based Optimization Network for Sparse-View CT Reconstruction** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3078067) · [代码](https://github.com/weiwenwu12/DRONE)
- **FDM: Degradation-Aware Deep Learning Framework for Sparse-View CT Reconstruction** — _Tomography 2021_ · [论文](https://doi.org/10.3390/tomography7040077) · [代码](https://github.com/sunchang2017/degradation-aware-sparse-CT-reconstruction)
- **LMFI: Learnable Multi-scale Fourier Interpolation for Sparse View CT Image Reconstruction** — _MICCAI 2021_ · [论文](https://doi.org/10.1007/978-3-030-87231-1_28)
- **MetaInv-Net: Meta Inversion Network for Sparse View CT Image Reconstruction** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2020.3033541) · [代码](https://github.com/haimiaozh/MetaInv-Net)
- **2-Step Sparse-View CT Reconstruction with a Domain-Specific Perceptual Network** — _预印本 2020_ · [论文](https://arxiv.org/abs/2012.04743)
- **AirNet: Fused analytical and iterative reconstruction with deep neural network regularization for sparse-data CT** — _Med Phys 2020_ · [论文](https://doi.org/10.1002/mp.14170)
- **DEER: Deep efficient end-to-end reconstruction (DEER) network for few-view breast CT image reconstruction** — _IEEE Access 2020_ · [论文](https://doi.org/10.1109/access.2020.3033795) · [代码](https://github.com/WANG-AXIS/DEER)
- **DLMIR: Deep learning methods for image reconstruction from angularly sparse data for CT and SAR imaging** — _ASARI 2020_ · [论文](https://doi.org/10.1117/12.2558953) · [代码](https://github.com/e-yavuz/Deep-Learning-Methods-for-Image-Reconstruction-from-Angularly-Sparse-Data-for-CT-and-SAR-Imaging)
- **ETEDN: An End-to-End Deep Network for Reconstructing CT Images Directly From Sparse Sinograms** — _TCI 2020_ · [论文](https://doi.org/10.1109/tci.2020.3039385) · [代码](https://github.com/wangwei-cmd/CT-image-reconstruction)
- **HDNet: Hybrid-domain neural network processing for sparse-view CT reconstruction** — _TRPMS 2020_ · [论文](https://doi.org/10.1109/trpms.2020.3011413)
- **Moreau-envelope-enhanced nonlocal shearlet transform and total variation for sparse-view CT reconstruction** — _Meas. Sci. Technol. 2020_ · [论文](https://doi.org/10.1088/1361-6501/aba282)
- **Multi-Scale Learned Iterative Reconstruction** — _TCI 2020_ · [论文](https://doi.org/10.1109/TCI.2020.2990299)
- **REDAEP: Robust and Enhanced Denoising Autoencoding Prior for Sparse-View CT Reconstruction** — _TRPMS 2020_ · [论文](https://doi.org/10.1109/trpms.2020.2989634)
- **SISTER: Spectral-Image Similarity-Based Tensor With Enhanced-Sparsity Reconstruction for Sparse-View Multi-Energy CT** — _TCI 2020_ · [论文](https://doi.org/10.1109/tci.2019.2956886)
- **Sparse-view CT reconstruction based on multi-level wavelet convolution neural network** — _Phys. Med. 2020_ · [论文](https://doi.org/10.1016/j.ejmp.2020.11.021)
- **TVWFR: Sparse View CT Image Reconstruction Based on Total Variation and Wavelet Frame Regularization** — _IEEE Access 2020_ · [论文](https://doi.org/10.1109/access.2020.2982229)
- **A deep learning reconstruction framework for X-ray computed tomography with incomplete data** — _PLoS One 2019_ · [论文](https://doi.org/10.1371/journal.pone.0224426)
- **Convolutional Sparse Coding for Compressed Sensing CT Reconstruction** — _TMI 2019_ · [论文](https://doi.org/10.1109/tmi.2019.2906853)
- **DL-PICCS: Accurate and robust sparse-view angle CT image reconstruction using deep learning and prior image constrained compressed sensing (DL-PICCS)** — _Med Phys 2019_ · [论文](https://doi.org/10.1002/mp.15183)
- **DNNSS: Deep-neural-network-based sinogram synthesis for sparse-view CT image reconstruction** — _TRPMS 2019_ · [论文](https://doi.org/10.1109/trpms.2018.2867611)
- **Extreme Few-view CT Reconstruction using Deep Inference** — _预印本 2019_ · [论文](https://arxiv.org/abs/1910.05375)
- **iCTNet: Sinogram interpolation for sparse-view micro-CT with deep learning neural network** — _SPIE MI 2019_ · [论文](https://arxiv.org/abs/1902.03362) · [代码](https://github.com/Swapneel7/Sparse-CT-Reconstruction-using-Deep-learning)
- **PSRV: Patient-specific reconstruction of volumetric computed tomography images from a single projection view via deep learning** — _Nat Biomed Eng 2019_ · [论文](https://doi.org/10.1038/s41551-019-0466-4)
- **SPARE: Sparse-view reconstruction challenge for 4D cone-beam CT from a 1-min scan** — _Med Phys 2019_ · [论文](https://doi.org/10.1002/mp.13687)
- **SPSS: Sharpness preserved sinogram synthesis using convolutional neural network for sparse-view CT imaging** — _SPIE MI 2019_ · [论文](https://doi.org/10.1117/12.2512894)
- **DD-Net: A Sparse-View CT Reconstruction Method Based on Combination of DenseNet and Deconvolution** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2823338) · [代码](https://github.com/zzc623/DD_Net)
- **TFU-Net: Framing U-Net via Deep Convolutional Framelets - Application to Sparse-view CT** — _TMI 2018_ · [论文](https://arxiv.org/abs/1708.08333)
- **An improved statistical iterative algorithm for sparse-view and limited-angle CT image reconstruction** — _Sci. Rep. 2017_ · [论文](https://doi.org/10.1038/s41598-017-11222-z)
- **Coded aperture optimization in compressive X-ray tomography: a gradient descent approach** — _Opt. Express 2017_ · [论文](https://doi.org/10.1364/oe.25.023833)
- **Deep Convolutional Neural Network for Inverse Problems in Imaging** — _TIP 2017_ · [论文](https://doi.org/10.1109/tip.2017.2713099)
- **Edge-preserving reconstruction from sparse projections of limited-angle computed tomography using L0-regularized gradient prior** — _Rev. Sci. Instrum. 2017_ · [论文](https://doi.org/10.1063/1.4981132)
- **SPIR: Dual energy CT with one full scan and a second sparse-view scan using structure preserving iterative reconstruction (SPIR)** — _PMB 2016_ · [论文](https://doi.org/10.1088/0031-9155/61/18/6684)
- **Sparse-View Spectral CT Reconstruction Using Spectral Patch-Based Low-Rank Penalty** — _TMI 2015_ · [论文](https://doi.org/10.1109/tmi.2014.2380993)
- **Tensor-based dictionary learning for dynamic tomographic reconstruction** — _PMB 2015_ · [论文](https://doi.org/10.1088/0031-9155/60/7/2803)
- **Image reconstruction from few views by L0-norm optimization** — _Chinese Phys. B 2014_ · [论文](https://doi.org/10.1088/1674-1056/23/7/078703)
- **Low-dose X-ray computed tomography image reconstruction with a combined low-mAs and sparse-view protocol** — _Opt. Express 2014_ · [论文](https://doi.org/10.1364/oe.22.015190)
- **Sparse-view computed laminography with a spherical sinusoidal scan for nondestructive testing** — _Opt. Express 2014_ · [论文](https://doi.org/10.1364/oe.22.017745)
- **TGV: Sparse-view x-ray CT reconstruction via total generalized variation regularization** — _PMB 2014_ · [论文](https://doi.org/10.1088/0031-9155/59/12/2997)
- **TV-Stokes: Total Variation-Stokes Strategy for Sparse-View X-ray CT Image Reconstruction** — _TMI 2014_ · [论文](https://doi.org/10.1109/tmi.2013.2295738)
- **Effects of sparse sampling schemes on image quality in low-dose CT** — _Med Phys 2013_ · [论文](https://doi.org/10.1118/1.4825096)
- **Feature constrained compressed sensing CT image reconstruction from incomplete data via robust principal component analysis of the database** — _PMB 2013_ · [论文](https://doi.org/10.1088/0031-9155/58/12/4047)
- **Image reconstruction based on total-variation minimization and alternating direction method in linear scan computed tomography** — _Chinese Phys. B 2013_ · [论文](https://doi.org/10.1088/1674-1056/22/7/078701)
- **Iterative CT Reconstruction Using Shearlet-Based Regularization** — _IEEE TNS 2013_ · [论文](https://doi.org/10.1109/tns.2013.2275994)
- **Iterative Image Reconstruction for Sparse-View CT Using Normal-Dose Image Induced Total Variation Prior** — _PLoS One 2013_ · [论文](https://doi.org/10.1371/journal.pone.0079709)
- **Optimization-based image reconstruction from sparse-view data in offset-detector CBCT** — _PMB 2013_ · [论文](https://doi.org/10.1088/0031-9155/58/2/205)
- **Sparse Tomography** — _SIAM J. Sci. Comput. 2013_ · [论文](https://doi.org/10.1137/120876277)
- **AWTV: Adaptive-weighted total variation minimization for sparse data toward low-dose x-ray computed tomography image reconstruction** — _PMB 2012_ · [论文](https://doi.org/10.1088/0031-9155/57/23/7923)
- **Few-view image reconstruction with dual dictionaries** — _PMB 2012_ · [论文](https://doi.org/10.1088/0031-9155/57/1/173)
- **Compressed sensing based cone-beam computed tomography reconstruction with a first-order method** — _Med Phys 2010_ · [论文](https://doi.org/10.1118/1.3481510)
- **Evaluation of sparse-view reconstruction from flat-panel-detector cone-beam CT** — _PMB 2010_ · [论文](https://doi.org/10.1088/0031-9155/55/22/001)
- **Directional View Interpolation for Compensation of Sparse Angular Sampling in Cone-Beam CT** — _TMI 2009_ · [论文](https://doi.org/10.1109/tmi.2008.2011550)
- **Few-View Projection Reconstruction With an Iterative Reconstruction-Reprojection Algorithm and TV Constraint** — _IEEE TNS 2009_ · [论文](https://doi.org/10.1109/tns.2008.2009990)
- **X-ray cargo container inspection system with few-view projection imaging** — _NIMA 2009_ · [论文](https://doi.org/10.1016/j.nima.2008.08.151)
- **Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization** — _PMB 2008_ · [论文](https://doi.org/10.1088/0031-9155/53/17/021)
- **Compressed sensing** — _IEEE TIT 2006_ · [论文](https://doi.org/10.1109/tit.2006.871582)
- **Robust uncertainty principles: exact signal reconstruction from highly incomplete frequency information** — _IEEE TIT 2006_ · [论文](https://doi.org/10.1109/tit.2005.862083)

### 有限角层析

<sub>角度楔形缺失，零空间使问题严重病态 · 44 篇论文</sub>

- **CryoDeRec: A Supervised Multi-task Framework for Joint cryo-ET Restoration Enabled by Generative Physical Simulation** — _CVPR 2026_ · [论文](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_A_Supervised_Multi-task_Framework_for_Joint_cryo-ET_Restoration_Enabled_by_CVPR_2026_paper.html) · [代码](https://github.com/ZhidongYang/CryoDeRec)
- **Equivariance2Inverse: A Practical Self-Supervised CT Reconstruction Method Benchmarked on Real, Limited-Angle, and Blurred Data** — _TCI 2026_ · [论文](https://arxiv.org/abs/2510.23317)
- **Geometry-Aware Diffusion Approximate Posterior Sampling for Sparse-View and Limited-Angle CT** — _预印本 2026_ · [论文](https://arxiv.org/abs/2610.08866)
- **High-Precision Image Reconstruction for Binary-Valued X-Ray CT From Limited-View Projections** — _TIM 2026_ · [论文](https://doi.org/10.1109/tim.2026.3670565)
- **OpenPros: A Large-Scale Dataset for Limited View Prostate Ultrasound Computed Tomography** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2505.12261) · [项目页](https://open-pros.github.io/)
- **Advancing Limited-Angle CT Reconstruction Through Diffusion-Based Sinogram Completion** — _ICIP 2025_ · [论文](https://arxiv.org/abs/2505.19385)
- **Data-Efficient Limited-Angle CT Using Deep Priors and Regularization** — _预印本 2025_ · [论文](https://arxiv.org/abs/2502.12293)
- **Diffusion-Based Limited-Angle CT Reconstruction under Noisy Conditions** — _ICIP 2025_ · [论文](https://arxiv.org/abs/2507.05647)
- **End-to-End Deep Learning for Interior Tomography with Low-Dose X-ray CT** — _PMB 2025_ · [论文](https://arxiv.org/abs/2501.05085)
- **Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency** — _ISBI 2025_ · [论文](https://arxiv.org/abs/2411.06181)
- **Limited-Angle CBCT Reconstruction via Geometry-Integrated Cycle-domain Denoising Diffusion Probabilistic Models** — _预印本 2025_ · [论文](https://arxiv.org/abs/2506.13545)
- **Limited-angle SPECT image reconstruction using deep image prior** — _PMB 2025_ · [论文](https://arxiv.org/abs/2503.18342)
- **Limited-angle x-ray nano-tomography with machine-learning enabled iterative reconstruction engine** — _npj Comput Mater 2025_ · [论文](https://doi.org/10.1038/s41524-025-01724-0)
- **Projection Embedded Diffusion Bridge for CT Reconstruction from Incomplete Data** — _预印本 2025_ · [论文](https://arxiv.org/abs/2510.22605)
- **SIRE-Net: Structure-Integrated Refinement and Enhancement Network for Limited-Angle CT Reconstruction** — _TIM 2025_ · [论文](https://doi.org/10.1109/tim.2025.3568935)
- **A Review of Deep Learning CT Reconstruction From Incomplete Projection Data** — _TRPMS 2024_ · [论文](https://doi.org/10.1109/trpms.2023.3316349)
- **Dolce: A Model-Based Probabilistic Diffusion Framework for Limited-Angle CT Reconstruction** — _ICCV 2023_ · [论文](https://doi.org/10.1109/ICCV51070.2023.00963)
- **SPIE-DIR: Self-Prior Information Enhanced Deep Iterative Reconstruction Using Two Complementary Limited-Angle Scans for DECT** — _TIM 2023_ · [论文](https://doi.org/10.1109/tim.2022.3227549)
- **DIOR: Deep Iterative Optimization-Based Residual-Learning for Limited-Angle CT Reconstruction** — _TMI 2022_ · [论文](https://doi.org/10.1109/tmi.2022.3148110)
- **UNDIP: Sparse-view and limited-angle CT reconstruction with untrained networks and deep image prior** — _CMPB 2022_ · [论文](https://doi.org/10.1016/j.cmpb.2022.107167)
- **CasRedSCAN: Limited View Tomographic Reconstruction Using a Cascaded Residual Dense Spatial-Channel Attention Network With Projection Data Fidelity Layer** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3066318)
- **DCTR: Dynamic CT Reconstruction From Limited Views With Implicit Neural Representations** — _ICCV 2021_ · [论文](https://doi.org/10.1109/iccv48922.2021.00226)
- **Limited-Angle CT Reconstruction via the L1/L2 Minimization** — _SIAM J. Imaging Sci. 2021_ · [论文](https://doi.org/10.1137/20m1341490)
- **SPECIAL: Single-Shot Projection Error Correction Integrated Adversarial Learning for Limited-Angle CT** — _TCI 2021_ · [论文](https://doi.org/10.1109/tci.2021.3098922)
- **Deep learning based image reconstruction algorithm for limited-angle translational computed tomography** — _PLoS One 2020_ · [论文](https://doi.org/10.1371/journal.pone.0226963)
- **HD-CNN: Artifact removal using a hybrid-domain convolutional neural network for limited-angle computed tomography imaging** — _PMB 2020_ · [论文](https://doi.org/10.1088/1361-6560/ab9066)
- **Limited View Tomographic Reconstruction Using a Deep Recurrent Framework with Residual Dense Spatial-Channel Attention Network and Sinogram Consistency** — _预印本 2020_ · [论文](https://arxiv.org/abs/2009.01782)
- **ℓ₀DL: Limited-Angle X-Ray CT Reconstruction Using Image Gradient ℓ₀-Norm With Dictionary Learning** — _TRPMS 2020_ · [论文](https://doi.org/10.1109/trpms.2020.2991887)
- **A deep learning reconstruction framework for X-ray computed tomography with incomplete data** — _PLoS One 2019_ · [论文](https://doi.org/10.1371/journal.pone.0224426)
- **ADMM-based deep reconstruction for limited-angle CT** — _PMB 2019_ · [论文](https://doi.org/10.1088/1361-6560/ab1aba)
- **Laminography in the lab: imaging planar objects using a conventional x-ray CT scanner** — _Meas. Sci. Technol. 2019_ · [论文](https://doi.org/10.1088/1361-6501/aafcae)
- **Learning the invisible: a hybrid deep learning-shearlet framework for limited angle computed tomography** — _Inverse Problems 2019_ · [论文](https://doi.org/10.1088/1361-6420/ab10ca)
- **An Image Reconstruction Method Based on Total Variation and Wavelet Tight Frame for Limited-Angle CT** — _IEEE Access 2018_ · [论文](https://doi.org/10.1109/access.2017.2779148)
- **CTNet: Lose The Views: Limited Angle CT Reconstruction via Implicit Sinogram Completion** — _CVPR 2018_ · [论文](https://doi.org/10.1109/cvpr.2018.00664)
- **DLCT: Deep Learning Computed Tomography: Learning Projection-Domain Weights From Image Domain in Limited Angle Problems** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2833499)
- **An improved statistical iterative algorithm for sparse-view and limited-angle CT image reconstruction** — _Sci. Rep. 2017_ · [论文](https://doi.org/10.1038/s41598-017-11222-z)
- **Edge-preserving reconstruction from sparse projections of limited-angle computed tomography using L0-regularized gradient prior** — _Rev. Sci. Instrum. 2017_ · [论文](https://doi.org/10.1063/1.4981132)
- **ReATV: Reweighted Anisotropic Total Variation Minimization for Limited-Angle CT Reconstruction** — _IEEE TNS 2017_ · [论文](https://doi.org/10.1109/tns.2017.2750199)
- **LIVE: A limited-angle intrafraction verification (LIVE) system for radiation therapy** — _Med Phys 2014_ · [论文](https://doi.org/10.1118/1.4861820)
- **A technique for estimating 4D-CBCT using prior knowledge and limited-angle projections** — _Med Phys 2013_ · [论文](https://doi.org/10.1118/1.4825097)
- **ATV: A limited-angle CT reconstruction method based on anisotropic TV minimization** — _PMB 2013_ · [论文](https://doi.org/10.1088/0031-9155/58/7/2119)
- **Comparison of image quality in computed laminography and tomography** — _Opt. Express 2012_ · [论文](https://doi.org/10.1364/oe.20.000794)
- **Task-based performance analysis of FBP, SART and ML for digital breast tomosynthesis using signal CNR and Channelised Hotelling Observers** — _Med Image Anal 2011_ · [论文](https://doi.org/10.1016/j.media.2010.07.004)
- **A novel digital tomosynthesis (DTS) reconstruction method using a deformation field map** — _Med Phys 2008_ · [论文](https://doi.org/10.1118/1.2940725)

### 低剂量 CT 去噪

<sub>管电流降低带来的噪声抑制，可在图像域、投影域或双域进行 · 57 篇论文</sub>

- **Dose-Aware Cold Diffusion with Physics Consistency for Generalizable Low-Dose CT Reconstruction** — _IJCNN 2026_ · [论文](https://arxiv.org/abs/2609.18943)
- **Foundation-VAE: Foundation VAEs for 3D CT Reconstruction, Augmentation, and Generation** — _ICML 2026_ · [论文](https://arxiv.org/abs/2605.30893) · [代码](https://github.com/qic999/Foundation-VAE)
- **HARU-Net: Hybrid Attention Residual U-Net for Edge-Preserving Denoising in Cone-Beam Computed Tomography** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.22544)
- **Low-Level Dataset Distillation for Medical Image Enhancement** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2511.13106) · [代码](https://github.com/xufz123/Med_LLDD)
- **Toward CT-Equivalent Image Quality in Low-Dose Radiotherapy Planning: Conditional Diffusion-Based CBCT-to-CT Synthesis and the Impact of CBCT Input Representation** — _预印本 2026_ · [论文](https://arxiv.org/abs/2608.08919)
- **DenoMamba: A Fused State-Space Model for Low-Dose CT Denoising** — _JBHI 2025_ · [论文](https://doi.org/10.1109/jbhi.2025.3629034) · [代码](https://github.com/icon-lab/DenoMamba)
- **End-to-End Deep Learning for Interior Tomography with Low-Dose X-ray CT** — _PMB 2025_ · [论文](https://arxiv.org/abs/2501.05085)
- **Noise-Inspired Diffusion Model for Generalizable Low-Dose CT Reconstruction** — _Med Image Anal 2025_ · [论文](https://arxiv.org/abs/2506.22012) · [代码](https://github.com/qgao21/NEED)
- **Zero-Shot Low-dose CT Denoising via Sinogram Flicking** — _预印本 2025_ · [论文](https://arxiv.org/abs/2504.07927)
- **EAGLE: An Edge-Aware Gradient Localization Enhanced Loss for CT Image Reconstruction** — _预印本 2024_ · [论文](https://arxiv.org/abs/2403.10695) · [代码](https://github.com/sypsyp97/Eagle_Loss)
- **ASCON: Anatomy-Aware Supervised Contrastive Learning Framework for Low-Dose CT Denoising** — _MICCAI 2023_ · [论文](https://doi.org/10.1007/978-3-031-43999-5_34) · [代码](https://github.com/hao1635/ASCON)
- **CTformer: Convolution-Free Token2Token Dilated Vision Transformer for Low-Dose CT Denoising** — _PMB 2023_ · [论文](https://doi.org/10.1088/1361-6560/acc000) · [代码](https://github.com/wdayang/CTformer)
- **DADN: Domain-adaptive denoising network for low-dose CT via noise estimation and transfer learning** — _Med Phys 2023_ · [论文](https://doi.org/10.1002/mp.15952)
- **IRDS: Iterative reconstruction of low-dose CT based on differential sparse** — _BSPC 2023_ · [论文](https://doi.org/10.1016/j.bspc.2022.104204)
- **Synergizing Physics/Model-based and Data-driven Methods for Low-Dose CT** — _IEEE SPM 2023_ · [论文](https://arxiv.org/abs/2203.15725)
- **CCN-CL: A content-noise complementary network with contrastive learning for low-dose computed tomography denoising** — _CBM 2022_ · [论文](https://doi.org/10.1016/j.compbiomed.2022.105759)
- **CoCoDiff: A Contextual Conditional Diffusion Model for Low-dose CT Image Denoising** — _SPIE DXRT 2022_ · [论文](https://doi.org/10.1117/12.2634939)
- **DESDGAN: A Dual-Encoder-Single-Decoder Based Low-Dose CT Denoising Network** — _JBHI 2022_ · [论文](https://doi.org/10.1109/jbhi.2022.3155788) · [代码](https://github.com/hanzefang/DESDGAN)
- **DFDLM: A Dataset-free Deep Learning Method for Low-Dose CT Image Reconstruction** — _Inverse Problems 2022_ · [论文](https://arxiv.org/abs/2205.00463)
- **DGR-2: An Unsupervised Reconstruction Method For Low-Dose CT Using Deep Generative Regularization Prior** — _BSPC 2022_ · [论文](https://arxiv.org/abs/2012.06448) · [代码](https://github.com/mozanunal/SparseCT)
- **DU-GAN: Generative Adversarial Networks with Dual-Domain U-Net Based Discriminators for Low-Dose CT Denoising** — _TIM 2022_ · [论文](https://doi.org/10.1109/tim.2021.3128703) · [代码](https://github.com/Hzzone/DU-GAN)
- **EASEL: Iterative Reconstruction for Low-Dose CT using Deep Gradient Priors of Generative Model** — _TRPMS 2022_ · [论文](https://doi.org/10.1109/trpms.2022.3148373) · [代码](https://github.com/yqx7150/EASEL)
- **Low-Dose CT Using Denoising Diffusion Probabilistic Model for 20× Speedup** — _预印本 2022_ · [论文](https://arxiv.org/abs/2209.15136)
- **MALAR: Multiple Adversarial Learning based Angiography Reconstruction for Ultra-low-dose Contrast Medium CT** — _JBHI 2022_ · [论文](https://doi.org/10.1109/jbhi.2022.3213595) · [代码](https://github.com/HIC-SYSU/MALAR)
- **CLEAR: Comprehensive Learning Enabled Adversarial Reconstruction for Subtle Structure Enhanced Low-Dose CT Imaging** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3097808)
- **DeACNN: Learning a Deep CNN Denoising Approach Using Anatomical Prior Information Implemented With Attention Mechanism for Low-Dose CT Imaging on Clinical Patient Data From Multiple Anatomical Sites** — _JBHI 2021_ · [论文](https://doi.org/10.1109/jbhi.2021.3061758)
- **MAGIC: Manifold and graph integrative convolutional network for low-dose CT reconstruction** — _TMI 2021_ · [论文](https://arxiv.org/abs/2008.00406)
- **MAP-NN: Competitive performance of a modularized deep neural network compared to commercial algorithms for low-dose CT image reconstruction** — _Nat Mach Intell 2021_ · [论文](https://doi.org/10.1038/s42256-019-0057-9)
- **N2S: Self-Supervised Training For Low-Dose Ct Reconstruction** — _ISBI 2021_ · [论文](https://doi.org/10.1109/isbi48211.2021.9433944)
- **SinoNet: Noise-Generating-Mechanism-Driven Unsupervised Learning for Low-Dose CT Sinogram Recovery** — _TRPMS 2021_ · [论文](https://doi.org/10.1109/trpms.2021.3083361)
- **CADL: Noise and spatial resolution properties of a commercially available deep learning‐based CT reconstruction algorithm** — _Med Phys 2020_ · [论文](https://doi.org/10.1002/mp.14319)
- **EDCNN: Edge Enhancement-Based Densely Connected Network with Compound Loss for Low-Dose CT Denoising** — _ICSP 2020_ · [论文](https://doi.org/10.1109/icsp48669.2020.9320928) · [代码](https://github.com/workingcoder/EDCNN)
- **REDAEP: Robust and Enhanced Denoising Autoencoding Prior for Sparse-View CT Reconstruction** — _TRPMS 2020_ · [论文](https://doi.org/10.1109/trpms.2020.2989634)
- **SACNN: Self-Attention Convolutional Neural Network for Low-Dose CT Denoising With Self-Supervised Perceptual Loss Network** — _TMI 2020_ · [论文](https://doi.org/10.1109/tmi.2020.2968472)
- **SPULTRA: Low-Dose CT Image Reconstruction with Joint Statistical and Learned Image Models** — _TMI 2019_ · [论文](https://doi.org/10.1109/tmi.2019.2934933)
- **SUPER-2: SUPER Learning: A Supervised-Unsupervised Framework for Low-Dose CT Image Reconstruction** — _ICCVW 2019_ · [论文](https://doi.org/10.1109/iccvw.2019.00490)
- **VVBP-tSVD: VVBP-Tensor in the FBP Algorithm: Its Properties and Application in Low-Dose CT Reconstruction** — _TMI 2019_ · [论文](https://doi.org/10.1109/tmi.2019.2935187)
- **3pADMM: Optimizing a parameterized plug-and-play ADMM for iterative low-dose CT reconstruction** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2865202)
- **SAGAN: Sharpness-Aware Low Dose CT Denoising Using Conditional Generative Adversarial Network** — _JDI 2018_ · [论文](https://doi.org/10.1007/s10278-018-0056-0) · [代码](https://github.com/xinario/SAGAN)
- **SSDA: Low-dose CT restoration via stacked sparse denoising autoencoders** — _Neurocomputing 2018_ · [论文](https://doi.org/10.1016/j.neucom.2018.01.015)
- **Statistical Image Reconstruction Using Mixed Poisson-Gaussian Noise Model for X-Ray CT** — _预印本 2018_ · [论文](https://arxiv.org/abs/1801.09533)
- **WavResNet: Deep Convolutional Framelet Denosing for Low-Dose CT via Wavelet Residual Network** — _TMI 2018_ · [论文](https://arxiv.org/abs/1707.09938)
- **WGAN-VGG: Low Dose CT Image Denoising Using a Generative Adversarial Network with Wasserstein Distance and Perceptual Loss** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2827462) · [代码](https://github.com/SSinyu/WGAN-VGG)
- **Applications of nonlocal means algorithm in low-dose X-ray CT image processing and reconstruction: A review** — _Med Phys 2017_ · [论文](https://doi.org/10.1002/mp.12097)
- **Deep Convolutional Neural Network for Inverse Problems in Imaging** — _TIP 2017_ · [论文](https://doi.org/10.1109/tip.2017.2713099)
- **IMAP-TV: Robust low-dose CT sinogram preprocessing via exploiting noise-generating mechanism** — _TMI 2017_ · [论文](https://doi.org/10.1109/tmi.2017.2767290)
- **KSAE: Iterative Low-dose CT Reconstruction with Priors Trained by Artificial Neural Network** — _TMI 2017_ · [论文](https://doi.org/10.1109/tmi.2017.2753138)
- **LoDoPaB-CT: , a benchmark dataset for low-dose computed tomography reconstruction (**Scientific Data**) -->** — _Scientific Data 2017_ · [论文](https://doi.org/10.1038/s41597-021-00893-z) · [代码](https://github.com/jleuschn/lodopab_tech_ref)
- **Low-dose CT via convolutional neural network** — _BOE 2017_ · [论文](https://doi.org/10.1364/boe.8.000679)
- **Low-Dose Dynamic Cerebral Perfusion Computed Tomography Reconstruction via Kronecker-Basis-Representation Tensor Sparsity Regularization** — _TMI 2017_ · [论文](https://doi.org/10.1109/tmi.2017.2749212)
- **RED-CNN: Low-Dose CT with a Residual Encoder-Decoder Convolutional Neural Network** — _TMI 2017_ · [论文](https://doi.org/10.1109/tmi.2017.2715284) · [代码](https://github.com/SSinyu/RED-CNN)
- **SENP: Low‐dose CT reconstruction using spatially encoded nonlocal penalty** — _Med Phys 2017_ · [论文](https://doi.org/10.1002/mp.12523)
- **Low-dose cerebral perfusion computed tomography image restoration via low-rank and total variation regularizations** — _Neurocomputing 2016_ · [论文](https://doi.org/10.1016/j.neucom.2016.01.090)
- **Low-dose X-ray computed tomography image reconstruction with a combined low-mAs and sparse-view protocol** — _Opt. Express 2014_ · [论文](https://doi.org/10.1364/oe.22.015190)
- **AWTV: Adaptive-weighted total variation minimization for sparse data toward low-dose x-ray computed tomography image reconstruction** — _PMB 2012_ · [论文](https://doi.org/10.1088/0031-9155/57/23/7923)
- **Low-Dose X-ray CT Reconstruction via Dictionary Learning** — _TMI 2012_ · [论文](https://doi.org/10.1109/tmi.2012.2195669)
- **K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation** — _IEEE TSP 2006_ · [论文](https://doi.org/10.1109/tsp.2006.881199)

### 金属伪影校正

<sub>高密度植入物引起的射线硬化、光子饥饿与散射 · 21 篇论文</sub>

- **Balancing Efficiency and Restoration: Lightweight Mamba-Based Model for CT Metal Artifact Reduction** — _TRPMS 2026_ · [论文](https://arxiv.org/abs/2604.06622) · [代码](https://github.com/RICKand-MORTY/MARMamba)
- **Complex Wavelet-Based Sinogram Segmentation for Metal Artifact Reduction in Cone-Beam CT** — _PMB 2026_ · [论文](https://arxiv.org/abs/2602.14315)
- **H3D-MarNet: Wavelet-Guided Dual-Path Learning for Metal Artifact Suppression and CT Modality Transformation for Radiotherapy Workflows** — _ICPR 2026_ · [论文](https://arxiv.org/abs/2605.12252)
- **Leveraging Image Editing Foundation Models for Data-Efficient CT Metal Artifact Reduction** — _CVPRW 2026_ · [论文](https://arxiv.org/abs/2604.05934) · [代码](https://github.com/ahmetemirdagi/CT-EditMAR)
- **MGMAR: Metal-Guided Metal Artifact Reduction for X-ray Computed Tomography** — _预印本 2026_ · [论文](https://arxiv.org/abs/2603.13447)
- **Splat-Based Metal Artifact Reduction in Cone-Beam CT via Compact Attenuation Modeling** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2608.04764)
- **Splat-based Metal Artifact Reduction in Cone-Beam CT via Polychromatic Modeling** — _CGF 2026_ · [论文](https://arxiv.org/abs/2608.13159)
- **Unsupervised Metal Artifact Reduction in Dental CBCT using Fine-tuned Cycle-Consistent Adversarial Networks** — _Digital 2026_ · [论文](https://arxiv.org/abs/2607.20977)
- **VoxelSynth3D: Interpretable Volumetric Image-Domain Metal Artifact Reduction with a Paired Synthetic CLINIC-Metal Benchmark** — _BHI 2026_ · [论文](https://arxiv.org/abs/2610.01512)
- **FIND-Net -- Fourier-Integrated Network with Dictionary Kernels for Metal Artifact Reduction** — _MICCAI 2025_ · [论文](https://arxiv.org/abs/2508.10617) · [代码](https://github.com/Farid-Tasharofi/FIND-Net)
- **ReMAR-DS: Recalibrated Feature Learning for Metal Artifact Reduction and CT Domain Transformation** — _ICIAP 2025_ · [论文](https://arxiv.org/abs/2506.19531)
- **DuDoDp-MAR: Unsupervised CT Metal Artifact Reduction by Plugging Diffusion Priors in Dual Domains** — _TMI 2024_ · [论文](https://doi.org/10.1109/tmi.2024.3351201) · [代码](https://github.com/DeepXuan/DuDoDp-MAR)
- **Polyner: Unsupervised Polychromatic Neural Representation for CT Metal Artifact Reduction** — _NeurIPS 2023_ · [论文](https://arxiv.org/abs/2306.15203) · [代码](https://github.com/iwuqing/Polyner)
- **SemiMAR: Semi-Supervised Learning for CT Metal Artifact Reduction** — _JBHI 2023_ · [论文](https://doi.org/10.1109/jbhi.2023.3312292) · [代码](https://github.com/zjk1988/SemiMAR)
- **ACDNet: Adaptive Convolutional Dictionary Network for CT Metal Artifact Reduction** — _IJCAI 2022_ · [论文](https://doi.org/10.24963/ijcai.2022/195) · [代码](https://github.com/hongwang01/ACDNet)
- **DuDoDR-Net: Dual-domain data consistent recurrent network for simultaneous sparse view and metal artifact reduction in computed tomography** — _MedIA 2022_ · [论文](https://doi.org/10.1016/j.media.2021.102289)
- **IDOL-Net: An Interactive Dual-Domain Parallel Network for CT Metal Artifact Reduction** — _TRPMS 2022_ · [论文](https://doi.org/10.1109/trpms.2022.3171440) · [代码](https://github.com/zjk1988/IDOL-Net)
- **DAN-Net: Dual-Domain Adaptive-Scaling Non-Local Network for CT Metal Artifact Reduction** — _MICCAI 2021_ · [论文](https://doi.org/10.1007/978-3-030-87231-1_24) · [代码](https://github.com/zjk1988/DAN-Net)
- **InDuDoNet: An Interpretable Dual Domain Network for CT Metal Artifact Reduction** — _MICCAI 2021_ · [论文](https://arxiv.org/abs/2109.05298) · [代码](https://github.com/hongwang01/InDuDoNet)
- **MAR-4Dec: Metal Artifact Reduction in CT: Where Are We After Four Decades?** — _IEEE Access 2016_ · [论文](https://doi.org/10.1109/ACCESS.2016.2608621)
- **PBAC: Prior-based artifact correction (PBAC) in computed tomography** — _Med Phys 2014_ · [论文](https://doi.org/10.1118/1.4851536)

### 能谱与双能 CT

<sub>多能采集、物质分解与光子计数 CT · 17 篇论文</sub>

- **$K$-NeAS: Scalable Multi-Material CT Reconstruction Using Neural SDFs** — _Off-Grid Workshop 2026_ · [论文](https://arxiv.org/abs/2607.14415)
- **Integration of Spectral CT with PET and SPECT: Bringing Tissue Composition Information to Molecular Imaging** — _预印本 2026_ · [论文](https://arxiv.org/abs/2609.27398)
- **Modeling X-Ray Photon Pile-Up with a Normalizing Flow** — _NeurIPS Workshop 2025_ · [论文](https://arxiv.org/abs/2511.11863)
- **SOUL-Net: A Sparse and Low-Rank Unrolling Network for Spectral CT Image Reconstruction** — _TNNLS 2024_ · [论文](https://doi.org/10.1109/tnnls.2023.3319408) · [代码](https://github.com/scuchenxiang/SOUL-Net)
- **FONT-SIR: Fourth-Order Nonlocal Tensor Decomposition Model for Spectral CT Image Reconstruction** — _TMI 2022_ · [论文](https://doi.org/10.1109/tmi.2022.3156270)
- **CD-Net: Comprehensive Domain Network With Spectral Complementary for DECT Sparse-View Reconstruction** — _TCI 2021_ · [论文](https://doi.org/10.1109/tci.2021.3070184)
- **LRTP: Spectral CT reconstruction via low-rank representation and region-specific texture preserving Markov random field regularization** — _TMI 2020_ · [论文](https://doi.org/10.1109/tmi.2020.2983414)
- **SISTER: Spectral-Image Similarity-Based Tensor With Enhanced-Sparsity Reconstruction for Sparse-View Multi-Energy CT** — _TCI 2020_ · [论文](https://doi.org/10.1109/tci.2019.2956886)
- **NLCTF: Non-Local Low-Rank Cube-Based Tensor Factorization for Spectral CT Reconstruction** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2878226)
- **SPIR: Dual energy CT with one full scan and a second sparse-view scan using structure preserving iterative reconstruction (SPIR)** — _PMB 2016_ · [论文](https://doi.org/10.1088/0031-9155/61/18/6684)
- **Dual- and Multi-Energy CT: Principles, Technical Approaches, and Clinical Applications** — _Radiology 2015_ · [论文](https://doi.org/10.1148/radiol.2015142631)
- **Sparse-View Spectral CT Reconstruction Using Spectral Patch-Based Low-Rank Penalty** — _TMI 2015_ · [论文](https://doi.org/10.1109/tmi.2014.2380993)
- **Experimental Feasibility of Multi-Energy Photon-Counting K-Edge Imaging in Pre-Clinical Computed Tomography** — _PMB 2008_ · [论文](https://doi.org/10.1088/0031-9155/53/15/002)
- **K-Edge Imaging in X-Ray Computed Tomography Using Multi-Bin Photon Counting Detectors** — _PMB 2007_ · [论文](https://doi.org/10.1088/0031-9155/52/15/020)
- **Statistical Image Reconstruction for Polyenergetic X-Ray Computed Tomography** — _TMI 2002_ · [论文](https://doi.org/10.1109/42.993128)
- **An Iterative Maximum-Likelihood Polychromatic Algorithm for CT** — _TMI 2001_ · [论文](https://doi.org/10.1109/42.959297)
- **Energy-Selective Reconstructions in X-Ray Computerised Tomography** — _PMB 1976_ · [论文](https://doi.org/10.1088/0031-9155/21/5/002)

### 锥束 CT

<sub>圆周、螺旋与非标准 CBCT 几何；在轨成像 · 66 篇论文</sub>

- **Anatomy-preserving unpaired cone-beam CT refinement for image-guided radiotherapy using pseudo-label guided diffusion** — _预印本 2026_ · [论文](https://arxiv.org/abs/2610.06094)
- **CBCT-Based Synthetic CT Generation Using Conditional Flow Matching Model** — _预印本 2026_ · [论文](https://arxiv.org/abs/2603.05796)
- **Complex Wavelet-Based Sinogram Segmentation for Metal Artifact Reduction in Cone-Beam CT** — _PMB 2026_ · [论文](https://arxiv.org/abs/2602.14315)
- **Cone-beam artifact reduction in Gamma Knife CBCT images using a line-arc-line scan trajectory** — _预印本 2026_ · [论文](https://arxiv.org/abs/2609.30169)
- **Cone-Beam CT Image Quality Enhancement Using A Latent Diffusion Model Trained with Simulated CBCT Artifacts** — _预印本 2026_ · [论文](https://arxiv.org/abs/2603.26014)
- **Continuity-driven Synergistic Diffusion with Neural Priors for Ultra-Sparse-View CBCT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.07980)
- **Dual-domain U-Nets with embedded back projection operators for motion-resolved 4D CBCT reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2608.03430)
- **Field-of-View Extension in Dental Cone-Beam CT via Implicit Neural Representations and Diffusion Model-Based Refinement** — _MICAD 2026_ · [论文](https://arxiv.org/abs/2609.28110) · [代码](https://github.com/SusanneSchaub/CBCT-FOV-Extension)
- **GH-NAF: Grid-Adaptive Hash-Level-Attended Neural Attenuation Fields for Discrepancy-Aware CBCT** — _CVPR 2026_ · [论文](https://openaccess.thecvf.com/content/CVPR2026/html/Oh_GH-NAF_Grid-Adaptive_Hash-Level-Attended_Neural_Attenuation_Fields_for_Discrepancy-Aware_CBCT_CVPR_2026_paper.html) · [代码](https://github.com/seongje-oh/GH-NAF)
- **H3D-MarNet: Wavelet-Guided Dual-Path Learning for Metal Artifact Suppression and CT Modality Transformation for Radiotherapy Workflows** — _ICPR 2026_ · [论文](https://arxiv.org/abs/2605.12252)
- **HARU-Net: Hybrid Attention Residual U-Net for Edge-Preserving Denoising in Cone-Beam Computed Tomography** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.22544)
- **High-Fidelity 3D Tooth Reconstruction by Fusing Intraoral Scans and CBCT Data via a Deep Implicit Representation** — _ISBI 2026_ · [论文](https://arxiv.org/abs/2601.15358)
- **Joint-decoupled iterative CBCT reconstruction with hybrid scatter estimation and voxel-adaptive beam hardening correction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2607.15812)
- **NGPS: Structure-Preserving Self-Supervised Denoising via Neighbor-Guided Patch Sampling** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2606.23200) · [代码](https://github.com/cv-cho/NGPS)
- **Non-circular scan trajectories for reducing cone-beam artifacts in Gamma Knife CBCT images: a simulation study** — _预印本 2026_ · [论文](https://arxiv.org/abs/2609.28232)
- **Riner: Unsupervised Multi-Parameter Inverse Solving for Reducing Ring Artifacts in 3D X-Ray CBCT** — _AAAI 2026_ · [论文](https://arxiv.org/abs/2412.05853) · [代码](https://github.com/iwuqing/Riner)
- **Robustness and Stability Analysis of Differentiable Shift-Variant FBP for Cone-Beam CT under Challenging Acquisition Settings** — _MELBA 2026_ · [论文](https://arxiv.org/abs/2607.09828) · [项目页](https://melba-journal.org/2026:014)
- **Spectral Consistent Flow for One-Step 3D Medical Image Translation** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2607.10627)
- **Splat-Based Metal Artifact Reduction in Cone-Beam CT via Compact Attenuation Modeling** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2608.04764)
- **Splat-based Metal Artifact Reduction in Cone-Beam CT via Polychromatic Modeling** — _CGF 2026_ · [论文](https://arxiv.org/abs/2608.13159)
- **Texture-preserving implicit neural representation for Cone beam CT truncated reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2606.06039)
- **Toward CT-Equivalent Image Quality in Low-Dose Radiotherapy Planning: Conditional Diffusion-Based CBCT-to-CT Synthesis and the Impact of CBCT Input Representation** — _预印本 2026_ · [论文](https://arxiv.org/abs/2608.08919)
- **Unsupervised Metal Artifact Reduction in Dental CBCT using Fine-tuned Cycle-Consistent Adversarial Networks** — _Digital 2026_ · [论文](https://arxiv.org/abs/2607.20977)
- **3D CBCT Artefact Removal Using Perpendicular Score-Based Diffusion Models** — _DGM4MICCAI 2025_ · [论文](https://arxiv.org/abs/2603.06300)
- **4DGS-4DCBCT: Spatiotemporal Gaussian Optimization for 4D Cone Beam CT Reconstruction from Sparsely Sampled Projections** — _预印本 2025_ · [论文](https://arxiv.org/abs/2501.04140) · [代码](https://github.com/fuyabo/4DGS_for_4DCBCT)
- **A Learnt Half-Quadratic Splitting-Based Algorithm for Fast and High-Quality Industrial Cone-beam CT Reconstruction** — _预印本 2025_ · [论文](https://arxiv.org/abs/2501.13128)
- **Adaptive Diffusion Models for Sparse-View Motion-Corrected Head Cone-beam CT** — _TRPMS 2025_ · [论文](https://arxiv.org/abs/2504.14033) · [项目页](https://antoinedepaepe.github.io/jrm-adm-io/)
- **An Iterative Reconstruction Method for Dental Cone-Beam Computed Tomography with a Truncated Field of View** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.07618)
- **DIGS: Dynamic CBCT Reconstruction using Deformation-Informed 4D Gaussian Splatting and a Low-Rank Free-Form Deformation Model** — _MICCAI 2025_ · [论文](https://arxiv.org/abs/2506.22280) · [代码](https://github.com/Yuliang-Huang/DIGS)
- **Enhancing Synthetic CT from CBCT via Multimodal Fusion and End-To-End Registration** — _CAIP 2025_ · [论文](https://arxiv.org/abs/2507.06067)
- **Enhancing Synthetic CT from CBCT via Multimodal Fusion: A Study on the Impact of CBCT Quality and Alignment** — _预印本 2025_ · [论文](https://arxiv.org/abs/2506.08716)
- **Equivariant Conditional Diffusion Model for Head and Neck CT Image Synthesis from CBCT** — _Med Phys 2025_ · [论文](https://arxiv.org/abs/2509.21913)
- **Equivariant Multiscale Learned Invertible Reconstruction for Cone Beam CT: From Simulated to Real Data** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.21180)
- **GANeXt: A Fully ConvNeXt-Enhanced Generative Adversarial Network for MRI- and CBCT-to-CT Synthesis** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.19336)
- **GLFC: Unified Global-Local Feature and Contrast Learning with Mamba-Enhanced UNet for Synthetic CT Generation from CBCT** — _ISBI 2025_ · [论文](https://arxiv.org/abs/2501.02992) · [代码](https://github.com/HiLab-git/GLFC)
- **Learning Wavelet-Sparse FDK for 3D Cone-Beam CT Reconstruction** — _Fully3D 2025_ · [论文](https://arxiv.org/abs/2505.13579)
- **MInDI-3D: Iterative Deep Learning in 3D for Sparse-view Cone Beam Computed Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.09616)
- **Motion-Grad: A Gradient-Based Approach to Fast and Accurate Head Motion Compensation in Cone-Beam CT** — _TMI 2025_ · [论文](https://doi.org/10.1109/tmi.2024.3474250) · [代码](https://github.com/mareikethies/geometry_gradients_CT)
- **Neural Discrete Representation Learning for Sparse-View CBCT Reconstruction: From Algorithm Design to Prospective Multicenter Clinical Evaluation** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.00873)
- **Physics-Inspired Gaussian Kolmogorov-Arnold Networks for X-ray Scatter Correction in Cone-Beam CT** — _预印本 2025_ · [论文](https://arxiv.org/abs/2510.24579)
- **Prior-Adapted Progressive Time-Resolved CBCT Reconstruction Using a Dynamic Reconstruction and Motion Estimation Method** — _预印本 2025_ · [论文](https://arxiv.org/abs/2504.18700)
- **Swap-Net: A Memory-Efficient 2.5D Network for Sparse-View 3D Cone Beam CT Reconstruction to ICF Applications** — _TCI 2025_ · [论文](https://doi.org/10.1109/tci.2025.3572699)
- **Synthetic CT image generation from CBCT: A Systematic Review** — _TRPMS 2025_ · [论文](https://arxiv.org/abs/2501.13972)
- **Time-resolved dynamic CBCT reconstruction using prior-model-free spatiotemporal Gaussian representation (PMF-STGR)** — _预印本 2025_ · [论文](https://arxiv.org/abs/2503.22139)
- **Ultrafast Deep Learning-Based Scatter Estimation in Cone-Beam Computed Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2509.08973)
- **XGenRecon: A New Perspective in Ultrasparse Volumetric CBCT Reconstruction Through Geometry-Controlled X-Ray Projection Generation** — _TRPMS 2025_ · [论文](https://doi.org/10.1109/trpms.2024.3420742)
- **DIF-Gaussian: Learning 3D Gaussians for Extremely Sparse-View Cone-Beam CT Reconstruction** — _MICCAI 2024_ · [论文](https://doi.org/10.1007/978-3-031-72104-5_41) · [代码](https://github.com/xmed-lab/DIF-Gaussian)
- **Scatter-DL: Scatter Correction Using Deep Learning for Cone-Beam Computed Tomography** — _DL4X-ray 2024_ · [论文](https://doi.org/10.1007/978-3-031-75653-5_6)
- **Sparse-View Cone Beam CT Reconstruction Using Data-Consistent Supervised and Adversarial Learning From Scarce Training Data** — _TCI 2023_ · [论文](https://doi.org/10.1109/TCI.2022.3225680)
- **SPQI: Structure-preserving quality improvement of cone beam CT images using contrastive learning** — _CBM 2023_ · [论文](https://doi.org/10.1016/j.compbiomed.2023.106803)
- **NAF: Neural Attenuation Fields for Sparse-View CBCT Reconstruction** — _MICCAI 2022_ · [论文](https://arxiv.org/abs/2209.14540) · [代码](https://github.com/Ruyi-Zha/naf_cbct)
- **SNAF: Sparse-View CBCT Reconstruction with Neural Attenuation Fields** — _预印本 2022_ · [论文](https://arxiv.org/abs/2211.17048)
- **SPARE: Sparse-view reconstruction challenge for 4D cone-beam CT from a 1-min scan** — _Med Phys 2019_ · [论文](https://doi.org/10.1002/mp.13687)
- **LIVE: A limited-angle intrafraction verification (LIVE) system for radiation therapy** — _Med Phys 2014_ · [论文](https://doi.org/10.1118/1.4861820)
- **A technique for estimating 4D-CBCT using prior knowledge and limited-angle projections** — _Med Phys 2013_ · [论文](https://doi.org/10.1118/1.4825097)
- **Artifact-resistant motion estimation with a patient-specific artifact model for motion-compensated cone-beam CT** — _Med Phys 2013_ · [论文](https://doi.org/10.1118/1.4820537)
- **Optimization-based image reconstruction from sparse-view data in offset-detector CBCT** — _PMB 2013_ · [论文](https://doi.org/10.1088/0031-9155/58/2/205)
- **Scatter-Rev: A General Framework and Review of Scatter Correction Methods in X-Ray Cone-Beam CT: Part 1 — Scatter Compensation Approaches** — _Med Phys 2011_ · [论文](https://doi.org/10.1118/1.3599033)
- **Compressed sensing based cone-beam computed tomography reconstruction with a first-order method** — _Med Phys 2010_ · [论文](https://doi.org/10.1118/1.3481510)
- **Evaluation of sparse-view reconstruction from flat-panel-detector cone-beam CT** — _PMB 2010_ · [论文](https://doi.org/10.1088/0031-9155/55/22/001)
- **Directional View Interpolation for Compensation of Sparse Angular Sampling in Cone-Beam CT** — _TMI 2009_ · [论文](https://doi.org/10.1109/tmi.2008.2011550)
- **High Temporal Resolution and Streak-Free Four-Dimensional Cone-Beam Computed Tomography** — _PMB 2008_ · [论文](https://doi.org/10.1088/0031-9155/53/20/006)
- **Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization** — _PMB 2008_ · [论文](https://doi.org/10.1088/0031-9155/53/17/021)
- **Respiratory Correlated Cone Beam CT** — _Med Phys 2005_ · [论文](https://doi.org/10.1118/1.1869074)
- **Cone-Beam Computed Tomography with a Flat-Panel Imager: Magnitude and Effects of X-Ray Scatter** — _Med Phys 2001_ · [论文](https://doi.org/10.1118/1.1339879)
- **FDK: Practical cone-beam algorithm** — _JOSA A 1984_ · [论文](https://doi.org/10.1364/JOSAA.1.000612)

### 动态与 4D CT

<sub>时间分辨重建、运动建模、灌注与心脏 CT · 21 篇论文</sub>

- **Dual-domain U-Nets with embedded back projection operators for motion-resolved 4D CBCT reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2608.03430)
- **Dynamic Black-hole Emission Tomography with Physics-Informed Neural Fields** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2602.08029)
- **4DGS-4DCBCT: Spatiotemporal Gaussian Optimization for 4D Cone Beam CT Reconstruction from Sparsely Sampled Projections** — _预印本 2025_ · [论文](https://arxiv.org/abs/2501.04140) · [代码](https://github.com/fuyabo/4DGS_for_4DCBCT)
- **DIGS: Dynamic CBCT Reconstruction using Deformation-Informed 4D Gaussian Splatting and a Low-Rank Free-Form Deformation Model** — _MICCAI 2025_ · [论文](https://arxiv.org/abs/2506.22280) · [代码](https://github.com/Yuliang-Huang/DIGS)
- **Motion-Grad: A Gradient-Based Approach to Fast and Accurate Head Motion Compensation in Cone-Beam CT** — _TMI 2025_ · [论文](https://doi.org/10.1109/tmi.2024.3474250) · [代码](https://github.com/mareikethies/geometry_gradients_CT)
- **Nonperiodic dynamic CT reconstruction using backward-warping INR with regularization of diffeomorphism (BIRD)** — _预印本 2025_ · [论文](https://arxiv.org/abs/2505.03463)
- **Prior-Adapted Progressive Time-Resolved CBCT Reconstruction Using a Dynamic Reconstruction and Motion Estimation Method** — _预印本 2025_ · [论文](https://arxiv.org/abs/2504.18700)
- **Time-resolved dynamic CBCT reconstruction using prior-model-free spatiotemporal Gaussian representation (PMF-STGR)** — _预印本 2025_ · [论文](https://arxiv.org/abs/2503.22139)
- **X2-Gaussian: 4D Radiative Gaussian Splatting for Continuous-Time Tomographic Reconstruction** — _ICCV 2025_ · [论文](https://doi.org/10.1109/iccv51701.2025.02293) · [代码](https://github.com/yuyouxixi/x2-gaussian)
- **DCTR: Dynamic CT Reconstruction From Limited Views With Implicit Neural Representations** — _ICCV 2021_ · [论文](https://doi.org/10.1109/iccv48922.2021.00226)
- **SPARE: Sparse-view reconstruction challenge for 4D cone-beam CT from a 1-min scan** — _Med Phys 2019_ · [论文](https://doi.org/10.1002/mp.13687)
- **Low-Dose Dynamic Cerebral Perfusion Computed Tomography Reconstruction via Kronecker-Basis-Representation Tensor Sparsity Regularization** — _TMI 2017_ · [论文](https://doi.org/10.1109/tmi.2017.2749212)
- **Low-dose cerebral perfusion computed tomography image restoration via low-rank and total variation regularizations** — _Neurocomputing 2016_ · [论文](https://doi.org/10.1016/j.neucom.2016.01.090)
- **Tensor-based dictionary learning for dynamic tomographic reconstruction** — _PMB 2015_ · [论文](https://doi.org/10.1088/0031-9155/60/7/2803)
- **A technique for estimating 4D-CBCT using prior knowledge and limited-angle projections** — _Med Phys 2013_ · [论文](https://doi.org/10.1118/1.4825097)
- **4D Cone Beam CT via Spatiotemporal Tensor Framelet** — _Med Phys 2012_ · [论文](https://doi.org/10.1118/1.4762288)
- **An Investigation of 4D Cone-Beam CT Algorithms for Slowly Rotating Scanners** — _Med Phys 2010_ · [论文](https://doi.org/10.1118/1.3480986)
- **On-the-Fly Motion-Compensated Cone-Beam CT Using an A Priori Model of the Respiratory Motion** — _Med Phys 2009_ · [论文](https://doi.org/10.1118/1.3115691)
- **High Temporal Resolution and Streak-Free Four-Dimensional Cone-Beam Computed Tomography** — _PMB 2008_ · [论文](https://doi.org/10.1088/0031-9155/53/20/006)
- **PICCS: Prior Image Constrained Compressed Sensing (PICCS): A Method to Accurately Reconstruct Dynamic CT Images from Highly Undersampled Projection Data Sets** — _Med Phys 2008_ · [论文](https://doi.org/10.1118/1.2836423)
- **Respiratory Correlated Cone Beam CT** — _Med Phys 2005_ · [论文](https://doi.org/10.1118/1.1869074)

### 散射校正

<sub>散射的估计与去除，涵盖硬件与软件两类方法 · 11 篇论文</sub>

- **Joint-decoupled iterative CBCT reconstruction with hybrid scatter estimation and voxel-adaptive beam hardening correction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2607.15812)
- **Physics-Inspired Gaussian Kolmogorov-Arnold Networks for X-ray Scatter Correction in Cone-Beam CT** — _预印本 2025_ · [论文](https://arxiv.org/abs/2510.24579)
- **Ultrafast Deep Learning-Based Scatter Estimation in Cone-Beam Computed Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2509.08973)
- **Scatter-DL: Scatter Correction Using Deep Learning for Cone-Beam Computed Tomography** — _DL4X-ray 2024_ · [论文](https://doi.org/10.1007/978-3-031-75653-5_6)
- **Real-Time Scatter Estimation for Medical CT Using the Deep Scatter Estimation: Method and Robustness Analysis with Respect to Different Anatomies, Dose Levels, Tube Voltages, and Data Truncation** — _Med Phys 2019_ · [论文](https://doi.org/10.1002/mp.13274)
- **DSE: Deep Scatter Estimation (DSE): Feasibility of Using a Deep Convolutional Neural Network for Scatter Estimation in X-Ray Computed Tomography** — _SPIE MI 2018_ · [论文](https://doi.org/10.1117/12.2292919)
- **A General Framework and Review of Scatter Correction Methods in Cone-Beam CT: Part 2 — Scatter Estimation Approaches** — _Med Phys 2011_ · [论文](https://doi.org/10.1118/1.3589140)
- **Scatter-Rev: A General Framework and Review of Scatter Correction Methods in X-Ray Cone-Beam CT: Part 1 — Scatter Compensation Approaches** — _Med Phys 2011_ · [论文](https://doi.org/10.1118/1.3599033)
- **Efficient Monte Carlo Based Scatter Artifact Reduction in Cone-Beam Micro-CT** — _TMI 2006_ · [论文](https://doi.org/10.1109/tmi.2006.872328)
- **Scatter Correction Method for X-Ray CT Using Primary Modulation: Theory and Preliminary Results** — _TMI 2006_ · [论文](https://doi.org/10.1109/tmi.2006.884636)
- **Cone-Beam Computed Tomography with a Flat-Panel Imager: Magnitude and Effects of X-Ray Scatter** — _Med Phys 2001_ · [论文](https://doi.org/10.1118/1.1339879)

### 几何标定与运动补偿

<sub>几何自标定、无标记配准、刚性与非刚性运动校正 · 26 篇论文</sub>

- **Active View Selection with Perturbed Gaussian Ensemble for Tomographic Reconstruction** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2603.06852)
- **Conditional Diffusion Posterior Alignment for Sparse-View CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2604.21960)
- **Cone-beam artifact reduction in Gamma Knife CBCT images using a line-arc-line scan trajectory** — _预印本 2026_ · [论文](https://arxiv.org/abs/2609.30169)
- **Exact-GS: Mathematically Rigorous and Accurate 3D Gaussian Splatting for 3D X-Ray Reconstruction** — _CVPR 2026_ · [论文](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Exact-GS_Mathematically_Rigorous_and_Accurate_3D_Gaussian_Splatting_for_3D_CVPR_2026_paper.html) · [代码](https://github.com/brucee1323/Exact-GS)
- **GB-SVFBP: Gaussian-Based Shift-Variant FBP neural network** — _预印本 2026_ · [论文](https://arxiv.org/abs/2607.11584)
- **Geometry-Aware Diffusion Approximate Posterior Sampling for Sparse-View and Limited-Angle CT** — _预印本 2026_ · [论文](https://arxiv.org/abs/2610.08866)
- **Revisiting Pose Sensitivity in Splat-based Computed Tomography under Sparse-view Reconstruction** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2608.04752)
- **Riner: Unsupervised Multi-Parameter Inverse Solving for Reducing Ring Artifacts in 3D X-Ray CBCT** — _AAAI 2026_ · [论文](https://arxiv.org/abs/2412.05853) · [代码](https://github.com/iwuqing/Riner)
- **Robustness and Stability Analysis of Differentiable Shift-Variant FBP for Cone-Beam CT under Challenging Acquisition Settings** — _MELBA 2026_ · [论文](https://arxiv.org/abs/2607.09828) · [项目页](https://melba-journal.org/2026:014)
- **Texture-preserving implicit neural representation for Cone beam CT truncated reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2606.06039)
- **TG-Field: Geometry-Aware Radiative Gaussian Fields for Tomographic Reconstruction** — _AAAI 2026_ · [论文](https://arxiv.org/abs/2602.11705)
- **Tomographic Sparse View Selection Using the View Covariance Loss** — _TPAMI 2026_ · [论文](https://doi.org/10.1109/TPAMI.2025.3600072)
- **A CT Geometry With Multiple Centers Of Rotation For Solving Sparse View Problem** — _预印本 2025_ · [论文](https://arxiv.org/abs/2502.06125)
- **An Iterative Reconstruction Method for Dental Cone-Beam Computed Tomography with a Truncated Field of View** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.07618)
- **Enhancing Synthetic CT from CBCT via Multimodal Fusion and End-To-End Registration** — _CAIP 2025_ · [论文](https://arxiv.org/abs/2507.06067)
- **Enhancing Synthetic CT from CBCT via Multimodal Fusion: A Study on the Impact of CBCT Quality and Alignment** — _预印本 2025_ · [论文](https://arxiv.org/abs/2506.08716)
- **Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency** — _ISBI 2025_ · [论文](https://arxiv.org/abs/2411.06181)
- **Limited-Angle CBCT Reconstruction via Geometry-Integrated Cycle-domain Denoising Diffusion Probabilistic Models** — _预印本 2025_ · [论文](https://arxiv.org/abs/2506.13545)
- **Motion-Grad: A Gradient-Based Approach to Fast and Accurate Head Motion Compensation in Cone-Beam CT** — _TMI 2025_ · [论文](https://doi.org/10.1109/tmi.2024.3474250) · [代码](https://github.com/mareikethies/geometry_gradients_CT)
- **Prior-Adapted Progressive Time-Resolved CBCT Reconstruction Using a Dynamic Reconstruction and Motion Estimation Method** — _预印本 2025_ · [论文](https://arxiv.org/abs/2504.18700)
- **BaggageCT: Fan-Beam CT Reconstruction for Unaligned Sparse-View X-Ray Baggage Data** — _预印本 2024_ · [论文](https://arxiv.org/abs/2412.03036)
- **GGLF: Gradient-based geometry learning for fan-beam CT reconstruction** — _PMB 2023_ · [论文](https://doi.org/10.1088/1361-6560/acf90e)
- **DSigNet: Downsampled Imaging Geometric Modeling for Accurate CT Reconstruction via Deep Learning** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3074783) · [代码](https://github.com/hejipro/DSigNet)
- **PDF: CT Reconstruction With PDF: Parameter-Dependent Framework for Data From Multiple Geometries and Dose Levels** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3085839)
- **Artifact-resistant motion estimation with a patient-specific artifact model for motion-compensated cone-beam CT** — _Med Phys 2013_ · [论文](https://doi.org/10.1118/1.4820537)
- **A novel digital tomosynthesis (DTS) reconstruction method using a deformation field map** — _Med Phys 2008_ · [论文](https://doi.org/10.1118/1.2940725)

### 深度展开与模型驱动学习

<sub>把经典求解器展开成网络的学习型迭代方案，可带或不带数据一致性约束 · 72 篇论文</sub>

- **CG-GLORE: A Conjugate Gradient-Based Global-Local Regularization Network for Sparse-View CT Reconstruction** — _BMVC 2026_ · [论文](https://arxiv.org/abs/2608.15246)
- **Dose-Aware Cold Diffusion with Physics Consistency for Generalizable Low-Dose CT Reconstruction** — _IJCNN 2026_ · [论文](https://arxiv.org/abs/2609.18943)
- **Dual-domain U-Nets with embedded back projection operators for motion-resolved 4D CBCT reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2608.03430)
- **Efficient Unrolled Networks for Large-Scale 3D Inverse Problems** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2601.02141) · [代码](https://github.com/romainvo/efficient-unrolling)
- **GB-SVFBP: Gaussian-Based Shift-Variant FBP neural network** — _预印本 2026_ · [论文](https://arxiv.org/abs/2607.11584)
- **HARU-Net: Hybrid Attention Residual U-Net for Edge-Preserving Denoising in Cone-Beam Computed Tomography** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.22544)
- **Learning Where and What to Lift for Bi-planar X-ray-to-CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2608.17255)
- **LUCID: Learned Undersampling-Adaptive Consistency-Guided Inference with Deterministic Flow Matching for Sparse-View CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2606.16212)
- **RAM: Reconstruct Anything Model: A Lightweight General Model for Computational Imaging** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2503.08915) · [代码](https://github.com/matthieutrs/ram)
- **Toward a Foundation Plug-and-Play Prior for Computed Tomography Reconstruction via a Multimodal Diffusion Model** — _SC Workshops 2026_ · [论文](https://arxiv.org/abs/2608.23190)
- **A Learnt Half-Quadratic Splitting-Based Algorithm for Fast and High-Quality Industrial Cone-beam CT Reconstruction** — _预印本 2025_ · [论文](https://arxiv.org/abs/2501.13128)
- **CoCo-PnP: Learning Cocoercive Conservative Denoisers via Helmholtz Decomposition for Poisson Inverse Problems** — _NeurIPS 2025_ · [论文](https://arxiv.org/abs/2505.08909) · [代码](https://github.com/FizzzFizzz/CoCo-PnP)
- **Data-Efficient Limited-Angle CT Using Deep Priors and Regularization** — _预印本 2025_ · [论文](https://arxiv.org/abs/2502.12293)
- **End-to-End Deep Learning for Interior Tomography with Low-Dose X-ray CT** — _PMB 2025_ · [论文](https://arxiv.org/abs/2501.05085)
- **Equivariant Multiscale Learned Invertible Reconstruction for Cone Beam CT: From Simulated to Real Data** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.21180)
- **FIND-Net -- Fourier-Integrated Network with Dictionary Kernels for Metal Artifact Reduction** — _MICCAI 2025_ · [论文](https://arxiv.org/abs/2508.10617) · [代码](https://github.com/Farid-Tasharofi/FIND-Net)
- **GANeXt: A Fully ConvNeXt-Enhanced Generative Adversarial Network for MRI- and CBCT-to-CT Synthesis** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.19336)
- **MInDI-3D: Iterative Deep Learning in 3D for Sparse-view Cone Beam Computed Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.09616)
- **Resolution-Agnostic Neural Operators for Multi-Rate Sparse-View CT** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.12236) · [代码](https://github.com/neuraloperator/sparse_ct)
- **Semantic contrastive learning for orthogonal X-ray computed tomography reconstruction** — _Fully3D 2025_ · [论文](https://arxiv.org/abs/2512.22674)
- **EAGLE: An Edge-Aware Gradient Localization Enhanced Loss for CT Image Reconstruction** — _预印本 2024_ · [论文](https://arxiv.org/abs/2403.10695) · [代码](https://github.com/sypsyp97/Eagle_Loss)
- **Plug-and-Play Learned Proximal Trajectory for 3D Sparse-View X-Ray Computed Tomography** — _ECCV 2024_ · [论文](https://doi.org/10.1007/978-3-031-72761-0_13)
- **SOUL-Net: A Sparse and Low-Rank Unrolling Network for Spectral CT Image Reconstruction** — _TNNLS 2024_ · [论文](https://doi.org/10.1109/tnnls.2023.3319408) · [代码](https://github.com/scuchenxiang/SOUL-Net)
- **DEAR: Deep Embedding-Attention-Refinement for Sparse-View CT Reconstruction** — _TIM 2023_ · [论文](https://doi.org/10.1109/tim.2022.3221136)
- **FreeSeed: Frequency-Band-Aware and Self-Guided Network for Sparse-View CT Reconstruction** — _MICCAI 2023_ · [论文](https://doi.org/10.1007/978-3-031-43999-5_24) · [代码](https://github.com/Masaaki-75/freeseed)
- **LEARN++: Recurrent Dual-Domain Reconstruction Network for Compressed Sensing CT** — _TRPMS 2023_ · [论文](https://doi.org/10.1109/trpms.2022.3222213)
- **MDST: multi-domain sparse-view CT reconstruction based on convolution and swin transformer** — _PMB 2023_ · [论文](https://doi.org/10.1088/1361-6560/acc2ab)
- **SPIE-DIR: Self-Prior Information Enhanced Deep Iterative Reconstruction Using Two Complementary Limited-Angle Scans for DECT** — _TIM 2023_ · [论文](https://doi.org/10.1109/tim.2022.3227549)
- **ACDNet: Adaptive Convolutional Dictionary Network for CT Metal Artifact Reduction** — _IJCAI 2022_ · [论文](https://doi.org/10.24963/ijcai.2022/195) · [代码](https://github.com/hongwang01/ACDNet)
- **ACID-A: Stabilizing deep tomographic reconstruction - Part A. Hybrid framework and experimental results** — _Patterns 2022_ · [论文](https://doi.org/10.1016/j.patter.2022.100474)
- **ACID-B: Stabilizing deep tomographic reconstruction - Part B. Convergence analysis and adversarial attacks** — _Patterns 2022_ · [论文](https://doi.org/10.1016/j.patter.2022.100475)
- **DDCL: Dual domain closed-loop learning for sparse-view CT reconstruction** — _ICIFXCT 2022_ · [论文](https://doi.org/10.1117/12.2646639)
- **DIOR: Deep Iterative Optimization-Based Residual-Learning for Limited-Angle CT Reconstruction** — _TMI 2022_ · [论文](https://doi.org/10.1109/tmi.2022.3148110)
- **DREAM-Net: Deep Residual Error Iterative Minimization Network for Sparse-View CT Reconstruction** — _TMI 2022_ · [论文](https://doi.org/10.1109/jbhi.2022.3225697)
- **DuDoTrans: Dual-Domain Transformer for Sparse-View CT Reconstruction** — _MLMIR 2022_ · [论文](https://doi.org/10.1007/978-3-031-17247-2_9) · [代码](https://github.com/cewang-sysu/DuDoTrans)
- **IDOL-Net: An Interactive Dual-Domain Parallel Network for CT Metal Artifact Reduction** — _TRPMS 2022_ · [论文](https://doi.org/10.1109/trpms.2022.3171440) · [代码](https://github.com/zjk1988/IDOL-Net)
- **CasRedSCAN: Limited View Tomographic Reconstruction Using a Cascaded Residual Dense Spatial-Channel Attention Network With Projection Data Fidelity Layer** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3066318)
- **DAN-Net: Dual-Domain Adaptive-Scaling Non-Local Network for CT Metal Artifact Reduction** — _MICCAI 2021_ · [论文](https://doi.org/10.1007/978-3-030-87231-1_24) · [代码](https://github.com/zjk1988/DAN-Net)
- **DeACNN: Learning a Deep CNN Denoising Approach Using Anatomical Prior Information Implemented With Attention Mechanism for Low-Dose CT Imaging on Clinical Patient Data From Multiple Anatomical Sites** — _JBHI 2021_ · [论文](https://doi.org/10.1109/jbhi.2021.3061758)
- **DRONE: Dual-Domain Residual-Based Optimization Network for Sparse-View CT Reconstruction** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3078067) · [代码](https://github.com/weiwenwu12/DRONE)
- **DSigNet: Downsampled Imaging Geometric Modeling for Accurate CT Reconstruction via Deep Learning** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3074783) · [代码](https://github.com/hejipro/DSigNet)
- **FISTA-Net: Learning a Fast Iterative Shrinkage Thresholding Network for Inverse Problems in Imaging** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3054167) · [代码](https://github.com/jinxixiang/FISTA-Net)
- **InDuDoNet: An Interpretable Dual Domain Network for CT Metal Artifact Reduction** — _MICCAI 2021_ · [论文](https://arxiv.org/abs/2109.05298) · [代码](https://github.com/hongwang01/InDuDoNet)
- **MetaInv-Net: Meta Inversion Network for Sparse View CT Image Reconstruction** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2020.3033541) · [代码](https://github.com/haimiaozh/MetaInv-Net)
- **PDF: CT Reconstruction With PDF: Parameter-Dependent Framework for Data From Multiple Geometries and Dose Levels** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3085839)
- **SPECIAL: Single-Shot Projection Error Correction Integrated Adversarial Learning for Limited-Angle CT** — _TCI 2021_ · [论文](https://doi.org/10.1109/tci.2021.3098922)
- **Tensor-Net: Learning to Reconstruct CT Images From the VVBP-Tensor** — _TMI 2021_ · [论文](https://doi.org/10.1109/tmi.2021.3090257)
- **A review on deep learning in medical image reconstruction** — _JORSC 2020_ · [论文](https://arxiv.org/abs/1906.10643)
- **AirNet: Fused analytical and iterative reconstruction with deep neural network regularization for sparse-data CT** — _Med Phys 2020_ · [论文](https://doi.org/10.1002/mp.14170)
- **DL-InvProb: Deep Learning Techniques for Inverse Problems in Imaging** — _IEEE JSAIT 2020_ · [论文](https://arxiv.org/abs/2005.06001)
- **ETEDN: An End-to-End Deep Network for Reconstructing CT Images Directly From Sparse Sinograms** — _TCI 2020_ · [论文](https://doi.org/10.1109/tci.2020.3039385) · [代码](https://github.com/wangwei-cmd/CT-image-reconstruction)
- **HD-CNN: Artifact removal using a hybrid-domain convolutional neural network for limited-angle computed tomography imaging** — _PMB 2020_ · [论文](https://doi.org/10.1088/1361-6560/ab9066)
- **iRadonMAP: Radon Inversion via Deep Learning** — _TMI 2020_ · [论文](https://arxiv.org/abs/1808.03015)
- **Learned convex regularizers for inverse problems** — _预印本 2020_ · [论文](https://arxiv.org/abs/2008.02839)
- **Limited View Tomographic Reconstruction Using a Deep Recurrent Framework with Residual Dense Spatial-Channel Attention Network and Sinogram Consistency** — _预印本 2020_ · [论文](https://arxiv.org/abs/2009.01782)
- **Momentum-Net: Fast and convergent iterative neural network for inverse problems** — _TPAMI 2020_ · [论文](https://doi.org/10.1109/tpami.2020.3012955)
- **Multi-Scale Learned Iterative Reconstruction** — _TCI 2020_ · [论文](https://doi.org/10.1109/TCI.2020.2990299)
- **SACNN: Self-Attention Convolutional Neural Network for Low-Dose CT Denoising With Self-Supervised Perceptual Loss Network** — _TMI 2020_ · [论文](https://doi.org/10.1109/tmi.2020.2968472)
- **ADMM-based deep reconstruction for limited-angle CT** — _PMB 2019_ · [论文](https://doi.org/10.1088/1361-6560/ab1aba)
- **Convolutional Sparse Coding for Compressed Sensing CT Reconstruction** — _TMI 2019_ · [论文](https://doi.org/10.1109/tmi.2019.2906853)
- **Learning the invisible: a hybrid deep learning-shearlet framework for limited angle computed tomography** — _Inverse Problems 2019_ · [论文](https://doi.org/10.1088/1361-6420/ab10ca)
- **SISVM: Learning to Reconstruct Computed Tomography Images Directly From Sinogram Data Under A Variety of Data Acquisition Conditions** — _TMI 2019_ · [论文](https://doi.org/10.1109/tmi.2019.2910760)
- **SPSS: Sharpness preserved sinogram synthesis using convolutional neural network for sparse-view CT imaging** — _SPIE MI 2019_ · [论文](https://doi.org/10.1117/12.2512894)
- **AUTOMAP: Image reconstruction by domain-transform manifold learning** — _Nature 2018_ · [论文](https://doi.org/10.1038/nature25988)
- **CNNRPGD: CNN-Based Projected Gradient Descent for Consistent CT Image Reconstruction** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2832656)
- **DD-Net: A Sparse-View CT Reconstruction Method Based on Combination of DenseNet and Deconvolution** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2823338) · [代码](https://github.com/zzc623/DD_Net)
- **DSE: Deep Scatter Estimation (DSE): Feasibility of Using a Deep Convolutional Neural Network for Scatter Estimation in X-Ray Computed Tomography** — _SPIE MI 2018_ · [论文](https://doi.org/10.1117/12.2292919)
- **LEARN: Learned Experts’ Assessment-Based Reconstruction Network for Sparse-Data CT** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2805692)
- **LPD: Learned Primal-Dual Reconstruction** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2799231)
- **PTPN: Intelligent Parameter Tuning in Optimization-Based Iterative CT Reconstruction via Deep Reinforcement Learning** — _TMI 2018_ · [论文](https://doi.org/10.1109/tmi.2018.2823679)
- **DeepCNN: A deep convolutional neural network using directional wavelets for low‐dose X‐ray CT reconstruction** — _Med Phys 2017_ · [论文](https://arxiv.org/abs/1610.09736)
- **VISS: View-interpolation of sparsely sampled sinogram using convolutional neural network** — _SPIE MI 2017_ · [论文](https://doi.org/10.1117/12.2254244)

### 自监督与免训练方法

<sub>无需成对数据的训练——深度图像先验、noise2noise 类方法、无监督正则 · 32 篇论文</sub>

- **3D Field of Junctions: A Noise-Robust, Training-Free Structural Prior for Volumetric Inverse Problems** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2603.02149) · [代码](https://github.com/voilalab/3D-Field-of-Junctions)
- **DINR: Regularizing INR with Diffusion Prior for Self-Supervised 3D Reconstruction of Neutron Computed Tomography Data** — _ICASSP 2026_ · [论文](https://arxiv.org/abs/2603.10947)
- **Equivariance2Inverse: A Practical Self-Supervised CT Reconstruction Method Benchmarked on Real, Limited-Angle, and Blurred Data** — _TCI 2026_ · [论文](https://arxiv.org/abs/2510.23317)
- **From Sparse X-rays to 3D CT: Training-Free Reconstruction with Diffusion Priors** — _DGM4MICCAI 2026_ · [论文](https://arxiv.org/abs/2606.20763) · [代码](https://github.com/Fredy-Zhang/TF-PRDiT)
- **HorusEye: a self-supervised foundation model for generalizable X-ray tomography restoration** — _Nat Comput Sci 2026_ · [论文](https://doi.org/10.1038/s43588-026-00973-3)
- **MedGMAE: Gaussian Masked Autoencoders for Medical Volumetric Representation Learning** — _ICLR 2026_ · [论文](https://openreview.net/forum?id=Z2XIRLv535) · [代码](https://github.com/windrise/MedGMAE)
- **NGPS: Structure-Preserving Self-Supervised Denoising via Neighbor-Guided Patch Sampling** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2606.23200) · [代码](https://github.com/cv-cho/NGPS)
- **Unsupervised Metal Artifact Reduction in Dental CBCT using Fine-tuned Cycle-Consistent Adversarial Networks** — _Digital 2026_ · [论文](https://arxiv.org/abs/2607.20977)
- **An unsupervised sparse-view CT reconstruction framework using combination of iterative deep image prior and ADMM** — _Med Phys 2025_ · [论文](https://doi.org/10.1002/mp.17933)
- **Limited-angle SPECT image reconstruction using deep image prior** — _PMB 2025_ · [论文](https://arxiv.org/abs/2503.18342)
- **Spener: Unsupervised Self-Prior Embedding Neural Representation for Sparse-View CT Reconstruction** — _AAAI 2025_ · [论文](https://doi.org/10.1609/aaai.v39i7.32794) · [代码](https://github.com/MeijiTian/Spener)
- **Zero-shot CT Super-Resolution using Diffusion-based 2D Projection Priors and Signed 3D Gaussians** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.15151)
- **Zero-Shot Low-dose CT Denoising via Sinogram Flicking** — _预印本 2025_ · [论文](https://arxiv.org/abs/2504.07927)
- **DuDoDp-MAR: Unsupervised CT Metal Artifact Reduction by Plugging Diffusion Priors in Dual Domains** — _TMI 2024_ · [论文](https://doi.org/10.1109/tmi.2024.3351201) · [代码](https://github.com/DeepXuan/DuDoDp-MAR)
- **RBP-DIP: Residual back projection with deep image prior for ill-posed CT reconstruction** — _Neural Netw. 2024_ · [论文](https://doi.org/10.1016/j.neunet.2024.106740)
- **PINER: Prior-Informed Implicit Neural Representation Learning for Test-Time Adaptation in Sparse-View CT Reconstruction** — _WACV 2023_ · [论文](https://doi.org/10.1109/wacv56688.2023.00197) · [代码](https://github.com/efzero/PINER)
- **Polyner: Unsupervised Polychromatic Neural Representation for CT Metal Artifact Reduction** — _NeurIPS 2023_ · [论文](https://arxiv.org/abs/2306.15203) · [代码](https://github.com/iwuqing/Polyner)
- **SemiMAR: Semi-Supervised Learning for CT Metal Artifact Reduction** — _JBHI 2023_ · [论文](https://doi.org/10.1109/jbhi.2023.3312292) · [代码](https://github.com/zjk1988/SemiMAR)
- **ACID-A: Stabilizing deep tomographic reconstruction - Part A. Hybrid framework and experimental results** — _Patterns 2022_ · [论文](https://doi.org/10.1016/j.patter.2022.100474)
- **ACID-B: Stabilizing deep tomographic reconstruction - Part B. Convergence analysis and adversarial attacks** — _Patterns 2022_ · [论文](https://doi.org/10.1016/j.patter.2022.100475)
- **An Educated Warm Start for Deep Image Prior-Based Micro CT Reconstruction** — _TCI 2022_ · [论文](https://doi.org/10.1109/tci.2022.3233188)
- **DFDLM: A Dataset-free Deep Learning Method for Low-Dose CT Image Reconstruction** — _Inverse Problems 2022_ · [论文](https://arxiv.org/abs/2205.00463)
- **DGR-2: An Unsupervised Reconstruction Method For Low-Dose CT Using Deep Generative Regularization Prior** — _BSPC 2022_ · [论文](https://arxiv.org/abs/2012.06448) · [代码](https://github.com/mozanunal/SparseCT)
- **GMM-unNet: Noise Characteristics Modeled Unsupervised Network for Robust CT Image Reconstruction** — _TMI 2022_ · [论文](https://doi.org/10.1109/tmi.2022.3197400)
- **UNDIP: Sparse-view and limited-angle CT reconstruction with untrained networks and deep image prior** — _CMPB 2022_ · [论文](https://doi.org/10.1016/j.cmpb.2022.107167)
- **IntraTomo: Self-supervised Learning-based Tomography via Sinogram Synthesis and Prediction** — _ICCV 2021_ · [论文](https://doi.org/10.1109/iccv48922.2021.00197) · [代码](https://github.com/vccimaging/IntraTomo)
- **N2S: Self-Supervised Training For Low-Dose Ct Reconstruction** — _ISBI 2021_ · [论文](https://doi.org/10.1109/isbi48211.2021.9433944)
- **SinoNet: Noise-Generating-Mechanism-Driven Unsupervised Learning for Low-Dose CT Sinogram Recovery** — _TRPMS 2021_ · [论文](https://doi.org/10.1109/trpms.2021.3083361)
- **SUPER: Unified Supervised-Unsupervised (SUPER) Learning for X-ray CT Image Reconstruction** — _TMI 2021_ · [论文](https://arxiv.org/abs/2010.02761)
- **DIP: Computed Tomography Reconstruction Using Deep Image Prior and Learned Reconstruction Methods** — _Inverse Problems 2020_ · [论文](https://doi.org/10.1088/1361-6420/aba415) · [代码](https://github.com/oterobaguer/dip-ct-benchmark)
- **SACNN: Self-Attention Convolutional Neural Network for Low-Dose CT Denoising With Self-Supervised Perceptual Loss Network** — _TMI 2020_ · [论文](https://doi.org/10.1109/tmi.2020.2968472)
- **SUPER-2: SUPER Learning: A Supervised-Unsupervised Framework for Low-Dose CT Image Reconstruction** — _ICCVW 2019_ · [论文](https://doi.org/10.1109/iccvw.2019.00490)

### 扩散与生成式先验

<sub>把分数模型与扩散模型用作层析反演的先验或采样器 · 56 篇论文</sub>

- **Anatomy-preserving unpaired cone-beam CT refinement for image-guided radiotherapy using pseudo-label guided diffusion** — _预印本 2026_ · [论文](https://arxiv.org/abs/2610.06094)
- **CBCT-Based Synthetic CT Generation Using Conditional Flow Matching Model** — _预印本 2026_ · [论文](https://arxiv.org/abs/2603.05796)
- **Conditional Diffusion for 3D CT Volume Reconstruction from 2D X-rays** — _BMVC 2026_ · [论文](https://arxiv.org/abs/2603.26509) · [代码](https://github.com/ai-med/AXON/)
- **Conditional Diffusion Posterior Alignment for Sparse-View CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2604.21960)
- **Cone-Beam CT Image Quality Enhancement Using A Latent Diffusion Model Trained with Simulated CBCT Artifacts** — _预印本 2026_ · [论文](https://arxiv.org/abs/2603.26014)
- **Continuity-driven Synergistic Diffusion with Neural Priors for Ultra-Sparse-View CBCT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.07980)
- **Cross-Distribution Diffusion Priors-Driven Iterative Reconstruction for Sparse-View CT** — _TMI 2026_ · [论文](https://arxiv.org/abs/2509.13576)
- **Cross-Modal Guidance for Fast Diffusion-Based Computed Tomography** — _ICASSP 2026_ · [论文](https://arxiv.org/abs/2603.01253)
- **DiffNR: Diffusion-Enhanced Neural Representation Optimization for Sparse-View 3D Tomographic Reconstruction** — _AAAI 2026_ · [论文](https://arxiv.org/abs/2604.21518) · [项目页](https://ooonesevennn.github.io/DiffNR/)
- **DINR: Regularizing INR with Diffusion Prior for Self-Supervised 3D Reconstruction of Neutron Computed Tomography Data** — _ICASSP 2026_ · [论文](https://arxiv.org/abs/2603.10947)
- **DM4CT: Benchmarking Diffusion Models for CT Reconstruction** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2602.18589) · [代码](https://github.com/DM4CT/DM4CT)
- **Dose-Aware Cold Diffusion with Physics Consistency for Generalizable Low-Dose CT Reconstruction** — _IJCNN 2026_ · [论文](https://arxiv.org/abs/2609.18943)
- **Field-of-View Extension in Dental Cone-Beam CT via Implicit Neural Representations and Diffusion Model-Based Refinement** — _MICAD 2026_ · [论文](https://arxiv.org/abs/2609.28110) · [代码](https://github.com/SusanneSchaub/CBCT-FOV-Extension)
- **Foundation-VAE: Foundation VAEs for 3D CT Reconstruction, Augmentation, and Generation** — _ICML 2026_ · [论文](https://arxiv.org/abs/2605.30893) · [代码](https://github.com/qic999/Foundation-VAE)
- **From Sparse X-rays to 3D CT: Training-Free Reconstruction with Diffusion Priors** — _DGM4MICCAI 2026_ · [论文](https://arxiv.org/abs/2606.20763) · [代码](https://github.com/Fredy-Zhang/TF-PRDiT)
- **Geometry-Aware Diffusion Approximate Posterior Sampling for Sparse-View and Limited-Angle CT** — _预印本 2026_ · [论文](https://arxiv.org/abs/2610.08866)
- **ISCS: Improving 2D Diffusion Models for 3D Medical Imaging with Inter-Slice Consistent Stochasticity** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2602.04162) · [代码](https://github.com/duchenhe/ISCS)
- **KLIP: Localized Distribution Shift Detection via KL-Divergence with Diffusion Priors in Inverse Problems** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2605.31596) · [代码](https://github.com/voilalab/KLIP)
- **LUCID: Learned Undersampling-Adaptive Consistency-Guided Inference with Deterministic Flow Matching for Sparse-View CT Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2606.16212)
- **Plug-and-Play Diffusion Meets ADMM: Dual-Variable Coupling for Robust Medical Image Reconstruction** — _ICML 2026_ · [论文](https://arxiv.org/abs/2602.23214) · [代码](https://github.com/duchenhe/DC-PnPDP)
- **Spectral Consistent Flow for One-Step 3D Medical Image Translation** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2607.10627)
- **Toward a Foundation Plug-and-Play Prior for Computed Tomography Reconstruction via a Multimodal Diffusion Model** — _SC Workshops 2026_ · [论文](https://arxiv.org/abs/2608.23190)
- **Toward CT-Equivalent Image Quality in Low-Dose Radiotherapy Planning: Conditional Diffusion-Based CBCT-to-CT Synthesis and the Impact of CBCT Input Representation** — _预印本 2026_ · [论文](https://arxiv.org/abs/2608.08919)
- **Towards reconstructing experimental sparse-view X-ray CT data with diffusion models** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.12755)
- **3D CBCT Artefact Removal Using Perpendicular Score-Based Diffusion Models** — _DGM4MICCAI 2025_ · [论文](https://arxiv.org/abs/2603.06300)
- **Adaptive Diffusion Models for Sparse-View Motion-Corrected Head Cone-beam CT** — _TRPMS 2025_ · [论文](https://arxiv.org/abs/2504.14033) · [项目页](https://antoinedepaepe.github.io/jrm-adm-io/)
- **Advancing Limited-Angle CT Reconstruction Through Diffusion-Based Sinogram Completion** — _ICIP 2025_ · [论文](https://arxiv.org/abs/2505.19385)
- **Bigger Isn't Always Better: Towards a General Prior for Medical Image Reconstruction** — _GCPR 2025_ · [论文](https://arxiv.org/abs/2501.07376) · [代码](https://github.com/VLOGroup/bigger-isnt-always-better)
- **CvG-Diff: Cross-View Generalized Diffusion Model for Sparse-View CT Reconstruction** — _MICCAI 2025_ · [论文](https://doi.org/10.1007/978-3-032-05325-1_14) · [代码](https://github.com/xmed-lab/CvG-Diff)
- **DiffNAF: Iterative Diffusion-Refined Neural Attenuation Fields for Multi-Source Stationary Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2511.14310)
- **Diffusion-Based Limited-Angle CT Reconstruction under Noisy Conditions** — _ICIP 2025_ · [论文](https://arxiv.org/abs/2507.05647)
- **DVG-Diffusion: Dual-View Guided Diffusion Model for CT Reconstruction from X-Rays** — _预印本 2025_ · [论文](https://arxiv.org/abs/2503.17804)
- **Equivariant Conditional Diffusion Model for Head and Neck CT Image Synthesis from CBCT** — _Med Phys 2025_ · [论文](https://arxiv.org/abs/2509.21913)
- **GANeXt: A Fully ConvNeXt-Enhanced Generative Adversarial Network for MRI- and CBCT-to-CT Synthesis** — _预印本 2025_ · [论文](https://arxiv.org/abs/2512.19336)
- **Limited-Angle CBCT Reconstruction via Geometry-Integrated Cycle-domain Denoising Diffusion Probabilistic Models** — _预印本 2025_ · [论文](https://arxiv.org/abs/2506.13545)
- **Mitigating Data Consistency Induced Discrepancy in Cascaded Diffusion Models for Sparse-View CT Reconstruction** — _TMI 2025_ · [论文](https://doi.org/10.1109/tmi.2025.3557243)
- **Noise-Inspired Diffusion Model for Generalizable Low-Dose CT Reconstruction** — _Med Image Anal 2025_ · [论文](https://arxiv.org/abs/2506.22012) · [代码](https://github.com/qgao21/NEED)
- **Ordered-subsets Multi-diffusion Model for Sparse-view CT Reconstruction** — _预印本 2025_ · [论文](https://arxiv.org/abs/2505.09985)
- **Projection Embedded Diffusion Bridge for CT Reconstruction from Incomplete Data** — _预印本 2025_ · [论文](https://arxiv.org/abs/2510.22605)
- **SDB: System-Embedded Diffusion Bridge Models** — _NeurIPS 2025_ · [论文](https://arxiv.org/abs/2506.23726) · [代码](https://github.com/sobieskibj/sdb)
- **Steerable Conditional Diffusion for Out-of-Distribution Adaptation in Medical Image Reconstruction** — _TMI 2025_ · [论文](https://doi.org/10.1109/tmi.2024.3524797)
- **When are Diffusion Priors Helpful in Sparse Reconstruction? A Study with Sparse-view CT** — _ISBI 2025_ · [论文](https://arxiv.org/abs/2502.02771)
- **Zero-shot CT Super-Resolution using Diffusion-based 2D Projection Priors and Signed 3D Gaussians** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.15151)
- **DiffRecon: Diffusion Models for Medical Image Reconstruction** — _BJR|AI 2024_ · [论文](https://doi.org/10.1093/bjrai/ubae013)
- **DuDoDp-MAR: Unsupervised CT Metal Artifact Reduction by Plugging Diffusion Priors in Dual Domains** — _TMI 2024_ · [论文](https://doi.org/10.1109/tmi.2024.3351201) · [代码](https://github.com/DeepXuan/DuDoDp-MAR)
- **Generative Modeling in Sinogram Domain for Sparse-view CT Reconstruction** — _TRPMS 2024_ · [论文](https://arxiv.org/abs/2211.13926)
- **SWORD: Stage-by-Stage Wavelet Optimization Refinement Diffusion Model for Sparse-View CT Reconstruction** — _TMI 2024_ · [论文](https://doi.org/10.1109/tmi.2024.3355455) · [代码](https://github.com/yqx7150/SWORD)
- **Two-View Industrial CT Reconstruction Based on a Multiscale Conditional Latent Diffusion Network** — _TIM 2024_ · [论文](https://doi.org/10.1109/TIM.2024.3476543)
- **Wavelet-Improved Score-Based Generative Model for Medical Imaging** — _TMI 2024_ · [论文](https://doi.org/10.1109/tmi.2023.3325824)
- **3DIP: Solving 3D Inverse Problems Using Pre-Trained 2D Diffusion Models** — _CVPR 2023_ · [论文](https://doi.org/10.1109/cvpr52729.2023.02159)
- **DDDM: Dual-Domain Diffusion Model for Sparse-View CT Reconstruction** — _预印本 2023_ · [论文](https://doi.org/10.36227/techrxiv.23726703) · [代码](https://github.com/YC-Markus/code-for-DDDM)
- **Dolce: A Model-Based Probabilistic Diffusion Framework for Limited-Angle CT Reconstruction** — _ICCV 2023_ · [论文](https://doi.org/10.1109/ICCV51070.2023.00963)
- **CoCoDiff: A Contextual Conditional Diffusion Model for Low-dose CT Image Denoising** — _SPIE DXRT 2022_ · [论文](https://doi.org/10.1117/12.2634939)
- **DiffMed: Diffusion Models for Medical Image Analysis: A Comprehensive Survey** — _预印本 2022_ · [论文](https://arxiv.org/abs/2211.07804)
- **EASEL: Iterative Reconstruction for Low-Dose CT using Deep Gradient Priors of Generative Model** — _TRPMS 2022_ · [论文](https://doi.org/10.1109/trpms.2022.3148373) · [代码](https://github.com/yqx7150/EASEL)
- **Low-Dose CT Using Denoising Diffusion Probabilistic Model for 20× Speedup** — _预印本 2022_ · [论文](https://arxiv.org/abs/2209.15136)

### 隐式神经表示

<sub>用坐标网络（INR / NeRF）直接表示待求的体数据本身 · 24 篇论文</sub>

- **DiffNR: Diffusion-Enhanced Neural Representation Optimization for Sparse-View 3D Tomographic Reconstruction** — _AAAI 2026_ · [论文](https://arxiv.org/abs/2604.21518) · [项目页](https://ooonesevennn.github.io/DiffNR/)
- **DINR: Regularizing INR with Diffusion Prior for Self-Supervised 3D Reconstruction of Neutron Computed Tomography Data** — _ICASSP 2026_ · [论文](https://arxiv.org/abs/2603.10947)
- **Dynamic Black-hole Emission Tomography with Physics-Informed Neural Fields** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2602.08029)
- **Field-of-View Extension in Dental Cone-Beam CT via Implicit Neural Representations and Diffusion Model-Based Refinement** — _MICAD 2026_ · [论文](https://arxiv.org/abs/2609.28110) · [代码](https://github.com/SusanneSchaub/CBCT-FOV-Extension)
- **GH-NAF: Grid-Adaptive Hash-Level-Attended Neural Attenuation Fields for Discrepancy-Aware CBCT** — _CVPR 2026_ · [论文](https://openaccess.thecvf.com/content/CVPR2026/html/Oh_GH-NAF_Grid-Adaptive_Hash-Level-Attended_Neural_Attenuation_Fields_for_Discrepancy-Aware_CBCT_CVPR_2026_paper.html) · [代码](https://github.com/seongje-oh/GH-NAF)
- **NAB: Neural Adaptive Binning for Sparse-View CT Reconstruction** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2602.02356) · [代码](https://github.com/Wangduo-Xie/NAB_CT_reconstruction)
- **Texture-preserving implicit neural representation for Cone beam CT truncated reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2606.06039)
- **Accelerated Optimization of Implicit Neural Representations for CT Reconstruction** — _预印本 2025_ · [论文](https://arxiv.org/abs/2504.13390)
- **Coordinate-Based Speed of Sound Recovery for Aberration-Corrected Photoacoustic Computed Tomography** — _ICCV 2025_ · [论文](https://arxiv.org/abs/2409.10876) · [项目页](https://lukeli0425.github.io/Coord-SoS-PACT/)
- **DiffNAF: Iterative Diffusion-Refined Neural Attenuation Fields for Multi-Source Stationary Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2511.14310)
- **Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency** — _ISBI 2025_ · [论文](https://arxiv.org/abs/2411.06181)
- **Nonperiodic dynamic CT reconstruction using backward-warping INR with regularization of diffeomorphism (BIRD)** — _预印本 2025_ · [论文](https://arxiv.org/abs/2505.03463)
- **Recover Biological Structure from Sparse-View Diffraction Images with Neural Volumetric Prior** — _ICCV 2025_ · [论文](https://arxiv.org/abs/2510.16391)
- **Spener: Unsupervised Self-Prior Embedding Neural Representation for Sparse-View CT Reconstruction** — _AAAI 2025_ · [论文](https://doi.org/10.1609/aaai.v39i7.32794) · [代码](https://github.com/MeijiTian/Spener)
- **INCODE: Implicit Neural Conditioning with Prior Knowledge Embeddings** — _WACV 2024_ · [论文](https://doi.org/10.1109/wacv57701.2024.00133) · [代码](https://github.com/xmindflow/INCODE)
- **INR-Joint: Implicit Neural Representations for Robust Joint Sparse-View CT Reconstruction** — _TMLR 2024_ · [论文](https://arxiv.org/abs/2405.02509) · [代码](https://github.com/jiayangshi/INR4JointCTRecon)
- **Neural Field Regularization by Denoising for 3D Sparse-View X-Ray Computed Tomography** — _3DV 2024_ · [论文](https://doi.org/10.1109/3dv62453.2024.00094)
- **SAX-NeRF: Structure-Aware Sparse-View X-Ray 3D Reconstruction** — _CVPR 2024_ · [论文](https://doi.org/10.1109/cvpr52733.2024.01062) · [代码](https://github.com/caiyuanhao1998/SAX-NeRF)
- **PINER: Prior-Informed Implicit Neural Representation Learning for Test-Time Adaptation in Sparse-View CT Reconstruction** — _WACV 2023_ · [论文](https://doi.org/10.1109/wacv56688.2023.00197) · [代码](https://github.com/efzero/PINER)
- **Polyner: Unsupervised Polychromatic Neural Representation for CT Metal Artifact Reduction** — _NeurIPS 2023_ · [论文](https://arxiv.org/abs/2306.15203) · [代码](https://github.com/iwuqing/Polyner)
- **NAF: Neural Attenuation Fields for Sparse-View CBCT Reconstruction** — _MICCAI 2022_ · [论文](https://arxiv.org/abs/2209.14540) · [代码](https://github.com/Ruyi-Zha/naf_cbct)
- **SNAF: Sparse-View CBCT Reconstruction with Neural Attenuation Fields** — _预印本 2022_ · [论文](https://arxiv.org/abs/2211.17048)
- **UncertaINR: Uncertainty Quantification of End-to-End Implicit Neural Representations for Computed Tomography** — _预印本 2022_ · [论文](https://arxiv.org/abs/2202.10847)
- **DCTR: Dynamic CT Reconstruction From Limited Views With Implicit Neural Representations** — _ICCV 2021_ · [论文](https://doi.org/10.1109/iccv48922.2021.00226)

### 高斯溅射

<sub>以显式高斯基元作为可微的层析表示 · 25 篇论文</sub>

- **Active View Selection with Perturbed Gaussian Ensemble for Tomographic Reconstruction** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2603.06852)
- **Exact-GS: Mathematically Rigorous and Accurate 3D Gaussian Splatting for 3D X-Ray Reconstruction** — _CVPR 2026_ · [论文](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Exact-GS_Mathematically_Rigorous_and_Accurate_3D_Gaussian_Splatting_for_3D_CVPR_2026_paper.html) · [代码](https://github.com/brucee1323/Exact-GS)
- **FaCT-GS: Fast and Scalable CT Reconstruction with Gaussian Splatting** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2604.01844) · [代码](https://github.com/PaPieta/fact-gs)
- **GB-SVFBP: Gaussian-Based Shift-Variant FBP neural network** — _预印本 2026_ · [论文](https://arxiv.org/abs/2607.11584)
- **GR-Gaussian: Graph-Based Radiative Gaussian Splatting for Sparse-View Tomography** — _TCI 2026_ · [论文](https://doi.org/10.1109/TCI.2026.3701585)
- **MedGMAE: Gaussian Masked Autoencoders for Medical Volumetric Representation Learning** — _ICLR 2026_ · [论文](https://openreview.net/forum?id=Z2XIRLv535) · [代码](https://github.com/windrise/MedGMAE)
- **Projection-Volume Fidelity Divergence: Diagnosing and Controlling Optimization Drift in Sparse-View 3D Gaussian Tomography** — _预印本 2026_ · [论文](https://arxiv.org/abs/2606.22525)
- **Radioactive 3D Gaussian Ray Tracing for Tomographic Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2602.01057)
- **Revisiting Pose Sensitivity in Splat-based Computed Tomography under Sparse-view Reconstruction** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2608.04752)
- **Shape-guided Gaussian Splatting for Sparse-View X-ray 3D Reconstruction** — _预印本 2026_ · [论文](https://arxiv.org/abs/2609.10376) · [代码](https://github.com/polyshape-lab/ShapeGuidedGaussian)
- **Splat-Based Metal Artifact Reduction in Cone-Beam CT via Compact Attenuation Modeling** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2608.04764)
- **Splat-based Metal Artifact Reduction in Cone-Beam CT via Polychromatic Modeling** — _CGF 2026_ · [论文](https://arxiv.org/abs/2608.13159)
- **TG-Field: Geometry-Aware Radiative Gaussian Fields for Tomographic Reconstruction** — _AAAI 2026_ · [论文](https://arxiv.org/abs/2602.11705)
- **4DGS-4DCBCT: Spatiotemporal Gaussian Optimization for 4D Cone Beam CT Reconstruction from Sparsely Sampled Projections** — _预印本 2025_ · [论文](https://arxiv.org/abs/2501.04140) · [代码](https://github.com/fuyabo/4DGS_for_4DCBCT)
- **DGR: Discretized Gaussian Representation for Tomographic Reconstruction** — _ICCV 2025_ · [论文](https://doi.org/10.1109/iccv51701.2025.02325) · [代码](https://github.com/wskingdom/DGR)
- **DIGS: Dynamic CBCT Reconstruction using Deformation-Informed 4D Gaussian Splatting and a Low-Rank Free-Form Deformation Model** — _MICCAI 2025_ · [论文](https://arxiv.org/abs/2506.22280) · [代码](https://github.com/Yuliang-Huang/DIGS)
- **InsideOut: Integrated RGB-Radiative Gaussian Splatting for Comprehensive 3D Object Representation** — _ICCV 2025_ · [论文](https://arxiv.org/abs/2510.17864)
- **Time-resolved dynamic CBCT reconstruction using prior-model-free spatiotemporal Gaussian representation (PMF-STGR)** — _预印本 2025_ · [论文](https://arxiv.org/abs/2503.22139)
- **Vol3DGS: Volumetrically Consistent 3D Gaussian Rasterization** — _CVPR 2025_ · [论文](https://arxiv.org/abs/2412.03378) · [代码](https://github.com/chinmay0301ucsd/Vol3DGS)
- **X-GRM: Large Gaussian Reconstruction Model for Sparse-view X-rays to Computed Tomography** — _预印本 2025_ · [论文](https://arxiv.org/abs/2505.15235) · [代码](https://github.com/CUHK-AIM-Group/X-GRM)
- **X2-Gaussian: 4D Radiative Gaussian Splatting for Continuous-Time Tomographic Reconstruction** — _ICCV 2025_ · [论文](https://doi.org/10.1109/iccv51701.2025.02293) · [代码](https://github.com/yuyouxixi/x2-gaussian)
- **Zero-shot CT Super-Resolution using Diffusion-based 2D Projection Priors and Signed 3D Gaussians** — _预印本 2025_ · [论文](https://arxiv.org/abs/2508.15151)
- **DIF-Gaussian: Learning 3D Gaussians for Extremely Sparse-View Cone-Beam CT Reconstruction** — _MICCAI 2024_ · [论文](https://doi.org/10.1007/978-3-031-72104-5_41) · [代码](https://github.com/xmed-lab/DIF-Gaussian)
- **R2-Gaussian: Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction** — _NeurIPS 2024_ · [论文](https://arxiv.org/abs/2405.20693) · [代码](https://github.com/Ruyi-Zha/r2_gaussian)
- **X-Gaussian: Radiative Gaussian Splatting for Efficient X-Ray Novel View Synthesis** — _ECCV 2024_ · [论文](https://arxiv.org/abs/2403.04116) · [代码](https://github.com/caiyuanhao1998/X-Gaussian)

### 其他主题

<sub>工业无损检测、相位衬度、定量 CT、重建软件，以及不属于以上各类的工作 · 28 篇论文</sub>

- **At FullTilt: Real-Time Open-Set 3D Macromolecule Detection Directly from Tilted 2D Projections** — _NeurIPS 2026_ · [论文](https://arxiv.org/abs/2604.10766)
- **CryoDeRec: A Supervised Multi-task Framework for Joint cryo-ET Restoration Enabled by Generative Physical Simulation** — _CVPR 2026_ · [论文](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_A_Supervised_Multi-task_Framework_for_Joint_cryo-ET_Restoration_Enabled_by_CVPR_2026_paper.html) · [代码](https://github.com/ZhidongYang/CryoDeRec)
- **Dynamic Black-hole Emission Tomography with Physics-Informed Neural Fields** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2602.08029)
- **Event-Based Sparse-View Background-Oriented Schlieren Tomography** — _ECCV 2026_ · [论文](https://doi.org/10.1007/978-3-032-37335-9_18)
- **High-Precision Image Reconstruction for Binary-Valued X-Ray CT From Limited-View Projections** — _TIM 2026_ · [论文](https://doi.org/10.1109/tim.2026.3670565)
- **HorusEye: a self-supervised foundation model for generalizable X-ray tomography restoration** — _Nat Comput Sci 2026_ · [论文](https://doi.org/10.1038/s43588-026-00973-3)
- **Neuromorphic X-Ray Computed Tomography** — _ECCV 2026_ · [论文](https://doi.org/10.1007/978-3-032-37577-3_8) · [项目页](https://wanghongjian98.github.io/projects/neuroxct/)
- **OpenPros: A Large-Scale Dataset for Limited View Prostate Ultrasound Computed Tomography** — _ICLR 2026_ · [论文](https://arxiv.org/abs/2505.12261) · [项目页](https://open-pros.github.io/)
- **VoDaSuRe: A Large-Scale Dataset Revealing Domain Shift in Volumetric Super-Resolution** — _CVPR 2026_ · [论文](https://arxiv.org/abs/2603.23153) · [项目页](https://augusthoeg.github.io/VoDaSuRe/)
- **XDen-1K: A Density Field Dataset of Real-World Objects** — _ECCV 2026_ · [论文](https://arxiv.org/abs/2512.10668)
- **Coordinate-Based Speed of Sound Recovery for Aberration-Corrected Photoacoustic Computed Tomography** — _ICCV 2025_ · [论文](https://arxiv.org/abs/2409.10876) · [项目页](https://lukeli0425.github.io/Coord-SoS-PACT/)
- **Investigating the effects of machine learning generalization for enhancing accuracy in fast X-ray computed tomography for industrial metrology** — _CIRP Annals 2025_ · [论文](https://doi.org/10.1016/j.cirp.2025.04.025)
- **Limited-angle x-ray nano-tomography with machine-learning enabled iterative reconstruction engine** — _npj Comput Mater 2025_ · [论文](https://doi.org/10.1038/s41524-025-01724-0)
- **Modeling X-Ray Photon Pile-Up with a Normalizing Flow** — _NeurIPS Workshop 2025_ · [论文](https://arxiv.org/abs/2511.11863)
- **MONSTR: Model-Oriented Neutron Strain Tomographic Reconstruction** — _预印本 2025_ · [论文](https://arxiv.org/abs/2505.22187)
- **Recover Biological Structure from Sparse-View Diffraction Images with Neural Volumetric Prior** — _ICCV 2025_ · [论文](https://arxiv.org/abs/2510.16391)
- **How auto-differentiation can improve CT workflows: classical algorithms in a modern framework** — _Opt. Express 2024_ · [论文](https://doi.org/10.1364/oe.502920)
- **Machine learning based sinogram interpolation for X-ray computed tomography validated on experimental data** — _Precis. Eng. 2024_ · [论文](https://doi.org/10.1016/j.precisioneng.2024.02.020)
- **Machine learning in industrial X-ray computed tomography - a review** — _CIRP JMST 2024_ · [论文](https://doi.org/10.1016/j.cirpj.2024.05.004)
- **Two-View Industrial CT Reconstruction Based on a Multiscale Conditional Latent Diffusion Network** — _TIM 2024_ · [论文](https://doi.org/10.1109/TIM.2024.3476543)
- **Fast algorithms based on Empirical Interpolation Methods for selecting best projections in Sparse-View X-ray Computed Tomography using a priori information** — _NDT&E Int. 2023_ · [论文](https://doi.org/10.1016/j.ndteint.2022.102768)
- **The realisation of fast X-ray computed tomography using a limited number of projection images for dimensional metrology** — _NDT&E Int. 2023_ · [论文](https://doi.org/10.1016/j.ndteint.2023.102852)
- **Review of high energy x-ray computed tomography for non-destructive dimensional metrology of large metallic advanced manufactured components** — _RoPP 2022_ · [论文](https://doi.org/10.1088/1361-6633/ac43f6)
- **Laminography in the lab: imaging planar objects using a conventional x-ray CT scanner** — _Meas. Sci. Technol. 2019_ · [论文](https://doi.org/10.1088/1361-6501/aafcae)
- **Coded aperture optimization in compressive X-ray tomography: a gradient descent approach** — _Opt. Express 2017_ · [论文](https://doi.org/10.1364/oe.25.023833)
- **Sparse-view computed laminography with a spherical sinusoidal scan for nondestructive testing** — _Opt. Express 2014_ · [论文](https://doi.org/10.1364/oe.22.017745)
- **Comparison of image quality in computed laminography and tomography** — _Opt. Express 2012_ · [论文](https://doi.org/10.1364/oe.20.000794)
- **X-ray cargo container inspection system with few-view projection imaging** — _NIMA 2009_ · [论文](https://doi.org/10.1016/j.nima.2008.08.151)

<div align="right"><a href="#top">回到顶部 ↑</a></div>

## 工具包与库

| 工具包 | 语言 | Star | Description |
| --- | --- | --- | --- |
| [**MONAI**](https://github.com/Project-MONAI/MONAI) | Python | 8760 | 基于 PyTorch 的医学影像框架，提供 CT 重建相关的变换与预训练模型。 |
| [**3D Slicer**](https://github.com/Slicer/Slicer) | C++ | 2652 | 医学影像计算领域最主要的开源平台；用于查看、分割与配准 CT 体数据，也可以以扩展模块的形式搭建重建流程原型。 |
| [**pydicom**](https://github.com/pydicom/pydicom) | Python | 2219 | 读写 DICOM 文件——处理临床 CT 数据的标准入口。 |
| [**DeepInverse**](https://github.com/deepinv/deepinv) | Python | 827 | 面向成像逆问题的 PyTorch 库——物理算子、学习型去噪器、展开网络与基准测试。 |
| [**TIGRE**](https://github.com/CERN/TIGRE) | MATLAB / Python | 812 | GPU 加速（CUDA）的锥束与平行束 CT 工具箱；提供 FDK、SART、SIRT、CGLS 及 TV 变体。 |
| [**ASTRA Toolbox**](https://github.com/astra-toolbox/astra-toolbox) | C++ / Python / MATLAB | 637 | 历史悠久的研究型工具箱，投影算子与算法覆盖面很广；CPU/GPU 上的参照基线。 |
| [**PyLops**](https://github.com/equinor/pylops) | Python | 540 | 线性算子库，含 Radon 变换与一整套求解器（CGLS、LSQR、TV、稀疏性促进）。不想自己写无矩阵算子时，做变分 CT 原型最干净的选择。 |
| [**ODL**](https://github.com/odlgroup/odl) | Python | 434 | 算子离散化库——以泛函分析的框架组织逆问题，内置 CT 几何。 |
| [**TomoPy**](https://github.com/tomopy/tomopy) | Python | 397 | 同步辐射显微/纳米层析的参照工具箱；gridrec、FBP 与相位恢复。 |
| [**tomviz**](https://github.com/OpenChemistry/tomviz) | C++ | 367 | 跨平台应用层析数据可视化与处理。 |
| [**sigpy**](https://github.com/mikgroup/sigpy) | Python | 339 | 面向迭代图像重建的信号处理包；近端算子与 NUFFT/Radon 原语。 |
| [**voxenra**](https://github.com/l5769389/voxenra) | Python | 299 | 跨平台的 CT/MRI/PET-CT DICOM 阅片器，支持多平面重组、三维体绘制与融合——用来快速目检重建结果很顺手。 |
| [**RTK**](https://github.com/RTKConsortium/RTK) | C++ | 298 | 构建在 ITK 之上的重建工具包；在临床 CBCT 与介入研究中广泛使用。 |
| [**torch-radon**](https://github.com/matteo-ronchetti/torch-radon) | Python | 280 | PyTorch 中的可微分 Radon 变换与滤波反投影。 |
| [**LEAP**](https://github.com/llnl/LEAP) | CUDA / Python | 254 | LLNL 的 Livermore 能耗感知处理器，面向三维透射 CT；达到生产级水准的基于模型的重建。 |
| [**RadIO**](https://github.com/analysiscenter/radio) | Python | 227 | 精简易读的 Python 包，实现 Radon 变换与 FBP。 |
| [**PyTomography**](https://github.com/PyTomography/PyTomography) | Python | 173 | 端到端的医学影像重建，带定量能力，包含基于 CT 的衰减校正。 |
| [**xraylib**](https://github.com/tschoonj/xraylib) | C / Python | 173 | X 射线与物质相互作用的截面、荧光产额与康普顿剖面；做真实仿真所需的物理层。 |
| [**Core Imaging Library (CIL)**](https://github.com/TomographicImaging/CIL) | Python | 155 | CCPi 的变分 CT 重建框架，附有一整套优化算法目录。 |
| [**TomoPhantom**](https://github.com/dkazanc/TomoPhantom) | Python | 135 | 解析式的二维/三维/四维体模生成，配合正投影，用于受控的重建实验。 |
| [**MIRT**](https://github.com/JeffFessler/MIRT.jl) | Julia | 126 | 密歇根大学图像重建工具箱。涵盖极广的经典、统计与惩罚似然重建方法的参照实现；是长期存在的 MATLAB 版 MIRT 的 Julia 移植。 |
| [**OMEGA**](https://github.com/villekf/OMEGA) | MATLAB / Python | 111 | 开源的多维层析重建软件，覆盖 PET/SPECT/CT。 |
| [**Learned Primal-Dual**](https://github.com/adler-j/learned_primal_dual) | Python | 110 | 学习式原始-对偶重建的参照实现——最典型的展开式原始-对偶方案，最初即用于 CT。 |
| [**tomosipo**](https://github.com/cicwi/tomosipo) | Python | 107 | 以极低的负担描述二维/三维投影几何；封装 ASTRA 并与 PyTorch 打通。 |
| [**Learned Gradient Tomography**](https://github.com/adler-j/learned_gradient_tomography) | Python | 97 | 面向不适定层析的学习式梯度下降参照实现（Adler & Öktem）；后来许多展开式 CT 网络的源头。 |
| [**leehoy/CTReconstruction**](https://github.com/leehoy/CTReconstruction) | Python | 96 | 精简易读的 Python 实现，含 FBP 与迭代 CT 重建算法——适合作为从零实现的参照。 |
| [**Discorpy**](https://github.com/DiamondLightSource/discorpy) | Python | 93 | 亚像素级的相机与透镜畸变标定；用于在重建前校正探测器/几何畸变。 |
| [**IRtools**](https://github.com/jnagy1/IRtools) | MATLAB | 91 | 迭代正则化工具——混合 Krylov 方法、Tikhonov、TV 与一般形式正则化，随包附带大规模层析测试问题。来自 Hansen 课题组。 |
| [**Physics-ArX**](https://github.com/nadeemlab/Physics-ArX) | Python | 79 | 基于物理的数据增强库，把真实的 CT/CBCT 噪声、散射与伪影模型注入既有图像，以构造成对训练数据。 |
| [**Algotom**](https://github.com/algotom/algotom) | Python | 69 | 层析数据处理算法集——环状伪影与伪影去除、畸变校正、去噪、相位恢复与重建。为同步辐射光束线开发。 |
| [**CCPi Regularisation Toolkit**](https://github.com/TomographicImaging/CCPi-Regularisation-Toolkit) | C / Python | 63 | TV、TGV、方向性 TV 以及 CIL 所用其它正则项的 CPU/GPU 实现。 |
| [**LION**](https://github.com/CambridgeCIA/LION) | Python | 63 | 学习式迭代优化网络——基于 PyTorch 的展开式重建，用于 CT 与 PET。 |
| [**Sarepy**](https://github.com/nghia-vo/sarepy) | Python | 63 | 层析中环状伪影去除的数值方法——最完备的开源条纹/环状滤波器集合。 |
| [**DBT-Reconstruction**](https://github.com/LAVI-USP/DBT-Reconstruction) | MATLAB | 62 | 数字乳腺层析（DBT）的开源重建工具箱，覆盖 DBT 特有几何，并提供 FBP 与迭代求解器。 |
| [**LD-CT simulator**](https://github.com/smuzd/LD-CT-simulation) | MATLAB | 59 | 低剂量 CT 仿真器，用经过验证的噪声模型把高剂量图像转成逼真的低剂量对应图像。 |
| [**XrayPhysics**](https://github.com/kylechampley/XrayPhysics) | C++ / Python | 56 | X 射线截面、源能谱建模、多材料射束硬化校正与双能分解。出自 LEAP 的作者，需要物理上诚实的能谱时，它与仿真器天然配合。 |
| [**pySART**](https://github.com/djvine/pySART) | Python | 33 | 同时代数重建技术（SART）的精简参照实现。 |
| [**svmbir**](https://github.com/cabouman/svmbir) | C / Python | 28 | 快速的超体素模型迭代重建，支持近端映射插件。 |
| [**tofu**](https://github.com/ufo-kit/tofu) | Python | 20 | 架在 UFO 框架之上的辅助层，用于搭建快速 GPU 层析重建流程。 |
| [**CBCT Scatter Correction Tool**](https://github.com/YangkangJiang/Cone-beam-CT-scatter-correction-tool) | Python | 15 | 为数不多的锥束 CT 散射估计与校正开源实现之一。 |
| [**libcbct**](https://github.com/tatsy/libcbct) | C++ | 10 | 轻量锥束 CT 重建库，含 FDK 与迭代求解器。 |
| [**mumott**](https://gitlab.com/liebi-group/software/mumott) | Python | 4 | 面向倒空间数据的张量层析重建，由丹麦技术大学（DTU）开发。专用而非通用，但它是张量层析模型最完整的开源实现。 |
| [**DIRECTT Reconstruction GUI**](https://github.com/BAMresearch/DIRECTT) | Python | 1 | 基于 ASTRA 工具箱的 Python 图形界面，用于 X 射线 CT 数据重建，并内置 DIRECTT 算法。DIRECTT 面向的正是只有极少量投影、且扫描轨迹任意的情形，并把采集路径本身一并纳入反问题求解——多数基于算子的工具箱基本不涉及这个角度。由德国联邦材料研究与测试研究所（BAM）开发，发表于 Review of Scientific Instruments 2020；运行 Main.py 即可启动。虽属小众、星标很少，但明确处理轨迹问题的工具本就寥寥无几。 |
| [**pyHST2**](https://gitlab.esrf.fr/tomotools/pyhst2) | C / Python | 0 | ESRF 光束线的重建代码——gridrec、FBP 与迭代方法，带用于传播型相位衬度层析的相位恢复。同步辐射领域长期的主力工具。 |

<div align="right"><a href="#top">回到顶部 ↑</a></div>

## 数据集

**数据**列说明一份发布包含什么：_投影域 + 图像域_ 表示既有原始投影又有参考体，因而可以对前向模型做端到端评分；_仅投影域_ 表示只有原始数据；_仅图像域_ 表示只有图像域数据，无法用来检验投影模型。

| 数据集 | 成像模态 | 数据 | 许可 | Description |
| --- | --- | --- | --- | --- |
| [**LoDoPaB-CT**](https://zenodo.org/records/3384092) | 2D fan-beam | 投影域 + 图像域 | CC BY 4.0 | 41,000 张仿真人体胸腔切片（LIDC/IDRI），两个剂量水平。事实上的低剂量 CT 标准基准；附有调优良好的 FBP/U-Net 参考流程。 |
| [**LDCT-and-Projection-data**](https://www.cancerimagingarchive.net/collection/ldct-and-projection-data/) | helical CT | 投影域 + 图像域 | CC BY-NC 4.0 | Mayo Clinic 发布，经 TCIA 分发。299 例胸部／腹部／头部扫描，四个剂量水平（全剂量 / 1/4 / 10% / 5%），并以开放的 **DICOM-CT-PD** 格式提供原始正弦图。它源自 2016 年 AAPM 低剂量 CT 大挑战，目前是投影域方法最好的真实数据来源。 |
| [**2DeteCT**](https://zenodo.org/records/6984866) | 2D fan-beam | 投影域 + 图像域 | CC BY 4.0 | 5,000 张真实实验采集的混合物体二维切片，三个剂量水平，多种源-探测器几何。非常适合做可复现的真实数据 CT 基准测试。 |
| [**Walnut-CBCT**](https://www.fips.fi/dataset.php) | cone-beam | 仅投影域 | CC BY 4.0 | 芬兰逆问题学会。真实采集的核桃锥束投影，提供多种角度采样——稀疏视角与有限角 CBCT 的标准测试床。 |
| [**Helsinki Tomography Challenge 2022**](https://www.fips.fi/HTC2022.php) | 2D fan-beam | 仅投影域 | CC BY 4.0 | 体模与莲藕的真实有限角正弦图；配套挑战赛定义了标准的有限角协议。 |
| [**SPARE 4D-CBCT**](https://image-x.sydney.edu.au/spare-challenge/) | cone-beam, 4D | 投影域 + 图像域 | research use | 用于呼吸运动分辨重建的胸部四维锥束 CT；动态 CBCT 的参照基准。 |
| [**ToothFairy2**](https://doi.org/10.5281/zenodo.10990960) | cone-beam, dental | 仅图像域 | CC BY 4.0 | 480 例牙科 CBCT 扫描，带三维牙齿与颌骨标注；规模可观，适合做 CBCT 域预训练。**仅图像域**——只发布体数据，不带原始投影。 |
| [**Cone-Beam CT (CBCT) Head & Neck**](https://www.cancerimagingarchive.net/collection/head-neck/) | cone-beam | 仅图像域 | CC BY-NC 3.0 | 配对的计划 CT 与机载 CBCT——放射治疗中 CBCT 校正与合成 CT 工作的标准场景。 |
| [**LIDC-IDRI**](https://www.cancerimagingarchive.net/collection/lidc-idri/) | helical CT | 仅图像域 | CC BY 3.0 | 1,018 例胸部 CT，带四位放射科医师的结节标注。LoDoPaB-CT 与多数仿真低剂量数据所依据的解剖来源。 |
| [**DeepLesion**](https://nihcc.app.box.com/v/DeepLesion) | helical CT | 仅图像域 | CC BY 3.0 | 覆盖 4,427 名患者、10,594 次检查的 32,735 处病灶标注——CT 域骨干网络的大规模预训练语料。 |
| [**LUNA16**](https://luna16.grand-challenge.org/) | helical CT | 仅图像域 | CC BY 3.0 | 888 例薄层胸部 CT，统一重采样到 1 mm 并带结节标注；干净、整理得当的去噪/检测基准。 |
| [**KiTS23**](https://kits-challenge.org/kits23/) | contrast CT | 仅图像域 | CC BY-NC 4.0 | 489 例腹部 CT，带肾肿瘤与囊肿标注，横跨三届挑战赛。 |
| [**Pancreas-CT (NIH)**](https://www.cancerimagingarchive.net/collection/pancreas-ct/) | contrast CT | 仅图像域 | CC BY 3.0 | 82 例腹部增强 CT，带专家标注的胰腺掩膜；规模不大但使用极广的参照集。 |
| [**BTCV (Beyond the Cranial Vault)**](https://www.synapse.org/#!Synapse:syn3193805/wiki/217789) | contrast CT | 仅图像域 | CC BY-NC 4.0 | 30 例腹部 CT，带 13 个器官标注；是多器官基准中 FLARE/AMOS 一脉的源头。 |
| [**TotalSegmentator**](https://zenodo.org/records/10047292) | contrast CT | 仅图像域 | CC BY 4.0 | 1,228 例 CT、104 个解剖结构——规模最大的开源 CT 结构集，也是很强的预训练目标。 |
| [**AMOS22**](https://amos22.grand-challenge.org/) | CT / MRI | 仅图像域 | CC BY-NC-SA 4.0 | 500 例 CT 加 100 例 MRI 腹部扫描、15 个器官；刻意采用异构设备，因此很考验鲁棒性。 |
| [**Medical Segmentation Decathlon**](http://medicaldecathlon.com/) | CT / MRI | 仅图像域 | CC BY-SA 4.0 | 十个任务，其中四个是 CT（肺、胰腺、结肠、肝血管）。被引用最多的多任务医学分割基准。 |
| [**VerSe**](https://github.com/anjany/verse) | CT / CBCT | 仅图像域 | CC BY-SA 4.0 | 3,741 例 CT/CBCT 脊柱扫描，带椎体与椎间盘标签；临床 CT 与 CBCT 混合，因此与伪影鲁棒性相关。 |
| [**RibFrac**](https://ribfrac.grand-challenge.org/) | CT | 仅图像域 | CC BY-NC 4.0 | 5,000 例 CT、660 处肋骨骨折标注；规模大，常被用作 CT 辅助语料。 |
| [**CT-ORG**](https://www.cancerimagingarchive.net/collection/ct-org/) | contrast CT | 仅图像域 | CC BY 3.0 | 140 例 CT，带多器官掩膜，其中含 Liver Tumor Segmentation 基准的一个子集。 |
| [**STOIC 2021**](https://portal.imaging.datacommons.cancer.gov/collections/stoic/) | CT | 仅图像域 | CC BY-NC 3.0 | 来自多中心国际研究的 23,000 余例 COVID-19 胸部 CT；规模极大的真实临床分布偏移测试。此处通过 NCI Imaging Data Commons 镜像收录，同一批数据提供可查询 API。 |
| [**MosMedData**](https://mosmed.ai/en/datasets/datasets/covid191110/) | CT | 仅图像域 | CC BY-NC-ND 3.0 | 1,110 例胸部 CT，带 COVID-19 严重程度分级；常被复用为低质量/低剂量鲁棒性测试集。 |
| [**HNSCC (Head & Neck)**](https://www.cancerimagingarchive.net/collection/hnscc/) | contrast CT + PET | 仅图像域 | CC BY-NC 3.0 | 多机构的头颈部 CT，带 GTV/CTV 勾画；与 HECKTOR 挑战赛配套。 |
| [**CTPelvic1K**](https://github.com/MIRACLE-Center/CTPelvic1K) | contrast CT | 仅图像域 | CC BY-NC 4.0 | 跨 7 个子集的 1,184 例盆腔 CT；值得注意的是含**金属植入物**病例，是真实金属伪影的少数开放来源之一。 |
| [**FLARE22**](https://flare22.grand-challenge.org/) | contrast CT | 仅图像域 | CC BY-NC-SA 4.0 | 2,000 例腹部 CT、13 个器官标签，来自 20 余台设备；大规模鲁棒性基准。 |
| [**AutoPET-II**](https://autopet-ii.grand-challenge.org/) | PET/CT | 仅图像域 | CC BY-NC 4.0 | 1,014 例全身 PET/CT 检查，带病灶掩膜；当 CT 重建要喂给下游任务时相关。 |
| [**HECKTOR**](https://hecktor.grand-challenge.org/) | PET/CT | 仅图像域 | CC BY-NC 4.0 | 头颈部 PET/CT，带原发肿瘤勾画；五届标注口径一致。 |
| [**CT Lymph Nodes**](https://www.cancerimagingarchive.net/collection/ct-lymph-nodes/) | contrast CT | 仅图像域 | CC BY 3.0 | 176 例腹部 CT，带纵隔与腹部淋巴结标注。 |
| [**NLST**](https://www.cancerimagingarchive.net/collection/nlst/) | low-dose CT | 仅图像域 | restricted (TCIA NCI) | 26,254 例基线低剂量筛查 CT——迄今最大的真实低剂量 CT 集合，但获取需要申请授权。 |
| [**AAPM DL-Sparse-View CT data**](https://www.aapm.org/GrandChallenge/DL-sparse-view-CT/) | helical CT (re-projected) | 投影域 + 图像域 | CC BY 3.0 | 2016 年挑战赛队列重新投影为每圈 2/4/8/16/32/64 个视角，在固定解剖真值下给出可控的稀疏视角轴。 |
| [**Finnish Inverse Problems Society (FIPS) datasets**](https://www.fips.fi/dataset.php) | fan-beam / cone-beam | 仅投影域 | CC BY 4.0 | 一批真实测量的正弦图（核桃、莲藕、苹果、胡萝卜、体模），采集几何记录详尽——检验重建算子最干净的公开来源。 |
| [**LoDoPaB-CT (benchmark release paper)**](https://doi.org/10.1038/s41597-021-00893-z) | 2D fan-beam | 仅图像域 | CC BY 4.0 | LoDoPaB-CT 数据集在 **Scientific Data** 上的数据描述论文——在该切分上报告结果时应引用的文献。记录了仿真协议与 FBP/U-Net 参照基线。 |
| [**COBRA2026: a large-scale multicenter pelvic cone-beam computed tomography projection dataset**](https://arxiv.org/abs/2607.20037) | - | 仅图像域 | - | 以公开投影数据集的形式发布（获取方式见论文）。 |
| [**MORE: Multi-Organ Medical Image REconstruction Dataset**](https://arxiv.org/abs/2510.26759) | - | 仅图像域 | - | 以公开投影数据集的形式发布（获取方式见论文）。已被 ACMMM 2025 接收。 |
| [**TomoBank**](https://tomobank.readthedocs.io/en/latest/) | synchrotron micro-CT | 投影域 + 图像域 | see source | 由美国阿贡国家实验室 Advanced Photon Source 维护的层析数据仓库，收录大量实验采集与仿真的层析数据，覆盖多种仪器与样品类型。它的价值在于用真正来自光束线的数据来检验和比较重建方法，而不是只靠体模。 |
| [**SparseBeads**](https://zenodo.org/records/290117) | micro-CT | 投影域 + 图像域 | CC BY 4.0 | 48 组真实采集的珠体体模扫描，图像稀疏程度被系统地拉开梯度，专为稀疏正则化重建的基准评测而发布。灵感来自 SophiaBeads，是在已知真值下横比不同正则项时的参照点。 |
| [**Walnut-21 (two dose levels)**](https://zenodo.org/records/3763412) | cone-beam | 仅投影域 | CC BY 4.0 | 21 颗核桃的高分辨率锥束扫描，每颗都以两个辐射剂量水平各采一次——同一物体的一版「干净」与一版「带噪」。这种配对采集正是它的用处：噪声水平可以直接对照已知解剖结构来比较，而不是靠推测。 |
| [**FleX-ray Walnut CBCT Collection (CWI)**](https://zenodo.org/records/2686726) | cone-beam micro-CT | 投影域 + 图像域 | CC BY 4.0 | 42 个核桃，每个沿三条不同轨道各采集一次——因此可由合并视角算出无伪影的参考体，用作监督学习的真值。值得注意的是这并非又一个单一物体体模：其设计意图是同一类物体之间的自然变异。完整流水线一并给出——原始投影、扫描几何、预处理与重建脚本（均为开源软件）以及重建后的体数据，因而既可用于高锥角伪影抑制，也可用于稀疏角／有限角重建、超分辨与分割。数据分六个 Zenodo 存档发布，覆盖样本 1–42。 |
| [**LoDoInd**](https://zenodo.org/records/10356955) | industrial cone-beam CT | 仅图像域 | CC BY-NC 4.0 | 同一批工业 CT 试件的五个剂量级别，其中含一次近乎无噪的参考扫描，全部预先配准，跨剂量级别的切片彼此对齐。与医学低剂量数据集的关键差别在于几何与试件——这是工业硬件的检测数据而非临床解剖，所以当目标是 NDT 流水线而非诊断流程时，它才是该用的基准。每级 4000 张 1250×1250 切片；因 Zenodo 单次上传上限 50 GB，拆分为三个存档。 |
| [**Carved cheese (FIPS)**](https://zenodo.org/records/1254210) | 2D fan-beam | 仅投影域 | CC BY 4.0 | 芬兰逆问题学会发布的一个雕花奶酪单层二维切片，提供三种分辨率，并附带把 X 射线变换写成显式线性算子的测量矩阵。正弦图之外还把前向算子直接交到你手上，可省掉一整类几何不匹配的错误，这也是它在把重建方法移植到真实实测数据时始终作为标准首测的原因。文档见 arXiv:1705.05732。 |

<div align="right"><a href="#top">回到顶部 ↑</a></div>

## 基准与挑战赛

| 基准 / 挑战赛 | 年份 | 任务 | Description |
| --- | --- | --- | --- |
| [**Generating synthetic computed tomography for radiotherapy: SynthRAD2025 challenge report**](https://arxiv.org/abs/2605.13555) | 2026 | reconstruction | 共 59 页：正文 26 页 + 补充材料；正文 8 幅图，补充 3 幅图。目前正由 Medical Image Analysis 期刊审稿中。 |
| [**CT-DegradBench: A Physics-Informed Benchmark for CT Degradation Detection and Severity Estimation**](https://arxiv.org/abs/2605.16431) | 2026 | reconstruction | 已被 CVPR 2026 VISION Workshop（DEXTER track）接收。 |
| [**SPARE Challenge**](https://image-x.sydney.edu.au/spare-challenge/) | 2024 | dynamic, cbct, reconstruction | 从一分钟扫描重建胸部四维锥束 CT。首个被广泛采用的呼吸分辨动态 CBCT 基准；由悉尼大学 Image X 研究所主办。 |
| [**DeepInverse benchmark suite**](https://deepinv.github.io/) | 2024 | reconstruction, benchmarking | 统一的 PyTorch 基准框架，覆盖 CT、MRI、去模糊与图像修复，提供可复现指标与预训练基线——把新 CT 方法与强通用求解器对比的最实用途径。 |
| [**SynthRAD2023 Challenge**](https://synthrad2023.grand-challenge.org/) | 2023 | cbct, synthetic-ct, reconstruction | 从 CBCT 与 MRI 生成合成 CT。与此处相关，是因为 CBCT→CT 任务恰恰由重建伪影（散射、截断、射束硬化）主导——该挑战赛迫使方法正面处理它们，而不是假设输入干净。 |
| [**AAPM DL-Sparse-View CT Challenge**](https://www.aapm.org/GrandChallenge/DL-sparse-view-CT/) | 2022 | sparse-view, reconstruction | 在重新投影的临床数据上固定稀疏视角协议（2/4/8/16/32/64 视角），提供官方指标与公开排行榜。稀疏视角 CT 的标准参照点。 |
| [**Helsinki Tomography Challenge**](https://www.fips.fi/HTC2022.php) | 2022 | limited-angle, reconstruction | 真实测量的有限角正弦图。值得注意的是优胜方案是经典/基于模型的，而非纯学习型——是一个有用的反例。 |
| [**AutoPET Challenge**](https://autopet.grand-challenge.org/) | 2022 | segmentation | 跨三届的全身 PET/CT 病灶分割，刻意隐藏多中心测试队列。 |
| [**CTooth / CTooth+**](https://github.com/liangjiubujiu/CTooth) | 2022 | segmentation, cbct | 全标注的三维牙科 CBCT 数据集与牙齿分割基准（5,803 层 CBCT），后扩展为 CTooth+。在伪影严重的领域里，是一个规模不大但标注精良的 CBCT 基准。 |
| [**LoDoPaB-CT benchmark**](https://lodopab.grand-challenge.org/) | 2021 | low-dose, reconstruction | 在 LoDoPaB-CT 切分上以大挑战赛方式评测，并发布经过调优的 FBP+U-Net 参照基线，使改进幅度可度量。 |
| [**MICCAI FLARE**](https://flare.grand-challenge.org/) | 2021 | segmentation | 跨四届（FLARE21/22/23/24）的多器官腹部 CT 分割；是 CT 重建输出的标准下游鲁棒性检验目标。 |
| [**HECKTOR Challenge**](https://hecktor.grand-challenge.org/) | 2020 | segmentation, prognosis | 头颈部 PET/CT 肿瘤勾画；五届使其成为运行时间较长的医学影像挑战赛之一。 |
| [**KiTS Challenge**](https://kits-challenge.org/) | 2019 | segmentation | 肾肿瘤分割，三届（2019/2021/2023），标注质量严格受控，并高度强调跨机构泛化。 |
| [**VerSe Challenge**](https://verse2019.grand-challenge.org/) | 2019 | segmentation, cbct | 同时覆盖 CT 与 CBCT 的椎体标注，带大规模隐藏测试集；CBCT 那一半天然适合作为伪影严重输入的压力测试。 |
| [**CHAOS Challenge**](https://chaos.grand-challenge.org/) | 2019 | segmentation | 腹部 CT 与 MRI 器官分割，包含低剂量与平扫协议，并明确做跨模态评测。 |
| [**Medical Segmentation Decathlon**](http://medicaldecathlon.com/) | 2018 | segmentation | 十个任务，测试集固定且隐藏，并严格禁止针对单一任务调优——真正公平的泛化基准。 |
| [**Noise2Noise denoising protocol**](https://github.com/NVlabs/noise2noise) | 2018 | denoising, self-supervised | 让「无需干净真值即可训练去噪器」流行起来的参照实现。在 CT 上它成为标准的「无干净真值」评测协议——多数无监督 CT 去噪论文都在此设定下、用 Mayo-LDCT 式切分报告结果。 |
| [**AAPM Low-Dose CT Grand Challenge**](https://www.aapm.org/grandchallenge/lowdosect/) | 2016 | low-dose, denoising, reconstruction | 确立了 1/4 剂量 / 10% / 5% 协议与 Mayo 腹部队列的挑战赛。几乎每一篇低剂量 CT 论文至今仍在该切分上报告结果。 |
| [**SPIE-AAPM-NCI LungX Challenge**](https://www.cancerimagingarchive.net/collection/spie-aapm-lung-ct-challenge/) | 2015 | detection, low-dose | 低剂量筛查 CT 上的肺结节检测；早期证明了在低剂量数据上达到阅片者水平是可行的。数据经 TCIA 分发。 |

<div align="right"><a href="#top">回到顶部 ↑</a></div>

## 学习资源

**图书**

- [Computed Tomography - From Photon Statistics to Modern Cone-Beam CT](https://doi.org/10.1007/978-3-540-39408-2) — Buzug（2008）。从物理（光子统计、多色性、探测器响应）通向重建算法的最佳单本桥梁之作。
- [Computed Tomography - Principles, Design, Artifacts, and Recent Advances](https://www.spiedigitallibrary.org/ebooks/PM/Computed-Tomography-Principles-Design-Artifacts-and-Recent-Advances-Third-Edition/eISBN-9781628418040/10.1117/3.1764041) — Hsieh（第 3 版，2015，SPIE）。出自 CT 厂商内部视角：系统设计、剂量、伪影分类与临床校正策略。
- [CT Principles and Algorithms](https://www.google.com/search?q=%E5%BA%84%E5%A4%A9%E6%88%88+CT%E5%8E%9F%E7%90%86%E4%B8%8E%E7%AE%97%E6%B3%95) — 庄天戈。中文的 CT 原理与算法入门读物；被广泛用作第一门课程的教材，也是偏好中文的读者最自然的切入点。
- [Foundations of Image Science](https://doi.org/10.1002/0471722138) — Barrett & Myers（2004）。成像系统理论的百科式参考——傅里叶串扰、基于任务的评估，以及迭代重建的数学基础。
- [Fundamentals of Computerized Tomography - Image Reconstruction from Projections](https://doi.org/10.1007/978-1-84628-723-7) — Herman（第 2 版，2009）。非常实用，给出明确的算法与伪代码，并细致处理采样与离散化伪影。
- [Industrial CT Technology and Principles](https://www.google.com/search?q=%E5%BC%A0%E6%9C%9D%E5%AE%97+%E5%B7%A5%E4%B8%9ACT%E6%8A%80%E6%9C%AF%E5%92%8C%E5%8E%9F%E7%90%86) — 张朝宗。工业（无损检测）CT 的参考书——几何、射线源、探测器与工业侧的伪影来源，正是医学教材止步之处。
- [Medical Image Reconstruction - A Conceptual Tutorial](https://doi.org/10.1007/978-3-642-05368-9) — Zeng（2010）。刻意以直觉优先：用最少的符号解释 FBP、迭代与解析方法为何如此表现。
- [Medical Tomographic Image Reconstruction Simulation Experiments](https://www.google.com/search?q=%E9%BB%84%E5%8A%9B%E5%AE%87+%E5%8C%BB%E5%AD%A6%E6%96%AD%E5%B1%82%E5%9B%BE%E5%83%8F%E9%87%8D%E5%BB%BA%E4%BB%BF%E7%9C%9F%E5%AE%9E%E9%AA%8C) — 黄力宇。中文的实践型实验手册：把每个重建算法做成仿真实验，而不是当作理论来讲。
- [Principles of Computerized Tomographic Imaging](https://www.slaney.org/pct/pct-toc.html) — Kak & Slaney（1988）。**免费 PDF。** 奠基之作：Radon 变换、傅里叶切片定理、FBP、代数重建、扇束/锥束重排。建议先读第 1–3 章。
- [The Mathematics of Computerized Tomography](https://doi.org/10.1137/1.9780898719284) — Natterer（1986，SIAM 重印本）。严谨的逆问题处理——Sobolev 空间上的 Radon 变换、采样理论、不适定性与正则化。

**课程**

- [Principles of Medical Imaging (MIT OCW 22.058)](https://ocw.mit.edu/courses/22-058-principles-of-medical-imaging-fall-2002/) — 免费的讲义与习题集，覆盖投影成像、Radon 变换与重建，并旁及 MRI、超声与 PET。

**教程**

- [ASTRA Toolbox documentation and tutorials](https://astra-toolbox.com/docs/index.html) — 最容易上手的动手入口：CPU/GPU 正投影与反投影算子、FBP、SART/SIRT、CGLS，每种几何都配可运行示例。
- [DeepInverse documentation](https://deepinv.github.io/) — 现代的 PyTorch 优先教程路径：物理算子、学习型去噪器、即插即用与扩散采样器，全部配有 CT 示例。
- [ODL examples](https://github.com/odlgroup/odl/tree/master/examples) — 演示如何把 CT 问题表述为算子与泛函，再用近端方法求解——变分 CT 最清晰的入门。
- [Radon transform in scikit-image](https://scikit-image.org/docs/stable/auto_examples/transform/plot_radon_transform.html) — 二十行代码，从体模到正弦图再用 FBP 反推回来；接触真实几何之前建立直觉最快的途径。
- [TIGRE demos](https://github.com/CERN/TIGRE/tree/master/Python/demos) — 可运行的 GPU 演示，从解析 FBP 到迭代、全变分与即插即用重建，另附 CBCT 几何标定演示。

**工具**

- [gVXR (gVirtualXray)](https://gvirtualxray.sourceforge.io/) — GPU 加速的 X 射线投影仿真器，支持任意三维场景与多色能谱——适合构建大规模合成投影数据集。
- [NIST X-Ray Mass Attenuation Coefficients](https://www.nist.gov/pml/x-ray-mass-attenuation-coefficients) — **NIST。** 全周期表 mu/rho 与 mu_en/rho 的权威表格。XrayPhysics 与 SpekPy 内部即以此校准——需要核检多色模型时很有用。
- [SimpleITK](https://github.com/SimpleITK/SimpleITK) — 医学体数据的标准 I/O 与重采样层；本列表中几乎所有 CT 数据集都通过它加载最省事。
- [SpekPy](https://pypi.org/project/spekpy/) — X 射线管能谱仿真（TASMIP/IPEM 一脉），以 Python 包发布。用它生成逼真的多色能谱，用于射束硬化实验。
- [TomoPhantom](https://github.com/dkazanc/TomoPhantom) — 快速的解析式二维/三维/四维体模生成，内置噪声与偏移模型；便于做受控重建研究。
- [X-Ray Data Booklet](https://xdb.lbl.gov/) — **LBNL。** 元素 X 射线性质的标准速查手册——吸收边、荧光产额与散射截面。仿真需要某个物理常数时的第一去处。
- [XDesign](https://github.com/AdvancedPhotonSource/xdesign) — 可微分的 CT 采集仿真——在训练循环内建模多色能谱、探测器响应与几何。最初与 CIL 一同开发，现由 Advanced Photon Source 维护。

**其他列表**

- [Awesome 3D Gaussian Splatting](https://github.com/MrNeRF/awesome-3D-gaussian-splatting) — 3DGS 的参照列表。其中贴近层析的条目（r2_gaussian、X-Gaussian、X2-Gaussian）是通往高斯泼溅 CT 的桥梁。
- [Awesome CT Reconstruction (LoraLinH)](https://github.com/LoraLinH/Awesome-CT-Reconstruction) — 最知名的前作 CT 重建列表。适合交叉核对 2020–2024 年文献的覆盖情况。
- [Awesome Medical Imaging](https://github.com/fepegar/awesome-medical-imaging) — 更宽泛的医学影像分析资源：数据集、工具包与预训练模型，在 CT 流程中常被复用。
- [Awesome NeRF and 3DGS for SLAM](https://github.com/3D-Vision-World/awesome-NeRF-and-3DGS-SLAM) — 机器人/视觉社区的神经场文献；当前被移植到 CT 的隐式表示技术即源自此处。
- [CT Denoising Review](https://github.com/SSinyu/CT-Denoising-Review) — 专注低剂量 CT 去噪，侧重 SSinyu/Mayo 一脉的方法。
- [Low-Dose CT Denoising (code collection)](https://github.com/houguanqun/Low-Dose-CT-denoising) — 持续更新的低剂量 CT 去噪代码合集，按年份组织——便于查找某篇论文背后的实现。

<div align="right"><a href="#top">回到顶部 ↑</a></div>

## 联系方式

本列表由作者策展并维护，不接受拉取请求。如有疑问、勘误，或希望增删某篇论文，请提交 [issue](https://github.com/cslht11/awesome-computed-tomography/issues) 或发送邮件至 **[heitieya@163.com](mailto:heitieya@163.com)**。

## 许可

内容（`data/`、本 README 与生成的网站）采用 [CC BY-NC-SA 4.0](LICENSE-content) 许可：

- **署名**：使用时请注明出处。
- **非商业性使用**：不得用于商业用途，如需商用请先联系。
- **相同方式共享**：改编作品须以相同许可发布。

代码（`scripts/`、`web/`、`.github/`）采用 [MIT](LICENSE) 许可。表格中的许可列描述的是**那些项目自身**而非本列表；每条条目都只是指向论文的链接，从不复制论文内容。
