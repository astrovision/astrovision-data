<a href="https://imgur.com/Vs3Rwin"><img src="https://i.imgur.com/Vs3Rwin.png" title="source: imgur.com" /></a>

# _This repository features scripts for downloading and manipulating the AstroVision datasets_ [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1A79acc-RwQG2X1OoNd_UL1fT7T3FNtpN)

<a href="https://imgur.com/RjSwdG2"><img src="https://i.imgur.com/RjSwdG2.png" title="source: imgur.com" /></a>

# About

AstroVision is a first-of-a-kind, large-scale dataset of real small body images from both legacy and ongoing deep space missions, which currently features over 110,000 densely annotated, real images of sixteen small bodies from eight missions. AstroVision was developed to facilitate the study of computer vision and deep learning for autonomous navigation in the vicinity of a small body, with speicial emphasis on training and evaluation of deep learning-based keypoint detection and feature description methods.

If you find our datasets useful for your research, please cite the [AstroVision paper](https://www.sciencedirect.com/science/article/pii/S0094576523000103):

```bibtex
@article{driver2023astrovision,
  title={{AstroVision}: Towards Autonomous Feature Detection and Description for Missions to Small Bodies Using Deep Learning},
  author={Driver, Travis and Skinner, Katherine and Dor, Mehregan and Tsiotras, Panagiotis},
  journal={Acta Astronautica: Special Issue on AI for Space},
  year={2023},
  volume={210},
  pages={393--410}
}
```

Please make sure to :star: star and :eye: watch the repository to show support and get notified of any updates!

# Downloading the datasets

### **Note:** We will continue to release datasets and update this repository over the coming months. Available datasets can be found by checking the `lists/` directory or our 🤗 [Hugging Face page](https://huggingface.co/datasets/travisdriver/astrovision-data)

The AstroVision datasets may be downloaded using the provided `download_astrovision.py` script or by downloading them directly from our 🤗 [Hugging Face page](https://huggingface.co/datasets/travisdriver/astrovision-data). The train and test data may be downloaded using the `--train` and `--test` options, respectively:

```bash
python download_astrovision.py --train  # downloads training data to data/test
python download_astrovision.py --test  # downloads training data to data/train
```

The `--segments` (`--clusters`) option will download _all available_ segments (clusters). If you'd like to download segments (clusters) from a specific dataset, use the `--dataset_name <name_of_dataset>` option, e.g., `--dataset_name dawn_ceres`. Specific segments (clusters) from a specific dataset may be downloaded using the `--dataset_name <name_of_dataset>` and `--segment_name <name_of_segment>` (`--cluster_name <name_of_cluster>`) options, e.g.,

```bash
python download_astrovision.py --segments --dataset_name dawn_ceres --segment_name 2015293_c6_orbit125  # download specific segment
python download_astrovision.py --clusters --dataset_name dawn_ceres --cluster_name 00000032  # download specific cluster
```

Below we provide more detailed information about each dataset.

| Mission          | Target                    | Launch (yyyy/mm/dd) | # Images | Disk (GB)  | Clusters | Segments |
|:----------------:|:-------------------------:|:-------------------:|:--------:|:----------:|:--------:|:--------:|
| NEAR             | 433 Eros                  | 1996/02/17          |    12827 |    13.1 | TBA | TBA |
| Cassini          | Mimas (Saturn I)          | 1997/10/15          |      307 |     3.0 | N/A | [cas_mimas](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/cas_mimas) |
|                  | Tethys (Saturn III)       |                     |      751 |     9.2 | N/A | [cas_tethys](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/cas_tethys) |
|                  | Dione (Saturn IV)         |                     |     1381 |    12.0 | N/A | [cas_dione](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/cas_dione) |
|                  | Rhea (Saturn V)           |                     |      665 |     5.1 | N/A | [cas_rhea](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/cas_rhea) |
|                  | Phoebe (Saturn IX)        |                     |       96 |     0.8 | N/A | [cas_phoebe](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/cas_phoebe) |
|                  | Janus (Saturn X)          |                     |      184 |     2.0 | N/A | [cas_janus](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/cas_janus) |
|                  | Epimetheus (Saturn XI)    |                     |      133 |     1.3 | N/A | [cas_epim](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/cas_epim) |
| Hayabusa         | 25143 Itokawa             | 2003/05/09          |      560 |     5.4 | N/A | [haya_itokawa](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/haya_itokawa) |
| Mars Express     | Phobos (Mars I)           | 2003/06/02          |      890 |     4.1 | N/A | TBA |
| Rosetta (NavCam) | 67P/Churyumov–Gerasimenko | 2004/03/02          |    12315 |    95.0 | TBA / [test](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/clusters/test/rosetta_67p) | TBA |
| Rosetta (OSIRIS) | 67P/Churyumov–Gerasimenko | 2004/03/02          |    13993 |    95.0 | TBA / [test](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/clusters/test/rosiris_67p) | TBA |
|                  | 21 Lutetia                |                     |       40 |     2.1 | N/A | [rosetta_lutetia](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/rosetta_lutetia) |
| Dawn             | 1 Ceres                   | 2007/09/27          |    38540 |   204.8 | [train](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/clusters/train/dawn_ceres) / [test](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/clusters/test/dawn_ceres) | TBA |
|                  | 4 Vesta                   |                     |    17504 |    93.3 | [train](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/clusters/train/dawn_vesta) / [test](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/clusters/test/dawn_vesta) | [dawn_vesta](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/segments/dawn_vesta) |
| Hayabusa2        | 162173 Ryugu              | 2014/12/03          |      640 |     6.0 | N/A | TBA |
| OSIRIS-REx       | 101955 Bennu              | 2016/09/08          |    16618 |   106.5 | [train](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/clusters/train/orex_bennu) / [test](https://huggingface.co/datasets/travisdriver/astrovision-data/tree/main/clusters/test/orex_bennu) | TBA |
| TOTAL            |                           |                     |   117493 |   658.7 |     |                |

# Data format

Following the popular [COLMAP data format](https://colmap.github.io/format.html), each data segment contains the files `images.bin`, `cameras.bin`, and `points3D.bin`, which contain the camera extrinsics and keypoints, camera intrinsics, and 3D point cloud data, respectively.

- `cameras.bin` encodes a dictionary of `camera_id` and [`Camera`](third_party/colmap/scripts/python/read_write_model.py) pairs. `Camera` objects are structured as follows:
  - `Camera.id`: defines the unique (and possibly noncontiguious) identifier for the `Camera`.
  - `Camera.model`: the camera model. We utilize the "PINHOLE" camera model, as AstroVision contains undistorted images.
  - `Camera.width` & `Camera.height`: the width and height of the sensor in pixels.
  - `Camera.params`: `List` of cameras parameters (intrinsics). For the "PINHOLE" camera model, `params = [fx, fy, cx, cy]`, where `fx` and `fy` are the focal lengths in $x$ and $y$, respectively, and (`cx`, `cy`) is the principal point of the camera.

- `images.bin` encodes a dictionary of `image_id` and [`Image`](third_party/colmap/scripts/python/read_write_model.py) pairs. `Image` objects are structured as follows:
  - `Image.id`: defines the unique (and possibly noncontiguious) identifier for the `Image`.
  - `Image.tvec`: $\mathbf{r}^\mathcal{C_ i}_ {\mathrm{BC}_ i}$, i.e., the relative position of the origin of the camera frame $\mathcal{C}_ i$ with respect to the origin of the body-fixed frame $\mathcal{B}$ expressed in the $\mathcal{C}_ i$ frame.
  - `Image.qvec`: $\mathbf{q}_ {\mathcal{C}_ i\mathcal{B}}$, i.e., the relative orientation of the camera frame $\mathcal{C}_ i$ with respect to the body-fixed frame $\mathcal{B}$. The user may call `Image.qvec2rotmat()` to get the corresponding rotation matrix $R_ {\mathcal{C}_ i\mathcal{B}}$.
  - `Image.camera_id`: the identifer for the camera that was used to capture the image.
  - `Image.name`: the name of the corresponding file, e.g., `00000000.png`.
  - `Image.xys`: contains all of the keypoints $\mathbf{p}^{(i)}_ k$ in image $i$, stored as a ($N$, 2) array. In our case, the keypoints are the forward-projected model vertices.
  - `Image.point3D_ids`: stores the `point3D_id` for each keypoint in `Image.xys`, which can be used to fetch the corresponding `point3D` from the `points3D` dictionary.

- `points3D.bin` enocdes a dictionary of `point3D_id` and [`Point3D`](third_party/colmap/scripts/python/read_write_model.py) pairs. `Point3D` objects are structured as follows:
  - `Point3D.id`: defines the unique (and possibly noncontiguious) identifier for the `Point3D`.
  - `Point3D.xyz`: the 3D-coordinates of the landmark in the body-fixed frame, i.e., $\mathbf{\ell} _{k}^\mathcal{B}$.
  - `Point3D.image_ids`: the ID of the images in which the landmark was observed.
  - `Point3D.point2D_idxs`: the index in `Image.xys` that corresponds to the landmark observation, i.e., `xy = images[Point3D.image_ids[k]].xys[Point3D.point2D_idxs[k]]` given some index `k`.

These three data containers, along with the ground truth shape model, completely describe the scene.

In addition to the scene geometry, each image is annotated with a landmark map, a depth map, and a visibility mask.

<a href="https://imgur.com/DGUC0ef"><img src="https://i.imgur.com/DGUC0ef.png" title="source: imgur.com" /></a>

- The _landmark map_ provides a consistent, discrete set of reference points for sparse correspondence computation and is derived by forward-projecting vertices from a medium-resolution (i.e., $\sim$ 800k facets) shape model onto the image plane. We classify visible landmarks by tracing rays (via the [Trimesh library](https://trimsh.org/)) from the landmarks toward the camera origin and recording landmarks whose line-of-sight ray does not intersect the 3D model.
- The _depth map_ provides a dense representation of the imaged surface and is computed by backward-projecting rays at each pixel in the image and recording the depth of the intersection between the ray and a high-resolution (i.e., $\sim$ 3.2 million facets) shape model.
- The _visbility mask_ provides an estimate of the non-occluded portions of the imaged surface.

**Note:** Instead of the traditional $z$-depth parametrization used for depth maps, we use the _absolute depth_, similar to the inverse depth parameterization. Let $\mathbf{m}^{(i)}_ k = K^{-1} \underline{\mathbf{p}}^{(i)}_ k$, where $K$ is the calibration matrix. Then, the landmark $\mathbf{\ell}_ k$ corresponding to keypoint $\mathbf{p}^{(i)}_ {k}$ with depth $d^{\mathcal{C}_ i}_ k$ (from the depth map) can be computed via

$$
\begin{align}
    \underline{\mathbf{\ell}}_ {k}^\mathcal{B} = \Pi^{-1}\left(\mathbf{p}^{(i)}_ k, d^{\mathcal{C}_ i}_ k, T_ {\mathcal{C}_ i\mathcal{B}}; K\right) &= T_ {\mathcal{C}_ i\mathcal{B}}^{-1} \begin{bmatrix} d^{\mathcal{C}_ i}_ k \mathbf{m}^{(i)}_ k / \|\mathbf{m}^{(i)}_ k\| \\ 1 \end{bmatrix} \\
    &= \frac{d^{\mathcal{C}_ i}_ k}{\|\mathbf{m}^{(i)}_ k\|} R_ {\mathcal{BC_i}} \mathbf{m}^{(i)} _k + \mathbf{r}^\mathcal{B} _{\mathrm{C} _i\mathrm{B}}.
\end{align}
$$

Please refer to our [Google Colaboratory demo](https://colab.research.google.com/drive/1A79acc-RwQG2X1OoNd_UL1fT7T3FNtpN?usp=sharing) for more details. [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1A79acc-RwQG2X1OoNd_UL1fT7T3FNtpN)

# Dataset tools

We will be releasing tools for manipulating (e.g., splitting and stitching) and generating the AstroVision dataset in a future release.

# Projects that have used AstroVision

Below is a list of papers that have utilized the AstroVision datasets:

- [Deep Monocular Hazard Detection for Safe Small Body Landing](https://arxiv.org/abs/2301.13254). AIAA/AAS Space Flight Mechanics Meeting, 2023
- [Efficient Feature Description for Small Body Relative Navigation using Binary Convolutional Neural Networks](https://arxiv.org/abs/2304.04985). AAS Guidance, Navigation, and Control (GN&C) Conference, 2023.
