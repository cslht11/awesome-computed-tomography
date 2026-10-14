# TODO — one-line blurbs still missing

256 of the 399 papers carry a blurb in `data/summaries.yaml`; **143 do not** and
simply show no hover card (nothing is wrong with them — the title is just plain text).

**Every blurb that exists is also translated.** `data/summaries.zh.yaml` holds the
Chinese wording for all 256, so the Chinese site shows Chinese and the English site
shows English. When you fill in one of the entries below, add **both** files — and
run `python scripts/oneoff/translate_summaries.py --status` to see what is still
missing on either side.

## How to fill one in

Add an entry keyed by the paper id, in the same file:

```yaml
some-paper-id: >-
  One or two sentences on what the work does and why it is on this list.
```

- Write it in English (the Chinese site shows the English blurb for now).
- Base it on the paper itself — do not paraphrase into claims the paper does not make.
- `scripts/build.py` reports how many table notes fall back; `scripts/export_site_data.py` merges these into the payload.

## Why they are missing

The first pass took every arXiv abstract (158/158) plus the DOIs whose publishers
give Crossref an abstract (47). The second pass searched arXiv by title for the
rest, accepting a hit only at >=0.90 title similarity (+51). What is left are
journal and conference papers with no arXiv preprint and no Crossref abstract —
IEEE, Elsevier, Springer and SPIE mostly do not hand abstracts to Crossref.

## The list

### 2024 and later — 24 papers

| id | year | venue | title |
| --- | --- | --- | --- |
| `cryoderec` | 2026 | CVPR | A Supervised Multi-task Framework for Joint cryo-ET Restoration Enabled by Generative Physical Simulation |
| `event-based-bos-tomography` | 2026 | ECCV | Event-Based Sparse-View Background-Oriented Schlieren Tomography |
| `exact-gs` | 2026 | CVPR | Exact-GS: Mathematically Rigorous and Accurate 3D Gaussian Splatting for 3D X-Ray Reconstruction |
| `gh-naf` | 2026 | CVPR | GH-NAF: Grid-Adaptive Hash-Level-Attended Neural Attenuation Fields for Discrepancy-Aware CBCT |
| `gr-gaussian` | 2026 | TCI | GR-Gaussian: Graph-Based Radiative Gaussian Splatting for Sparse-View Tomography |
| `binary-ct-limited-view-2026` | 2026 | TIM | High-Precision Image Reconstruction for Binary-Valued X-Ray CT From Limited-View Projections |
| `horuseye-2026` | 2026 | Nat Comput Sci | HorusEye: A self-supervised foundation model for generalizable X-ray tomography restoration |
| `medgmae` | 2026 | ICLR | MedGMAE: Gaussian Masked Autoencoders for Medical Volumetric Representation Learning |
| `view-covariance-loss-2026` | 2026 | TPAMI | Tomographic Sparse View Selection Using the View Covariance Loss |
| `fast-ct-ml-generalization-2025` | 2025 | CIRP Annals | Investigating the effects of machine learning generalization for enhancing accuracy in fast X-ray computed tomography for industrial metrology |
| `lctfound` | 2025 | Nat Commun | A lung CT vision foundation model facilitating disease diagnosis and medical imaging |
| `sire-net-2025` | 2025 | TIM | SIRE-Net: Structure-Integrated Refinement and Enhancement Network for Limited-Angle CT Reconstruction |
| `swap-net-2025` | 2025 | TCI | Swap-Net: A Memory-Efficient 2.5D Network for Sparse-View 3D Cone Beam CT Reconstruction to ICF Applications |
| `x2-gaussian` | 2025 | ICCV | X2-Gaussian: 4D Radiative Gaussian Splatting for Continuous-Time Tomographic Reconstruction |
| `xgenrecon-2025` | 2025 | TRPMS | XGenRecon: A New Perspective in Ultrasparse Volumetric CBCT Reconstruction Through Geometry-Controlled X-Ray Projection Generation |
| `dl-ct-incomplete-data-review-2024` | 2024 | TRPMS | A Review of Deep Learning CT Reconstruction From Incomplete Projection Data |
| `sinogram-interpolation-2024` | 2024 | Precis. Eng. | Machine learning based sinogram interpolation for X-ray computed tomography validated on experimental data |
| `ml-industrial-ct-review-2024` | 2024 | CIRP JMST | Machine learning in industrial X-ray computed tomography - a review |
| `neural-field-denoising-2024` | 2024 | 3DV | Neural Field Regularization by Denoising for 3D Sparse-View X-Ray Computed Tomography |
| `pnp-proximal-trajectory-2024` | 2024 | ECCV | Plug-and-Play Learned Proximal Trajectory for 3D Sparse-View X-Ray Computed Tomography |
| `rbp-dip-2024` | 2024 | Neural Netw. | RBP-DIP: Residual back projection with deep image prior for ill-posed CT reconstruction |
| `scatter-dl` | 2024 | DL4X-ray | Scatter Correction Using Deep Learning for Cone-Beam Computed Tomography |
| `two-view-industrial-diffusion-2024` | 2024 | TIM | Two-View Industrial CT Reconstruction Based on a Multiscale Conditional Latent Diffusion Network |
| `wav-sgm` | 2024 | TMI | Wavelet-Improved Score-Based Generative Model for Medical Imaging |

