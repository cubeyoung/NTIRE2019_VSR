# NTIRE2019_VSR
NTIRE2019_VideoSuperResolution Challenge 
# NTIRE2019_VSR
NTIRE2019_VideoSuperResolution Challenge 

### Introduction

In this code, we propose efficient module based Video image SR networks
and tackle multiple VSR problems in NTIRE 2019 VSR challenge by recycling trained networks. Our proposed
EMBVSR allowed us to reduce training time with effectively deeper networks, to use modular ensemble for improved
performance, and to separate subproblems for better performance. We utilized RCAN which is state-of-the-art network for Singel image sueprresolution.

    
### Installation

Install <a href="https://pytorch.org/">pytorch</a>. The code is tested under 0.4.1 GPU version and Python 3.6  on Ubuntu 16.04.

### Training and Test

1. Download the datasets you need.

2. Start training process by running following commands:

    ```Shell
    sh demo.sh
    ```
    
### Acknowledgment

This code is based on EDSR. Thanks to the contributors of EDSR.

    @inproceedings{lim2017enhanced,
      title={Enhanced deep residual networks for single image super-resolution},
      author={Lim, Bee and Son, Sanghyun and Kim, Heewon and Nah, Seungjun and Lee, Kyoung Mu},
      booktitle={The IEEE conference on computer vision and pattern recognition (CVPR) workshops},
      pages={1132-1140},
      year={2017}
    }
