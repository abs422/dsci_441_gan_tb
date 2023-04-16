import streamlit as st
from PIL import Image


st.set_page_config(
    page_title = "Tuberculosis Prediction App",
    page_icon = "Yo",
)

st.title("Main Page - Introduction to App")
st.sidebar.success("")

image = Image.open("C:/Lehigh/Study Material/DSCI 441 - Statistical and Machine Learning/Project/multipage_app/img1.png")
# st.image(image, channels="RGB")

st.write("""
### Tuberculosis diagnosis using Anomaly Detection with AnoGAN
With increased resource utilization due to increased burden on patients as well as healthcare 
system, detection of diagnosis using automated machine learning techniques is the need of 
the hour. We have come a long way in supporting physicians and health policy makers by 
identifying brand-new biomarkers for myriad of diseases. As data scientists, we still have a 
longer road ahead in matching physician expertise for detecting different diagnoses using 
algorithms. Using deep learning and medical images like X-Ray, in this study we attempt to 
devise a methodology to identify tuberculosis in patients. We always find more data records 
with absence of disease than presence and this statistically pose a major challenge to develop 
a supervised disease detection model. Therefore, in this study we turn to unsupervised 
techniques to develop an anomaly detection model using Generative Networks. We believe 
that with enough samples of Chest X-Ray images for healthy patients, we can train a 
Generative Adversarial Network (GAN) to detect the disease. The disease should lie in outlier 
zone for a GAN model trained for regenerating images of only healthy patients. There has 
been a long-standing hypothesis that lung segmentation could improve pulmonary disease 
identification. However, there are minimal instances where segmentation has improved the 
disease identification with a significant margin. In this study, we may also record the effect of 
lung segmentation on anomaly detection model to detect Tuberculosis. Eventually, we build 
a “Plotly/Dash” Dashboard which uses a new Chest X-Ray image to predict if the patient has 
Tuberculosis. This product could assist physician in making more informed and faster decision. 
A similar product could even be provided to patients allowing them to test presence or 
possibility of having a certain diagnosis in real time, allowing patients to become aware and 
eventually supporting the common cause of early diagnosis and early medical actions
""")
