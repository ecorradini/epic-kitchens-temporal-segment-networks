# Temporal Segment Networks fork for Epic Kitchens Dataset
Codes and models.

## Prerequisites
* [Ubuntu](https://www.ubuntu.com/)
* [NVIDIA CUDA](https://developer.nvidia.com/cuda-zone)
* [NVIDIA cuDNN](https://developer.nvidia.com/cudnn)
* [Caffe with VideoDataLayer](https://github.com/yjxiong/caffe)
* [dense_flow](https://github.com/yjxiong/dense_flow)
* Python

## Installation
First install CUDA from NVIDIA website (runfile recomended) with the NVIDIA proprietary driver.

Use the `build_all.sh` script.

### Troubleshooting
#### 1. Caffe Makefile.config
Caffe needs to be configured before compiling.

To do so first run `mv Makefile.config.example Makefile.config` and then edit the file.
```
CPU_ONLY:=1 uncomment to build only with CPU (not recomended)
USE_CUDNN:=1 uncomment to build with cuDNN support (recomended but cuDNN required)
```
Check your GPU in [CUDA list](https://developer.nvidia.com/cuda-gpus) and, if needed, add its code to `CUDA_ARCH`.
```
For CUDA < 6.0, comment the *_50 through *_61 lines for compatibility.
For CUDA < 8.0, comment the *_60 and *_61 lines for compatibility.
For CUDA >= 9.0, comment the *_20 and *_21 lines for compatibility.
```
> For example: NVIDIA GTX 1080: comment the *_20 and *_21 and add *_61 lines.

#### 2. Cuda.cmake
If you get an error saying that `compute_20` architecture is not supported, modify `cmake/Cuda.cmake`.
Just change the row `set(Caffe_known_gpu_archs .... )` adding codes used for Makefile.config.

## References
* This project is based on [temporal-segment-networks](https://github.com/yjxiong/temporal-segment-networks) for academic purposes.
* This project uses [Epic Kitchens](https://epic-kitchens.github.io/2018) dataset.
