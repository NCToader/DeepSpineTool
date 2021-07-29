# DeepSpineTool
This repository contains our GUI application for automatic spine segmentation and refinement. 

## Installation
Requires **Python 3.6.8 or later** and **CUDA 10.1** (to enable the use of GPUs to greatly reduce the automatic segmentation time. It can be used without CUDA on CPU, with a longer execution time.).
1. Download the current project:
   > git clone https://gitfront.io/r/user-4306573/cea608399c9a77e6a945a4cad004634422d13436/DeepSpineTool.git
2. Install dependencies (from the root directory of the project):
   > pip install -r requirements.txt.
3. Download our models (`models.zip`) from https://bit.ly/2WlCiFc 
4. Extract the previous file in the root folder of the project. 

After the previous steps, folder structure should be:
* `DeepSpineTool`
     * `app`
     * `models`
        * `M1`
        * `M2`
        * `M3`
     * ...
 
## Installation for Windows 10
The previous instructions can be used to run our application in any operating system that supports its dependencies. We also provide an executable ready to run in Windows 10.
To use this executable:
1. Download `DeepSpineTool executable win10.zip` from https://bit.ly/2WlCiFc
2. Extract the previous file
3. Download our models (`models.zip`) from https://bit.ly/2WlCiFc 
4. Extract the previous file in `DeepSpineTool executable win10`

After the previous steps, folder structure should be: 
 * `DeepSpineTool executable win10`
     * `DeepSpineTool.exe`
     * `models`
        * `M1`
        * `M2`
        * `M3`
     * ...

## Usage
To present our application functionality, we provide a sample project. It can be downloaded from: https://bit.ly/2WlCiFc (`sample.scn`) 

#### Running the application
* To start the tool, use the following command (if using the executable: Open `DeepSpineTool.exe`):
    > python main.py

* Once the main window appears, in the upper menu, open the sample project with  `Scene` > `Load` and accept the prompt message.
* Locate the sample project and open it.

#### View an image
* To view the image, select `ROI_RAW_test6.tif` in the `Scene Manager` pane
* In the upper menu, hover on `Image` > `Viewers` and click on `Basic Image 3D Viewer` 

#### Segment an image
* To segment the image, select `ROI_RAW_test6.tif` in the `Scene Manager` pane
* In the upper menu, hover on `Segmentation` > `Deep Learning` and click one of `M1` `M2` or `M3` (If no option shows when hovering over `Deep Learning`, the model folder has not been placed correctly, please check the installation instruction)
* Click on the `Close when finished` checkbox from the progress prompt and wait for the process to finish
* The segmented image has been added to the `Scene Manager` pane (`ROI_RAW_test6.tif (Seg: u_net3d_deep)`) and can be viewed following the steps from the previous section


