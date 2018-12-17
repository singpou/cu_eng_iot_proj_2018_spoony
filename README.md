# Columbia University Engineering - IoT Final Project 2018: Spooony, your smart spoon

This repository provides the documentation and code for our IoT device:  Spooony, your smart spoon. Team members are Jan-Felix Schneider, Sing Pou Lee and Tvisha Gangwani.

<p align="center"> 
<img src="images/prize.jpeg" alt="drawing" width="500"/>
</p>
<p align="center"><i>Our project won the 1st prize at the Columbia EE/CE Master Student Projects Expo 2018</i></p> 

# Brief Description of Project
We understand that many people wish to have a healthier diet and track what they are eating but find it very cumbersome to do so (imagine manual data entry on an app). Therefore, we want to build a practical and functional spoon that can do all that for us automatically and in a fun way. 

The implementation of this spoon required the following fields of knowledge: embedded systems (sensors & actuators), cloud computing for the server, data visualization for the dashboard and data science/deep learning for image recognition.  

Please click on the link below to access our project website and video:

<a href = "https://www.youtube.com/watch?v=E_3mwVcQvrg&feature=youtu.be"> YouTube Video </a>


# Organization of Files

* *__raspi_code__* sub-dir: contains all code to run on our Pi. They are for our Pi to communicate with our sensors and actuators (accelerometer, pressure sensor, thermometer, camera, LED, OLED display) and to send and receive information from the server. `main1.py` is the main file to run for Spoony; the functions in the rest of the files are called by the main file.  

* *__server_code__* sub-dir: contains all code that runs on our server. It includes code to run our trained Convolutional Neural Network (CNN) model for image classification and for our analytics dashboard.

* *__img_reg_model_code__* sub-dir: contains two notebooks for our image recognition task. The first notebook contains code to process our training dataset - resize images to the desired dimensions; save images as numpy matrices. The second notebook contains code to build our image recognition model and train it on our own food images - building the model involved transfer learning from Xception which was loaded with weights pre-trained on ImageNet, with the last fully-connected layer replaced with our own.

* *__images__* sub-dir: contains our team photo and social media app icons for our dashboard.
