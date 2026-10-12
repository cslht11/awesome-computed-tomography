<a id="top"></a>
<div align="center">

<img src="assets/logo.svg" width="88" alt="">

# Awesome Computed Tomography

**A curated, verified list of CT reconstruction research** — papers, toolkits, datasets and benchmarks for CT, CBCT and micro-CT.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![Website](https://img.shields.io/badge/website-computedtomography.org-3f51b5?style=flat-square)](https://computedtomography.org/) [![Papers](https://img.shields.io/badge/papers-392-555?style=flat-square)](#papers) [![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-555?style=flat-square)](#license)

**[Website](https://computedtomography.org/)** · [Papers](#papers) · [Toolkits](#toolkits) · [Datasets](#datasets) · [Benchmarks](#benchmarks) · [Learning](#learning)

</div>

**EN** · [中文](README.zh-CN.md)

| 392 papers | 84% peer-reviewed | 91 with code | 44 toolkits | 41 datasets | 19 benchmarks | 1917–2026 |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |

Sparse-view, limited-angle, low-dose, metal-artifact, spectral, cone-beam and 4D CT — from FBP and iterative solvers to unrolled networks, diffusion priors, neural fields and Gaussian splatting. Every paper link is resolved against Crossref, arXiv or the publisher's record. For search and filters, use the **[website](https://computedtomography.org/)**.

## Papers

| | | |
| --- | --- | --- |
| [Surveys & Reviews](#surveys--reviews) <sub>23</sub> | [Classical & Iterative Reconstruction](#classical--iterative-reconstruction) <sub>68</sub> | [Sparse-View CT](#sparse-view-ct) <sub>137</sub> |
| [Limited-Angle Tomography](#limited-angle-tomography) <sub>45</sub> | [Low-Dose CT Denoising](#low-dose-ct-denoising) <sub>58</sub> | [Metal Artifact Reduction](#metal-artifact-reduction) <sub>21</sub> |
| [Spectral & Dual-Energy CT](#spectral--dual-energy-ct) <sub>18</sub> | [Cone-Beam CT](#cone-beam-ct) <sub>66</sub> | [Dynamic & 4D CT](#dynamic--4d-ct) <sub>21</sub> |
| [Scatter Correction](#scatter-correction) <sub>11</sub> | [Geometry Calibration & Motion Compensation](#geometry-calibration--motion-compensation) <sub>25</sub> | [Deep Unrolling & Model-Based Learning](#deep-unrolling--model-based-learning) <sub>68</sub> |
| [Self-Supervised & Untrained Methods](#self-supervised--untrained-methods) <sub>32</sub> | [Diffusion & Generative Priors](#diffusion--generative-priors) <sub>55</sub> | [Implicit Neural Representations](#implicit-neural-representations) <sub>24</sub> |
| [Gaussian Splatting](#gaussian-splatting) <sub>24</sub> | [Other Topics](#other-topics) <sub>29</sub> |  |

Newest first within each topic. Each entry gives its venue and year in italics; _preprint_ marks work not (yet) published at a peer-reviewed venue, dated by its first public posting.

### Surveys & Reviews

<sub>Overview papers, tutorials and comparative studies · 23 papers</sub>

- **DM4CT: Benchmarking Diffusion Models for CT Reconstruction** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2602.18589) · [Code](https://github.com/DM4CT/DM4CT)
- **Are Pixel-Wise Metrics Reliable for Sparse-View Computed Tomography Reconstruction?** — _NeurIPS 2025_ · [Paper](https://arxiv.org/abs/2506.02093) · [Code](https://github.com/MrGiovanni/CARE)
- **Synthetic CT image generation from CBCT: A Systematic Review** — _TRPMS 2025_ · [Paper](https://arxiv.org/abs/2501.13972)
- **A Review of Deep Learning CT Reconstruction From Incomplete Projection Data** — _TRPMS 2024_ · [Paper](https://doi.org/10.1109/trpms.2023.3316349)
- **DiffRecon: Diffusion Models for Medical Image Reconstruction** — _BJR|AI 2024_ · [Paper](https://doi.org/10.1093/bjrai/ubae013)
- **Machine learning in industrial X-ray computed tomography - a review** — _CIRP JMST 2024_ · [Paper](https://doi.org/10.1016/j.cirpj.2024.05.004)
- **DiffMed: Diffusion Models for Medical Image Analysis: A Comprehensive Survey** — _preprint 2022_ · [Paper](https://arxiv.org/abs/2211.07804)
- **Review of high energy x-ray computed tomography for non-destructive dimensional metrology of large metallic advanced manufactured components** — _RoPP 2022_ · [Paper](https://doi.org/10.1088/1361-6633/ac43f6)
- **A review on deep learning in medical image reconstruction** — _JORSC 2020_ · [Paper](https://arxiv.org/abs/1906.10643)
- **DL-CT-Rev: Deep Learning for Tomographic Image Reconstruction** — _Nat Mach Intell 2020_ · [Paper](https://doi.org/10.1038/s42256-020-00273-z)
- **DL-InvProb: Deep Learning Techniques for Inverse Problems in Imaging** — _JSAIT 2020_ · [Paper](https://arxiv.org/abs/2005.06001)
- **Sparsity2DL: Image Reconstruction: From Sparsity to Data-Adaptive Methods and Machine Learning** — _Proc. IEEE 2020_ · [Paper](https://doi.org/10.1109/JPROC.2019.2936204)
- **CT-Evolution: The Evolution of Image Reconstruction for CT: From Filtered Back Projection to Artificial Intelligence** — _Eur Radiol 2019_ · [Paper](https://doi.org/10.1007/s00330-018-5810-7)
- **DataDriven: Solving Inverse Problems Using Data-Driven Models** — _Acta Numerica 2019_ · [Paper](https://doi.org/10.1017/S0962492919000059)
- **Applications of nonlocal means algorithm in low-dose X-ray CT image processing and reconstruction: A review** — _Med Phys 2017_ · [Paper](https://doi.org/10.1002/mp.12097)
- **CNN-InvRev: Convolutional Neural Networks for Inverse Problems in Imaging: A Review** — _SPM 2017_ · [Paper](https://doi.org/10.1109/MSP.2017.2739299)
- **MAR-4Dec: Metal Artifact Reduction in CT: Where Are We After Four Decades?** — _IEEE Access 2016_ · [Paper](https://doi.org/10.1109/ACCESS.2016.2608621)
- **Dual- and Multi-Energy CT: Principles, Technical Approaches, and Clinical Applications** — _Radiology 2015_ · [Paper](https://doi.org/10.1148/radiol.2015142631)
- **A General Framework and Review of Scatter Correction Methods in Cone-Beam CT: Part 2 — Scatter Estimation Approaches** — _Med Phys 2011_ · [Paper](https://doi.org/10.1118/1.3589140)
- **Scatter-Rev: A General Framework and Review of Scatter Correction Methods in X-Ray Cone-Beam CT: Part 1 — Scatter Compensation Approaches** — _Med Phys 2011_ · [Paper](https://doi.org/10.1118/1.3599033)
- **Task-based performance analysis of FBP, SART and ML for digital breast tomosynthesis using signal CNR and Channelised Hotelling Observers** — _Med Image Anal 2011_ · [Paper](https://doi.org/10.1016/j.media.2010.07.004)
- **Tomographic Reconstruction in the 21st Century** — _SPM 2010_ · [Paper](https://doi.org/10.1109/msp.2010.936743)
- **Why do commercial CT scanners still employ traditional, filtered back-projection for image reconstruction?** — _Inverse Problems 2009_ · [Paper](https://doi.org/10.1088/0266-5611/25/12/123009)

### Classical & Iterative Reconstruction

<sub>Analytical (FBP/FDK) and iterative (SART/SIRT/CGLS) reconstruction, hand-crafted regularizers (TV, TGV, non-local) · 68 papers</sub>

- **Complex Wavelet-Based Sinogram Segmentation for Metal Artifact Reduction in Cone-Beam CT** — _PMB 2026_ · [Paper](https://arxiv.org/abs/2602.14315)
- **Computed Tomography Reconstruction Algorithm Using Markov Random Field Model** — _J. Phys. Soc. Jpn. 2026_ · [Paper](https://arxiv.org/abs/2605.11637)
- **Cross-Distribution Diffusion Priors-Driven Iterative Reconstruction for Sparse-View CT** — _TMI 2026_ · [Paper](https://arxiv.org/abs/2509.13576)
- **DC-PnPDP: Plug-and-Play Diffusion Meets ADMM: Dual-Variable Coupling for Robust Medical Image Reconstruction** — _ICML 2026_ · [Paper](https://arxiv.org/abs/2602.23214) · [Code](https://github.com/duchenhe/DC-PnPDP) · [Project](https://duchenhe.com/project/DCPnPDP/)
- **H3D-MarNet: Wavelet-Guided Dual-Path Learning for Metal Artifact Suppression and CT Modality Transformation for Radiotherapy Workflows** — _ICPR 2026_ · [Paper](https://arxiv.org/abs/2605.12252)
- **Robustness and Stability Analysis of Differentiable Shift-Variant FBP for Cone-Beam CT under Challenging Acquisition Settings** — _MELBA 2026_ · [Paper](https://arxiv.org/abs/2607.09828) · [Project](https://melba-journal.org/2026:014)
- **Variational Garrote for Sparse Inverse Problems** — _J. Comput. Sci. 2026_ · [Paper](https://doi.org/10.1016/j.jocs.2026.102980)
- **An Iterative Reconstruction Method for Dental Cone-Beam Computed Tomography with a Truncated Field of View** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.07618)
- **CoCo-PnP: Learning Cocoercive Conservative Denoisers via Helmholtz Decomposition for Poisson Inverse Problems** — _NeurIPS 2025_ · [Paper](https://arxiv.org/abs/2505.08909) · [Code](https://github.com/FizzzFizzz/CoCo-PnP)
- **Learning Wavelet-Sparse FDK for 3D Cone-Beam CT Reconstruction** — _Fully3D 2025_ · [Paper](https://arxiv.org/abs/2505.13579)
- **MONSTR: Model-Oriented Neutron Strain Tomographic Reconstruction** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2505.22187)
- **SDB: System-Embedded Diffusion Bridge Models** — _NeurIPS 2025_ · [Paper](https://arxiv.org/abs/2506.23726) · [Code](https://github.com/sobieskibj/sdb)
- **Data-Driven Filter Design in FBP: Transforming CT Reconstruction with Trainable Fourier Series** — _preprint 2024_ · [Paper](https://arxiv.org/abs/2401.16039)
- **How auto-differentiation can improve CT workflows: classical algorithms in a modern framework** — _Opt. Express 2024_ · [Paper](https://doi.org/10.1364/oe.502920)
- **IRDS: Iterative reconstruction of low-dose CT based on differential sparse** — _BSPC 2023_ · [Paper](https://doi.org/10.1016/j.bspc.2022.104204)
- **EASEL: Iterative Reconstruction for Low-Dose CT using Deep Gradient Priors of Generative Model** — _TRPMS 2022_ · [Paper](https://doi.org/10.1109/trpms.2022.3148373) · [Code](https://github.com/yqx7150/EASEL)
- **ALPD: Adversarially learned iterative reconstruction for imaging inverse problems** — _SSVM 2021_ · [Paper](https://arxiv.org/abs/2103.16151) · [Code](https://github.com/Subhadip-1/adversarial_primal_dual_tomography)
- **DL-PICCS: Accurate and robust sparse-view angle CT image reconstruction using deep learning and prior image constrained compressed sensing (DL-PICCS)** — _Med Phys 2021_ · [Paper](https://doi.org/10.1002/mp.15183)
- **FISTA-Net: Learning a Fast Iterative Shrinkage Thresholding Network for Inverse Problems in Imaging** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3054167) · [Code](https://github.com/jinxixiang/FISTA-Net)
- **Limited-Angle CT Reconstruction via the L1/L2 Minimization** — _SIAM J. Imaging Sci. 2021_ · [Paper](https://doi.org/10.1137/20m1341490)
- **Tensor-Net: Learning to Reconstruct CT Images From the VVBP-Tensor** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3090257)
- **FSTensor: Full-spectrum-knowledge-aware tensor model for energy-resolved CT iterative reconstruction** — _TMI 2020_ · [Paper](https://doi.org/10.1109/tmi.2020.2976692)
- **iRadonMAP: Radon Inversion via Deep Learning** — _TMI 2020_ · [Paper](https://arxiv.org/abs/1808.03015)
- **Learned convex regularizers for inverse problems** — _preprint 2020_ · [Paper](https://arxiv.org/abs/2008.02839)
- **Momentum-Net: Fast and convergent iterative neural network for inverse problems** — _TPAMI 2020_ · [Paper](https://doi.org/10.1109/tpami.2020.3012955)
- **Moreau-envelope-enhanced nonlocal shearlet transform and total variation for sparse-view CT reconstruction** — _Meas. Sci. Technol. 2020_ · [Paper](https://doi.org/10.1088/1361-6501/aba282)
- **Sparsity2DL: Image Reconstruction: From Sparsity to Data-Adaptive Methods and Machine Learning** — _Proc. IEEE 2020_ · [Paper](https://doi.org/10.1109/JPROC.2019.2936204)
- **TVWFR: Sparse View CT Image Reconstruction Based on Total Variation and Wavelet Frame Regularization** — _IEEE Access 2020_ · [Paper](https://doi.org/10.1109/access.2020.2982229)
- **CT-Evolution: The Evolution of Image Reconstruction for CT: From Filtered Back Projection to Artificial Intelligence** — _Eur Radiol 2019_ · [Paper](https://doi.org/10.1007/s00330-018-5810-7)
- **DataDriven: Solving Inverse Problems Using Data-Driven Models** — _Acta Numerica 2019_ · [Paper](https://doi.org/10.1017/S0962492919000059)
- **PDE: A regional adaptive variational PDE model for computed tomography image reconstruction** — _PR 2019_ · [Paper](https://doi.org/10.1016/j.patcog.2019.03.009)
- **SISVM: Learning to Reconstruct Computed Tomography Images Directly From Sinogram Data Under A Variety of Data Acquisition Conditions** — _TMI 2019_ · [Paper](https://doi.org/10.1109/tmi.2019.2910760)
- **VVBP-tSVD: VVBP-Tensor in the FBP Algorithm: Its Properties and Application in Low-Dose CT Reconstruction** — _TMI 2019_ · [Paper](https://doi.org/10.1109/tmi.2019.2935187)
- **An Image Reconstruction Method Based on Total Variation and Wavelet Tight Frame for Limited-Angle CT** — _IEEE Access 2018_ · [Paper](https://doi.org/10.1109/access.2017.2779148)
- **PTPN: Intelligent Parameter Tuning in Optimization-Based Iterative CT Reconstruction via Deep Reinforcement Learning** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2823679)
- **RAD: Regularization analysis and design for prior-image-based X-ray CT reconstruction** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2847250)
- **Statistical Image Reconstruction Using Mixed Poisson-Gaussian Noise Model for X-Ray CT** — _preprint 2018_ · [Paper](https://arxiv.org/abs/1801.09533)
- **An improved statistical iterative algorithm for sparse-view and limited-angle CT image reconstruction** — _Sci. Rep. 2017_ · [Paper](https://doi.org/10.1038/s41598-017-11222-z)
- **Edge-preserving reconstruction from sparse projections of limited-angle computed tomography using L0-regularized gradient prior** — _Rev. Sci. Instrum. 2017_ · [Paper](https://doi.org/10.1063/1.4981132)
- **ReATV: Reweighted Anisotropic Total Variation Minimization for Limited-Angle CT Reconstruction** — _TNS 2017_ · [Paper](https://doi.org/10.1109/tns.2017.2750199)
- **SENP: Low‐dose CT reconstruction using spatially encoded nonlocal penalty** — _Med Phys 2017_ · [Paper](https://doi.org/10.1002/mp.12523)
- **Image reconstruction from few views by L0-norm optimization** — _Chinese Phys. B 2014_ · [Paper](https://doi.org/10.1088/1674-1056/23/7/078703)
- **TGV: Sparse-view x-ray CT reconstruction via total generalized variation regularization** — _PMB 2014_ · [Paper](https://doi.org/10.1088/0031-9155/59/12/2997)
- **TV-Stokes: Total Variation-Stokes Strategy for Sparse-View X-ray CT Image Reconstruction** — _TMI 2014_ · [Paper](https://doi.org/10.1109/tmi.2013.2295738)
- **ATV: A limited-angle CT reconstruction method based on anisotropic TV minimization** — _PMB 2013_ · [Paper](https://doi.org/10.1088/0031-9155/58/7/2119)
- **Feature constrained compressed sensing CT image reconstruction from incomplete data via robust principal component analysis of the database** — _PMB 2013_ · [Paper](https://doi.org/10.1088/0031-9155/58/12/4047)
- **Image reconstruction based on total-variation minimization and alternating direction method in linear scan computed tomography** — _Chinese Phys. B 2013_ · [Paper](https://doi.org/10.1088/1674-1056/22/7/078701)
- **Iterative CT Reconstruction Using Shearlet-Based Regularization** — _TNS 2013_ · [Paper](https://doi.org/10.1109/tns.2013.2275994)
- **Iterative Image Reconstruction for Sparse-View CT Using Normal-Dose Image Induced Total Variation Prior** — _PLoS One 2013_ · [Paper](https://doi.org/10.1371/journal.pone.0079709)
- **Sparse Tomography** — _SIAM J. Sci. Comput. 2013_ · [Paper](https://doi.org/10.1137/120876277)
- **AWTV: Adaptive-weighted total variation minimization for sparse data toward low-dose x-ray computed tomography image reconstruction** — _PMB 2012_ · [Paper](https://doi.org/10.1088/0031-9155/57/23/7923)
- **Few-view image reconstruction with dual dictionaries** — _PMB 2012_ · [Paper](https://doi.org/10.1088/0031-9155/57/1/173)
- **Low-Dose X-ray CT Reconstruction via Dictionary Learning** — _TMI 2012_ · [Paper](https://doi.org/10.1109/tmi.2012.2195669)
- **Task-based performance analysis of FBP, SART and ML for digital breast tomosynthesis using signal CNR and Channelised Hotelling Observers** — _Med Image Anal 2011_ · [Paper](https://doi.org/10.1016/j.media.2010.07.004)
- **Compressed sensing based cone-beam computed tomography reconstruction with a first-order method** — _Med Phys 2010_ · [Paper](https://doi.org/10.1118/1.3481510)
- **Few-View Projection Reconstruction With an Iterative Reconstruction-Reprojection Algorithm and TV Constraint** — _TNS 2009_ · [Paper](https://doi.org/10.1109/tns.2008.2009990)
- **Why do commercial CT scanners still employ traditional, filtered back-projection for image reconstruction?** — _Inverse Problems 2009_ · [Paper](https://doi.org/10.1088/0266-5611/25/12/123009)
- **Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization** — _PMB 2008_ · [Paper](https://doi.org/10.1088/0031-9155/53/17/021)
- **Compressed sensing** — _TIT 2006_ · [Paper](https://doi.org/10.1109/tit.2006.871582)
- **K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation** — _TSP 2006_ · [Paper](https://doi.org/10.1109/tsp.2006.881199)
- **Robust uncertainty principles: exact signal reconstruction from highly incomplete frequency information** — _TIT 2006_ · [Paper](https://doi.org/10.1109/tit.2005.862083)
- **ROF: Nonlinear total variation based noise removal algorithms** — _Physica D 1992_ · [Paper](https://doi.org/10.1016/0167-2789(92)90242-f)
- **FDK: Practical cone-beam algorithm** — _JOSA A 1984_ · [Paper](https://doi.org/10.1364/JOSAA.1.000612)
- **SART: Simultaneous Algebraic Reconstruction Technique (SART): A superior implementation of the ART algorithm** — _Ultrasonic Imaging 1984_ · [Paper](https://doi.org/10.1016/0161-7346(84)90008-7)
- **MLEM: Maximum Likelihood Reconstruction for Emission Tomography** — _TMI 1982_ · [Paper](https://doi.org/10.1109/tmi.1982.4307558)
- **Shepp-Logan: The Fourier reconstruction of a head section** — _TNS 1974_ · [Paper](https://doi.org/10.1109/tns.1974.6499235)
- **Three-dimensional Reconstruction from Radiographs and Electron Micrographs: Application of Convolutions instead of Fourier Transforms** — _PNAS 1971_ · [Paper](https://doi.org/10.1073/pnas.68.9.2236)
- **Über die Bestimmung von Funktionen durch ihre Integralwerte längs gewisser Mannigfaltigkeiten (Johann Radon)** — _Ber. Verh. Sächs. Akad. Wiss. Leipzig, Math.-Phys. Kl. 1917_ · [Paper](https://doi.org/10.1109/TMI.1986.4307775)

  The paper that defines the Radon transform — the forward operator every analytic method here inverts, published 54 years before the first CT scanner. The original appeared in the Leipzig academy reports, volume 69, pages 262–277; the link is P. C. Parks's English translation, "On the determination of functions from their integral values along certain manifolds", IEEE Transactions on Medical Imaging 5(4):170–176, 1986.

### Sparse-View CT

<sub>Reconstruction from a reduced number of projection angles · 137 papers</sub>

- **3D Field of Junctions: A Noise-Robust, Training-Free Structural Prior for Volumetric Inverse Problems** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2603.02149) · [Code](https://github.com/voilalab/3D-Field-of-Junctions)
- **CG-GLORE: A Conjugate Gradient-Based Global-Local Regularization Network for Sparse-View CT Reconstruction** — _BMVC 2026_ · [Paper](https://arxiv.org/abs/2608.15246)
- **Conditional Diffusion Posterior Alignment for Sparse-View CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2604.21960)
- **Continuity-driven Synergistic Diffusion with Neural Priors for Ultra-Sparse-View CBCT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.07980)
- **Cross-Distribution Diffusion Priors-Driven Iterative Reconstruction for Sparse-View CT** — _TMI 2026_ · [Paper](https://arxiv.org/abs/2509.13576)
- **DC-PnPDP: Plug-and-Play Diffusion Meets ADMM: Dual-Variable Coupling for Robust Medical Image Reconstruction** — _ICML 2026_ · [Paper](https://arxiv.org/abs/2602.23214) · [Code](https://github.com/duchenhe/DC-PnPDP) · [Project](https://duchenhe.com/project/DCPnPDP/)
- **DeepSparse: A Foundation Model for Sparse-View CBCT Reconstruction** — _TMI 2026_ · [Paper](https://doi.org/10.1109/tmi.2026.3674948) · [Code](https://github.com/xmed-lab/DeepSparse)

  DiCE (Dual-Dimensional Cross-Scale Embedding) pre-trained by HyViP (Hybrid View Sampling Pretraining) on both sparse- and dense-view projections, then fine-tuned in two steps. Presented as the first foundation model for sparse-view CBCT.
- **DiffNR: Diffusion-Enhanced Neural Representation Optimization for Sparse-View 3D Tomographic Reconstruction** — _AAAI 2026_ · [Paper](https://arxiv.org/abs/2604.21518) · [Project](https://ooonesevennn.github.io/DiffNR/)
- **Efficient Unrolled Networks for Large-Scale 3D Inverse Problems** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2601.02141) · [Code](https://github.com/romainvo/efficient-unrolling)
- **Event-Based Sparse-View Background-Oriented Schlieren Tomography** — _ECCV 2026_ · [Paper](https://doi.org/10.1007/978-3-032-37335-9_18)
- **From Sparse X-rays to 3D CT: Training-Free Reconstruction with Diffusion Priors** — _DGM4MICCAI 2026_ · [Paper](https://arxiv.org/abs/2606.20763) · [Code](https://github.com/Fredy-Zhang/TF-PRDiT)
- **GR-Gaussian: Graph-Based Radiative Gaussian Splatting for Sparse-View Tomography** — _TCI 2026_ · [Paper](https://doi.org/10.1109/TCI.2026.3701585)
- **ILV: Iterative Latent Volumes for Fast and Accurate Sparse-View CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2603.14915) · [Project](https://sngryonglee.github.io/ILV/)
- **ISCS: Improving 2D Diffusion Models for 3D Medical Imaging with Inter-Slice Consistent Stochasticity** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2602.04162) · [Code](https://github.com/duchenhe/ISCS)
- **KLIP: Localized Distribution Shift Detection via KL-Divergence with Diffusion Priors in Inverse Problems** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2605.31596) · [Code](https://github.com/voilalab/KLIP)
- **Learning Where and What to Lift for Bi-planar X-ray-to-CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2608.17255)
- **LUCID: Learned Undersampling-Adaptive Consistency-Guided Inference with Deterministic Flow Matching for Sparse-View CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2606.16212)
- **NAB: Neural Adaptive Binning for Sparse-View CT Reconstruction** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2602.02356) · [Code](https://github.com/Wangduo-Xie/NAB_CT_reconstruction)
- **Projection-Volume Fidelity Divergence: Diagnosing and Controlling Optimization Drift in Sparse-View 3D Gaussian Tomography** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2606.22525)
- **Revisiting Pose Sensitivity in Splat-based Computed Tomography under Sparse-view Reconstruction** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2608.04752)
- **Shape-guided Gaussian Splatting for Sparse-View X-ray 3D Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2609.10376) · [Code](https://github.com/polyshape-lab/ShapeGuidedGaussian)
- **TAMP: Imaging foundation model for universal enhancement of non-ideal measurement CT** — _Nat Commun 2026_ · [Paper](https://doi.org/10.1038/s41467-026-73943-y) · [Code](https://github.com/YutingHe-list/TAMP)

  Multi-scale integrated Transformer Amplifier. Pre-trained on 10.8M physics-driven simulated non-ideal-measurement images, then adapted to a protocol with a parameter-efficient fine-tune on a few slices — one backbone for low-dose, sparse-view and limited-angle at once.
- **Tomographic Sparse View Selection Using the View Covariance Loss** — _TPAMI 2026_ · [Paper](https://doi.org/10.1109/TPAMI.2025.3600072)
- **Towards reconstructing experimental sparse-view X-ray CT data with diffusion models** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.12755)
- **Variational Garrote for Sparse Inverse Problems** — _J. Comput. Sci. 2026_ · [Paper](https://doi.org/10.1016/j.jocs.2026.102980)
- **XDen-1K: A Density Field Dataset of Real-World Objects** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2512.10668)
- **A CT Geometry With Multiple Centers Of Rotation For Solving Sparse View Problem** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2502.06125)
- **Adaptive Diffusion Models for Sparse-View Motion-Corrected Head Cone-beam CT** — _TRPMS 2025_ · [Paper](https://arxiv.org/abs/2504.14033) · [Project](https://antoinedepaepe.github.io/jrm-adm-io/)
- **An unsupervised sparse-view CT reconstruction framework using combination of iterative deep image prior and ADMM** — _Med Phys 2025_ · [Paper](https://doi.org/10.1002/mp.17933)
- **Are Pixel-Wise Metrics Reliable for Sparse-View Computed Tomography Reconstruction?** — _NeurIPS 2025_ · [Paper](https://arxiv.org/abs/2506.02093) · [Code](https://github.com/MrGiovanni/CARE)
- **CvG-Diff: Cross-View Generalized Diffusion Model for Sparse-View CT Reconstruction** — _MICCAI 2025_ · [Paper](https://doi.org/10.1007/978-3-032-05325-1_14) · [Code](https://github.com/xmed-lab/CvG-Diff)
- **Investigating the effects of machine learning generalization for enhancing accuracy in fast X-ray computed tomography for industrial metrology** — _CIRP Annals 2025_ · [Paper](https://doi.org/10.1016/j.cirp.2025.04.025)
- **Latent Space Consistency for Sparse-View CT Reconstruction** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2507.11152)
- **LCTfound: A lung CT vision foundation model facilitating disease diagnosis and medical imaging** — _Nat Commun 2025_ · [Paper](https://doi.org/10.1038/s41467-025-66620-z) · [Code](https://github.com/gingerbread000/LCTfound) · [Data](https://huggingface.co/datasets/GuoxunZhang1997/LCTfound)

  Diffusion-pretrained on 105,184 multi-centre lung CT scans with joint encoding of images and clinical text. Eight downstream tasks, of which CT enhancement and sparse-view reconstruction are the reconstruction-relevant ones.
- **MInDI-3D: Iterative Deep Learning in 3D for Sparse-view Cone Beam Computed Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.09616)
- **Mitigating Data Consistency Induced Discrepancy in Cascaded Diffusion Models for Sparse-View CT Reconstruction** — _TMI 2025_ · [Paper](https://doi.org/10.1109/tmi.2025.3557243)
- **Neural Discrete Representation Learning for Sparse-View CBCT Reconstruction: From Algorithm Design to Prospective Multicenter Clinical Evaluation** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2512.00873)
- **Ordered-subsets Multi-diffusion Model for Sparse-view CT Reconstruction** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2505.09985)
- **Recover Biological Structure from Sparse-View Diffraction Images with Neural Volumetric Prior** — _ICCV 2025_ · [Paper](https://arxiv.org/abs/2510.16391)
- **Resolution-Agnostic Neural Operators for Multi-Rate Sparse-View CT** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2512.12236) · [Code](https://github.com/neuraloperator/sparse_ct)
- **Semantic contrastive learning for orthogonal X-ray computed tomography reconstruction** — _Fully3D 2025_ · [Paper](https://arxiv.org/abs/2512.22674)
- **Spener: Unsupervised Self-Prior Embedding Neural Representation for Sparse-View CT Reconstruction** — _AAAI 2025_ · [Paper](https://doi.org/10.1609/aaai.v39i7.32794) · [Code](https://github.com/MeijiTian/Spener)
- **Steerable Conditional Diffusion for Out-of-Distribution Adaptation in Medical Image Reconstruction** — _TMI 2025_ · [Paper](https://doi.org/10.1109/tmi.2024.3524797)
- **Swap-Net: A Memory-Efficient 2.5D Network for Sparse-View 3D Cone Beam CT Reconstruction to ICF Applications** — _TCI 2025_ · [Paper](https://doi.org/10.1109/tci.2025.3572699)
- **When are Diffusion Priors Helpful in Sparse Reconstruction? A Study with Sparse-view CT** — _ISBI 2025_ · [Paper](https://arxiv.org/abs/2502.02771)
- **X-GRM: Large Gaussian Reconstruction Model for Sparse-view X-rays to Computed Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2505.15235) · [Code](https://github.com/CUHK-AIM-Group/X-GRM)
- **XGenRecon: A New Perspective in Ultrasparse Volumetric CBCT Reconstruction Through Geometry-Controlled X-Ray Projection Generation** — _TRPMS 2025_ · [Paper](https://doi.org/10.1109/trpms.2024.3420742)
- **A Review of Deep Learning CT Reconstruction From Incomplete Projection Data** — _TRPMS 2024_ · [Paper](https://doi.org/10.1109/trpms.2023.3316349)
- **BaggageCT: Fan-Beam CT Reconstruction for Unaligned Sparse-View X-Ray Baggage Data** — _preprint 2024_ · [Paper](https://arxiv.org/abs/2412.03036)
- **DIF-Gaussian: Learning 3D Gaussians for Extremely Sparse-View Cone-Beam CT Reconstruction** — _MICCAI 2024_ · [Paper](https://doi.org/10.1007/978-3-031-72104-5_41) · [Code](https://github.com/xmed-lab/DIF-Gaussian)
- **Generative Modeling in Sinogram Domain for Sparse-view CT Reconstruction** — _TRPMS 2024_ · [Paper](https://doi.org/10.1109/trpms.2023.3309474)
- **INR-Joint: Implicit Neural Representations for Robust Joint Sparse-View CT Reconstruction** — _TMLR 2024_ · [Paper](https://arxiv.org/abs/2405.02509) · [Code](https://github.com/jiayangshi/INR4JointCTRecon)
- **Machine learning based sinogram interpolation for X-ray computed tomography validated on experimental data** — _Precis. Eng. 2024_ · [Paper](https://doi.org/10.1016/j.precisioneng.2024.02.020)
- **Neural Field Regularization by Denoising for 3D Sparse-View X-Ray Computed Tomography** — _3DV 2024_ · [Paper](https://doi.org/10.1109/3dv62453.2024.00094)
- **Plug-and-Play Learned Proximal Trajectory for 3D Sparse-View X-Ray Computed Tomography** — _ECCV 2024_ · [Paper](https://doi.org/10.1007/978-3-031-72761-0_13)
- **R2-Gaussian: Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction** — _NeurIPS 2024_ · [Paper](https://arxiv.org/abs/2405.20693) · [Code](https://github.com/Ruyi-Zha/r2_gaussian)
- **RBP-DIP: Residual back projection with deep image prior for ill-posed CT reconstruction** — _Neural Netw. 2024_ · [Paper](https://doi.org/10.1016/j.neunet.2024.106740)
- **SAX-NeRF: Structure-Aware Sparse-View X-Ray 3D Reconstruction** — _CVPR 2024_ · [Paper](https://doi.org/10.1109/cvpr52733.2024.01062) · [Code](https://github.com/caiyuanhao1998/SAX-NeRF)
- **SWORD: Stage-by-Stage Wavelet Optimization Refinement Diffusion Model for Sparse-View CT Reconstruction** — _TMI 2024_ · [Paper](https://doi.org/10.1109/tmi.2024.3355455) · [Code](https://github.com/yqx7150/SWORD)
- **Two-View Industrial CT Reconstruction Based on a Multiscale Conditional Latent Diffusion Network** — _TIM 2024_ · [Paper](https://doi.org/10.1109/TIM.2024.3476543)
- **Wavelet-Improved Score-Based Generative Model for Medical Imaging** — _TMI 2024_ · [Paper](https://doi.org/10.1109/tmi.2023.3325824)
- **DDDM: Dual-Domain Diffusion Model for Sparse-View CT Reconstruction** — _preprint 2023_ · [Paper](https://doi.org/10.36227/techrxiv.23726703) · [Code](https://github.com/YC-Markus/code-for-DDDM)
- **DEAR: Deep Embedding-Attention-Refinement for Sparse-View CT Reconstruction** — _TIM 2023_ · [Paper](https://doi.org/10.1109/tim.2022.3221136)
- **DREAM-Net: Deep Residual Error Iterative Minimization Network for Sparse-View CT Reconstruction** — _JBHI 2023_ · [Paper](https://doi.org/10.1109/jbhi.2022.3225697)
- **Fast algorithms based on Empirical Interpolation Methods for selecting best projections in Sparse-View X-ray Computed Tomography using a priori information** — _NDT&E Int. 2023_ · [Paper](https://doi.org/10.1016/j.ndteint.2022.102768)
- **FreeSeed: Frequency-Band-Aware and Self-Guided Network for Sparse-View CT Reconstruction** — _MICCAI 2023_ · [Paper](https://doi.org/10.1007/978-3-031-43999-5_24) · [Code](https://github.com/Masaaki-75/freeseed)
- **LEARN++: Recurrent Dual-Domain Reconstruction Network for Compressed Sensing CT** — _TRPMS 2023_ · [Paper](https://doi.org/10.1109/trpms.2022.3222213)
- **MDST: multi-domain sparse-view CT reconstruction based on convolution and swin transformer** — _PMB 2023_ · [Paper](https://doi.org/10.1088/1361-6560/acc2ab)
- **PINER: Prior-Informed Implicit Neural Representation Learning for Test-Time Adaptation in Sparse-View CT Reconstruction** — _WACV 2023_ · [Paper](https://doi.org/10.1109/wacv56688.2023.00197) · [Code](https://github.com/efzero/PINER)
- **Sparse-View Cone Beam CT Reconstruction Using Data-Consistent Supervised and Adversarial Learning From Scarce Training Data** — _TCI 2023_ · [Paper](https://doi.org/10.1109/TCI.2022.3225680)
- **SPIE-DIR: Self-Prior Information Enhanced Deep Iterative Reconstruction Using Two Complementary Limited-Angle Scans for DECT** — _TIM 2023_ · [Paper](https://doi.org/10.1109/tim.2022.3227549)
- **The realisation of fast X-ray computed tomography using a limited number of projection images for dimensional metrology** — _NDT&E Int. 2023_ · [Paper](https://doi.org/10.1016/j.ndteint.2023.102852)
- **An Educated Warm Start for Deep Image Prior-Based Micro CT Reconstruction** — _TCI 2022_ · [Paper](https://doi.org/10.1109/tci.2022.3233188)
- **DDCL: Dual domain closed-loop learning for sparse-view CT reconstruction** — _ICIFXCT 2022_ · [Paper](https://doi.org/10.1117/12.2646639)
- **DuDoDR-Net: Dual-domain data consistent recurrent network for simultaneous sparse view and metal artifact reduction in computed tomography** — _Med Image Anal 2022_ · [Paper](https://doi.org/10.1016/j.media.2021.102289)
- **DuDoTrans: Dual-Domain Transformer for Sparse-View CT Reconstruction** — _MLMIR 2022_ · [Paper](https://doi.org/10.1007/978-3-031-17247-2_9) · [Code](https://github.com/cewang-sysu/DuDoTrans)
- **NAF: Neural Attenuation Fields for Sparse-View CBCT Reconstruction** — _MICCAI 2022_ · [Paper](https://arxiv.org/abs/2209.14540) · [Code](https://github.com/Ruyi-Zha/naf_cbct)
- **PLANet: Learning Projection Views for Sparse-View CT Reconstruction** — _ACM MM 2022_ · [Paper](https://doi.org/10.1145/3503161.3548204)
- **SNAF: Sparse-View CBCT Reconstruction with Neural Attenuation Fields** — _preprint 2022_ · [Paper](https://arxiv.org/abs/2211.17048)
- **UNDIP: Sparse-view and limited-angle CT reconstruction with untrained networks and deep image prior** — _CMPB 2022_ · [Paper](https://doi.org/10.1016/j.cmpb.2022.107167)
- **CD-Net: Comprehensive Domain Network With Spectral Complementary for DECT Sparse-View Reconstruction** — _TCI 2021_ · [Paper](https://doi.org/10.1109/tci.2021.3070184)
- **DL-PICCS: Accurate and robust sparse-view angle CT image reconstruction using deep learning and prior image constrained compressed sensing (DL-PICCS)** — _Med Phys 2021_ · [Paper](https://doi.org/10.1002/mp.15183)
- **DRONE: Dual-Domain Residual-Based Optimization Network for Sparse-View CT Reconstruction** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3078067) · [Code](https://github.com/weiwenwu12/DRONE)
- **FDM: Degradation-Aware Deep Learning Framework for Sparse-View CT Reconstruction** — _Tomography 2021_ · [Paper](https://doi.org/10.3390/tomography7040077) · [Code](https://github.com/sunchang2017/degradation-aware-sparse-CT-reconstruction)
- **LMFI: Learnable Multi-scale Fourier Interpolation for Sparse View CT Image Reconstruction** — _MICCAI 2021_ · [Paper](https://doi.org/10.1007/978-3-030-87231-1_28)
- **MetaInv-Net: Meta Inversion Network for Sparse View CT Image Reconstruction** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2020.3033541) · [Code](https://github.com/haimiaozh/MetaInv-Net)
- **2-Step Sparse-View CT Reconstruction with a Domain-Specific Perceptual Network** — _preprint 2020_ · [Paper](https://arxiv.org/abs/2012.04743)
- **AirNet: Fused analytical and iterative reconstruction with deep neural network regularization for sparse-data CT** — _Med Phys 2020_ · [Paper](https://doi.org/10.1002/mp.14170)
- **DEER: Deep efficient end-to-end reconstruction (DEER) network for few-view breast CT image reconstruction** — _IEEE Access 2020_ · [Paper](https://doi.org/10.1109/access.2020.3033795) · [Code](https://github.com/WANG-AXIS/DEER)
- **DLMIR: Deep learning methods for image reconstruction from angularly sparse data for CT and SAR imaging** — _ASARI 2020_ · [Paper](https://doi.org/10.1117/12.2558953) · [Code](https://github.com/e-yavuz/Deep-Learning-Methods-for-Image-Reconstruction-from-Angularly-Sparse-Data-for-CT-and-SAR-Imaging)
- **ETEDN: An End-to-End Deep Network for Reconstructing CT Images Directly From Sparse Sinograms** — _TCI 2020_ · [Paper](https://doi.org/10.1109/tci.2020.3039385) · [Code](https://github.com/wangwei-cmd/CT-image-reconstruction)
- **HDNet: Hybrid-domain neural network processing for sparse-view CT reconstruction** — _TRPMS 2020_ · [Paper](https://doi.org/10.1109/trpms.2020.3011413)
- **Moreau-envelope-enhanced nonlocal shearlet transform and total variation for sparse-view CT reconstruction** — _Meas. Sci. Technol. 2020_ · [Paper](https://doi.org/10.1088/1361-6501/aba282)
- **Multi-Scale Learned Iterative Reconstruction** — _TCI 2020_ · [Paper](https://doi.org/10.1109/TCI.2020.2990299)
- **REDAEP: Robust and Enhanced Denoising Autoencoding Prior for Sparse-View CT Reconstruction** — _TRPMS 2020_ · [Paper](https://doi.org/10.1109/trpms.2020.2989634)
- **SISTER: Spectral-Image Similarity-Based Tensor With Enhanced-Sparsity Reconstruction for Sparse-View Multi-Energy CT** — _TCI 2020_ · [Paper](https://doi.org/10.1109/tci.2019.2956886)
- **Sparse-view CT reconstruction based on multi-level wavelet convolution neural network** — _Phys. Med. 2020_ · [Paper](https://doi.org/10.1016/j.ejmp.2020.11.021)
- **TVWFR: Sparse View CT Image Reconstruction Based on Total Variation and Wavelet Frame Regularization** — _IEEE Access 2020_ · [Paper](https://doi.org/10.1109/access.2020.2982229)
- **A deep learning reconstruction framework for X-ray computed tomography with incomplete data** — _PLoS One 2019_ · [Paper](https://doi.org/10.1371/journal.pone.0224426)
- **Convolutional Sparse Coding for Compressed Sensing CT Reconstruction** — _TMI 2019_ · [Paper](https://doi.org/10.1109/tmi.2019.2906853)
- **DNNSS: Deep-neural-network-based sinogram synthesis for sparse-view CT image reconstruction** — _TRPMS 2019_ · [Paper](https://doi.org/10.1109/trpms.2018.2867611)
- **Extreme Few-view CT Reconstruction using Deep Inference** — _preprint 2019_ · [Paper](https://arxiv.org/abs/1910.05375)
- **iCTNet: Sinogram interpolation for sparse-view micro-CT with deep learning neural network** — _SPIE MI 2019_ · [Paper](https://arxiv.org/abs/1902.03362) · [Code](https://github.com/Swapneel7/Sparse-CT-Reconstruction-using-Deep-learning)
- **PSRV: Patient-specific reconstruction of volumetric computed tomography images from a single projection view via deep learning** — _Nat Biomed Eng 2019_ · [Paper](https://doi.org/10.1038/s41551-019-0466-4)
- **SPARE: Sparse-view reconstruction challenge for 4D cone-beam CT from a 1-min scan** — _Med Phys 2019_ · [Paper](https://doi.org/10.1002/mp.13687)
- **SPSS: Sharpness preserved sinogram synthesis using convolutional neural network for sparse-view CT imaging** — _SPIE MI 2019_ · [Paper](https://doi.org/10.1117/12.2512894)
- **DD-Net: A Sparse-View CT Reconstruction Method Based on Combination of DenseNet and Deconvolution** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2823338) · [Code](https://github.com/zzc623/DD_Net)
- **TFU-Net: Framing U-Net via Deep Convolutional Framelets - Application to Sparse-view CT** — _TMI 2018_ · [Paper](https://arxiv.org/abs/1708.08333)
- **An improved statistical iterative algorithm for sparse-view and limited-angle CT image reconstruction** — _Sci. Rep. 2017_ · [Paper](https://doi.org/10.1038/s41598-017-11222-z)
- **Coded aperture optimization in compressive X-ray tomography: a gradient descent approach** — _Opt. Express 2017_ · [Paper](https://doi.org/10.1364/oe.25.023833)
- **Deep Convolutional Neural Network for Inverse Problems in Imaging** — _TIP 2017_ · [Paper](https://doi.org/10.1109/tip.2017.2713099)
- **Edge-preserving reconstruction from sparse projections of limited-angle computed tomography using L0-regularized gradient prior** — _Rev. Sci. Instrum. 2017_ · [Paper](https://doi.org/10.1063/1.4981132)
- **SPIR: Dual energy CT with one full scan and a second sparse-view scan using structure preserving iterative reconstruction (SPIR)** — _PMB 2016_ · [Paper](https://doi.org/10.1088/0031-9155/61/18/6684)
- **Sparse-View Spectral CT Reconstruction Using Spectral Patch-Based Low-Rank Penalty** — _TMI 2015_ · [Paper](https://doi.org/10.1109/tmi.2014.2380993)
- **Tensor-based dictionary learning for dynamic tomographic reconstruction** — _PMB 2015_ · [Paper](https://doi.org/10.1088/0031-9155/60/7/2803)
- **Image reconstruction from few views by L0-norm optimization** — _Chinese Phys. B 2014_ · [Paper](https://doi.org/10.1088/1674-1056/23/7/078703)
- **Low-dose X-ray computed tomography image reconstruction with a combined low-mAs and sparse-view protocol** — _Opt. Express 2014_ · [Paper](https://doi.org/10.1364/oe.22.015190)
- **Sparse-view computed laminography with a spherical sinusoidal scan for nondestructive testing** — _Opt. Express 2014_ · [Paper](https://doi.org/10.1364/oe.22.017745)
- **TGV: Sparse-view x-ray CT reconstruction via total generalized variation regularization** — _PMB 2014_ · [Paper](https://doi.org/10.1088/0031-9155/59/12/2997)
- **TV-Stokes: Total Variation-Stokes Strategy for Sparse-View X-ray CT Image Reconstruction** — _TMI 2014_ · [Paper](https://doi.org/10.1109/tmi.2013.2295738)
- **Effects of sparse sampling schemes on image quality in low-dose CT** — _Med Phys 2013_ · [Paper](https://doi.org/10.1118/1.4825096)
- **Feature constrained compressed sensing CT image reconstruction from incomplete data via robust principal component analysis of the database** — _PMB 2013_ · [Paper](https://doi.org/10.1088/0031-9155/58/12/4047)
- **Image reconstruction based on total-variation minimization and alternating direction method in linear scan computed tomography** — _Chinese Phys. B 2013_ · [Paper](https://doi.org/10.1088/1674-1056/22/7/078701)
- **Iterative CT Reconstruction Using Shearlet-Based Regularization** — _TNS 2013_ · [Paper](https://doi.org/10.1109/tns.2013.2275994)
- **Iterative Image Reconstruction for Sparse-View CT Using Normal-Dose Image Induced Total Variation Prior** — _PLoS One 2013_ · [Paper](https://doi.org/10.1371/journal.pone.0079709)
- **Optimization-based image reconstruction from sparse-view data in offset-detector CBCT** — _PMB 2013_ · [Paper](https://doi.org/10.1088/0031-9155/58/2/205)
- **Sparse Tomography** — _SIAM J. Sci. Comput. 2013_ · [Paper](https://doi.org/10.1137/120876277)
- **AWTV: Adaptive-weighted total variation minimization for sparse data toward low-dose x-ray computed tomography image reconstruction** — _PMB 2012_ · [Paper](https://doi.org/10.1088/0031-9155/57/23/7923)
- **Few-view image reconstruction with dual dictionaries** — _PMB 2012_ · [Paper](https://doi.org/10.1088/0031-9155/57/1/173)
- **Compressed sensing based cone-beam computed tomography reconstruction with a first-order method** — _Med Phys 2010_ · [Paper](https://doi.org/10.1118/1.3481510)
- **Evaluation of sparse-view reconstruction from flat-panel-detector cone-beam CT** — _PMB 2010_ · [Paper](https://doi.org/10.1088/0031-9155/55/22/001)
- **Directional View Interpolation for Compensation of Sparse Angular Sampling in Cone-Beam CT** — _TMI 2009_ · [Paper](https://doi.org/10.1109/tmi.2008.2011550)
- **Few-View Projection Reconstruction With an Iterative Reconstruction-Reprojection Algorithm and TV Constraint** — _TNS 2009_ · [Paper](https://doi.org/10.1109/tns.2008.2009990)
- **X-ray cargo container inspection system with few-view projection imaging** — _NIMA 2009_ · [Paper](https://doi.org/10.1016/j.nima.2008.08.151)
- **Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization** — _PMB 2008_ · [Paper](https://doi.org/10.1088/0031-9155/53/17/021)
- **Compressed sensing** — _TIT 2006_ · [Paper](https://doi.org/10.1109/tit.2006.871582)
- **Robust uncertainty principles: exact signal reconstruction from highly incomplete frequency information** — _TIT 2006_ · [Paper](https://doi.org/10.1109/tit.2005.862083)

### Limited-Angle Tomography

<sub>Missing angular wedge, where the null space makes the problem severely ill-posed · 45 papers</sub>

- **CryoDeRec: A Supervised Multi-task Framework for Joint cryo-ET Restoration Enabled by Generative Physical Simulation** — _CVPR 2026_ · [Paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_A_Supervised_Multi-task_Framework_for_Joint_cryo-ET_Restoration_Enabled_by_CVPR_2026_paper.html) · [Code](https://github.com/ZhidongYang/CryoDeRec)
- **DC-PnPDP: Plug-and-Play Diffusion Meets ADMM: Dual-Variable Coupling for Robust Medical Image Reconstruction** — _ICML 2026_ · [Paper](https://arxiv.org/abs/2602.23214) · [Code](https://github.com/duchenhe/DC-PnPDP) · [Project](https://duchenhe.com/project/DCPnPDP/)
- **Equivariance2Inverse: A Practical Self-Supervised CT Reconstruction Method Benchmarked on Real, Limited-Angle, and Blurred Data** — _TCI 2026_ · [Paper](https://arxiv.org/abs/2510.23317)
- **Geometry-Aware Diffusion Approximate Posterior Sampling for Sparse-View and Limited-Angle CT** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2610.08866)
- **High-Precision Image Reconstruction for Binary-Valued X-Ray CT From Limited-View Projections** — _TIM 2026_ · [Paper](https://doi.org/10.1109/tim.2026.3670565)
- **OpenPros: A Large-Scale Dataset for Limited View Prostate Ultrasound Computed Tomography** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2505.12261) · [Project](https://open-pros.github.io/)
- **TAMP: Imaging foundation model for universal enhancement of non-ideal measurement CT** — _Nat Commun 2026_ · [Paper](https://doi.org/10.1038/s41467-026-73943-y) · [Code](https://github.com/YutingHe-list/TAMP)

  Multi-scale integrated Transformer Amplifier. Pre-trained on 10.8M physics-driven simulated non-ideal-measurement images, then adapted to a protocol with a parameter-efficient fine-tune on a few slices — one backbone for low-dose, sparse-view and limited-angle at once.
- **Advancing Limited-Angle CT Reconstruction Through Diffusion-Based Sinogram Completion** — _ICIP 2025_ · [Paper](https://arxiv.org/abs/2505.19385)
- **Data-Efficient Limited-Angle CT Using Deep Priors and Regularization** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2502.12293)
- **Diffusion-Based Limited-Angle CT Reconstruction under Noisy Conditions** — _ICIP 2025_ · [Paper](https://arxiv.org/abs/2507.05647)
- **End-to-End Deep Learning for Interior Tomography with Low-Dose X-ray CT** — _PMB 2025_ · [Paper](https://arxiv.org/abs/2501.05085)
- **Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency** — _ISBI 2025_ · [Paper](https://arxiv.org/abs/2411.06181)
- **Limited-Angle CBCT Reconstruction via Geometry-Integrated Cycle-domain Denoising Diffusion Probabilistic Models** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2506.13545)
- **Limited-angle SPECT image reconstruction using deep image prior** — _PMB 2025_ · [Paper](https://arxiv.org/abs/2503.18342)
- **Limited-angle x-ray nano-tomography with machine-learning enabled iterative reconstruction engine** — _npj Comput Mater 2025_ · [Paper](https://doi.org/10.1038/s41524-025-01724-0)
- **Projection Embedded Diffusion Bridge for CT Reconstruction from Incomplete Data** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2510.22605)
- **SIRE-Net: Structure-Integrated Refinement and Enhancement Network for Limited-Angle CT Reconstruction** — _TIM 2025_ · [Paper](https://doi.org/10.1109/tim.2025.3568935)
- **A Review of Deep Learning CT Reconstruction From Incomplete Projection Data** — _TRPMS 2024_ · [Paper](https://doi.org/10.1109/trpms.2023.3316349)
- **Dolce: A Model-Based Probabilistic Diffusion Framework for Limited-Angle CT Reconstruction** — _ICCV 2023_ · [Paper](https://doi.org/10.1109/ICCV51070.2023.00963)
- **SPIE-DIR: Self-Prior Information Enhanced Deep Iterative Reconstruction Using Two Complementary Limited-Angle Scans for DECT** — _TIM 2023_ · [Paper](https://doi.org/10.1109/tim.2022.3227549)
- **DIOR: Deep Iterative Optimization-Based Residual-Learning for Limited-Angle CT Reconstruction** — _TMI 2022_ · [Paper](https://doi.org/10.1109/tmi.2022.3148110)
- **UNDIP: Sparse-view and limited-angle CT reconstruction with untrained networks and deep image prior** — _CMPB 2022_ · [Paper](https://doi.org/10.1016/j.cmpb.2022.107167)
- **CasRedSCAN: Limited View Tomographic Reconstruction Using a Cascaded Residual Dense Spatial-Channel Attention Network With Projection Data Fidelity Layer** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3066318)
- **DCTR: Dynamic CT Reconstruction From Limited Views With Implicit Neural Representations** — _ICCV 2021_ · [Paper](https://doi.org/10.1109/iccv48922.2021.00226)
- **Limited-Angle CT Reconstruction via the L1/L2 Minimization** — _SIAM J. Imaging Sci. 2021_ · [Paper](https://doi.org/10.1137/20m1341490)
- **SPECIAL: Single-Shot Projection Error Correction Integrated Adversarial Learning for Limited-Angle CT** — _TCI 2021_ · [Paper](https://doi.org/10.1109/tci.2021.3098922)
- **Deep learning based image reconstruction algorithm for limited-angle translational computed tomography** — _PLoS One 2020_ · [Paper](https://doi.org/10.1371/journal.pone.0226963)
- **HD-CNN: Artifact removal using a hybrid-domain convolutional neural network for limited-angle computed tomography imaging** — _PMB 2020_ · [Paper](https://doi.org/10.1088/1361-6560/ab9066)
- **ℓ₀DL: Limited-Angle X-Ray CT Reconstruction Using Image Gradient ℓ₀-Norm With Dictionary Learning** — _TRPMS 2020_ · [Paper](https://doi.org/10.1109/trpms.2020.2991887)
- **A deep learning reconstruction framework for X-ray computed tomography with incomplete data** — _PLoS One 2019_ · [Paper](https://doi.org/10.1371/journal.pone.0224426)
- **ADMM-based deep reconstruction for limited-angle CT** — _PMB 2019_ · [Paper](https://doi.org/10.1088/1361-6560/ab1aba)
- **Laminography in the lab: imaging planar objects using a conventional x-ray CT scanner** — _Meas. Sci. Technol. 2019_ · [Paper](https://doi.org/10.1088/1361-6501/aafcae)
- **Learning the invisible: a hybrid deep learning-shearlet framework for limited angle computed tomography** — _Inverse Problems 2019_ · [Paper](https://doi.org/10.1088/1361-6420/ab10ca)
- **An Image Reconstruction Method Based on Total Variation and Wavelet Tight Frame for Limited-Angle CT** — _IEEE Access 2018_ · [Paper](https://doi.org/10.1109/access.2017.2779148)
- **CTNet: Lose The Views: Limited Angle CT Reconstruction via Implicit Sinogram Completion** — _CVPR 2018_ · [Paper](https://doi.org/10.1109/cvpr.2018.00664)
- **DLCT: Deep Learning Computed Tomography: Learning Projection-Domain Weights From Image Domain in Limited Angle Problems** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2833499)
- **An improved statistical iterative algorithm for sparse-view and limited-angle CT image reconstruction** — _Sci. Rep. 2017_ · [Paper](https://doi.org/10.1038/s41598-017-11222-z)
- **Edge-preserving reconstruction from sparse projections of limited-angle computed tomography using L0-regularized gradient prior** — _Rev. Sci. Instrum. 2017_ · [Paper](https://doi.org/10.1063/1.4981132)
- **ReATV: Reweighted Anisotropic Total Variation Minimization for Limited-Angle CT Reconstruction** — _TNS 2017_ · [Paper](https://doi.org/10.1109/tns.2017.2750199)
- **LIVE: A limited-angle intrafraction verification (LIVE) system for radiation therapy** — _Med Phys 2014_ · [Paper](https://doi.org/10.1118/1.4861820)
- **A technique for estimating 4D-CBCT using prior knowledge and limited-angle projections** — _Med Phys 2013_ · [Paper](https://doi.org/10.1118/1.4825097)
- **ATV: A limited-angle CT reconstruction method based on anisotropic TV minimization** — _PMB 2013_ · [Paper](https://doi.org/10.1088/0031-9155/58/7/2119)
- **Comparison of image quality in computed laminography and tomography** — _Opt. Express 2012_ · [Paper](https://doi.org/10.1364/oe.20.000794)
- **Task-based performance analysis of FBP, SART and ML for digital breast tomosynthesis using signal CNR and Channelised Hotelling Observers** — _Med Image Anal 2011_ · [Paper](https://doi.org/10.1016/j.media.2010.07.004)
- **A novel digital tomosynthesis (DTS) reconstruction method using a deformation field map** — _Med Phys 2008_ · [Paper](https://doi.org/10.1118/1.2940725)

### Low-Dose CT Denoising

<sub>Noise suppression at reduced tube current, in image, projection or dual domain · 58 papers</sub>

- **DenoMamba: A Fused State-Space Model for Low-Dose CT Denoising** — _JBHI 2026_ · [Paper](https://doi.org/10.1109/jbhi.2025.3629034) · [Code](https://github.com/icon-lab/DenoMamba)
- **Dose-Aware Cold Diffusion with Physics Consistency for Generalizable Low-Dose CT Reconstruction** — _IJCNN 2026_ · [Paper](https://arxiv.org/abs/2609.18943)
- **Foundation-VAE: Foundation VAEs for 3D CT Reconstruction, Augmentation, and Generation** — _ICML 2026_ · [Paper](https://arxiv.org/abs/2605.30893) · [Code](https://github.com/qic999/Foundation-VAE)
- **HARU-Net: Hybrid Attention Residual U-Net for Edge-Preserving Denoising in Cone-Beam Computed Tomography** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.22544)
- **Low-Level Dataset Distillation for Medical Image Enhancement** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2511.13106) · [Code](https://github.com/xufz123/Med_LLDD)
- **TAMP: Imaging foundation model for universal enhancement of non-ideal measurement CT** — _Nat Commun 2026_ · [Paper](https://doi.org/10.1038/s41467-026-73943-y) · [Code](https://github.com/YutingHe-list/TAMP)

  Multi-scale integrated Transformer Amplifier. Pre-trained on 10.8M physics-driven simulated non-ideal-measurement images, then adapted to a protocol with a parameter-efficient fine-tune on a few slices — one backbone for low-dose, sparse-view and limited-angle at once.
- **Toward CT-Equivalent Image Quality in Low-Dose Radiotherapy Planning: Conditional Diffusion-Based CBCT-to-CT Synthesis and the Impact of CBCT Input Representation** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2608.08919)
- **End-to-End Deep Learning for Interior Tomography with Low-Dose X-ray CT** — _PMB 2025_ · [Paper](https://arxiv.org/abs/2501.05085)
- **Noise-Inspired Diffusion Model for Generalizable Low-Dose CT Reconstruction** — _Med Image Anal 2025_ · [Paper](https://arxiv.org/abs/2506.22012) · [Code](https://github.com/qgao21/NEED)
- **Zero-Shot Low-dose CT Denoising via Sinogram Flicking** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2504.07927)
- **EAGLE: An Edge-Aware Gradient Localization Enhanced Loss for CT Image Reconstruction** — _preprint 2024_ · [Paper](https://arxiv.org/abs/2403.10695) · [Code](https://github.com/sypsyp97/Eagle_Loss)
- **ASCON: Anatomy-Aware Supervised Contrastive Learning Framework for Low-Dose CT Denoising** — _MICCAI 2023_ · [Paper](https://doi.org/10.1007/978-3-031-43999-5_34) · [Code](https://github.com/hao1635/ASCON)
- **CTformer: Convolution-Free Token2Token Dilated Vision Transformer for Low-Dose CT Denoising** — _PMB 2023_ · [Paper](https://doi.org/10.1088/1361-6560/acc000) · [Code](https://github.com/wdayang/CTformer)
- **DADN: Domain-adaptive denoising network for low-dose CT via noise estimation and transfer learning** — _Med Phys 2023_ · [Paper](https://doi.org/10.1002/mp.15952)
- **IRDS: Iterative reconstruction of low-dose CT based on differential sparse** — _BSPC 2023_ · [Paper](https://doi.org/10.1016/j.bspc.2022.104204)
- **Synergizing Physics/Model-based and Data-driven Methods for Low-Dose CT** — _SPM 2023_ · [Paper](https://arxiv.org/abs/2203.15725)
- **An Unsupervised Reconstruction Method For Low-Dose CT Using Deep Generative Regularization Prior** — _BSPC 2022_ · [Paper](https://arxiv.org/abs/2012.06448) · [Code](https://github.com/mozanunal/SparseCT)
- **CCN-CL: A content-noise complementary network with contrastive learning for low-dose computed tomography denoising** — _CBM 2022_ · [Paper](https://doi.org/10.1016/j.compbiomed.2022.105759)
- **CoCoDiff: A Contextual Conditional Diffusion Model for Low-dose CT Image Denoising** — _SPIE DXRT 2022_ · [Paper](https://doi.org/10.1117/12.2634939)
- **DESDGAN: A Dual-Encoder-Single-Decoder Based Low-Dose CT Denoising Network** — _JBHI 2022_ · [Paper](https://doi.org/10.1109/jbhi.2022.3155788) · [Code](https://github.com/hanzefang/DESDGAN)
- **DFDLM: A Dataset-free Deep Learning Method for Low-Dose CT Image Reconstruction** — _Inverse Problems 2022_ · [Paper](https://arxiv.org/abs/2205.00463)
- **DU-GAN: Generative Adversarial Networks with Dual-Domain U-Net Based Discriminators for Low-Dose CT Denoising** — _TIM 2022_ · [Paper](https://doi.org/10.1109/tim.2021.3128703) · [Code](https://github.com/Hzzone/DU-GAN)
- **EASEL: Iterative Reconstruction for Low-Dose CT using Deep Gradient Priors of Generative Model** — _TRPMS 2022_ · [Paper](https://doi.org/10.1109/trpms.2022.3148373) · [Code](https://github.com/yqx7150/EASEL)
- **Low-Dose CT Using Denoising Diffusion Probabilistic Model for 20× Speedup** — _preprint 2022_ · [Paper](https://arxiv.org/abs/2209.15136)
- **MALAR: Multiple Adversarial Learning based Angiography Reconstruction for Ultra-low-dose Contrast Medium CT** — _JBHI 2022_ · [Paper](https://doi.org/10.1109/jbhi.2022.3213595) · [Code](https://github.com/HIC-SYSU/MALAR)
- **CLEAR: Comprehensive Learning Enabled Adversarial Reconstruction for Subtle Structure Enhanced Low-Dose CT Imaging** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3097808)
- **DeACNN: Learning a Deep CNN Denoising Approach Using Anatomical Prior Information Implemented With Attention Mechanism for Low-Dose CT Imaging on Clinical Patient Data From Multiple Anatomical Sites** — _JBHI 2021_ · [Paper](https://doi.org/10.1109/jbhi.2021.3061758)
- **LoDoPaB-CT: a benchmark dataset for low-dose computed tomography reconstruction** — _Scientific Data 2021_ · [Paper](https://doi.org/10.1038/s41597-021-00893-z) · [Code](https://github.com/jleuschn/lodopab_tech_ref)
- **MAGIC: Manifold and graph integrative convolutional network for low-dose CT reconstruction** — _TMI 2021_ · [Paper](https://arxiv.org/abs/2008.00406)
- **N2S: Self-Supervised Training For Low-Dose Ct Reconstruction** — _ISBI 2021_ · [Paper](https://doi.org/10.1109/isbi48211.2021.9433944)
- **SinoNet: Noise-Generating-Mechanism-Driven Unsupervised Learning for Low-Dose CT Sinogram Recovery** — _TRPMS 2021_ · [Paper](https://doi.org/10.1109/trpms.2021.3083361)
- **CADL: Noise and spatial resolution properties of a commercially available deep learning‐based CT reconstruction algorithm** — _Med Phys 2020_ · [Paper](https://doi.org/10.1002/mp.14319)
- **EDCNN: Edge Enhancement-Based Densely Connected Network with Compound Loss for Low-Dose CT Denoising** — _ICSP 2020_ · [Paper](https://doi.org/10.1109/icsp48669.2020.9320928) · [Code](https://github.com/workingcoder/EDCNN)
- **REDAEP: Robust and Enhanced Denoising Autoencoding Prior for Sparse-View CT Reconstruction** — _TRPMS 2020_ · [Paper](https://doi.org/10.1109/trpms.2020.2989634)
- **SACNN: Self-Attention Convolutional Neural Network for Low-Dose CT Denoising With Self-Supervised Perceptual Loss Network** — _TMI 2020_ · [Paper](https://doi.org/10.1109/tmi.2020.2968472)
- **MAP-NN: Competitive performance of a modularized deep neural network compared to commercial algorithms for low-dose CT image reconstruction** — _Nat Mach Intell 2019_ · [Paper](https://doi.org/10.1038/s42256-019-0057-9)
- **SPULTRA: Low-Dose CT Image Reconstruction with Joint Statistical and Learned Image Models** — _TMI 2019_ · [Paper](https://doi.org/10.1109/tmi.2019.2934933)
- **SUPER-2: SUPER Learning: A Supervised-Unsupervised Framework for Low-Dose CT Image Reconstruction** — _ICCVW 2019_ · [Paper](https://doi.org/10.1109/iccvw.2019.00490)
- **VVBP-tSVD: VVBP-Tensor in the FBP Algorithm: Its Properties and Application in Low-Dose CT Reconstruction** — _TMI 2019_ · [Paper](https://doi.org/10.1109/tmi.2019.2935187)
- **3pADMM: Optimizing a parameterized plug-and-play ADMM for iterative low-dose CT reconstruction** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2865202)
- **SAGAN: Sharpness-Aware Low Dose CT Denoising Using Conditional Generative Adversarial Network** — _JDI 2018_ · [Paper](https://doi.org/10.1007/s10278-018-0056-0) · [Code](https://github.com/xinario/SAGAN)
- **SSDA: Low-dose CT restoration via stacked sparse denoising autoencoders** — _Neurocomputing 2018_ · [Paper](https://doi.org/10.1016/j.neucom.2018.01.015)
- **Statistical Image Reconstruction Using Mixed Poisson-Gaussian Noise Model for X-Ray CT** — _preprint 2018_ · [Paper](https://arxiv.org/abs/1801.09533)
- **WavResNet: Deep Convolutional Framelet Denosing for Low-Dose CT via Wavelet Residual Network** — _TMI 2018_ · [Paper](https://arxiv.org/abs/1707.09938)
- **WGAN-VGG: Low Dose CT Image Denoising Using a Generative Adversarial Network with Wasserstein Distance and Perceptual Loss** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2827462) · [Code](https://github.com/SSinyu/WGAN-VGG)
- **Applications of nonlocal means algorithm in low-dose X-ray CT image processing and reconstruction: A review** — _Med Phys 2017_ · [Paper](https://doi.org/10.1002/mp.12097)
- **Deep Convolutional Neural Network for Inverse Problems in Imaging** — _TIP 2017_ · [Paper](https://doi.org/10.1109/tip.2017.2713099)
- **IMAP-TV: Robust low-dose CT sinogram preprocessing via exploiting noise-generating mechanism** — _TMI 2017_ · [Paper](https://doi.org/10.1109/tmi.2017.2767290)
- **KSAE: Iterative Low-dose CT Reconstruction with Priors Trained by Artificial Neural Network** — _TMI 2017_ · [Paper](https://doi.org/10.1109/tmi.2017.2753138)
- **Low-dose CT via convolutional neural network** — _BOE 2017_ · [Paper](https://doi.org/10.1364/boe.8.000679)
- **Low-Dose Dynamic Cerebral Perfusion Computed Tomography Reconstruction via Kronecker-Basis-Representation Tensor Sparsity Regularization** — _TMI 2017_ · [Paper](https://doi.org/10.1109/tmi.2017.2749212)
- **RED-CNN: Low-Dose CT with a Residual Encoder-Decoder Convolutional Neural Network** — _TMI 2017_ · [Paper](https://doi.org/10.1109/tmi.2017.2715284) · [Code](https://github.com/SSinyu/RED-CNN)
- **SENP: Low‐dose CT reconstruction using spatially encoded nonlocal penalty** — _Med Phys 2017_ · [Paper](https://doi.org/10.1002/mp.12523)
- **Low-dose cerebral perfusion computed tomography image restoration via low-rank and total variation regularizations** — _Neurocomputing 2016_ · [Paper](https://doi.org/10.1016/j.neucom.2016.01.090)
- **Low-dose X-ray computed tomography image reconstruction with a combined low-mAs and sparse-view protocol** — _Opt. Express 2014_ · [Paper](https://doi.org/10.1364/oe.22.015190)
- **AWTV: Adaptive-weighted total variation minimization for sparse data toward low-dose x-ray computed tomography image reconstruction** — _PMB 2012_ · [Paper](https://doi.org/10.1088/0031-9155/57/23/7923)
- **Low-Dose X-ray CT Reconstruction via Dictionary Learning** — _TMI 2012_ · [Paper](https://doi.org/10.1109/tmi.2012.2195669)
- **K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation** — _TSP 2006_ · [Paper](https://doi.org/10.1109/tsp.2006.881199)

### Metal Artifact Reduction

<sub>Beam hardening, photon starvation and scatter caused by high-density implants · 21 papers</sub>

- **Balancing Efficiency and Restoration: Lightweight Mamba-Based Model for CT Metal Artifact Reduction** — _TRPMS 2026_ · [Paper](https://arxiv.org/abs/2604.06622) · [Code](https://github.com/RICKand-MORTY/MARMamba)
- **Complex Wavelet-Based Sinogram Segmentation for Metal Artifact Reduction in Cone-Beam CT** — _PMB 2026_ · [Paper](https://arxiv.org/abs/2602.14315)
- **H3D-MarNet: Wavelet-Guided Dual-Path Learning for Metal Artifact Suppression and CT Modality Transformation for Radiotherapy Workflows** — _ICPR 2026_ · [Paper](https://arxiv.org/abs/2605.12252)
- **Leveraging Image Editing Foundation Models for Data-Efficient CT Metal Artifact Reduction** — _CVPRW 2026_ · [Paper](https://arxiv.org/abs/2604.05934) · [Code](https://github.com/ahmetemirdagi/CT-EditMAR)
- **MGMAR: Metal-Guided Metal Artifact Reduction for X-ray Computed Tomography** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2603.13447)
- **Splat-Based Metal Artifact Reduction in Cone-Beam CT via Compact Attenuation Modeling** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2608.04764)

  Conference paper (CVPR 2026) introducing a compact per-Gaussian attenuation parameterization. The same group's CGF 45(2) 2026 journal paper is the extended version. Both are peer-reviewed, so both are listed.
- **Splat-based Metal Artifact Reduction in Cone-Beam CT via Polychromatic Modeling** — _CGF 2026_ · [Paper](https://arxiv.org/abs/2608.13159)

  Journal paper (Computer Graphics Forum 45(2), 2026). Extends the same group's CVPR 2026 conference paper on this problem with joint spectral self-calibration, system-response modelling and a released synthetic CBCT dataset. Both are peer-reviewed, so both are listed.
- **Unsupervised Metal Artifact Reduction in Dental CBCT using Fine-tuned Cycle-Consistent Adversarial Networks** — _Digital 2026_ · [Paper](https://arxiv.org/abs/2607.20977)
- **VoxelSynth3D: Interpretable Volumetric Image-Domain Metal Artifact Reduction with a Paired Synthetic CLINIC-Metal Benchmark** — _BHI 2026_ · [Paper](https://arxiv.org/abs/2610.01512)
- **FIND-Net -- Fourier-Integrated Network with Dictionary Kernels for Metal Artifact Reduction** — _MICCAI 2025_ · [Paper](https://arxiv.org/abs/2508.10617) · [Code](https://github.com/Farid-Tasharofi/FIND-Net)
- **ReMAR-DS: Recalibrated Feature Learning for Metal Artifact Reduction and CT Domain Transformation** — _ICIAP 2025_ · [Paper](https://arxiv.org/abs/2506.19531)
- **DuDoDp-MAR: Unsupervised CT Metal Artifact Reduction by Plugging Diffusion Priors in Dual Domains** — _TMI 2024_ · [Paper](https://doi.org/10.1109/tmi.2024.3351201) · [Code](https://github.com/DeepXuan/DuDoDp-MAR)
- **Polyner: Unsupervised Polychromatic Neural Representation for CT Metal Artifact Reduction** — _NeurIPS 2023_ · [Paper](https://arxiv.org/abs/2306.15203) · [Code](https://github.com/iwuqing/Polyner)
- **SemiMAR: Semi-Supervised Learning for CT Metal Artifact Reduction** — _JBHI 2023_ · [Paper](https://doi.org/10.1109/jbhi.2023.3312292) · [Code](https://github.com/zjk1988/SemiMAR)
- **ACDNet: Adaptive Convolutional Dictionary Network for CT Metal Artifact Reduction** — _IJCAI 2022_ · [Paper](https://doi.org/10.24963/ijcai.2022/195) · [Code](https://github.com/hongwang01/ACDNet)
- **DuDoDR-Net: Dual-domain data consistent recurrent network for simultaneous sparse view and metal artifact reduction in computed tomography** — _Med Image Anal 2022_ · [Paper](https://doi.org/10.1016/j.media.2021.102289)
- **IDOL-Net: An Interactive Dual-Domain Parallel Network for CT Metal Artifact Reduction** — _TRPMS 2022_ · [Paper](https://doi.org/10.1109/trpms.2022.3171440) · [Code](https://github.com/zjk1988/IDOL-Net)
- **DAN-Net: Dual-Domain Adaptive-Scaling Non-Local Network for CT Metal Artifact Reduction** — _MICCAI 2021_ · [Paper](https://doi.org/10.1007/978-3-030-87231-1_24) · [Code](https://github.com/zjk1988/DAN-Net)
- **InDuDoNet: An Interpretable Dual Domain Network for CT Metal Artifact Reduction** — _MICCAI 2021_ · [Paper](https://arxiv.org/abs/2109.05298) · [Code](https://github.com/hongwang01/InDuDoNet)
- **MAR-4Dec: Metal Artifact Reduction in CT: Where Are We After Four Decades?** — _IEEE Access 2016_ · [Paper](https://doi.org/10.1109/ACCESS.2016.2608621)
- **PBAC: Prior-based artifact correction (PBAC) in computed tomography** — _Med Phys 2014_ · [Paper](https://doi.org/10.1118/1.4851536)

### Spectral & Dual-Energy CT

<sub>Multi-energy acquisition, material decomposition, photon-counting CT · 18 papers</sub>

- **$K$-NeAS: Scalable Multi-Material CT Reconstruction Using Neural SDFs** — _Off-Grid Workshop 2026_ · [Paper](https://arxiv.org/abs/2607.14415)
- **Integration of Spectral CT with PET and SPECT: Bringing Tissue Composition Information to Molecular Imaging** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2609.27398)
- **Modeling X-Ray Photon Pile-Up with a Normalizing Flow** — _NeurIPS Workshop 2025_ · [Paper](https://arxiv.org/abs/2511.11863)
- **SOUL-Net: A Sparse and Low-Rank Unrolling Network for Spectral CT Image Reconstruction** — _TNNLS 2024_ · [Paper](https://doi.org/10.1109/tnnls.2023.3319408) · [Code](https://github.com/scuchenxiang/SOUL-Net)
- **FONT-SIR: Fourth-Order Nonlocal Tensor Decomposition Model for Spectral CT Image Reconstruction** — _TMI 2022_ · [Paper](https://doi.org/10.1109/tmi.2022.3156270)
- **CD-Net: Comprehensive Domain Network With Spectral Complementary for DECT Sparse-View Reconstruction** — _TCI 2021_ · [Paper](https://doi.org/10.1109/tci.2021.3070184)
- **FSTensor: Full-spectrum-knowledge-aware tensor model for energy-resolved CT iterative reconstruction** — _TMI 2020_ · [Paper](https://doi.org/10.1109/tmi.2020.2976692)
- **LRTP: Spectral CT reconstruction via low-rank representation and region-specific texture preserving Markov random field regularization** — _TMI 2020_ · [Paper](https://doi.org/10.1109/tmi.2020.2983414)
- **SISTER: Spectral-Image Similarity-Based Tensor With Enhanced-Sparsity Reconstruction for Sparse-View Multi-Energy CT** — _TCI 2020_ · [Paper](https://doi.org/10.1109/tci.2019.2956886)
- **NLCTF: Non-Local Low-Rank Cube-Based Tensor Factorization for Spectral CT Reconstruction** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2878226)
- **SPIR: Dual energy CT with one full scan and a second sparse-view scan using structure preserving iterative reconstruction (SPIR)** — _PMB 2016_ · [Paper](https://doi.org/10.1088/0031-9155/61/18/6684)
- **Dual- and Multi-Energy CT: Principles, Technical Approaches, and Clinical Applications** — _Radiology 2015_ · [Paper](https://doi.org/10.1148/radiol.2015142631)
- **Sparse-View Spectral CT Reconstruction Using Spectral Patch-Based Low-Rank Penalty** — _TMI 2015_ · [Paper](https://doi.org/10.1109/tmi.2014.2380993)
- **Experimental Feasibility of Multi-Energy Photon-Counting K-Edge Imaging in Pre-Clinical Computed Tomography** — _PMB 2008_ · [Paper](https://doi.org/10.1088/0031-9155/53/15/002)
- **K-Edge Imaging in X-Ray Computed Tomography Using Multi-Bin Photon Counting Detectors** — _PMB 2007_ · [Paper](https://doi.org/10.1088/0031-9155/52/15/020)
- **Statistical Image Reconstruction for Polyenergetic X-Ray Computed Tomography** — _TMI 2002_ · [Paper](https://doi.org/10.1109/42.993128)
- **An Iterative Maximum-Likelihood Polychromatic Algorithm for CT** — _TMI 2001_ · [Paper](https://doi.org/10.1109/42.959297)
- **Energy-Selective Reconstructions in X-Ray Computerised Tomography** — _PMB 1976_ · [Paper](https://doi.org/10.1088/0031-9155/21/5/002)

### Cone-Beam CT

<sub>Circular, helical and non-standard CBCT geometries; on-board imaging · 66 papers</sub>

- **Anatomy-preserving unpaired cone-beam CT refinement for image-guided radiotherapy using pseudo-label guided diffusion** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2610.06094)
- **CBCT-Based Synthetic CT Generation Using Conditional Flow Matching Model** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2603.05796)
- **Complex Wavelet-Based Sinogram Segmentation for Metal Artifact Reduction in Cone-Beam CT** — _PMB 2026_ · [Paper](https://arxiv.org/abs/2602.14315)
- **Cone-beam artifact reduction in Gamma Knife CBCT images using a line-arc-line scan trajectory** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2609.30169)
- **Cone-Beam CT Image Quality Enhancement Using A Latent Diffusion Model Trained with Simulated CBCT Artifacts** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2603.26014)
- **Continuity-driven Synergistic Diffusion with Neural Priors for Ultra-Sparse-View CBCT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.07980)
- **DeepSparse: A Foundation Model for Sparse-View CBCT Reconstruction** — _TMI 2026_ · [Paper](https://doi.org/10.1109/tmi.2026.3674948) · [Code](https://github.com/xmed-lab/DeepSparse)

  DiCE (Dual-Dimensional Cross-Scale Embedding) pre-trained by HyViP (Hybrid View Sampling Pretraining) on both sparse- and dense-view projections, then fine-tuned in two steps. Presented as the first foundation model for sparse-view CBCT.
- **Dual-domain U-Nets with embedded back projection operators for motion-resolved 4D CBCT reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2608.03430)
- **Field-of-View Extension in Dental Cone-Beam CT via Implicit Neural Representations and Diffusion Model-Based Refinement** — _MICAD 2026_ · [Paper](https://arxiv.org/abs/2609.28110) · [Code](https://github.com/SusanneSchaub/CBCT-FOV-Extension)
- **GH-NAF: Grid-Adaptive Hash-Level-Attended Neural Attenuation Fields for Discrepancy-Aware CBCT** — _CVPR 2026_ · [Paper](https://openaccess.thecvf.com/content/CVPR2026/html/Oh_GH-NAF_Grid-Adaptive_Hash-Level-Attended_Neural_Attenuation_Fields_for_Discrepancy-Aware_CBCT_CVPR_2026_paper.html) · [Code](https://github.com/seongje-oh/GH-NAF)
- **H3D-MarNet: Wavelet-Guided Dual-Path Learning for Metal Artifact Suppression and CT Modality Transformation for Radiotherapy Workflows** — _ICPR 2026_ · [Paper](https://arxiv.org/abs/2605.12252)
- **HARU-Net: Hybrid Attention Residual U-Net for Edge-Preserving Denoising in Cone-Beam Computed Tomography** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.22544)
- **High-Fidelity 3D Tooth Reconstruction by Fusing Intraoral Scans and CBCT Data via a Deep Implicit Representation** — _ISBI 2026_ · [Paper](https://arxiv.org/abs/2601.15358)
- **Joint-decoupled iterative CBCT reconstruction with hybrid scatter estimation and voxel-adaptive beam hardening correction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2607.15812)
- **NGPS: Structure-Preserving Self-Supervised Denoising via Neighbor-Guided Patch Sampling** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2606.23200) · [Code](https://github.com/cv-cho/NGPS)
- **Non-circular scan trajectories for reducing cone-beam artifacts in Gamma Knife CBCT images: a simulation study** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2609.28232)
- **Riner: Unsupervised Multi-Parameter Inverse Solving for Reducing Ring Artifacts in 3D X-Ray CBCT** — _AAAI 2026_ · [Paper](https://arxiv.org/abs/2412.05853) · [Code](https://github.com/iwuqing/Riner)
- **Robustness and Stability Analysis of Differentiable Shift-Variant FBP for Cone-Beam CT under Challenging Acquisition Settings** — _MELBA 2026_ · [Paper](https://arxiv.org/abs/2607.09828) · [Project](https://melba-journal.org/2026:014)
- **Spectral Consistent Flow for One-Step 3D Medical Image Translation** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2607.10627)
- **Splat-Based Metal Artifact Reduction in Cone-Beam CT via Compact Attenuation Modeling** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2608.04764)

  Conference paper (CVPR 2026) introducing a compact per-Gaussian attenuation parameterization. The same group's CGF 45(2) 2026 journal paper is the extended version. Both are peer-reviewed, so both are listed.
- **Splat-based Metal Artifact Reduction in Cone-Beam CT via Polychromatic Modeling** — _CGF 2026_ · [Paper](https://arxiv.org/abs/2608.13159)

  Journal paper (Computer Graphics Forum 45(2), 2026). Extends the same group's CVPR 2026 conference paper on this problem with joint spectral self-calibration, system-response modelling and a released synthetic CBCT dataset. Both are peer-reviewed, so both are listed.
- **Texture-preserving implicit neural representation for Cone beam CT truncated reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2606.06039)
- **Toward CT-Equivalent Image Quality in Low-Dose Radiotherapy Planning: Conditional Diffusion-Based CBCT-to-CT Synthesis and the Impact of CBCT Input Representation** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2608.08919)
- **Unsupervised Metal Artifact Reduction in Dental CBCT using Fine-tuned Cycle-Consistent Adversarial Networks** — _Digital 2026_ · [Paper](https://arxiv.org/abs/2607.20977)
- **3D CBCT Artefact Removal Using Perpendicular Score-Based Diffusion Models** — _DGM4MICCAI 2025_ · [Paper](https://arxiv.org/abs/2603.06300)
- **4DGS-4DCBCT: Spatiotemporal Gaussian Optimization for 4D Cone Beam CT Reconstruction from Sparsely Sampled Projections** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2501.04140) · [Code](https://github.com/fuyabo/4DGS_for_4DCBCT)
- **A Learnt Half-Quadratic Splitting-Based Algorithm for Fast and High-Quality Industrial Cone-beam CT Reconstruction** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2501.13128)
- **Adaptive Diffusion Models for Sparse-View Motion-Corrected Head Cone-beam CT** — _TRPMS 2025_ · [Paper](https://arxiv.org/abs/2504.14033) · [Project](https://antoinedepaepe.github.io/jrm-adm-io/)
- **An Iterative Reconstruction Method for Dental Cone-Beam Computed Tomography with a Truncated Field of View** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.07618)
- **DIGS: Dynamic CBCT Reconstruction using Deformation-Informed 4D Gaussian Splatting and a Low-Rank Free-Form Deformation Model** — _MICCAI 2025_ · [Paper](https://arxiv.org/abs/2506.22280) · [Code](https://github.com/Yuliang-Huang/DIGS)
- **Enhancing Synthetic CT from CBCT via Multimodal Fusion and End-To-End Registration** — _CAIP 2025_ · [Paper](https://arxiv.org/abs/2507.06067)
- **Equivariant Conditional Diffusion Model for Head and Neck CT Image Synthesis from CBCT** — _Med Phys 2025_ · [Paper](https://arxiv.org/abs/2509.21913)
- **Equivariant Multiscale Learned Invertible Reconstruction for Cone Beam CT: From Simulated to Real Data** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2512.21180)
- **GANeXt: A Fully ConvNeXt-Enhanced Generative Adversarial Network for MRI- and CBCT-to-CT Synthesis** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2512.19336)
- **GLFC: Unified Global-Local Feature and Contrast Learning with Mamba-Enhanced UNet for Synthetic CT Generation from CBCT** — _ISBI 2025_ · [Paper](https://arxiv.org/abs/2501.02992) · [Code](https://github.com/HiLab-git/GLFC)
- **Learning Wavelet-Sparse FDK for 3D Cone-Beam CT Reconstruction** — _Fully3D 2025_ · [Paper](https://arxiv.org/abs/2505.13579)
- **MInDI-3D: Iterative Deep Learning in 3D for Sparse-view Cone Beam Computed Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.09616)
- **Motion-Grad: A Gradient-Based Approach to Fast and Accurate Head Motion Compensation in Cone-Beam CT** — _TMI 2025_ · [Paper](https://doi.org/10.1109/tmi.2024.3474250) · [Code](https://github.com/mareikethies/geometry_gradients_CT)
- **Neural Discrete Representation Learning for Sparse-View CBCT Reconstruction: From Algorithm Design to Prospective Multicenter Clinical Evaluation** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2512.00873)
- **Physics-Inspired Gaussian Kolmogorov-Arnold Networks for X-ray Scatter Correction in Cone-Beam CT** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2510.24579)
- **Prior-Adapted Progressive Time-Resolved CBCT Reconstruction Using a Dynamic Reconstruction and Motion Estimation Method** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2504.18700)
- **Swap-Net: A Memory-Efficient 2.5D Network for Sparse-View 3D Cone Beam CT Reconstruction to ICF Applications** — _TCI 2025_ · [Paper](https://doi.org/10.1109/tci.2025.3572699)
- **Synthetic CT image generation from CBCT: A Systematic Review** — _TRPMS 2025_ · [Paper](https://arxiv.org/abs/2501.13972)
- **Time-resolved dynamic CBCT reconstruction using prior-model-free spatiotemporal Gaussian representation (PMF-STGR)** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2503.22139)
- **Ultrafast Deep Learning-Based Scatter Estimation in Cone-Beam Computed Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2509.08973)
- **XGenRecon: A New Perspective in Ultrasparse Volumetric CBCT Reconstruction Through Geometry-Controlled X-Ray Projection Generation** — _TRPMS 2025_ · [Paper](https://doi.org/10.1109/trpms.2024.3420742)
- **DIF-Gaussian: Learning 3D Gaussians for Extremely Sparse-View Cone-Beam CT Reconstruction** — _MICCAI 2024_ · [Paper](https://doi.org/10.1007/978-3-031-72104-5_41) · [Code](https://github.com/xmed-lab/DIF-Gaussian)
- **Scatter-DL: Scatter Correction Using Deep Learning for Cone-Beam Computed Tomography** — _DL4X-ray 2024_ · [Paper](https://doi.org/10.1007/978-3-031-75653-5_6)
- **Sparse-View Cone Beam CT Reconstruction Using Data-Consistent Supervised and Adversarial Learning From Scarce Training Data** — _TCI 2023_ · [Paper](https://doi.org/10.1109/TCI.2022.3225680)
- **SPQI: Structure-preserving quality improvement of cone beam CT images using contrastive learning** — _CBM 2023_ · [Paper](https://doi.org/10.1016/j.compbiomed.2023.106803)
- **NAF: Neural Attenuation Fields for Sparse-View CBCT Reconstruction** — _MICCAI 2022_ · [Paper](https://arxiv.org/abs/2209.14540) · [Code](https://github.com/Ruyi-Zha/naf_cbct)
- **SNAF: Sparse-View CBCT Reconstruction with Neural Attenuation Fields** — _preprint 2022_ · [Paper](https://arxiv.org/abs/2211.17048)
- **SPARE: Sparse-view reconstruction challenge for 4D cone-beam CT from a 1-min scan** — _Med Phys 2019_ · [Paper](https://doi.org/10.1002/mp.13687)
- **LIVE: A limited-angle intrafraction verification (LIVE) system for radiation therapy** — _Med Phys 2014_ · [Paper](https://doi.org/10.1118/1.4861820)
- **A technique for estimating 4D-CBCT using prior knowledge and limited-angle projections** — _Med Phys 2013_ · [Paper](https://doi.org/10.1118/1.4825097)
- **Artifact-resistant motion estimation with a patient-specific artifact model for motion-compensated cone-beam CT** — _Med Phys 2013_ · [Paper](https://doi.org/10.1118/1.4820537)
- **Optimization-based image reconstruction from sparse-view data in offset-detector CBCT** — _PMB 2013_ · [Paper](https://doi.org/10.1088/0031-9155/58/2/205)
- **Scatter-Rev: A General Framework and Review of Scatter Correction Methods in X-Ray Cone-Beam CT: Part 1 — Scatter Compensation Approaches** — _Med Phys 2011_ · [Paper](https://doi.org/10.1118/1.3599033)
- **Compressed sensing based cone-beam computed tomography reconstruction with a first-order method** — _Med Phys 2010_ · [Paper](https://doi.org/10.1118/1.3481510)
- **Evaluation of sparse-view reconstruction from flat-panel-detector cone-beam CT** — _PMB 2010_ · [Paper](https://doi.org/10.1088/0031-9155/55/22/001)
- **Directional View Interpolation for Compensation of Sparse Angular Sampling in Cone-Beam CT** — _TMI 2009_ · [Paper](https://doi.org/10.1109/tmi.2008.2011550)
- **High Temporal Resolution and Streak-Free Four-Dimensional Cone-Beam Computed Tomography** — _PMB 2008_ · [Paper](https://doi.org/10.1088/0031-9155/53/20/006)
- **Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization** — _PMB 2008_ · [Paper](https://doi.org/10.1088/0031-9155/53/17/021)
- **Respiratory Correlated Cone Beam CT** — _Med Phys 2005_ · [Paper](https://doi.org/10.1118/1.1869074)
- **Cone-Beam Computed Tomography with a Flat-Panel Imager: Magnitude and Effects of X-Ray Scatter** — _Med Phys 2001_ · [Paper](https://doi.org/10.1118/1.1339879)
- **FDK: Practical cone-beam algorithm** — _JOSA A 1984_ · [Paper](https://doi.org/10.1364/JOSAA.1.000612)

### Dynamic & 4D CT

<sub>Time-resolved reconstruction, motion modelling, perfusion and cardiac CT · 21 papers</sub>

- **Dual-domain U-Nets with embedded back projection operators for motion-resolved 4D CBCT reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2608.03430)
- **Dynamic Black-hole Emission Tomography with Physics-Informed Neural Fields** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2602.08029)
- **4DGS-4DCBCT: Spatiotemporal Gaussian Optimization for 4D Cone Beam CT Reconstruction from Sparsely Sampled Projections** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2501.04140) · [Code](https://github.com/fuyabo/4DGS_for_4DCBCT)
- **DIGS: Dynamic CBCT Reconstruction using Deformation-Informed 4D Gaussian Splatting and a Low-Rank Free-Form Deformation Model** — _MICCAI 2025_ · [Paper](https://arxiv.org/abs/2506.22280) · [Code](https://github.com/Yuliang-Huang/DIGS)
- **Motion-Grad: A Gradient-Based Approach to Fast and Accurate Head Motion Compensation in Cone-Beam CT** — _TMI 2025_ · [Paper](https://doi.org/10.1109/tmi.2024.3474250) · [Code](https://github.com/mareikethies/geometry_gradients_CT)
- **Nonperiodic dynamic CT reconstruction using backward-warping INR with regularization of diffeomorphism (BIRD)** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2505.03463)
- **Prior-Adapted Progressive Time-Resolved CBCT Reconstruction Using a Dynamic Reconstruction and Motion Estimation Method** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2504.18700)
- **Time-resolved dynamic CBCT reconstruction using prior-model-free spatiotemporal Gaussian representation (PMF-STGR)** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2503.22139)
- **X2-Gaussian: 4D Radiative Gaussian Splatting for Continuous-Time Tomographic Reconstruction** — _ICCV 2025_ · [Paper](https://doi.org/10.1109/iccv51701.2025.02293) · [Code](https://github.com/yuyouxixi/x2-gaussian)
- **DCTR: Dynamic CT Reconstruction From Limited Views With Implicit Neural Representations** — _ICCV 2021_ · [Paper](https://doi.org/10.1109/iccv48922.2021.00226)
- **SPARE: Sparse-view reconstruction challenge for 4D cone-beam CT from a 1-min scan** — _Med Phys 2019_ · [Paper](https://doi.org/10.1002/mp.13687)
- **Low-Dose Dynamic Cerebral Perfusion Computed Tomography Reconstruction via Kronecker-Basis-Representation Tensor Sparsity Regularization** — _TMI 2017_ · [Paper](https://doi.org/10.1109/tmi.2017.2749212)
- **Low-dose cerebral perfusion computed tomography image restoration via low-rank and total variation regularizations** — _Neurocomputing 2016_ · [Paper](https://doi.org/10.1016/j.neucom.2016.01.090)
- **Tensor-based dictionary learning for dynamic tomographic reconstruction** — _PMB 2015_ · [Paper](https://doi.org/10.1088/0031-9155/60/7/2803)
- **A technique for estimating 4D-CBCT using prior knowledge and limited-angle projections** — _Med Phys 2013_ · [Paper](https://doi.org/10.1118/1.4825097)
- **4D Cone Beam CT via Spatiotemporal Tensor Framelet** — _Med Phys 2012_ · [Paper](https://doi.org/10.1118/1.4762288)
- **An Investigation of 4D Cone-Beam CT Algorithms for Slowly Rotating Scanners** — _Med Phys 2010_ · [Paper](https://doi.org/10.1118/1.3480986)
- **On-the-Fly Motion-Compensated Cone-Beam CT Using an A Priori Model of the Respiratory Motion** — _Med Phys 2009_ · [Paper](https://doi.org/10.1118/1.3115691)
- **High Temporal Resolution and Streak-Free Four-Dimensional Cone-Beam Computed Tomography** — _PMB 2008_ · [Paper](https://doi.org/10.1088/0031-9155/53/20/006)
- **PICCS: Prior Image Constrained Compressed Sensing (PICCS): A Method to Accurately Reconstruct Dynamic CT Images from Highly Undersampled Projection Data Sets** — _Med Phys 2008_ · [Paper](https://doi.org/10.1118/1.2836423)
- **Respiratory Correlated Cone Beam CT** — _Med Phys 2005_ · [Paper](https://doi.org/10.1118/1.1869074)

### Scatter Correction

<sub>Scatter estimation and removal, both hardware- and software-based · 11 papers</sub>

- **Joint-decoupled iterative CBCT reconstruction with hybrid scatter estimation and voxel-adaptive beam hardening correction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2607.15812)
- **Physics-Inspired Gaussian Kolmogorov-Arnold Networks for X-ray Scatter Correction in Cone-Beam CT** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2510.24579)
- **Ultrafast Deep Learning-Based Scatter Estimation in Cone-Beam Computed Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2509.08973)
- **Scatter-DL: Scatter Correction Using Deep Learning for Cone-Beam Computed Tomography** — _DL4X-ray 2024_ · [Paper](https://doi.org/10.1007/978-3-031-75653-5_6)
- **Real-Time Scatter Estimation for Medical CT Using the Deep Scatter Estimation: Method and Robustness Analysis with Respect to Different Anatomies, Dose Levels, Tube Voltages, and Data Truncation** — _Med Phys 2019_ · [Paper](https://doi.org/10.1002/mp.13274)
- **DSE: Deep Scatter Estimation (DSE): Feasibility of Using a Deep Convolutional Neural Network for Scatter Estimation in X-Ray Computed Tomography** — _SPIE MI 2018_ · [Paper](https://doi.org/10.1117/12.2292919)
- **A General Framework and Review of Scatter Correction Methods in Cone-Beam CT: Part 2 — Scatter Estimation Approaches** — _Med Phys 2011_ · [Paper](https://doi.org/10.1118/1.3589140)
- **Scatter-Rev: A General Framework and Review of Scatter Correction Methods in X-Ray Cone-Beam CT: Part 1 — Scatter Compensation Approaches** — _Med Phys 2011_ · [Paper](https://doi.org/10.1118/1.3599033)
- **Efficient Monte Carlo Based Scatter Artifact Reduction in Cone-Beam Micro-CT** — _TMI 2006_ · [Paper](https://doi.org/10.1109/tmi.2006.872328)
- **Scatter Correction Method for X-Ray CT Using Primary Modulation: Theory and Preliminary Results** — _TMI 2006_ · [Paper](https://doi.org/10.1109/tmi.2006.884636)
- **Cone-Beam Computed Tomography with a Flat-Panel Imager: Magnitude and Effects of X-Ray Scatter** — _Med Phys 2001_ · [Paper](https://doi.org/10.1118/1.1339879)

### Geometry Calibration & Motion Compensation

<sub>Geometric self-calibration, marker-free alignment, rigid and non-rigid motion correction · 25 papers</sub>

- **Active View Selection with Perturbed Gaussian Ensemble for Tomographic Reconstruction** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2603.06852)
- **Conditional Diffusion Posterior Alignment for Sparse-View CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2604.21960)
- **Cone-beam artifact reduction in Gamma Knife CBCT images using a line-arc-line scan trajectory** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2609.30169)
- **Exact-GS: Mathematically Rigorous and Accurate 3D Gaussian Splatting for 3D X-Ray Reconstruction** — _CVPR 2026_ · [Paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Exact-GS_Mathematically_Rigorous_and_Accurate_3D_Gaussian_Splatting_for_3D_CVPR_2026_paper.html) · [Code](https://github.com/brucee1323/Exact-GS)
- **GB-SVFBP: Gaussian-Based Shift-Variant FBP neural network** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2607.11584)
- **Geometry-Aware Diffusion Approximate Posterior Sampling for Sparse-View and Limited-Angle CT** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2610.08866)
- **Revisiting Pose Sensitivity in Splat-based Computed Tomography under Sparse-view Reconstruction** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2608.04752)
- **Riner: Unsupervised Multi-Parameter Inverse Solving for Reducing Ring Artifacts in 3D X-Ray CBCT** — _AAAI 2026_ · [Paper](https://arxiv.org/abs/2412.05853) · [Code](https://github.com/iwuqing/Riner)
- **Robustness and Stability Analysis of Differentiable Shift-Variant FBP for Cone-Beam CT under Challenging Acquisition Settings** — _MELBA 2026_ · [Paper](https://arxiv.org/abs/2607.09828) · [Project](https://melba-journal.org/2026:014)
- **Texture-preserving implicit neural representation for Cone beam CT truncated reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2606.06039)
- **TG-Field: Geometry-Aware Radiative Gaussian Fields for Tomographic Reconstruction** — _AAAI 2026_ · [Paper](https://arxiv.org/abs/2602.11705)
- **Tomographic Sparse View Selection Using the View Covariance Loss** — _TPAMI 2026_ · [Paper](https://doi.org/10.1109/TPAMI.2025.3600072)
- **A CT Geometry With Multiple Centers Of Rotation For Solving Sparse View Problem** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2502.06125)
- **An Iterative Reconstruction Method for Dental Cone-Beam Computed Tomography with a Truncated Field of View** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.07618)
- **Enhancing Synthetic CT from CBCT via Multimodal Fusion and End-To-End Registration** — _CAIP 2025_ · [Paper](https://arxiv.org/abs/2507.06067)
- **Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency** — _ISBI 2025_ · [Paper](https://arxiv.org/abs/2411.06181)
- **Limited-Angle CBCT Reconstruction via Geometry-Integrated Cycle-domain Denoising Diffusion Probabilistic Models** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2506.13545)
- **Motion-Grad: A Gradient-Based Approach to Fast and Accurate Head Motion Compensation in Cone-Beam CT** — _TMI 2025_ · [Paper](https://doi.org/10.1109/tmi.2024.3474250) · [Code](https://github.com/mareikethies/geometry_gradients_CT)
- **Prior-Adapted Progressive Time-Resolved CBCT Reconstruction Using a Dynamic Reconstruction and Motion Estimation Method** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2504.18700)
- **BaggageCT: Fan-Beam CT Reconstruction for Unaligned Sparse-View X-Ray Baggage Data** — _preprint 2024_ · [Paper](https://arxiv.org/abs/2412.03036)
- **GGLF: Gradient-based geometry learning for fan-beam CT reconstruction** — _PMB 2023_ · [Paper](https://doi.org/10.1088/1361-6560/acf90e)
- **DSigNet: Downsampled Imaging Geometric Modeling for Accurate CT Reconstruction via Deep Learning** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3074783) · [Code](https://github.com/hejipro/iRadonMAP-DSigNet)
- **PDF: CT Reconstruction With PDF: Parameter-Dependent Framework for Data From Multiple Geometries and Dose Levels** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3085839)
- **Artifact-resistant motion estimation with a patient-specific artifact model for motion-compensated cone-beam CT** — _Med Phys 2013_ · [Paper](https://doi.org/10.1118/1.4820537)
- **A novel digital tomosynthesis (DTS) reconstruction method using a deformation field map** — _Med Phys 2008_ · [Paper](https://doi.org/10.1118/1.2940725)

### Deep Unrolling & Model-Based Learning

<sub>Learned iterative schemes that unroll a classical solver, with or without data consistency · 68 papers</sub>

- **CG-GLORE: A Conjugate Gradient-Based Global-Local Regularization Network for Sparse-View CT Reconstruction** — _BMVC 2026_ · [Paper](https://arxiv.org/abs/2608.15246)
- **Dose-Aware Cold Diffusion with Physics Consistency for Generalizable Low-Dose CT Reconstruction** — _IJCNN 2026_ · [Paper](https://arxiv.org/abs/2609.18943)
- **Dual-domain U-Nets with embedded back projection operators for motion-resolved 4D CBCT reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2608.03430)
- **Efficient Unrolled Networks for Large-Scale 3D Inverse Problems** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2601.02141) · [Code](https://github.com/romainvo/efficient-unrolling)
- **GB-SVFBP: Gaussian-Based Shift-Variant FBP neural network** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2607.11584)
- **HARU-Net: Hybrid Attention Residual U-Net for Edge-Preserving Denoising in Cone-Beam Computed Tomography** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.22544)
- **Learning Where and What to Lift for Bi-planar X-ray-to-CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2608.17255)
- **LUCID: Learned Undersampling-Adaptive Consistency-Guided Inference with Deterministic Flow Matching for Sparse-View CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2606.16212)
- **RAM: Reconstruct Anything Model: A Lightweight General Model for Computational Imaging** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2503.08915) · [Code](https://github.com/matthieutrs/ram)
- **Toward a Foundation Plug-and-Play Prior for Computed Tomography Reconstruction via a Multimodal Diffusion Model** — _SC Workshops 2026_ · [Paper](https://arxiv.org/abs/2608.23190)
- **A Learnt Half-Quadratic Splitting-Based Algorithm for Fast and High-Quality Industrial Cone-beam CT Reconstruction** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2501.13128)
- **CoCo-PnP: Learning Cocoercive Conservative Denoisers via Helmholtz Decomposition for Poisson Inverse Problems** — _NeurIPS 2025_ · [Paper](https://arxiv.org/abs/2505.08909) · [Code](https://github.com/FizzzFizzz/CoCo-PnP)
- **Data-Efficient Limited-Angle CT Using Deep Priors and Regularization** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2502.12293)
- **End-to-End Deep Learning for Interior Tomography with Low-Dose X-ray CT** — _PMB 2025_ · [Paper](https://arxiv.org/abs/2501.05085)
- **Equivariant Multiscale Learned Invertible Reconstruction for Cone Beam CT: From Simulated to Real Data** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2512.21180)
- **FIND-Net -- Fourier-Integrated Network with Dictionary Kernels for Metal Artifact Reduction** — _MICCAI 2025_ · [Paper](https://arxiv.org/abs/2508.10617) · [Code](https://github.com/Farid-Tasharofi/FIND-Net)
- **MInDI-3D: Iterative Deep Learning in 3D for Sparse-view Cone Beam Computed Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.09616)
- **Resolution-Agnostic Neural Operators for Multi-Rate Sparse-View CT** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2512.12236) · [Code](https://github.com/neuraloperator/sparse_ct)
- **Semantic contrastive learning for orthogonal X-ray computed tomography reconstruction** — _Fully3D 2025_ · [Paper](https://arxiv.org/abs/2512.22674)
- **EAGLE: An Edge-Aware Gradient Localization Enhanced Loss for CT Image Reconstruction** — _preprint 2024_ · [Paper](https://arxiv.org/abs/2403.10695) · [Code](https://github.com/sypsyp97/Eagle_Loss)
- **Plug-and-Play Learned Proximal Trajectory for 3D Sparse-View X-Ray Computed Tomography** — _ECCV 2024_ · [Paper](https://doi.org/10.1007/978-3-031-72761-0_13)
- **SOUL-Net: A Sparse and Low-Rank Unrolling Network for Spectral CT Image Reconstruction** — _TNNLS 2024_ · [Paper](https://doi.org/10.1109/tnnls.2023.3319408) · [Code](https://github.com/scuchenxiang/SOUL-Net)
- **DEAR: Deep Embedding-Attention-Refinement for Sparse-View CT Reconstruction** — _TIM 2023_ · [Paper](https://doi.org/10.1109/tim.2022.3221136)
- **DREAM-Net: Deep Residual Error Iterative Minimization Network for Sparse-View CT Reconstruction** — _JBHI 2023_ · [Paper](https://doi.org/10.1109/jbhi.2022.3225697)
- **FreeSeed: Frequency-Band-Aware and Self-Guided Network for Sparse-View CT Reconstruction** — _MICCAI 2023_ · [Paper](https://doi.org/10.1007/978-3-031-43999-5_24) · [Code](https://github.com/Masaaki-75/freeseed)
- **LEARN++: Recurrent Dual-Domain Reconstruction Network for Compressed Sensing CT** — _TRPMS 2023_ · [Paper](https://doi.org/10.1109/trpms.2022.3222213)
- **SPIE-DIR: Self-Prior Information Enhanced Deep Iterative Reconstruction Using Two Complementary Limited-Angle Scans for DECT** — _TIM 2023_ · [Paper](https://doi.org/10.1109/tim.2022.3227549)
- **ACDNet: Adaptive Convolutional Dictionary Network for CT Metal Artifact Reduction** — _IJCAI 2022_ · [Paper](https://doi.org/10.24963/ijcai.2022/195) · [Code](https://github.com/hongwang01/ACDNet)
- **ACID-A: Stabilizing deep tomographic reconstruction - Part A. Hybrid framework and experimental results** — _Patterns 2022_ · [Paper](https://doi.org/10.1016/j.patter.2022.100474)
- **ACID-B: Stabilizing deep tomographic reconstruction - Part B. Convergence analysis and adversarial attacks** — _Patterns 2022_ · [Paper](https://doi.org/10.1016/j.patter.2022.100475)
- **DDCL: Dual domain closed-loop learning for sparse-view CT reconstruction** — _ICIFXCT 2022_ · [Paper](https://doi.org/10.1117/12.2646639)
- **DIOR: Deep Iterative Optimization-Based Residual-Learning for Limited-Angle CT Reconstruction** — _TMI 2022_ · [Paper](https://doi.org/10.1109/tmi.2022.3148110)
- **IDOL-Net: An Interactive Dual-Domain Parallel Network for CT Metal Artifact Reduction** — _TRPMS 2022_ · [Paper](https://doi.org/10.1109/trpms.2022.3171440) · [Code](https://github.com/zjk1988/IDOL-Net)
- **CasRedSCAN: Limited View Tomographic Reconstruction Using a Cascaded Residual Dense Spatial-Channel Attention Network With Projection Data Fidelity Layer** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3066318)
- **DAN-Net: Dual-Domain Adaptive-Scaling Non-Local Network for CT Metal Artifact Reduction** — _MICCAI 2021_ · [Paper](https://doi.org/10.1007/978-3-030-87231-1_24) · [Code](https://github.com/zjk1988/DAN-Net)
- **DeACNN: Learning a Deep CNN Denoising Approach Using Anatomical Prior Information Implemented With Attention Mechanism for Low-Dose CT Imaging on Clinical Patient Data From Multiple Anatomical Sites** — _JBHI 2021_ · [Paper](https://doi.org/10.1109/jbhi.2021.3061758)
- **DRONE: Dual-Domain Residual-Based Optimization Network for Sparse-View CT Reconstruction** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3078067) · [Code](https://github.com/weiwenwu12/DRONE)
- **DSigNet: Downsampled Imaging Geometric Modeling for Accurate CT Reconstruction via Deep Learning** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3074783) · [Code](https://github.com/hejipro/iRadonMAP-DSigNet)
- **FISTA-Net: Learning a Fast Iterative Shrinkage Thresholding Network for Inverse Problems in Imaging** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3054167) · [Code](https://github.com/jinxixiang/FISTA-Net)
- **InDuDoNet: An Interpretable Dual Domain Network for CT Metal Artifact Reduction** — _MICCAI 2021_ · [Paper](https://arxiv.org/abs/2109.05298) · [Code](https://github.com/hongwang01/InDuDoNet)
- **MetaInv-Net: Meta Inversion Network for Sparse View CT Image Reconstruction** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2020.3033541) · [Code](https://github.com/haimiaozh/MetaInv-Net)
- **PDF: CT Reconstruction With PDF: Parameter-Dependent Framework for Data From Multiple Geometries and Dose Levels** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3085839)
- **SPECIAL: Single-Shot Projection Error Correction Integrated Adversarial Learning for Limited-Angle CT** — _TCI 2021_ · [Paper](https://doi.org/10.1109/tci.2021.3098922)
- **Tensor-Net: Learning to Reconstruct CT Images From the VVBP-Tensor** — _TMI 2021_ · [Paper](https://doi.org/10.1109/tmi.2021.3090257)
- **A review on deep learning in medical image reconstruction** — _JORSC 2020_ · [Paper](https://arxiv.org/abs/1906.10643)
- **AirNet: Fused analytical and iterative reconstruction with deep neural network regularization for sparse-data CT** — _Med Phys 2020_ · [Paper](https://doi.org/10.1002/mp.14170)
- **DL-InvProb: Deep Learning Techniques for Inverse Problems in Imaging** — _JSAIT 2020_ · [Paper](https://arxiv.org/abs/2005.06001)
- **ETEDN: An End-to-End Deep Network for Reconstructing CT Images Directly From Sparse Sinograms** — _TCI 2020_ · [Paper](https://doi.org/10.1109/tci.2020.3039385) · [Code](https://github.com/wangwei-cmd/CT-image-reconstruction)
- **HD-CNN: Artifact removal using a hybrid-domain convolutional neural network for limited-angle computed tomography imaging** — _PMB 2020_ · [Paper](https://doi.org/10.1088/1361-6560/ab9066)
- **iRadonMAP: Radon Inversion via Deep Learning** — _TMI 2020_ · [Paper](https://arxiv.org/abs/1808.03015)
- **Learned convex regularizers for inverse problems** — _preprint 2020_ · [Paper](https://arxiv.org/abs/2008.02839)
- **Momentum-Net: Fast and convergent iterative neural network for inverse problems** — _TPAMI 2020_ · [Paper](https://doi.org/10.1109/tpami.2020.3012955)
- **Multi-Scale Learned Iterative Reconstruction** — _TCI 2020_ · [Paper](https://doi.org/10.1109/TCI.2020.2990299)
- **SACNN: Self-Attention Convolutional Neural Network for Low-Dose CT Denoising With Self-Supervised Perceptual Loss Network** — _TMI 2020_ · [Paper](https://doi.org/10.1109/tmi.2020.2968472)
- **ADMM-based deep reconstruction for limited-angle CT** — _PMB 2019_ · [Paper](https://doi.org/10.1088/1361-6560/ab1aba)
- **Convolutional Sparse Coding for Compressed Sensing CT Reconstruction** — _TMI 2019_ · [Paper](https://doi.org/10.1109/tmi.2019.2906853)
- **Learning the invisible: a hybrid deep learning-shearlet framework for limited angle computed tomography** — _Inverse Problems 2019_ · [Paper](https://doi.org/10.1088/1361-6420/ab10ca)
- **SISVM: Learning to Reconstruct Computed Tomography Images Directly From Sinogram Data Under A Variety of Data Acquisition Conditions** — _TMI 2019_ · [Paper](https://doi.org/10.1109/tmi.2019.2910760)
- **SPSS: Sharpness preserved sinogram synthesis using convolutional neural network for sparse-view CT imaging** — _SPIE MI 2019_ · [Paper](https://doi.org/10.1117/12.2512894)
- **AUTOMAP: Image reconstruction by domain-transform manifold learning** — _Nature 2018_ · [Paper](https://doi.org/10.1038/nature25988)
- **CNNRPGD: CNN-Based Projected Gradient Descent for Consistent CT Image Reconstruction** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2832656)
- **DD-Net: A Sparse-View CT Reconstruction Method Based on Combination of DenseNet and Deconvolution** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2823338) · [Code](https://github.com/zzc623/DD_Net)
- **DSE: Deep Scatter Estimation (DSE): Feasibility of Using a Deep Convolutional Neural Network for Scatter Estimation in X-Ray Computed Tomography** — _SPIE MI 2018_ · [Paper](https://doi.org/10.1117/12.2292919)
- **LEARN: Learned Experts’ Assessment-Based Reconstruction Network for Sparse-Data CT** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2805692)
- **LPD: Learned Primal-Dual Reconstruction** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2799231)
- **PTPN: Intelligent Parameter Tuning in Optimization-Based Iterative CT Reconstruction via Deep Reinforcement Learning** — _TMI 2018_ · [Paper](https://doi.org/10.1109/tmi.2018.2823679)
- **DeepCNN: A deep convolutional neural network using directional wavelets for low‐dose X‐ray CT reconstruction** — _Med Phys 2017_ · [Paper](https://arxiv.org/abs/1610.09736)
- **VISS: View-interpolation of sparsely sampled sinogram using convolutional neural network** — _SPIE MI 2017_ · [Paper](https://doi.org/10.1117/12.2254244)

### Self-Supervised & Untrained Methods

<sub>Training without paired data — deep image prior, noise2noise-style, unsupervised regularization · 32 papers</sub>

- **3D Field of Junctions: A Noise-Robust, Training-Free Structural Prior for Volumetric Inverse Problems** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2603.02149) · [Code](https://github.com/voilalab/3D-Field-of-Junctions)
- **DINR: Regularizing INR with Diffusion Prior for Self-Supervised 3D Reconstruction of Neutron Computed Tomography Data** — _ICASSP 2026_ · [Paper](https://arxiv.org/abs/2603.10947)
- **Equivariance2Inverse: A Practical Self-Supervised CT Reconstruction Method Benchmarked on Real, Limited-Angle, and Blurred Data** — _TCI 2026_ · [Paper](https://arxiv.org/abs/2510.23317)
- **From Sparse X-rays to 3D CT: Training-Free Reconstruction with Diffusion Priors** — _DGM4MICCAI 2026_ · [Paper](https://arxiv.org/abs/2606.20763) · [Code](https://github.com/Fredy-Zhang/TF-PRDiT)
- **HorusEye: a self-supervised foundation model for generalizable X-ray tomography restoration** — _Nat Comput Sci 2026_ · [Paper](https://doi.org/10.1038/s43588-026-00973-3) · [Code](https://github.com/Arturia-Pendragon-Iris/HorusEye)
- **MedGMAE: Gaussian Masked Autoencoders for Medical Volumetric Representation Learning** — _ICLR 2026_ · [Paper](https://openreview.net/forum?id=Z2XIRLv535) · [Code](https://github.com/windrise/MedGMAE)
- **NGPS: Structure-Preserving Self-Supervised Denoising via Neighbor-Guided Patch Sampling** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2606.23200) · [Code](https://github.com/cv-cho/NGPS)
- **Unsupervised Metal Artifact Reduction in Dental CBCT using Fine-tuned Cycle-Consistent Adversarial Networks** — _Digital 2026_ · [Paper](https://arxiv.org/abs/2607.20977)
- **An unsupervised sparse-view CT reconstruction framework using combination of iterative deep image prior and ADMM** — _Med Phys 2025_ · [Paper](https://doi.org/10.1002/mp.17933)
- **Limited-angle SPECT image reconstruction using deep image prior** — _PMB 2025_ · [Paper](https://arxiv.org/abs/2503.18342)
- **Spener: Unsupervised Self-Prior Embedding Neural Representation for Sparse-View CT Reconstruction** — _AAAI 2025_ · [Paper](https://doi.org/10.1609/aaai.v39i7.32794) · [Code](https://github.com/MeijiTian/Spener)
- **Zero-shot CT Super-Resolution using Diffusion-based 2D Projection Priors and Signed 3D Gaussians** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.15151)
- **Zero-Shot Low-dose CT Denoising via Sinogram Flicking** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2504.07927)
- **DuDoDp-MAR: Unsupervised CT Metal Artifact Reduction by Plugging Diffusion Priors in Dual Domains** — _TMI 2024_ · [Paper](https://doi.org/10.1109/tmi.2024.3351201) · [Code](https://github.com/DeepXuan/DuDoDp-MAR)
- **RBP-DIP: Residual back projection with deep image prior for ill-posed CT reconstruction** — _Neural Netw. 2024_ · [Paper](https://doi.org/10.1016/j.neunet.2024.106740)
- **PINER: Prior-Informed Implicit Neural Representation Learning for Test-Time Adaptation in Sparse-View CT Reconstruction** — _WACV 2023_ · [Paper](https://doi.org/10.1109/wacv56688.2023.00197) · [Code](https://github.com/efzero/PINER)
- **Polyner: Unsupervised Polychromatic Neural Representation for CT Metal Artifact Reduction** — _NeurIPS 2023_ · [Paper](https://arxiv.org/abs/2306.15203) · [Code](https://github.com/iwuqing/Polyner)
- **SemiMAR: Semi-Supervised Learning for CT Metal Artifact Reduction** — _JBHI 2023_ · [Paper](https://doi.org/10.1109/jbhi.2023.3312292) · [Code](https://github.com/zjk1988/SemiMAR)
- **ACID-A: Stabilizing deep tomographic reconstruction - Part A. Hybrid framework and experimental results** — _Patterns 2022_ · [Paper](https://doi.org/10.1016/j.patter.2022.100474)
- **ACID-B: Stabilizing deep tomographic reconstruction - Part B. Convergence analysis and adversarial attacks** — _Patterns 2022_ · [Paper](https://doi.org/10.1016/j.patter.2022.100475)
- **An Educated Warm Start for Deep Image Prior-Based Micro CT Reconstruction** — _TCI 2022_ · [Paper](https://doi.org/10.1109/tci.2022.3233188)
- **An Unsupervised Reconstruction Method For Low-Dose CT Using Deep Generative Regularization Prior** — _BSPC 2022_ · [Paper](https://arxiv.org/abs/2012.06448) · [Code](https://github.com/mozanunal/SparseCT)
- **DFDLM: A Dataset-free Deep Learning Method for Low-Dose CT Image Reconstruction** — _Inverse Problems 2022_ · [Paper](https://arxiv.org/abs/2205.00463)
- **GMM-unNet: Noise Characteristics Modeled Unsupervised Network for Robust CT Image Reconstruction** — _TMI 2022_ · [Paper](https://doi.org/10.1109/tmi.2022.3197400)
- **UNDIP: Sparse-view and limited-angle CT reconstruction with untrained networks and deep image prior** — _CMPB 2022_ · [Paper](https://doi.org/10.1016/j.cmpb.2022.107167)
- **IntraTomo: Self-supervised Learning-based Tomography via Sinogram Synthesis and Prediction** — _ICCV 2021_ · [Paper](https://doi.org/10.1109/iccv48922.2021.00197) · [Code](https://github.com/vccimaging/IntraTomo)
- **N2S: Self-Supervised Training For Low-Dose Ct Reconstruction** — _ISBI 2021_ · [Paper](https://doi.org/10.1109/isbi48211.2021.9433944)
- **SinoNet: Noise-Generating-Mechanism-Driven Unsupervised Learning for Low-Dose CT Sinogram Recovery** — _TRPMS 2021_ · [Paper](https://doi.org/10.1109/trpms.2021.3083361)
- **SUPER: Unified Supervised-Unsupervised (SUPER) Learning for X-ray CT Image Reconstruction** — _TMI 2021_ · [Paper](https://arxiv.org/abs/2010.02761)
- **DIP: Computed Tomography Reconstruction Using Deep Image Prior and Learned Reconstruction Methods** — _Inverse Problems 2020_ · [Paper](https://doi.org/10.1088/1361-6420/aba415) · [Code](https://github.com/oterobaguer/dip-ct-benchmark)
- **SACNN: Self-Attention Convolutional Neural Network for Low-Dose CT Denoising With Self-Supervised Perceptual Loss Network** — _TMI 2020_ · [Paper](https://doi.org/10.1109/tmi.2020.2968472)
- **SUPER-2: SUPER Learning: A Supervised-Unsupervised Framework for Low-Dose CT Image Reconstruction** — _ICCVW 2019_ · [Paper](https://doi.org/10.1109/iccvw.2019.00490)

### Diffusion & Generative Priors

<sub>Score-based, diffusion and other learned generative priors used as priors or samplers for tomographic inversion · 55 papers</sub>

- **Anatomy-preserving unpaired cone-beam CT refinement for image-guided radiotherapy using pseudo-label guided diffusion** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2610.06094)
- **CBCT-Based Synthetic CT Generation Using Conditional Flow Matching Model** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2603.05796)
- **Conditional Diffusion for 3D CT Volume Reconstruction from 2D X-rays** — _BMVC 2026_ · [Paper](https://arxiv.org/abs/2603.26509) · [Code](https://github.com/ai-med/AXON/)
- **Conditional Diffusion Posterior Alignment for Sparse-View CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2604.21960)
- **Cone-Beam CT Image Quality Enhancement Using A Latent Diffusion Model Trained with Simulated CBCT Artifacts** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2603.26014)
- **Continuity-driven Synergistic Diffusion with Neural Priors for Ultra-Sparse-View CBCT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.07980)
- **Cross-Distribution Diffusion Priors-Driven Iterative Reconstruction for Sparse-View CT** — _TMI 2026_ · [Paper](https://arxiv.org/abs/2509.13576)
- **Cross-Modal Guidance for Fast Diffusion-Based Computed Tomography** — _ICASSP 2026_ · [Paper](https://arxiv.org/abs/2603.01253)
- **DC-PnPDP: Plug-and-Play Diffusion Meets ADMM: Dual-Variable Coupling for Robust Medical Image Reconstruction** — _ICML 2026_ · [Paper](https://arxiv.org/abs/2602.23214) · [Code](https://github.com/duchenhe/DC-PnPDP) · [Project](https://duchenhe.com/project/DCPnPDP/)
- **DiffNR: Diffusion-Enhanced Neural Representation Optimization for Sparse-View 3D Tomographic Reconstruction** — _AAAI 2026_ · [Paper](https://arxiv.org/abs/2604.21518) · [Project](https://ooonesevennn.github.io/DiffNR/)
- **DINR: Regularizing INR with Diffusion Prior for Self-Supervised 3D Reconstruction of Neutron Computed Tomography Data** — _ICASSP 2026_ · [Paper](https://arxiv.org/abs/2603.10947)
- **DM4CT: Benchmarking Diffusion Models for CT Reconstruction** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2602.18589) · [Code](https://github.com/DM4CT/DM4CT)
- **Dose-Aware Cold Diffusion with Physics Consistency for Generalizable Low-Dose CT Reconstruction** — _IJCNN 2026_ · [Paper](https://arxiv.org/abs/2609.18943)
- **Field-of-View Extension in Dental Cone-Beam CT via Implicit Neural Representations and Diffusion Model-Based Refinement** — _MICAD 2026_ · [Paper](https://arxiv.org/abs/2609.28110) · [Code](https://github.com/SusanneSchaub/CBCT-FOV-Extension)
- **Foundation-VAE: Foundation VAEs for 3D CT Reconstruction, Augmentation, and Generation** — _ICML 2026_ · [Paper](https://arxiv.org/abs/2605.30893) · [Code](https://github.com/qic999/Foundation-VAE)
- **From Sparse X-rays to 3D CT: Training-Free Reconstruction with Diffusion Priors** — _DGM4MICCAI 2026_ · [Paper](https://arxiv.org/abs/2606.20763) · [Code](https://github.com/Fredy-Zhang/TF-PRDiT)
- **Geometry-Aware Diffusion Approximate Posterior Sampling for Sparse-View and Limited-Angle CT** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2610.08866)
- **ISCS: Improving 2D Diffusion Models for 3D Medical Imaging with Inter-Slice Consistent Stochasticity** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2602.04162) · [Code](https://github.com/duchenhe/ISCS)
- **KLIP: Localized Distribution Shift Detection via KL-Divergence with Diffusion Priors in Inverse Problems** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2605.31596) · [Code](https://github.com/voilalab/KLIP)
- **LUCID: Learned Undersampling-Adaptive Consistency-Guided Inference with Deterministic Flow Matching for Sparse-View CT Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2606.16212)
- **Spectral Consistent Flow for One-Step 3D Medical Image Translation** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2607.10627)
- **Toward a Foundation Plug-and-Play Prior for Computed Tomography Reconstruction via a Multimodal Diffusion Model** — _SC Workshops 2026_ · [Paper](https://arxiv.org/abs/2608.23190)
- **Toward CT-Equivalent Image Quality in Low-Dose Radiotherapy Planning: Conditional Diffusion-Based CBCT-to-CT Synthesis and the Impact of CBCT Input Representation** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2608.08919)
- **Towards reconstructing experimental sparse-view X-ray CT data with diffusion models** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.12755)
- **3D CBCT Artefact Removal Using Perpendicular Score-Based Diffusion Models** — _DGM4MICCAI 2025_ · [Paper](https://arxiv.org/abs/2603.06300)
- **Adaptive Diffusion Models for Sparse-View Motion-Corrected Head Cone-beam CT** — _TRPMS 2025_ · [Paper](https://arxiv.org/abs/2504.14033) · [Project](https://antoinedepaepe.github.io/jrm-adm-io/)
- **Advancing Limited-Angle CT Reconstruction Through Diffusion-Based Sinogram Completion** — _ICIP 2025_ · [Paper](https://arxiv.org/abs/2505.19385)
- **Bigger Isn't Always Better: Towards a General Prior for Medical Image Reconstruction** — _GCPR 2025_ · [Paper](https://arxiv.org/abs/2501.07376) · [Code](https://github.com/VLOGroup/bigger-isnt-always-better)
- **CvG-Diff: Cross-View Generalized Diffusion Model for Sparse-View CT Reconstruction** — _MICCAI 2025_ · [Paper](https://doi.org/10.1007/978-3-032-05325-1_14) · [Code](https://github.com/xmed-lab/CvG-Diff)
- **DiffNAF: Iterative Diffusion-Refined Neural Attenuation Fields for Multi-Source Stationary Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2511.14310)
- **Diffusion-Based Limited-Angle CT Reconstruction under Noisy Conditions** — _ICIP 2025_ · [Paper](https://arxiv.org/abs/2507.05647)
- **DVG-Diffusion: Dual-View Guided Diffusion Model for CT Reconstruction from X-Rays** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2503.17804)
- **Equivariant Conditional Diffusion Model for Head and Neck CT Image Synthesis from CBCT** — _Med Phys 2025_ · [Paper](https://arxiv.org/abs/2509.21913)
- **Limited-Angle CBCT Reconstruction via Geometry-Integrated Cycle-domain Denoising Diffusion Probabilistic Models** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2506.13545)
- **Mitigating Data Consistency Induced Discrepancy in Cascaded Diffusion Models for Sparse-View CT Reconstruction** — _TMI 2025_ · [Paper](https://doi.org/10.1109/tmi.2025.3557243)
- **Noise-Inspired Diffusion Model for Generalizable Low-Dose CT Reconstruction** — _Med Image Anal 2025_ · [Paper](https://arxiv.org/abs/2506.22012) · [Code](https://github.com/qgao21/NEED)
- **Ordered-subsets Multi-diffusion Model for Sparse-view CT Reconstruction** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2505.09985)
- **Projection Embedded Diffusion Bridge for CT Reconstruction from Incomplete Data** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2510.22605)
- **SDB: System-Embedded Diffusion Bridge Models** — _NeurIPS 2025_ · [Paper](https://arxiv.org/abs/2506.23726) · [Code](https://github.com/sobieskibj/sdb)
- **Steerable Conditional Diffusion for Out-of-Distribution Adaptation in Medical Image Reconstruction** — _TMI 2025_ · [Paper](https://doi.org/10.1109/tmi.2024.3524797)
- **When are Diffusion Priors Helpful in Sparse Reconstruction? A Study with Sparse-view CT** — _ISBI 2025_ · [Paper](https://arxiv.org/abs/2502.02771)
- **Zero-shot CT Super-Resolution using Diffusion-based 2D Projection Priors and Signed 3D Gaussians** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.15151)
- **DiffRecon: Diffusion Models for Medical Image Reconstruction** — _BJR|AI 2024_ · [Paper](https://doi.org/10.1093/bjrai/ubae013)
- **DuDoDp-MAR: Unsupervised CT Metal Artifact Reduction by Plugging Diffusion Priors in Dual Domains** — _TMI 2024_ · [Paper](https://doi.org/10.1109/tmi.2024.3351201) · [Code](https://github.com/DeepXuan/DuDoDp-MAR)
- **Generative Modeling in Sinogram Domain for Sparse-view CT Reconstruction** — _TRPMS 2024_ · [Paper](https://doi.org/10.1109/trpms.2023.3309474)
- **SWORD: Stage-by-Stage Wavelet Optimization Refinement Diffusion Model for Sparse-View CT Reconstruction** — _TMI 2024_ · [Paper](https://doi.org/10.1109/tmi.2024.3355455) · [Code](https://github.com/yqx7150/SWORD)
- **Two-View Industrial CT Reconstruction Based on a Multiscale Conditional Latent Diffusion Network** — _TIM 2024_ · [Paper](https://doi.org/10.1109/TIM.2024.3476543)
- **Wavelet-Improved Score-Based Generative Model for Medical Imaging** — _TMI 2024_ · [Paper](https://doi.org/10.1109/tmi.2023.3325824)
- **3DIP: Solving 3D Inverse Problems Using Pre-Trained 2D Diffusion Models** — _CVPR 2023_ · [Paper](https://doi.org/10.1109/cvpr52729.2023.02159)
- **DDDM: Dual-Domain Diffusion Model for Sparse-View CT Reconstruction** — _preprint 2023_ · [Paper](https://doi.org/10.36227/techrxiv.23726703) · [Code](https://github.com/YC-Markus/code-for-DDDM)
- **Dolce: A Model-Based Probabilistic Diffusion Framework for Limited-Angle CT Reconstruction** — _ICCV 2023_ · [Paper](https://doi.org/10.1109/ICCV51070.2023.00963)
- **CoCoDiff: A Contextual Conditional Diffusion Model for Low-dose CT Image Denoising** — _SPIE DXRT 2022_ · [Paper](https://doi.org/10.1117/12.2634939)
- **DiffMed: Diffusion Models for Medical Image Analysis: A Comprehensive Survey** — _preprint 2022_ · [Paper](https://arxiv.org/abs/2211.07804)
- **EASEL: Iterative Reconstruction for Low-Dose CT using Deep Gradient Priors of Generative Model** — _TRPMS 2022_ · [Paper](https://doi.org/10.1109/trpms.2022.3148373) · [Code](https://github.com/yqx7150/EASEL)
- **Low-Dose CT Using Denoising Diffusion Probabilistic Model for 20× Speedup** — _preprint 2022_ · [Paper](https://arxiv.org/abs/2209.15136)

### Implicit Neural Representations

<sub>Coordinate-based networks (INR / NeRF) that represent the volume itself as the unknown · 24 papers</sub>

- **DiffNR: Diffusion-Enhanced Neural Representation Optimization for Sparse-View 3D Tomographic Reconstruction** — _AAAI 2026_ · [Paper](https://arxiv.org/abs/2604.21518) · [Project](https://ooonesevennn.github.io/DiffNR/)
- **DINR: Regularizing INR with Diffusion Prior for Self-Supervised 3D Reconstruction of Neutron Computed Tomography Data** — _ICASSP 2026_ · [Paper](https://arxiv.org/abs/2603.10947)
- **Dynamic Black-hole Emission Tomography with Physics-Informed Neural Fields** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2602.08029)
- **Field-of-View Extension in Dental Cone-Beam CT via Implicit Neural Representations and Diffusion Model-Based Refinement** — _MICAD 2026_ · [Paper](https://arxiv.org/abs/2609.28110) · [Code](https://github.com/SusanneSchaub/CBCT-FOV-Extension)
- **GH-NAF: Grid-Adaptive Hash-Level-Attended Neural Attenuation Fields for Discrepancy-Aware CBCT** — _CVPR 2026_ · [Paper](https://openaccess.thecvf.com/content/CVPR2026/html/Oh_GH-NAF_Grid-Adaptive_Hash-Level-Attended_Neural_Attenuation_Fields_for_Discrepancy-Aware_CBCT_CVPR_2026_paper.html) · [Code](https://github.com/seongje-oh/GH-NAF)
- **NAB: Neural Adaptive Binning for Sparse-View CT Reconstruction** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2602.02356) · [Code](https://github.com/Wangduo-Xie/NAB_CT_reconstruction)
- **Texture-preserving implicit neural representation for Cone beam CT truncated reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2606.06039)
- **Accelerated Optimization of Implicit Neural Representations for CT Reconstruction** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2504.13390)
- **Coordinate-Based Speed of Sound Recovery for Aberration-Corrected Photoacoustic Computed Tomography** — _ICCV 2025_ · [Paper](https://arxiv.org/abs/2409.10876) · [Project](https://lukeli0425.github.io/Coord-SoS-PACT/)
- **DiffNAF: Iterative Diffusion-Refined Neural Attenuation Fields for Multi-Source Stationary Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2511.14310)
- **Epi-NAF: Enhancing Neural Attenuation Fields for Limited-Angle CT with Epipolar Consistency** — _ISBI 2025_ · [Paper](https://arxiv.org/abs/2411.06181)
- **Nonperiodic dynamic CT reconstruction using backward-warping INR with regularization of diffeomorphism (BIRD)** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2505.03463)
- **Recover Biological Structure from Sparse-View Diffraction Images with Neural Volumetric Prior** — _ICCV 2025_ · [Paper](https://arxiv.org/abs/2510.16391)
- **Spener: Unsupervised Self-Prior Embedding Neural Representation for Sparse-View CT Reconstruction** — _AAAI 2025_ · [Paper](https://doi.org/10.1609/aaai.v39i7.32794) · [Code](https://github.com/MeijiTian/Spener)
- **INCODE: Implicit Neural Conditioning with Prior Knowledge Embeddings** — _WACV 2024_ · [Paper](https://doi.org/10.1109/wacv57701.2024.00133) · [Code](https://github.com/xmindflow/INCODE)
- **INR-Joint: Implicit Neural Representations for Robust Joint Sparse-View CT Reconstruction** — _TMLR 2024_ · [Paper](https://arxiv.org/abs/2405.02509) · [Code](https://github.com/jiayangshi/INR4JointCTRecon)
- **Neural Field Regularization by Denoising for 3D Sparse-View X-Ray Computed Tomography** — _3DV 2024_ · [Paper](https://doi.org/10.1109/3dv62453.2024.00094)
- **SAX-NeRF: Structure-Aware Sparse-View X-Ray 3D Reconstruction** — _CVPR 2024_ · [Paper](https://doi.org/10.1109/cvpr52733.2024.01062) · [Code](https://github.com/caiyuanhao1998/SAX-NeRF)
- **PINER: Prior-Informed Implicit Neural Representation Learning for Test-Time Adaptation in Sparse-View CT Reconstruction** — _WACV 2023_ · [Paper](https://doi.org/10.1109/wacv56688.2023.00197) · [Code](https://github.com/efzero/PINER)
- **Polyner: Unsupervised Polychromatic Neural Representation for CT Metal Artifact Reduction** — _NeurIPS 2023_ · [Paper](https://arxiv.org/abs/2306.15203) · [Code](https://github.com/iwuqing/Polyner)
- **NAF: Neural Attenuation Fields for Sparse-View CBCT Reconstruction** — _MICCAI 2022_ · [Paper](https://arxiv.org/abs/2209.14540) · [Code](https://github.com/Ruyi-Zha/naf_cbct)
- **SNAF: Sparse-View CBCT Reconstruction with Neural Attenuation Fields** — _preprint 2022_ · [Paper](https://arxiv.org/abs/2211.17048)
- **UncertaINR: Uncertainty Quantification of End-to-End Implicit Neural Representations for Computed Tomography** — _preprint 2022_ · [Paper](https://arxiv.org/abs/2202.10847)
- **DCTR: Dynamic CT Reconstruction From Limited Views With Implicit Neural Representations** — _ICCV 2021_ · [Paper](https://doi.org/10.1109/iccv48922.2021.00226)

### Gaussian Splatting

<sub>Explicit Gaussian primitives as a differentiable tomographic representation · 24 papers</sub>

- **Active View Selection with Perturbed Gaussian Ensemble for Tomographic Reconstruction** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2603.06852)
- **Exact-GS: Mathematically Rigorous and Accurate 3D Gaussian Splatting for 3D X-Ray Reconstruction** — _CVPR 2026_ · [Paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Exact-GS_Mathematically_Rigorous_and_Accurate_3D_Gaussian_Splatting_for_3D_CVPR_2026_paper.html) · [Code](https://github.com/brucee1323/Exact-GS)
- **FaCT-GS: Fast and Scalable CT Reconstruction with Gaussian Splatting** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2604.01844) · [Code](https://github.com/PaPieta/fact-gs)
- **GR-Gaussian: Graph-Based Radiative Gaussian Splatting for Sparse-View Tomography** — _TCI 2026_ · [Paper](https://doi.org/10.1109/TCI.2026.3701585)
- **MedGMAE: Gaussian Masked Autoencoders for Medical Volumetric Representation Learning** — _ICLR 2026_ · [Paper](https://openreview.net/forum?id=Z2XIRLv535) · [Code](https://github.com/windrise/MedGMAE)
- **Projection-Volume Fidelity Divergence: Diagnosing and Controlling Optimization Drift in Sparse-View 3D Gaussian Tomography** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2606.22525)
- **Radioactive 3D Gaussian Ray Tracing for Tomographic Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2602.01057)
- **Revisiting Pose Sensitivity in Splat-based Computed Tomography under Sparse-view Reconstruction** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2608.04752)
- **Shape-guided Gaussian Splatting for Sparse-View X-ray 3D Reconstruction** — _preprint 2026_ · [Paper](https://arxiv.org/abs/2609.10376) · [Code](https://github.com/polyshape-lab/ShapeGuidedGaussian)
- **Splat-Based Metal Artifact Reduction in Cone-Beam CT via Compact Attenuation Modeling** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2608.04764)

  Conference paper (CVPR 2026) introducing a compact per-Gaussian attenuation parameterization. The same group's CGF 45(2) 2026 journal paper is the extended version. Both are peer-reviewed, so both are listed.
- **Splat-based Metal Artifact Reduction in Cone-Beam CT via Polychromatic Modeling** — _CGF 2026_ · [Paper](https://arxiv.org/abs/2608.13159)

  Journal paper (Computer Graphics Forum 45(2), 2026). Extends the same group's CVPR 2026 conference paper on this problem with joint spectral self-calibration, system-response modelling and a released synthetic CBCT dataset. Both are peer-reviewed, so both are listed.
- **TG-Field: Geometry-Aware Radiative Gaussian Fields for Tomographic Reconstruction** — _AAAI 2026_ · [Paper](https://arxiv.org/abs/2602.11705)
- **4DGS-4DCBCT: Spatiotemporal Gaussian Optimization for 4D Cone Beam CT Reconstruction from Sparsely Sampled Projections** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2501.04140) · [Code](https://github.com/fuyabo/4DGS_for_4DCBCT)
- **DGR: Discretized Gaussian Representation for Tomographic Reconstruction** — _ICCV 2025_ · [Paper](https://doi.org/10.1109/iccv51701.2025.02325) · [Code](https://github.com/wskingdom/DGR)
- **DIGS: Dynamic CBCT Reconstruction using Deformation-Informed 4D Gaussian Splatting and a Low-Rank Free-Form Deformation Model** — _MICCAI 2025_ · [Paper](https://arxiv.org/abs/2506.22280) · [Code](https://github.com/Yuliang-Huang/DIGS)
- **InsideOut: Integrated RGB-Radiative Gaussian Splatting for Comprehensive 3D Object Representation** — _ICCV 2025_ · [Paper](https://arxiv.org/abs/2510.17864)
- **Time-resolved dynamic CBCT reconstruction using prior-model-free spatiotemporal Gaussian representation (PMF-STGR)** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2503.22139)
- **Vol3DGS: Volumetrically Consistent 3D Gaussian Rasterization** — _CVPR 2025_ · [Paper](https://arxiv.org/abs/2412.03378) · [Code](https://github.com/chinmay0301ucsd/Vol3DGS)
- **X-GRM: Large Gaussian Reconstruction Model for Sparse-view X-rays to Computed Tomography** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2505.15235) · [Code](https://github.com/CUHK-AIM-Group/X-GRM)
- **X2-Gaussian: 4D Radiative Gaussian Splatting for Continuous-Time Tomographic Reconstruction** — _ICCV 2025_ · [Paper](https://doi.org/10.1109/iccv51701.2025.02293) · [Code](https://github.com/yuyouxixi/x2-gaussian)
- **Zero-shot CT Super-Resolution using Diffusion-based 2D Projection Priors and Signed 3D Gaussians** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2508.15151)
- **DIF-Gaussian: Learning 3D Gaussians for Extremely Sparse-View Cone-Beam CT Reconstruction** — _MICCAI 2024_ · [Paper](https://doi.org/10.1007/978-3-031-72104-5_41) · [Code](https://github.com/xmed-lab/DIF-Gaussian)
- **R2-Gaussian: Rectifying Radiative Gaussian Splatting for Tomographic Reconstruction** — _NeurIPS 2024_ · [Paper](https://arxiv.org/abs/2405.20693) · [Code](https://github.com/Ruyi-Zha/r2_gaussian)
- **X-Gaussian: Radiative Gaussian Splatting for Efficient X-Ray Novel View Synthesis** — _ECCV 2024_ · [Paper](https://arxiv.org/abs/2403.04116) · [Code](https://github.com/caiyuanhao1998/X-Gaussian)

### Other Topics

<sub>Industrial NDT, phase-contrast, quantitative CT, reconstruction software and anything that does not fit above · 29 papers</sub>

- **At FullTilt: Real-Time Open-Set 3D Macromolecule Detection Directly from Tilted 2D Projections** — _NeurIPS 2026_ · [Paper](https://arxiv.org/abs/2604.10766)
- **CryoDeRec: A Supervised Multi-task Framework for Joint cryo-ET Restoration Enabled by Generative Physical Simulation** — _CVPR 2026_ · [Paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_A_Supervised_Multi-task_Framework_for_Joint_cryo-ET_Restoration_Enabled_by_CVPR_2026_paper.html) · [Code](https://github.com/ZhidongYang/CryoDeRec)
- **Dynamic Black-hole Emission Tomography with Physics-Informed Neural Fields** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2602.08029)
- **Event-Based Sparse-View Background-Oriented Schlieren Tomography** — _ECCV 2026_ · [Paper](https://doi.org/10.1007/978-3-032-37335-9_18)
- **High-Precision Image Reconstruction for Binary-Valued X-Ray CT From Limited-View Projections** — _TIM 2026_ · [Paper](https://doi.org/10.1109/tim.2026.3670565)
- **HorusEye: a self-supervised foundation model for generalizable X-ray tomography restoration** — _Nat Comput Sci 2026_ · [Paper](https://doi.org/10.1038/s43588-026-00973-3) · [Code](https://github.com/Arturia-Pendragon-Iris/HorusEye)
- **Neuromorphic X-Ray Computed Tomography** — _ECCV 2026_ · [Paper](https://doi.org/10.1007/978-3-032-37577-3_8) · [Project](https://wanghongjian98.github.io/projects/neuroxct/)
- **OpenPros: A Large-Scale Dataset for Limited View Prostate Ultrasound Computed Tomography** — _ICLR 2026_ · [Paper](https://arxiv.org/abs/2505.12261) · [Project](https://open-pros.github.io/)
- **VoDaSuRe: A Large-Scale Dataset Revealing Domain Shift in Volumetric Super-Resolution** — _CVPR 2026_ · [Paper](https://arxiv.org/abs/2603.23153) · [Project](https://augusthoeg.github.io/VoDaSuRe/)
- **XDen-1K: A Density Field Dataset of Real-World Objects** — _ECCV 2026_ · [Paper](https://arxiv.org/abs/2512.10668)
- **Coordinate-Based Speed of Sound Recovery for Aberration-Corrected Photoacoustic Computed Tomography** — _ICCV 2025_ · [Paper](https://arxiv.org/abs/2409.10876) · [Project](https://lukeli0425.github.io/Coord-SoS-PACT/)
- **Investigating the effects of machine learning generalization for enhancing accuracy in fast X-ray computed tomography for industrial metrology** — _CIRP Annals 2025_ · [Paper](https://doi.org/10.1016/j.cirp.2025.04.025)
- **LCTfound: A lung CT vision foundation model facilitating disease diagnosis and medical imaging** — _Nat Commun 2025_ · [Paper](https://doi.org/10.1038/s41467-025-66620-z) · [Code](https://github.com/gingerbread000/LCTfound) · [Data](https://huggingface.co/datasets/GuoxunZhang1997/LCTfound)

  Diffusion-pretrained on 105,184 multi-centre lung CT scans with joint encoding of images and clinical text. Eight downstream tasks, of which CT enhancement and sparse-view reconstruction are the reconstruction-relevant ones.
- **Limited-angle x-ray nano-tomography with machine-learning enabled iterative reconstruction engine** — _npj Comput Mater 2025_ · [Paper](https://doi.org/10.1038/s41524-025-01724-0)
- **Modeling X-Ray Photon Pile-Up with a Normalizing Flow** — _NeurIPS Workshop 2025_ · [Paper](https://arxiv.org/abs/2511.11863)
- **MONSTR: Model-Oriented Neutron Strain Tomographic Reconstruction** — _preprint 2025_ · [Paper](https://arxiv.org/abs/2505.22187)
- **Recover Biological Structure from Sparse-View Diffraction Images with Neural Volumetric Prior** — _ICCV 2025_ · [Paper](https://arxiv.org/abs/2510.16391)
- **How auto-differentiation can improve CT workflows: classical algorithms in a modern framework** — _Opt. Express 2024_ · [Paper](https://doi.org/10.1364/oe.502920)
- **Machine learning based sinogram interpolation for X-ray computed tomography validated on experimental data** — _Precis. Eng. 2024_ · [Paper](https://doi.org/10.1016/j.precisioneng.2024.02.020)
- **Machine learning in industrial X-ray computed tomography - a review** — _CIRP JMST 2024_ · [Paper](https://doi.org/10.1016/j.cirpj.2024.05.004)
- **Two-View Industrial CT Reconstruction Based on a Multiscale Conditional Latent Diffusion Network** — _TIM 2024_ · [Paper](https://doi.org/10.1109/TIM.2024.3476543)
- **Fast algorithms based on Empirical Interpolation Methods for selecting best projections in Sparse-View X-ray Computed Tomography using a priori information** — _NDT&E Int. 2023_ · [Paper](https://doi.org/10.1016/j.ndteint.2022.102768)
- **The realisation of fast X-ray computed tomography using a limited number of projection images for dimensional metrology** — _NDT&E Int. 2023_ · [Paper](https://doi.org/10.1016/j.ndteint.2023.102852)
- **Review of high energy x-ray computed tomography for non-destructive dimensional metrology of large metallic advanced manufactured components** — _RoPP 2022_ · [Paper](https://doi.org/10.1088/1361-6633/ac43f6)
- **Laminography in the lab: imaging planar objects using a conventional x-ray CT scanner** — _Meas. Sci. Technol. 2019_ · [Paper](https://doi.org/10.1088/1361-6501/aafcae)
- **Coded aperture optimization in compressive X-ray tomography: a gradient descent approach** — _Opt. Express 2017_ · [Paper](https://doi.org/10.1364/oe.25.023833)
- **Sparse-view computed laminography with a spherical sinusoidal scan for nondestructive testing** — _Opt. Express 2014_ · [Paper](https://doi.org/10.1364/oe.22.017745)
- **Comparison of image quality in computed laminography and tomography** — _Opt. Express 2012_ · [Paper](https://doi.org/10.1364/oe.20.000794)
- **X-ray cargo container inspection system with few-view projection imaging** — _NIMA 2009_ · [Paper](https://doi.org/10.1016/j.nima.2008.08.151)

<div align="right"><a href="#top">back to top ↑</a></div>

## Toolkits

| Toolkit | Language | Stars | Description |
| --- | --- | --- | --- |
| [**MONAI**](https://github.com/Project-MONAI/MONAI) | Python | 8760 | PyTorch-based framework for medical imaging with CT reconstruction transforms and pretrained models. |
| [**3D Slicer**](https://github.com/Slicer/Slicer) | C++ | 2652 | The dominant open platform for medical image computing; used to inspect, segment and register CT volumes and to prototype reconstruction pipelines as extensions. |
| [**pydicom**](https://github.com/pydicom/pydicom) | Python | 2219 | Read, modify and write DICOM files — the standard entry point for clinical CT data. |
| [**DeepInverse**](https://github.com/deepinv/deepinv) | Python | 827 | PyTorch library for imaging inverse problems — physics operators, learned denoisers, unrolled networks and benchmarks. |
| [**TIGRE**](https://github.com/CERN/TIGRE) | MATLAB / Python | 812 | GPU-accelerated (CUDA) toolbox for cone-beam and parallel-beam CT; FDK, SART, SIRT, CGLS and TV variants. |
| [**ASTRA Toolbox**](https://github.com/astra-toolbox/astra-toolbox) | C++ / Python / MATLAB | 637 | Long-standing research toolbox with a large set of projectors and algorithms; the reference CPU/GPU baseline. |
| [**PyLops**](https://github.com/PyLops/pylops) | Python | 540 | Linear-operator library with a Radon transform and a large set of solvers (CGLS, LSQR, TV, sparsity-promoting). The cleanest way to prototype a variational CT problem without writing your own matrix-free operators. |
| [**ODL**](https://github.com/odlgroup/odl) | Python | 434 | Operator Discretization Library — a functional-analytic framework for inverse problems, with CT geometries built in. |
| [**TomoPy**](https://github.com/tomopy/tomopy) | Python | 397 | Reference toolkit for synchrotron micro/nano tomography; gridrec, FBP and phase retrieval. |
| [**tomviz**](https://github.com/OpenChemistry/tomviz) | C++ | 367 | Cross-platform application for tomographic data visualisation and processing. |
| [**sigpy**](https://github.com/mikgroup/sigpy) | Python | 339 | Signal-processing package for iterative image reconstruction; proximal operators and NUFFT primitives. |
| [**voxenra**](https://github.com/l5769389/voxenra) | Python | 299 | Cross-platform DICOM viewer for CT, MRI and PET/CT with multiplanar reformatting, 3D volume rendering and fusion — handy for eyeballing reconstruction output. |
| [**RTK**](https://github.com/RTKConsortium/RTK) | C++ | 298 | Reconstruction Toolkit built on ITK; widely used in clinical CBCT and interventional research. |
| [**torch-radon**](https://github.com/matteo-ronchetti/torch-radon) | Python | 280 | Differentiable Radon transform and filtered backprojection in PyTorch. |
| [**LEAP**](https://github.com/llnl/LEAP) | CUDA / Python | 254 | LLNL's LivermorE AI Projector for Computed Tomography (LEAP); production-grade model-based iterative reconstruction for 3D transmission CT. |
| [**RadIO**](https://github.com/analysiscenter/radio) | Python | 227 | A CT preprocessing and augmentation framework oriented towards lung-nodule pipelines; despite the name, there is no Radon transform or FBP here. |
| [**PyTomography**](https://github.com/PyTomography/PyTomography) | Python | 173 | End-to-end medical image reconstruction with quantification, including CT-based attenuation correction. |
| [**xraylib**](https://github.com/tschoonj/xraylib) | C / Python | 173 | X-ray matter interaction cross sections, fluorescence yields and Compton profiles; the physics layer for realistic simulation. |
| [**Core Imaging Library (CIL)**](https://github.com/TomographicImaging/CIL) | Python | 155 | CCPi framework for variational CT reconstruction with a large catalogue of optimisation algorithms. |
| [**TomoPhantom**](https://github.com/dkazanc/TomoPhantom) | Python | 135 | Analytical 2D/3D/4D phantom generation plus forward projection for controlled reconstruction experiments. Also listed under Learning. |
| [**MIRT**](https://github.com/JeffFessler/MIRT.jl) | Julia | 126 | Michigan Image Reconstruction Toolbox. Reference implementations of a very wide range of classical, statistical and penalised-likelihood reconstruction methods; the Julia port of the long-standing MATLAB MIRT. |
| [**OMEGA**](https://github.com/villekf/OMEGA) | MATLAB / Python | 111 | Open-source multi-dimensional tomographic reconstruction software covering PET/SPECT/CT. |
| [**Learned Primal-Dual**](https://github.com/adler-j/learned_primal_dual) | Python | 110 | Reference implementation of Learned Primal-Dual reconstruction — the canonical unrolled primal-dual scheme, originally applied to CT. |
| [**tomosipo**](https://github.com/cicwi/tomosipo) | Python | 107 | Painless specification of 2D/3D projection geometries; wraps ASTRA and integrates with PyTorch. |
| [**Learned Gradient Tomography**](https://github.com/adler-j/learned_gradient_tomography) | Python | 97 | Reference implementation of learned gradient descent for ill-posed tomography (Adler & Öktem); the origin of many later unrolled CT networks. |
| [**leehoy/CTReconstruction**](https://github.com/leehoy/CTReconstruction) | Python | 96 | Compact, readable Python and MATLAB CT reconstruction code. FBP plus ASD-POCS, SART and EM already exist under python/, though the README still lists iterative reconstruction as "to be added". |
| [**Discorpy**](https://github.com/DiamondLightSource/discorpy) | Python | 93 | Sub-pixel camera and lens distortion calibration; used to correct detector/geometry distortions before reconstruction. |
| [**IRtools**](https://github.com/jnagy1/IRtools) | MATLAB | 91 | Iterative Regularization Tools — hybrid Krylov methods, Tikhonov, TV and general-form regularisation, shipped with large-scale tomography test problems. From Hansen's group. |
| [**Physics-ArX**](https://github.com/nadeemlab/Physics-ArX) | Python | 79 | Physics-based data-augmentation library that injects realistic CT/CBCT noise, scatter and artefact models into existing images to build paired training data. |
| [**Algotom**](https://github.com/algotom/algotom) | Python | 69 | Data-processing algorithms for tomography — ring and artefact removal, distortion correction, denoising, phase retrieval and reconstruction. Developed for synchrotron beamlines. |
| [**CCPi Regularisation Toolkit**](https://github.com/TomographicImaging/CCPi-Regularisation-Toolkit) | C / Python | 63 | CPU/GPU implementations of TV, TGV, directional TV and other regularisers used by CIL. |
| [**LION**](https://github.com/CambridgeCIA/LION) | Python | 63 | Learned Iterative Optimization Networks — unrolled reconstruction with PyTorch, used in CT and PET. |
| [**Sarepy**](https://github.com/nghia-vo/sarepy) | Python | 63 | Numerical techniques for ring-artefact removal in tomography — the most complete open collection of stripe/ring filters. |
| [**DBT-Reconstruction**](https://github.com/LAVI-USP/DBT-Reconstruction) | MATLAB | 62 | Open-source reconstruction toolbox for digital breast tomosynthesis, covering DBT-specific geometry alongside FBP and iterative solvers. |
| [**LD-CT simulator**](https://github.com/smuzd/LD-CT-simulation) | MATLAB | 59 | Low-dose CT simulator that converts high-dose images into realistic low-dose counterparts using a validated noise model. |
| [**XrayPhysics**](https://github.com/kylechampley/XrayPhysics) | C++ / Python | 56 | X-ray cross sections, source-spectrum modelling, multi-material beam-hardening correction and dual-energy decomposition. From the LEAP author, and it pairs naturally with a simulator when you need a physically honest spectrum. |
| [**pySART**](https://github.com/djvine/pySART) | Python | 33 | Compact reference implementation of the Simultaneous Algebraic Reconstruction Technique. |
| [**svmbir**](https://github.com/cabouman/svmbir) | C / Python | 28 | Fast Super-Voxel Model Based Iterative Reconstruction with proximal-map plug-ins. |
| [**tofu**](https://github.com/ufo-kit/tofu) | Python | 20 | Helper layer on top of the UFO framework for fast GPU tomographic reconstruction pipelines. |
| [**CBCT Scatter Correction Tool**](https://github.com/YangkangJiang/Cone-beam-CT-scatter-correction-tool) | - | 15 | One of the very few open tools for cone-beam CT scatter estimation and correction; distributed as a prebuilt Windows executable, with no source in the repository. |
| [**libcbct**](https://github.com/tatsy/libcbct) | C++ | 10 | Lightweight cone-beam CT reconstruction library with FDK and iterative solvers; non-commercial licence. |
| [**mumott**](https://gitlab.com/liebi-group/software/mumott) | Python | 4 | Tensor-tomography reconstruction for reciprocal-space data, developed at DTU. Specialised rather than general-purpose, but it is the most complete open implementation of the tensor-tomography model. |
| [**DIRECTT Reconstruction GUI**](https://github.com/BAMresearch/DIRECTT) | Python | 1 | A Python GUI built on the ASTRA toolbox for reconstructing X-ray CT data, with the DIRECTT algorithm included. DIRECTT targets the regime where only a handful of projections are available along an arbitrary scanning trajectory and folds the acquisition path itself into the inverse problem - a corner that operator-based toolboxes mostly leave untouched. From BAM and published in Review of Scientific Instruments 2020; run Main.py to launch. Niche and lightly starred, but there is little else that covers trajectories explicitly. |
| [**pyHST2**](https://gitlab.esrf.fr/tomotools/pyhst2) | C / Python | - | The ESRF beamline reconstruction code — gridrec, FBP and iterative methods with phase retrieval for propagation-based phase-contrast tomography. Long-standing workhorse of the synchrotron community. |

<div align="right"><a href="#top">back to top ↑</a></div>

## Datasets

**Data** says what a release contains: _proj + image_ has raw projections and a reference volume, so a forward model can be scored end to end; _projections_ has raw data only; _image_ is image-domain only and cannot test a projection model.

| Dataset | Modality | Data | License | Description |
| --- | --- | --- | --- | --- |
| [**LoDoPaB-CT**](https://zenodo.org/records/3384092) | 2D fan-beam | proj + image | CC BY 4.0 | 42,895 simulated human thorax slice pairs (LIDC/IDRI) at a single noise level (N0 = 4096) — other dose levels have to be re-simulated. The de-facto standard low-dose CT benchmark; ships a well-tuned FBP/U-Net reference pipeline. |
| [**LDCT-and-Projection-data**](https://www.cancerimagingarchive.net/collection/ldct-and-projection-data/) | helical CT | proj + image | CC BY 4.0 (head scans NIH controlled access) | Mayo Clinic, released through TCIA. 299 head / chest / abdomen exams (99 / 100 / 100), each with a routine-dose scan plus one simulated lower-dose projection set — head and abdomen at 25% of routine dose, chest at 10%. Chest and abdomen are open under CC BY 4.0; the 99 head scans need an NIH controlled-access request because they could be used to reconstruct a face. Raw sinograms in the open **DICOM-CT-PD** format. It grew out of the 2016 AAPM Low Dose CT Grand Challenge and is now the best real-data source for projection-domain methods. |
| [**2DeteCT**](https://zenodo.org/records/6984866) | 2D fan-beam | proj + image | CC BY 4.0 | 5,000 real experimental 2D slices of mixed objects, 3 dose levels, multiple source-detector geometries. Excellent for reproducible real-data CT benchmarking. |
| [**Walnut-CBCT**](https://www.fips.fi/dataset.php) | cone-beam | projections | CC BY 4.0 | Finnish Inverse Problems Society. Real cone-beam projections of a walnut at several angular samplings — a standard test bed for sparse-view and limited-angle CBCT. |
| [**Helsinki Tomography Challenge 2022**](https://www.fips.fi/HTC2022.php) | 2D fan-beam | projections | CC BY 4.0 | Real limited-angle sinograms of phantoms and of a lotus root; the accompanying challenge defines the standard limited-angle protocol. |
| [**SPARE 4D-CBCT**](https://image-x.sydney.edu.au/spare-challenge/) | cone-beam, 4D | proj + image | research use | Thoracic 4D cone-beam CT for breathing-motion-resolved reconstruction; the reference benchmark for dynamic CBCT. |
| [**ToothFairy2**](https://doi.org/10.5281/zenodo.10990960) | cone-beam, dental | image | CC BY 4.0 | 480 dental CBCT scans with 3D tooth and jaw annotations; large-scale and useful for CBCT-domain pretraining. |
| [**Cone-Beam CT (CBCT) Head & Neck**](https://www.cancerimagingarchive.net/collection/head-neck/) | cone-beam | image | CC BY-NC 3.0 | Paired planning CT and on-board CBCT — the standard setting for CBCT correction and synthetic-CT work in radiotherapy. |
| [**CT-RATE**](https://zenodo.org/records/6406114) | chest CT | image | see source | 50,188 reconstructed 3D chest CT volumes (14.3M 2D slices) from 25,692 scans of 21,304 patients, every volume paired with its radiology report and labelled for 18 abnormalities. Reconstructed with several methods and window settings, so it carries realistic reconstruction variability — but image domain only, with no raw projections. The corpus behind CT-CLIP and CT-CHAT. |
| [**LIDC-IDRI**](https://www.cancerimagingarchive.net/collection/lidc-idri/) | helical CT | image | CC BY 3.0 | 1,018 thoracic CT scans with four-radiologist nodule annotations. The source anatomy behind LoDoPaB-CT and most simulated low-dose data. |
| [**DeepLesion**](https://nihcc.app.box.com/v/DeepLesion) | helical CT | image | CC BY 3.0 | 32,735 lesion annotations across 10,594 studies from 4,427 patients — a large-scale pretraining corpus for CT-domain backbones. |
| [**LUNA16**](https://luna16.grand-challenge.org/) | helical CT | image | CC BY 3.0 | 888 thin-slice chest CT scans with unified 1 mm resampling and nodule annotations; a clean, well-curated denoising/detection benchmark. |
| [**KiTS23**](https://kits-challenge.org/kits23/) | contrast CT | image | CC BY-NC 4.0 | 599 abdominal CT scans (489 training + 110 test) with kidney-tumour and cyst annotations, from the KiTS23 edition. |
| [**Pancreas-CT (NIH)**](https://www.cancerimagingarchive.net/collection/pancreas-ct/) | contrast CT | image | CC BY 3.0 | 82 abdominal contrast CT scans with expert pancreas masks; a small but very widely used reference set. |
| [**BTCV (Beyond the Cranial Vault)**](https://www.synapse.org/#!Synapse:syn3193805/wiki/217789) | contrast CT | image | CC BY-NC 4.0 | 30 abdominal CT scans with 13-organ annotations; the origin of the FLARE/AMOS lineage of multi-organ benchmarks. |
| [**TotalSegmentator**](https://zenodo.org/records/10047292) | contrast CT | image | CC BY 4.0 | 1,228 CT scans with 104 anatomical structures — the largest open CT structure set, and a strong pretraining target. |
| [**AMOS22**](https://amos22.grand-challenge.org/) | CT / MRI | image | CC BY-NC-SA 4.0 | 500 CT + 100 MRI abdominal scans, 15 organs; deliberately heterogeneous scanners, so it stresses robustness. |
| [**Medical Segmentation Decathlon**](http://medicaldecathlon.com/) | CT / MRI | image | CC BY-SA 4.0 | Ten tasks, six of them CT (liver, lung, pancreas, hepatic vessels, spleen, colon). The single most cited multi-task medical segmentation benchmark. |
| [**VerSe**](https://github.com/anjany/verse) | CT | image | CC BY-SA 4.0 | 374 multi-detector CT spine scans from 355 patients, with vertebral labelling and instance segmentation (C1–L6 plus T13 variants). Multi-vendor, multi-site, and deliberately varied in field of view and pathology — a robust segmentation benchmark. |
| [**RibFrac**](https://ribfrac.grand-challenge.org/) | CT | image | CC BY-NC 4.0 | 660 CT scans carrying ~5,000 rib-fracture annotations (420 training / 80 validation / 160 evaluation); often used as an auxiliary CT corpus. |
| [**CT-ORG**](https://www.cancerimagingarchive.net/collection/ct-org/) | contrast CT | image | CC BY 3.0 | 140 CT scans with multi-organ masks, including a subset of the Liver Tumor Segmentation benchmark. |
| [**STOIC 2021**](https://portal.imaging.datacommons.cancer.gov/collections/stoic/) | CT | image | CC BY-NC 3.0 | 10,735 COVID-19 chest CT scans from the French first wave, collected for severe-outcome prediction; a large real-clinical distribution-shift test. Listed here through the NCI Imaging Data Commons mirror, which exposes the same collection with a queryable API. |
| [**MosMedData**](https://mosmed.ai/en/datasets/datasets/covid191110/) | CT | image | CC BY-NC-ND 3.0 | 1,110 chest CT scans with COVID-19 severity grades; frequently reused as a low-quality / low-dose robustness set. The original site is currently down — the Kaggle mirror carries the same collection. |
| [**HNSCC (Head & Neck)**](https://www.cancerimagingarchive.net/collection/hnscc/) | contrast CT + PET | image | CC BY-NC 3.0 | Multi-institution head-and-neck CT with GTV/CTV delineations; pairs with the HECKTOR challenge. |
| [**CTPelvic1K**](https://github.com/MIRACLE-Center/CTPelvic1K) | contrast CT | image | CC BY-NC 4.0 | 1,184 pelvic CT scans across 7 sub-datasets; notably includes **metal-implant** cases, one of the few open sources of real metal artefacts. |
| [**FLARE22**](https://flare22.grand-challenge.org/) | contrast CT | image | CC BY-NC-SA 4.0 | 2,000 abdominal CT scans with 13-organ labels across 20+ scanners; a large-scale robustness benchmark. |
| [**AutoPET-II**](https://autopet-ii.grand-challenge.org/) | PET/CT | image | CC BY-NC 4.0 | 1,014 whole-body PET/CT studies with lesion masks; relevant when CT reconstruction feeds a downstream task. |
| [**HECKTOR**](https://hecktor.grand-challenge.org/) | PET/CT | image | CC BY-NC 4.0 | Head-and-neck PET/CT with primary-tumour delineations; five editions of consistent annotations. |
| [**CT Lymph Nodes**](https://www.cancerimagingarchive.net/collection/ct-lymph-nodes/) | contrast CT | image | CC BY 3.0 | 176 abdominal CT scans with mediastinal and abdominal lymph-node annotations. |
| [**NLST**](https://www.cancerimagingarchive.net/collection/nlst/) | low-dose CT | image | restricted (TCIA NCI) | 26,254 baseline low-dose screening CT scans — by far the largest real low-dose CT collection, though access is gated. |
| [**AAPM DL-Sparse-View CT data**](https://www.aapm.org/GrandChallenge/DL-sparse-view-CT/) | 2D fan-beam (simulated) | proj + image | CC BY 4.0 | Data of the 2021 AAPM DL-sparse-view CT challenge: 4,000 simulated 2D breast-CT phantoms, each with an ideal noiseless 128-view fan-beam sinogram over 360° and its FBP image, plus 100 test cases. Truth is known exactly, so it isolates the sparse-view inverse problem from noise and model mismatch. |
| [**Finnish Inverse Problems Society (FIPS) datasets**](https://www.fips.fi/dataset.php) | fan-beam / cone-beam | projections | CC BY 4.0 | A family of real measured sinograms (walnut, lotus root, apple, carrot, phantoms) with carefully documented acquisition geometry — the cleanest public source for testing reconstruction operators. |
| [**LoDoPaB-CT (benchmark release paper)**](https://doi.org/10.1038/s41597-021-00893-z) | 2D fan-beam | image | CC BY 4.0 | The **Scientific Data** descriptor for the LoDoPaB-CT dataset — the citation to use when you report results on this split. Documents the simulation protocol and the FBP/U-Net reference baseline. |
| [**COBRA2026: a large-scale multicenter pelvic cone-beam computed tomography projection dataset**](https://arxiv.org/abs/2607.20037) | cone-beam | proj + image | CC BY-NC 4.0 | 867 pelvic radiotherapy CBCT exams from six European centres (Elekta and Varian systems), with raw projections, acquisition geometry, clinical CBCT and planning CT. ~950 GB, split 692/52/123; released under CC BY-NC 4.0 on Zenodo (doi:10.5281/zenodo.21322350). Also the basis of the COBRA2026 reconstruction challenge. |
| [**MORE: Multi-Organ Medical Image REconstruction Dataset**](https://arxiv.org/abs/2510.26759) | CT | image | CC BY-NC 4.0 | CT scans across 9 anatomies and 15 lesion types, built to test generalisation to unseen anatomy rather than a single organ. Released under CC BY-NC 4.0; accepted to ACM MM 2025. |
| [**TomoBank**](https://tomobank.readthedocs.io/en/latest/) | synchrotron micro-CT | proj + image | see source | A repository of experimental and simulated tomographic datasets curated at the Advanced Photon Source, covering a wide range of instruments and specimen types. Built for validating and comparing reconstruction methods on data that actually looks like what a beamline produces, rather than on phantoms. |
| [**SparseBeads**](https://zenodo.org/records/290117) | micro-CT | proj + image | CC BY 4.0 | 48 measured scans of bead phantoms whose image sparsity varies systematically, released specifically as a benchmark for sparsity-regularised reconstruction. Inspired by SophiaBeads, and the reference point for comparing a regulariser across known ground truth. |
| [**Walnut-21 (two dose levels)**](https://zenodo.org/records/3763412) | cone-beam | projections | CC BY 4.0 | High-resolution cone-beam scans of 21 walnuts, each acquired at two radiation dose levels - a good and a noisy version of the same object. The paired acquisition is what makes it useful: the noise level can be compared against known anatomy instead of being inferred. |
| [**FleX-ray Walnut CBCT Collection (CWI)**](https://zenodo.org/records/2686726) | cone-beam micro-CT | proj + image | CC BY 4.0 | 42 walnuts scanned on three different orbits each, so that artefact-free reference volumes can be computed from the combined views and used as supervised-learning ground truth. Worth noting that this is not another single-object phantom: the intent is natural variability across a class of objects. Ships the complete pipeline - raw projections, scanning geometry, pre-processing and reconstruction scripts (open software) and the reconstructed volumes - which makes it usable for high cone-angle artefact reduction, sparse and limited-angle reconstruction, super-resolution and segmentation alike. Split across six Zenodo deposits covering Samples 1-42. |
| [**LoDoInd**](https://zenodo.org/records/10356955) | industrial cone-beam CT | image | CC BY-NC 4.0 | Five dose levels of the same industrial CT specimens, including a near-noise-free reference scan, all pre-registered so slices line up across levels. What sets it apart from the medical low-dose sets is the geometry and the specimens - this is inspection data from industrial hardware, not clinical anatomy, so it is the reference to use when the target is an NDT pipeline rather than a diagnostic one. 4000 slices at 1250x1250 per level, spread over three Zenodo deposits because of the 50 GB per-upload cap. |
| [**Carved cheese (FIPS)**](https://zenodo.org/records/1254210) | 2D fan-beam | projections | CC BY 4.0 | A single 2D slice of a carved cheese from the Finnish Inverse Problems Society, published at three resolutions together with the measurement matrices that encode the X-ray transform as an explicit linear operator. Getting the forward operator handed to you alongside the sinogram removes an entire class of geometry-matching bugs, which is why it stays a standard first test whenever a reconstruction method is ported onto real measured data. Documentation lives at arXiv:1705.05732. |

<div align="right"><a href="#top">back to top ↑</a></div>

## Benchmarks

| Benchmark / Challenge | Year | Tasks | Description |
| --- | --- | --- | --- |
| [**Generating synthetic computed tomography for radiotherapy: SynthRAD2025 challenge report**](https://arxiv.org/abs/2605.13555) | 2026 | cbct, synthetic-ct, reconstruction | Synthetic CT generation from CBCT and MRI — the 2025 edition of SynthRAD, with the accompanying report documenting the tasks, data and results. Same CBCT-to-CT focus as the 2023 edition, where scatter, truncation and beam hardening dominate the input. |
| [**CT-DegradBench: A Physics-Informed Benchmark for CT Degradation Detection and Severity Estimation**](https://arxiv.org/abs/2605.16431) | 2026 | reconstruction | A physics-informed benchmark for detecting CT degradations (noise, blur, artefacts) and estimating their severity — it asks what is wrong with a scan, not only how to reconstruct it. Accepted at the CVPR 2026 VISION Workshop (DEXTER track). |
| [**SPARE Challenge**](https://image-x.sydney.edu.au/spare-challenge/) | 2024 | dynamic, cbct, reconstruction | Thoracic 4D cone-beam CT reconstruction from a one-minute scan. The first widely adopted benchmark for breathing-resolved dynamic CBCT; run by the Image X Institute at the University of Sydney. |
| [**DeepInverse benchmark suite**](https://deepinv.github.io/) | 2024 | reconstruction, benchmarking | A unified PyTorch benchmark harness covering CT, MRI, deblurring and inpainting, with reproducible metrics and pretrained baselines — the most practical way to compare a new CT method against strong generic solvers. |
| [**SynthRAD2023 Challenge**](https://synthrad2023.grand-challenge.org/) | 2023 | cbct, synthetic-ct, reconstruction | Synthetic CT generation from CBCT and MRI. Relevant here because the CBCT-to-CT task is exactly where reconstruction artefacts (scatter, truncation, beam hardening) dominate — the challenge forces methods to handle them rather than assume clean input. |
| [**Helsinki Tomography Challenge**](https://www.fips.fi/HTC2022.php) | 2022 | limited-angle, reconstruction | Real measured limited-angle sinograms. A purely learned network trained on synthetic data won; the only model-based entry (CIL, directional TV) placed third — evidence that classical methods stay competitive at limited angle. |
| [**AutoPET Challenge**](https://autopet.grand-challenge.org/) | 2022 | segmentation | Whole-body PET/CT lesion segmentation, run annually since 2022 (four editions by 2025), each with a deliberately hidden multi-centre test cohort. |
| [**CTooth / CTooth+**](https://github.com/liangjiubujiu/CTooth) | 2022 | segmentation, cbct | Fully annotated 3D dental CBCT dataset and benchmark for tooth segmentation (5,803 CBCT slices), later extended to CTooth+. A small but well-annotated CBCT benchmark in a domain where artefacts are severe. |
| [**AAPM DL-Sparse-View CT Challenge**](https://www.aapm.org/GrandChallenge/DL-sparse-view-CT/) | 2021 | sparse-view, reconstruction | Recover a 2D breast-CT phantom from ideal noiseless 128-view fan-beam data: 4,000 training pairs, 100 test cases, ranked by RMSE on a public leaderboard. A common reference point for deep-learning sparse-view CT. |
| [**LoDoPaB-CT benchmark**](https://lodopab.grand-challenge.org/) | 2021 | low-dose, reconstruction | Grand-challenge style evaluation on the LoDoPaB-CT split, with a published, tuned FBP+U-Net reference baseline so improvements are measurable. |
| [**MICCAI FLARE**](https://flare.grand-challenge.org/) | 2021 | segmentation | Multi-organ abdominal CT segmentation across four editions (FLARE21/22/23/24); the standard downstream-robustness target for CT reconstruction outputs. |
| [**HECKTOR Challenge**](https://hecktor.grand-challenge.org/) | 2020 | segmentation, prognosis | Head-and-neck PET/CT tumour delineation; five editions make it one of the longer-running medical imaging challenges. |
| [**KiTS Challenge**](https://kits-challenge.org/) | 2019 | segmentation | Kidney tumour segmentation, three editions (2019/2021/2023) with strictly controlled annotation quality and a strong emphasis on cross-institution generalisation. |
| [**VerSe Challenge**](https://verse2019.grand-challenge.org/) | 2019 | segmentation | Vertebra labelling and segmentation on multi-detector CT, run in two editions with MICCAI 2019 and 2020 (374 scans, 355 patients); the hidden test set is what makes results comparable. |
| [**CHAOS Challenge**](https://chaos.grand-challenge.org/) | 2019 | segmentation | Abdominal CT and MRI organ segmentation with explicit cross-modality evaluation; the CT scans are portal-venous-phase contrast-enhanced, not low-dose. |
| [**Medical Segmentation Decathlon**](http://medicaldecathlon.com/) | 2018 | segmentation | Ten tasks with a fixed, hidden test set and a strict rule that no task-specific tuning is allowed — a genuinely fair generalisation benchmark. |
| [**Noise2Noise denoising protocol**](https://github.com/NVlabs/noise2noise) | 2018 | denoising, self-supervised | The reference implementation that popularised training a denoiser without clean targets. On CT it became the standard 'no clean ground truth' evaluation protocol — most unsupervised CT denoising papers report on a Mayo-LDCT-style split under this setting. |
| [**AAPM Low-Dose CT Grand Challenge**](https://www.aapm.org/grandchallenge/lowdosect/) | 2016 | low-dose, denoising, reconstruction | The challenge that established the quarter-dose / 10% / 5% protocol and the Mayo abdominal cohort. Nearly every low-dose CT paper still reports on this split. |
| [**SPIE-AAPM-NCI LungX Challenge**](https://www.cancerimagingarchive.net/collection/spie-aapm-lung-ct-challenge/) | 2015 | diagnosis, low-dose | Lung nodule malignancy classification on low-dose screening CT — the task is diagnostic and benchmarked against radiologists, not nodule detection. 70 cases (10 training, 60 test), distributed through TCIA. |

<div align="right"><a href="#top">back to top ↑</a></div>

## Learning

**Books**

- [Computed Tomography - From Photon Statistics to Modern Cone-Beam CT](https://doi.org/10.1007/978-3-540-39408-2) — Buzug (2008). The best single bridge from the physics (photon statistics, polychromaticity, detector response) to the reconstruction algorithms.
- [Computed Tomography - Principles, Design, Artifacts, and Recent Advances](https://www.spiedigitallibrary.org/ebooks/PM/Computed-Tomography-Principles-Design-Artifacts-and-Recent-Advances-Third-Edition/eISBN-9781628418040/10.1117/3.1764041) — Hsieh (3rd ed. 2015, SPIE). Written from inside a CT vendor: system design, dose, artefact taxonomy and clinical correction strategies.
- [CT Principles and Algorithms](https://www.google.com/search?q=%E5%BA%84%E5%A4%A9%E6%88%88+CT%E5%8E%9F%E7%90%86%E4%B8%8E%E7%AE%97%E6%B3%95) — 庄天戈. The Chinese-language introduction to CT principles and algorithms; widely used as a first course text and the natural entry point for readers who prefer Chinese. The 1992 edition has no publisher page online, so the link is a title search.
- [Foundations of Image Science](https://doi.org/10.1002/0471722138) — Barrett & Myers (2004). The encyclopaedic reference for imaging-system theory — Fourier crosstalk, task-based assessment, and the mathematical basis of iterative reconstruction.
- [Fundamentals of Computerized Tomography - Image Reconstruction from Projections](https://doi.org/10.1007/978-1-84628-723-7) — Herman (2nd ed. 2009). Very practical, with explicit algorithms, pseudocode and a careful treatment of sampling and discretisation artefacts.
- [Industrial CT Technology and Principles](https://www.ecsponline.com/goods.php?id=47496) — 张朝宗. The reference for industrial (non-destructive-testing) CT — geometry, sources, detectors and artefact sources on the industrial side, where the medical textbooks stop.
- [Medical Image Reconstruction - A Conceptual Tutorial](https://doi.org/10.1007/978-3-642-05368-9) — Zeng (2010). Deliberately intuition-first: explains *why* FBP, iterative and analytic methods behave the way they do, with minimal notation.
- [Medical Tomographic Image Reconstruction Simulation Experiments](https://www.xduph.com/pages/BookDetail.aspx?doi=6cad1ac3-8019-4263-9773-ad8bd9e39203) — 黄力宇. A hands-on Chinese-language lab manual: builds each reconstruction algorithm as a simulation experiment rather than presenting it as theory.
- [Principles of Computerized Tomographic Imaging](https://www.slaney.org/pct/pct-toc.html) — Kak & Slaney (1988). **Free online**, chapter by chapter as PDFs. The foundation: Radon transform, Fourier-slice theorem, FBP, algebraic reconstruction, fan/cone-beam rebinning. Read chapters 1-3 first.
- [The Mathematics of Computerized Tomography](https://doi.org/10.1137/1.9780898719284) — Natterer (1986, SIAM reissue). The rigorous inverse-problem treatment — Radon transform on Sobolev spaces, sampling theory, ill-posedness and regularisation.

**Courses**

- [Principles of Medical Imaging (MIT OCW 22.058)](https://ocw.mit.edu/courses/22-058-principles-of-medical-imaging-fall-2002/) — Free lecture notes and problem sets covering projection imaging, the Radon transform and reconstruction alongside MRI, ultrasound and PET.

**Tutorials**

- [ASTRA Toolbox documentation and tutorials](https://astra-toolbox.com/docs/index.html) — The most accessible hands-on entry point: CPU/GPU forward and back projectors, FBP, SART/SIRT, CGLS, with runnable examples for each geometry.
- [DeepInverse documentation](https://deepinv.github.io/) — Modern PyTorch-first tutorial track: physics operators, learned denoisers, plug-and-play and diffusion samplers, all with CT examples.
- [ODL examples](https://github.com/odlgroup/odl/tree/master/examples) — Shows how to express a CT problem as operators and functionals, then solve it with proximal methods — the clearest introduction to variational CT.
- [Radon transform in scikit-image](https://scikit-image.org/docs/stable/auto_examples/transform/plot_radon_transform.html) — Twenty lines of code from a phantom to a sinogram and back with FBP; the fastest way to build intuition before touching a real geometry.
- [TIGRE demos](https://github.com/CERN/TIGRE/tree/master/Python/demos) — Runnable GPU demos from analytical FBP through iterative, total-variation and plug-and-play reconstruction, plus a CBCT geometry-calibration walkthrough.

**Tools**

- [gVXR (gVirtualXray)](https://gvirtualxray.sourceforge.io/) — GPU-accelerated X-ray projection simulator supporting arbitrary 3D scenes and polychromatic spectra — useful for building large synthetic projection datasets.
- [NIST X-Ray Mass Attenuation Coefficients](https://www.nist.gov/pml/x-ray-mass-attenuation-coefficients) — **NIST.** Authoritative tabulation of mu/rho and mu_en/rho across the periodic table. What XrayPhysics and SpekPy are internally calibrated against — useful whenever you need to sanity-check a polychromatic model.
- [SimpleITK](https://github.com/SimpleITK/SimpleITK) — The standard I/O and resampling layer for medical volumes; almost every CT dataset in this list is easiest to load through it.
- [SpekPy](https://pypi.org/project/spekpy/) — X-ray tube spectrum simulation (TASMIP/IPEM lineage), distributed as a Python package. Use it to generate realistic polychromatic spectra for beam-hardening experiments.
- [TomoPhantom](https://github.com/dkazanc/TomoPhantom) — Fast analytical 2D/3D/4D phantom generation with built-in noise and offset models; convenient for controlled reconstruction studies. Also listed among the toolkits.
- [X-Ray Data Booklet](https://xdb.lbl.gov/) — **LBNL.** The standard quick reference for X-ray properties of the elements — absorption edges, fluorescence yields and scattering cross-sections. The first place to look when a simulation needs a physical constant.
- [XDesign](https://github.com/AdvancedPhotonSource/xdesign) — Configurable X-ray phantom generation, acquisition simulation and reconstruction benchmarking, built for developing and comparing new tomographic reconstruction methods; analytic solutions keep the simulations fast. Maintained by the Advanced Photon Source.

**Other lists**

- [Awesome 3D Gaussian Splatting](https://github.com/MrNeRF/awesome-3D-gaussian-splatting) — The reference 3DGS list. Its tomography-adjacent entries (r2_gaussian, X-Gaussian, X2-Gaussian) are the bridge to Gaussian-splatting CT.
- [Awesome CT Reconstruction (LoraLinH)](https://github.com/LoraLinH/Awesome-CT-Reconstruction) — The best-known prior CT reconstruction list. Useful for cross-checking coverage of the 2020-2024 literature.
- [Awesome Medical Imaging](https://github.com/fepegar/awesome-medical-imaging) — Broader medical image analysis resources: datasets, toolkits and pretrained models that are frequently reused in CT pipelines.
- [Awesome NeRF and 3DGS for SLAM](https://github.com/3D-Vision-World/awesome-NeRF-and-3DGS-SLAM) — Neural-field literature in the robotics/vision community; the source of the implicit-representation techniques now being adapted to CT.
- [CT Denoising Review](https://github.com/SSinyu/CT-Denoising-Review) — Dedicated to low-dose CT denoising, with an emphasis on the SSinyu/Mayo lineage of methods.
- [Low-Dose CT Denoising (code collection)](https://github.com/houguanqun/Low-Dose-CT-denoising) — A running collection of low-dose CT denoising code releases, organised by year — convenient for locating the implementation behind a given paper.

<div align="right"><a href="#top">back to top ↑</a></div>

## Contact

This list is curated and maintained by its authors; pull requests are not accepted. Questions, corrections, or a paper you want added or removed: open an [issue](https://github.com/cslht11/awesome-computed-tomography/issues) or email **[heitieya@163.com](mailto:heitieya@163.com)**.

## License

The content (`data/`, this README and the rendered pages) is licensed under [CC BY-NC-SA 4.0](LICENSE-content):

- **Attribution**: credit this list when you use it.
- **NonCommercial**: no commercial use. For commercial use, ask first.
- **ShareAlike**: adaptations must be shared under the same licence.

Code (`scripts/`, `web/`, `.github/`, `assets/`, `site.config.yml`) is [MIT](LICENSE) — including the client scripts the build copies into `site/`. License columns describe the listed projects, not this one, and each entry points to a paper rather than copying it.