### 2018-2023 — 66 papers

| id | year | venue | title |
| --- | --- | --- | --- |
| `dear` | 2023 | TIM | Deep Embedding-Attention-Refinement for Sparse-View CT Reconstruction |
| `dream-net` | 2023 | JBHI | DREAM-Net: Deep Residual Error Iterative Minimization Network for Sparse-View CT Reconstruction |
| `empirical-interpolation-projections-2023` | 2023 | NDT&E Int. | Fast algorithms based on Empirical Interpolation Methods for selecting best projections in Sparse-View X-ray Computed Tomography using a priori information |
| `irds` | 2023 | BSPC | Iterative reconstruction of low-dose CT based on differential sparse |
| `piner` | 2023 | WACV | PINER: Prior-Informed Implicit Neural Representation Learning for Test-Time Adaptation in Sparse-View CT Reconstruction |
| `semimar` | 2023 | JBHI | SemiMAR: Semi-Supervised Learning for CT Metal Artifact Reduction |
| `spie-dir-2023` | 2023 | TIM | SPIE-DIR: Self-Prior Information Enhanced Deep Iterative Reconstruction Using Two Complementary Limited-Angle Scans for DECT |
| `spqi` | 2023 | CBM | Structure-preserving quality improvement of cone beam CT images using contrastive learning |
| `acid-a` | 2022 | Patterns | Stabilizing deep tomographic reconstruction - Part A. Hybrid framework and experimental results |
| `acid-b` | 2022 | Patterns | Stabilizing deep tomographic reconstruction - Part B. Convergence analysis and adversarial attacks |
| `ccn-cl` | 2022 | CBM | CCN-CL: A content-noise complementary network with contrastive learning for low-dose computed tomography denoising |
| `cocodiff-a-contextual-conditional-diffusion-model-for-low-` | 2022 | SPIE DXRT | CoCoDiff: A Contextual Conditional Diffusion Model for Low-dose CT Image Denoising |
| `ddcl` | 2022 | ICIFXCT | Dual domain closed-loop learning for sparse-view CT reconstruction |
| `desdgan` | 2022 | JBHI | A Dual-Encoder-Single-Decoder Based Low-Dose CT Denoising Network |
| `dior` | 2022 | TMI | DIOR: Deep Iterative Optimization-Based Residual-Learning for Limited-Angle CT Reconstruction |
| `dudodr-net-2022` | 2022 | Med Image Anal | DuDoDR-Net: Dual-domain data consistent recurrent network for simultaneous sparse view and metal artifact reduction in computed tomography |
| `dudotrans` | 2022 | MLMIR | DuDoTrans: Dual-Domain Transformer for Sparse-View CT Reconstruction |
| `font-sir` | 2022 | TMI | FONT-SIR: Fourth-Order Nonlocal Tensor Decomposition Model for Spectral CT Image Reconstruction |
| `gmm-unnet` | 2022 | TMI | Noise Characteristics Modeled Unsupervised Network for Robust CT Image Reconstruction |
| `malar` | 2022 | JBHI | Multiple Adversarial Learning based Angiography Reconstruction for Ultra-low-dose Contrast Medium CT |
| `planet` | 2022 | ACM MM | Learning Projection Views for Sparse-View CT Reconstruction |
| `undip` | 2022 | CMPB | Sparse-view and limited-angle CT reconstruction with untrained networks and deep image prior |
| `casredscan` | 2021 | TMI | Limited View Tomographic Reconstruction Using a Cascaded Residual Dense Spatial-Channel Attention Network With Projection Data Fidelity Layer |
| `cd-net` | 2021 | TCI | CD-Net: Comprehensive Domain Network With Spectral Complementary for DECT Sparse-View Reconstruction |
| `clear` | 2021 | TMI | CLEAR: Comprehensive Learning Enabled Adversarial Reconstruction for Subtle Structure Enhanced Low-Dose CT Imaging |
| `dan-net` | 2021 | MICCAI | Dual-Domain Adaptive-Scaling Non-Local Network for CT Metal Artifact Reduction |
| `dctr` | 2021 | ICCV | Dynamic CT Reconstruction From Limited Views With Implicit Neural Representations |
| `deacnn` | 2021 | JBHI | Learning a Deep CNN Denoising Approach Using Anatomical Prior Information Implemented With Attention Mechanism for Low-Dose CT Imaging on Clinical Patient Data From Multiple Anatomical Sites |
| `drone` | 2021 | TMI | DRONE: Dual-Domain Residual-Based Optimization Network for Sparse-View CT Reconstruction |
| `dsignet` | 2021 | TMI | Downsampled Imaging Geometric Modeling for Accurate CT Reconstruction via Deep Learning |
| `intratomo` | 2021 | ICCV | IntraTomo: Self-supervised Learning-based Tomography via Sinogram Synthesis and Prediction |
| `lmfi` | 2021 | MICCAI | Learnable Multi-scale Fourier Interpolation for Sparse View CT Image Reconstruction |
| `pdf` | 2021 | TMI | CT Reconstruction With PDF: Parameter-Dependent Framework for Data From Multiple Geometries and Dose Levels |
| `sinonet` | 2021 | TRPMS | Noise-Generating-Mechanism-Driven Unsupervised Learning for Low-Dose CT Sinogram Recovery |
| `special` | 2021 | TCI | SPECIAL: Single-Shot Projection Error Correction Integrated Adversarial Learning for Limited-Angle CT |
| `tensor-net` | 2021 | TMI | Learning to Reconstruct CT Images From the VVBP-Tensor |
| `dl-cl` | 2020 | PLoS One | Deep learning based image reconstruction algorithm for limited-angle translational computed tomography |
| `dl-ct-rev` | 2020 | Nat Mach Intell | Deep Learning for Tomographic Image Reconstruction |
| `dlmir` | 2020 | ASARI | Deep learning methods for image reconstruction from angularly sparse data for CT and SAR imaging |
| `etedn` | 2020 | TCI | An End-to-End Deep Network for Reconstructing CT Images Directly From Sparse Sinograms |
| `fstensor` | 2020 | TMI | FSTensor: Full-spectrum-knowledge-aware tensor model for energy-resolved CT iterative reconstruction |
| `hdnet` | 2020 | TRPMS | Hybrid-domain neural network processing for sparse-view CT reconstruction |
| `lrtp` | 2020 | TMI | Spectral CT reconstruction via low-rank representation and region-specific texture preserving Markov random field regularization |
| `redaep` | 2020 | TRPMS | REDAEP: Robust and Enhanced Denoising Autoencoding Prior for Sparse-View CT Reconstruction |
| `sacnn` | 2020 | TMI | SACNN: Self-Attention Convolutional Neural Network for Low-Dose CT Denoising With Self-Supervised Perceptual Loss Network |
| `sister` | 2020 | TCI | SISTER: Spectral-Image Similarity-Based Tensor With Enhanced-Sparsity Reconstruction for Sparse-View Multi-Energy CT |
| `mw-cnn` | 2020 | Phys. Med. | Sparse-view CT reconstruction based on multi-level wavelet convolution neural network |
| `tvwfr` | 2020 | IEEE Access | Sparse View CT Image Reconstruction Based on Total Variation and Wavelet Frame Regularization |
| `dl` | 2020 | TRPMS | Limited-Angle X-Ray CT Reconstruction Using Image Gradient ℓ₀-Norm With Dictionary Learning |
| `dl-incomplete` | 2019 | PLoS One | A deep learning reconstruction framework for X-ray computed tomography with incomplete data |
| `ct-evolution` | 2019 | Eur Radiol | The Evolution of Image Reconstruction for CT: From Filtered Back Projection to Artificial Intelligence |
| `lab-lamino` | 2019 | Meas. Sci. Technol. | Laminography in the lab: imaging planar objects using a conventional x-ray CT scanner |
| `map-nn` | 2019 | Nat Mach Intell | Competitive performance of a modularized deep neural network compared to commercial algorithms for low-dose CT image reconstruction |
| `pde` | 2019 | PR | A regional adaptive variational PDE model for computed tomography image reconstruction |
| `psrv` | 2019 | Nat Biomed Eng | Patient-specific reconstruction of volumetric computed tomography images from a single projection view via deep learning |
| `sisvm` | 2019 | TMI | Learning to Reconstruct Computed Tomography Images Directly From Sinogram Data Under A Variety of Data Acquisition Conditions |
| `spss` | 2019 | SPIE MI | Sharpness preserved sinogram synthesis using convolutional neural network for sparse-view CT imaging |
| `vvbp-tsvd` | 2019 | TMI | VVBP-Tensor in the FBP Algorithm: Its Properties and Application in Low-Dose CT Reconstruction |
| `3padmm` | 2018 | TMI | Optimizing a parameterized plug-and-play ADMM for iterative low-dose CT reconstruction |
| `tv-wtf` | 2018 | IEEE Access | An Image Reconstruction Method Based on Total Variation and Wavelet Tight Frame for Limited-Angle CT |
| `cnnrpgd` | 2018 | TMI | CNN-Based Projected Gradient Descent for Consistent CT Image Reconstruction |
| `dd-net` | 2018 | TMI | A Sparse-View CT Reconstruction Method Based on Combination of DenseNet and Deconvolution |
| `dlct` | 2018 | TMI | Deep Learning Computed Tomography: Learning Projection-Domain Weights From Image Domain in Limited Angle Problems |
| `dse` | 2018 | SPIE MI | Deep Scatter Estimation (DSE): Feasibility of Using a Deep Convolutional Neural Network for Scatter Estimation in X-Ray Computed Tomography |
| `rad` | 2018 | TMI | Regularization analysis and design for prior-image-based X-ray CT reconstruction |
| `ssdae` | 2018 | Neurocomputing | Low-dose CT restoration via stacked sparse denoising autoencoders |

