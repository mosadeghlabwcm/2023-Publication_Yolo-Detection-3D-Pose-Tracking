# 2023-Publication_Yolo-Detection-3D-Pose-Tracking
This repository contains the datasets and python code for Yolo Detection for 3D Pose Tracking of Cardiac Catheters.

With a rise in the rate of minimally invasive surgeries and the increasing prevalence of cardiovascular diseases, there has been a demand for enhanced guidance systems for catheter tracking. Traditional methods have struggled to provide precise pose information whilst deep learning techniques have provided an end to end solution. We propose Yolov5 bounding box neural network with post-processing for catheter detection and tracking based on four regions of the catheter: the tip, radio-opaque marker, bend, and entry point. 
Two datasets, containing fluoroscopic images in a paired and unpaired mode have been used to asses accuracy and robustness. 
Our method was able to accurately detect the bounding boxes with a 3D euclidean distance between prediction and ground truth as below:
- Entry: 0.235 ± 0.085 (mm)

- Marker: 0.261 ± 0.138 (mm)

- Tip: 0.285 ± 0.143 (mm)

- Bend: 0.424 ± 0.361 (mm) 

The below image provides an overview of the schematic view of our methodology:

<img width="550" class="center" alt="image" src="https://github.com/mosadeghlabwcm/2023-Publication_Yolo-Detection-3D-Pose-Tracking-/assets/44305444/f3f992c5-4021-46d6-82b7-6df0589185fb">


For using the code provided in this repository we have provided access to two datasets, one containing 1429 samples, a combinatory dataset and the other a 900 paired dataset. 
The second dataset has been generated for 3D coordinate detection and contains the images to two planes: AP and LAO90, setting a 90 degree angle with each other. Our Yolo based algorithm for catheter tracking resulted in accurate results showcased as below:


<img width="400" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdW1oNW9oem1hcjA1ZmtpMmlsOGw2bXV5YXQ4bXU1eGVpcDQyMjIyeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/g9hcovqIfRbkkfov3w/giphy-downsized-large.gif"> <img width="400" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGIxN25iaTBkNmRsNXY3ZXB3bWdyeHVuZHhkdTdmdnl0cjBqNnEzZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dBv74npfenqUo4NyDR/giphy.gif">

<br>

<b> Requirements </b>

This code was tested on:

    python 3.8.10
    numpy 1.21.6
    pandas 1.3.5

<b> Data </b>

Two folders have been provided in the code:

* The combinatory dataset, located in "combinedExperiment", includes implementation of the yolo algorithm with post-processing on paired LAO90 and AP samples combined with a dataset consisting of 529 fluoroscopic samples, with a custom-made         3D printed heart and a metal spray-painted spine to provide visibility under x-ray, gathered during a mock procedure in the catheterization lab. 

* The second dataset included in the "pairedExperiment" folder, includes implementation of the yolo algorithm with post-processing, conducted on 900 fluoroscopic images, without the 3D printed heart and metal spray painted spine, which has been            produced to enable assessment of the 3D coordinate generation of the catheter and to generalize the dataset, since these features may or may not be present in clinical images.

Note: Please adjust all paths prior to use and dedicate attention to the comments and notes provided in the code. 

