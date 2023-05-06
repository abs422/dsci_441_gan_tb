# DSCI 441 - Disease Identification using Anomaly detection
In this repository, you may find the implementation of AnoGAN with hyperparameter tuning for unsupervised anomaly detection in Chest X-Ray images. The model is trained on multiple sources available on google drive link provided below. 

### Motivation and Background
As data scientists, we still have a longer road ahead in matching physician expertise for detecting different diagnoses using algorithms. Using deep learning and medical images like X-Ray, in this study we attempt to devise a methodology to identify tuberculosis in patients. We always find more data records with absence of
disease than presence and this statistically pose a major challenge to develop a supervised disease detection model. Therefore, in this study we turn to unsupervised techniques to develop an anomaly detection model using Generative Networks. We believe that with enough samples of Chest X-Ray images for healthy patients, we can train a Generative Adversarial Network (GAN) to detect the disease. The disease instance should lie in the outlier zone of the trained GAN model as it could only regenerates image of healthy patients with minimal reconstruction loss.


### Main References for concepts and codes
1. Paper - https://arxiv.org/abs/1703.05921
2. AnoGAN(code, keras) : https://github.com/yjucho1/anoGAN
3. AnoGAN(code, tf) : https://github.com/LeeDoYup/AnoGAN

### Datasets used 
1. China Set - The Shenzhen set
2. Montgomery County - Chest X ray
3. TBX11K Set

### AnoGAN architecture
![anogan2](https://user-images.githubusercontent.com/111200749/232359547-9be3de20-df80-4f7d-b15e-e0987aa43c84.png)

### Desired plot for thresholding 
![sample_threshold](https://user-images.githubusercontent.com/111200749/232359587-14cfa741-374b-4a89-8183-fe38faad3220.png)

### Google drive used to save data and models
https://drive.google.com/drive/folders/1xGupJOw8dcwXeokWcGfcIl9vg1-i-cT1?usp=sharing 
https://drive.google.com/drive/folders/14LpXOHVdlrV_UUJSXgxbFFdu2YRCyGOa?usp=sharing

### Details about the files (dsci_441_gan_tb/)
Following are the description of files and folders in directory - dsci_441_gan_tb/

1. Model_d.hdf5 - Final saved discriminator model of trained GAN, was used in the streamlit app to make predictions
2. Model_g.hdf5 - Final saved generator model of trained GAN, was used in the streamlit app to make predictions
3. anogan_tb_detection.py - Final AnoGAN python code file, please see instructions below to run and regenerate the results
4. requirement.txt - This file contains list the modules required to run anogan_tb_detection.py and streamlit_app.py
5. streamlit_app.py - Final python code file to reproduce the streamlit app on streamlit community cloud
6. tb_shez.csv - Contain anomaly scores for tuberculosis patients, this file was used in the streamlit app to summarize the level of sickness among tuberculosis patients
7. tsne feature.png - A summary image highlighting the t-sne embedding of features representation from last layer of discriminator in GAN model, this is displayed in streamlit app to summarize GAN capability

### Details about the code files (dsci_441_gan_tb/AnoGAN - Anomaly detection)
This directory contains intermediate code files, trained models and weights, these files were <b>not</b> used to make final predictions
Following is the list of code files and folders in this directory (dsci_441_gan_tb/AnoGAN - Anomaly detection) -

1. anogan.py - The original source code file of AnoGAN, used as inspiration in this project to build a working AnoGAN model
2. main.py - The original source code file supporting AnoGAN implementation, used as inspiration in this project to build a working AnoGAN model
3. AnoGAN_v3.ipynb - The first working model of AnoGAN, predicting anomaly score for a givn test image
4. AnoGAN_v4.ipynb - More optimized working model of AnoGAN, predicting anomaly score for a givn test image
5. streamlit_app.py - A working streamlit app, with basic functionality of taking an image as an input and predicting if the image is of a Tuberculosis patient
6. anogan_v6.py - Please note .ipynb version of this code was > 25 Mb and hence could not be uploaded to GitHub

Instructions to run anogan_tb_detection.py and anogan_v6.py -

1. Please make sure to connect to the google srive where all data is situated using the below links
2. All the code can be sequentially run, however please avoid running the cells where models are saved as it may overwrite my existing model which is used for prediction, and follow beow instructions
3. At multiple instances the file, the healthy, sick (Non Tb) or Tb images are imported from google drive. All imported files are properly labeled. While importing training set, healthy images are imported and while making test set, Tb images are imported
4. Please make sure to change the directory to the location where the required images are saved.
5. You can use this link to access the folder on google drive which was used in the code. https://drive.google.com/drive/folders/1xGupJOw8dcwXeokWcGfcIl9vg1-i-cT1?usp=sharing https://drive.google.com/drive/folders/14LpXOHVdlrV_UUJSXgxbFFdu2YRCyGOa?usp=sharing

#### Link to tuberculosis prediction app hosted on streamlit community cloud 
https://abs422-dsci-441-gan-tb-streamlit-app-kp3tpv.streamlit.app/