### before 2018 — 53 papers

| id | year | venue | title |
| --- | --- | --- | --- |
| `cnn-invrev` | 2017 | SPM | Convolutional Neural Networks for Inverse Problems in Imaging: A Review |
| `coded-aperture` | 2017 | Opt. Express | Coded aperture optimization in compressive X-ray tomography: a gradient descent approach |
| `imap-tv` | 2017 | TMI | Robust low-dose CT sinogram preprocessing via exploiting noise-generating mechanism |
| `ksae` | 2017 | TMI | Iterative Low-dose CT Reconstruction with Priors Trained by Artificial Neural Network |
| `ldct-cnn` | 2017 | BOE | Low-dose CT via convolutional neural network |
| `kbr-perfusion` | 2017 | TMI | Low-Dose Dynamic Cerebral Perfusion Computed Tomography Reconstruction via Kronecker-Basis-Representation Tensor Sparsity Regularization |
| `ratv` | 2017 | TNS | Reweighted Anisotropic Total Variation Minimization for Limited-Angle CT Reconstruction |
| `red-cnn` | 2017 | TMI | Low-Dose CT with a Residual Encoder-Decoder Convolutional Neural Network |
| `viss` | 2017 | SPIE MI | View-interpolation of sparsely sampled sinogram using convolutional neural network |
| `lr-tv-perfusion` | 2016 | Neurocomputing | Low-dose cerebral perfusion computed tomography image restoration via low-rank and total variation regularizations |
| `mar-4dec` | 2016 | IEEE Access | Metal Artifact Reduction in CT: Where Are We After Four Decades? |
| `mccollough-2015` | 2015 | Radiology | Dual- and Multi-Energy CT: Principles, Technical Approaches, and Clinical Applications |
| `sv-spectral-lr` | 2015 | TMI | Sparse-View Spectral CT Reconstruction Using Spectral Patch-Based Low-Rank Penalty |
| `lowmas-sparseview` | 2014 | Opt. Express | Low-dose X-ray computed tomography image reconstruction with a combined low-mAs and sparse-view protocol |
| `sparse-view-laminography-2014` | 2014 | Opt. Express | Sparse-view computed laminography with a spherical sinusoidal scan for nondestructive testing |
| `sv-tgv` | 2014 | PMB | Sparse-view x-ray CT reconstruction via total generalized variation regularization |
| `tv-stokes` | 2014 | TMI | Total Variation-Stokes Strategy for Sparse-View X-ray CT Image Reconstruction |
| `atv-limited-angle` | 2013 | PMB | A limited-angle CT reconstruction method based on anisotropic TV minimization |
| `fc-cs-rpca` | 2013 | PMB | Feature constrained compressed sensing CT image reconstruction from incomplete data via robust principal component analysis of the database |
| `linct-tv-admm` | 2013 | Chinese Phys. B | Image reconstruction based on total-variation minimization and alternating direction method in linear scan computed tomography |
| `shearlet` | 2013 | TNS | Iterative CT Reconstruction Using Shearlet-Based Regularization |
| `ndi-tv` | 2013 | PLoS One | Iterative Image Reconstruction for Sparse-View CT Using Normal-Dose Image Induced Total Variation Prior |
| `offset-cbct` | 2013 | PMB | Optimization-based image reconstruction from sparse-view data in offset-detector CBCT |
| `awtv` | 2012 | PMB | Adaptive-weighted total variation minimization for sparse data toward low-dose x-ray computed tomography image reconstruction |
| `cl-vs-ct` | 2012 | Opt. Express | Comparison of image quality in computed laminography and tomography |
| `dual-dict` | 2012 | PMB | Few-view image reconstruction with dual dictionaries |
| `dict-learning-low-dose-2012` | 2012 | TMI | Low-Dose X-ray CT Reconstruction via Dictionary Learning |
| `dbt-task` | 2011 | Med Image Anal | Task-based performance analysis of FBP, SART and ML for digital breast tomosynthesis using signal CNR and Channelised Hotelling Observers |
| `sv-cbct-eval` | 2010 | PMB | Evaluation of sparse-view reconstruction from flat-panel-detector cone-beam CT |
| `tomo-21st` | 2010 | SPM | Tomographic Reconstruction in the 21st Century |
| `dir-view-interp` | 2009 | TMI | Directional View Interpolation for Compensation of Sparse Angular Sampling in Cone-Beam CT |
| `irr-tv` | 2009 | TNS | Few-View Projection Reconstruction With an Iterative Reconstruction-Reprojection Algorithm and TV Constraint |
| `why-fbp` | 2009 | Inverse Problems | Why do commercial CT scanners still employ traditional, filtered back-projection for image reconstruction? |
| `cargo-fewview` | 2009 | NIMA | X-ray cargo container inspection system with few-view projection imaging |
| `dts-deform` | 2008 | Med Phys | A novel digital tomosynthesis (DTS) reconstruction method using a deformation field map |
| `schlomka-2008` | 2008 | PMB | Experimental Feasibility of Multi-Energy Photon-Counting K-Edge Imaging in Pre-Clinical Computed Tomography |
| `leng-2008` | 2008 | PMB | High Temporal Resolution and Streak-Free Four-Dimensional Cone-Beam Computed Tomography |
| `sidky-pan-tv-2008` | 2008 | PMB | Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization |
| `piccs` | 2008 | Med Phys | Prior Image Constrained Compressed Sensing (PICCS): A Method to Accurately Reconstruct Dynamic CT Images from Highly Undersampled Projection Data Sets |
| `roessl-2007` | 2007 | PMB | K-Edge Imaging in X-Ray Computed Tomography Using Multi-Bin Photon Counting Detectors |
| `zbijewski-2006` | 2006 | TMI | Efficient Monte Carlo Based Scatter Artifact Reduction in Cone-Beam Micro-CT |
| `ksvd-2006` | 2006 | TSP | K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation |
| `zhu-2006` | 2006 | TMI | Scatter Correction Method for X-Ray CT Using Primary Modulation: Theory and Preliminary Results |
| `elbakri-2002` | 2002 | TMI | Statistical Image Reconstruction for Polyenergetic X-Ray Computed Tomography |
| `deman-2001` | 2001 | TMI | An Iterative Maximum-Likelihood Polychromatic Algorithm for CT |
| `siewerdsen-2001` | 2001 | Med Phys | Cone-Beam Computed Tomography with a Flat-Panel Imager: Magnitude and Effects of X-Ray Scatter |
| `rof-tv-1992` | 1992 | Physica D | Nonlinear total variation based noise removal algorithms |
| `fdk-1984` | 1984 | JOSA A | Practical cone-beam algorithm |
| `sart-1984` | 1984 | Ultrasonic Imaging | Simultaneous Algebraic Reconstruction Technique (SART): A superior implementation of the ART algorithm |
| `mlem-1982` | 1982 | TMI | Maximum Likelihood Reconstruction for Emission Tomography |
| `alvarez-1976` | 1976 | PMB | Energy-Selective Reconstructions in X-Ray Computerised Tomography |
| `shepp-logan-1974` | 1974 | TNS | The Fourier reconstruction of a head section |
| `radon-1917` | 1917 | Ber. Verh. Sächs. Akad. Wiss. Leipzig, Math.-Phys. Kl. | Über die Bestimmung von Funktionen durch ihre Integralwerte längs gewisser Mannigfaltigkeiten (Johann Radon) |

