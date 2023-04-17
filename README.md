# DSCI 441 - Disease Identification using Anomaly detection
In this repository, you may find the implementation of AnoGAN with hyperparameter tuning for unsupervised anomaly detection in Chest X-Ray images. The model is trained on multiple sources available on google drive link provided below. 

### Motivation and Background
As data scientists, we still have a longer road ahead in matching physician expertise for detecting different diagnoses using algorithms. Using deep learning and medical images like X-Ray, in this study we attempt to devise a methodology to identify tuberculosis in patients. We always find more data records with absence of
disease than presence and this statistically pose a major challenge to develop a supervised disease detection model. Therefore, in this study we turn to unsupervised techniques to develop an anomaly detection model using Generative Networks. We believe that with enough samples of Chest X-Ray images for healthy patients, we can train a Generative Adversarial Network (GAN) to detect the disease. The disease instance should lie in the outlier zone of the trained GAN model as it could only regenerates image of healthy patients with minimal reconstruction loss.


### Main References for concepts and codes
1. Paper - https://arxiv.org/abs/1703.05921
2. AnoGAN(code, keras) : https://github.com/yjucho1/anoGAN
3. AnoGAN(code, tf) : https://github.com/LeeDoYup/AnoGAN

### AnoGAN architecture
![anogan2](https://user-images.githubusercontent.com/111200749/232359547-9be3de20-df80-4f7d-b15e-e0987aa43c84.png)

### Desired plot for thresholding 
![sample_threshold](https://user-images.githubusercontent.com/111200749/232359587-14cfa741-374b-4a89-8183-fe38faad3220.png)

### Google drive used to save data and models
https://drive.google.com/drive/folders/1xGupJOw8dcwXeokWcGfcIl9vg1-i-cT1?usp=sharing 
https://drive.google.com/drive/folders/14LpXOHVdlrV_UUJSXgxbFFdu2YRCyGOa?usp=sharing

### Details about the code files 
Following is the list of code files and folders in this directory (dsci_441_gan_tb/AnoGAN - Anomaly detection) -

1. anogan.py - The original source code file of AnoGAN, used as inspiration in this project to build a working AnoGAN model
2. main.py - The original source code file supporting AnoGAN implementation, used as inspiration in this project to build a working AnoGAN model
3. AnoGAN_v3.ipynb - The first working model of AnoGAN, predicting anomaly score for a givn test image
4. AnoGAN_v4.ipynb - More optimized working model of AnoGAN, predicting anomaly score for a givn test image
5. streamlit_app.py - A working streamlit app, with basic functionality of taking an image as an input and predicting if the image is of a Tuberculosis patient

##### Current working code of AnoGAN model building and performance evaluation
1. anogan_v6.py - Please note .ipynb version of this code was > 25 Mb and hence could not be uploaded to GitHub

Instructions to run anogan_v6.py -

1. All the code can be sequentially run, however please avoid running the cells where models are saved as it may overwrite my existing model which is used for prediction, and follow beow instructions
2. At multiple instances the file, the healthy, sick (Non Tb) or Tb images are imported from google drive. All imported files are properly labeled. While importing training set, healthy images are imported and while making test set, Tb images are imported
3. Please make sure to change the directory to the location where the required images are saved.
4. You can use this link to access the folder on google drive which was used in the code. https://drive.google.com/drive/folders/1xGupJOw8dcwXeokWcGfcIl9vg1-i-cT1?usp=sharing https://drive.google.com/drive/folders/14LpXOHVdlrV_UUJSXgxbFFdu2YRCyGOa?usp=sharing
