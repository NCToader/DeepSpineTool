# DeepSpineTool
This repository contains our GUI application for automatic spine segmentation and refinement. 

## Installation
Requires **Python 3.6.8 or later** and **CUDA 10.1** (to enable the use of GPUs to greatly reduce the automatic segmentation time. It can be used without CUDA on CPU, with a longer execution time.).
1. Download the current project:
   > git clone https://gitfront.io/r/user-4306573/cea608399c9a77e6a945a4cad004634422d13436/DeepSpineTool.git
2. Install dependencies (from the root directory of the project):
   > pip install -r requirements.txt.
3. Download our models from https://bit.ly/2WlCiFc (`models.zip`)
4. Uncompress the previous file in the root folder of the project. 

This should be the content of the project after the previous steps:
 * app
    * ...
 * models
    * M1
    * M2
    * M3
 * ...

## Usage
To start the tool, use the following command:
> python main.py


