# Columbia University Engineering - IoT Final Project 2018: Spoony, your smart spoon

This repository contains all the code to implement our IoT device:  Spoony, your smart spoon. Contributors are Jan-Felix Schneider, Sing Pou Lee and Tvisha Gangwani.

<p align="center"> 
<img src="images/prize.jpeg" alt="drawing" width="500"/>
</p>
<p align="center"><i>Our project won the 1st prize at the Columbia EE/CE Master Student Projects Expo 2018</i></p> 

# Brief Description of Project
Understanding that many people wish to have a healthier diet and track what they are eating but find it inconvenient to do so, we want to build a practical, functional spoon that can do all that for us automatically. 

The implementation of this spoon required the following fields of knowledge:  embedded systems - sensors & actuators, cloud computing for the server, data visualization for the dashboard and data science/deep learning for image recognition.  

Please click on the link below to access our project website and video:
^^to add url^^

# Organization of Files

* _raspi_code_ sub-dir: contains all code that runs on our Pi. They are for our Pi to communicate with our sensors and actuators (accelerometer, pressure sensor, thermometer, camera, LED, OLED display) and to send and receive information from the server. `Main1.py` is the main file to run for operating Spoony; the functions in the rest of the files are called by the main file.  

* _server_code_ sub-dir: contains all code that runs on our server. It includes code to run our Convolutional Neural Network for image  classification and for our analytics dashboard.

* _img_reg_model_code_ sub-dir: contains two notebooks for our image recognition. The first notebook contains code to build the  training dataset - resize images to correct dim; save images as numpy matrices. The second notebook contains code to build our image recognition model and train on our own training iamges - Transfer learning using Xception loaded with weights pre-trained on ImageNet with last fully-connected layer replaced with our own.

* _images_ sub-dir: contains our team photo and social media app icons for our dashboard.
