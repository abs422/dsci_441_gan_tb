# -*- coding: utf-8 -*-
"""streamlit_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16FhWmQ4oqcf_PxerH5QJH__qvCbH4HzV
"""

from __future__ import print_function
import cv2
import numpy as np
import streamlit as st
import tensorflow as tf
import io
from PIL import Image
import base64
#from byte_array import byte_data
from keras.models import Sequential, Model
from keras.layers import Input, Reshape, Dense, Dropout, MaxPooling2D, Conv2D, Flatten
from keras.layers import Conv2DTranspose, LeakyReLU
from keras.layers.core import Activation
from keras.layers import BatchNormalization
from keras.optimizers import Adam, RMSprop
from keras import backend as K
from keras import initializers
from sklearn.manifold import TSNE
import matplotlib.pyplot as p
# import numpy as np
from tqdm import tqdm
# import cv2
import math
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2,preprocess_input as mobilenet_v2_preprocess_input


# import tensorflow as tf


from keras.utils. generic_utils import Progbar

z_dim = 10
img_size = 256
st.title("Tuberculosis Prediction App")
### combine images for visualization
def combine_images(generated_images):
    num = generated_images.shape[0]
    width = int(math.sqrt(num))
    height = int(math.ceil(float(num)/width))
    shape = generated_images.shape[1:4]
    image = np.zeros((height*shape[0], width*shape[1], shape[2]),
                     dtype=generated_images.dtype)
    for index, img in enumerate(generated_images):
        i = int(index/width)
        j = index % width
        image[i*shape[0]:(i+1)*shape[0], j*shape[1]:(j+1)*shape[1],:] = img[:, :, :]
    return image

### generator model define
def generator_model(z_dim = z_dim, imgsize = img_size, channels = 1): 
    col = int(imgsize / 4)
    inputs = Input((z_dim, ))
    fc1 = Dense(input_dim=z_dim, units=128*col*col)(inputs)
    fc1 = BatchNormalization()(fc1)
    fc1 = LeakyReLU(0.2)(fc1)

    fc2 = Reshape((col, col, 128), input_shape=(128*col*col,))(fc1)
    up1 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(fc2)
    conv1 = Conv2D(64, (3,3), padding='same')(up1)
    conv1 = BatchNormalization()(conv1)
    conv1 = Activation('relu')(conv1)

    up2 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(conv1)
    conv2 = Conv2D(channels, (5, 5), padding='same')(up2)
    outputs = Activation('tanh')(conv2)

    model = Model(inputs=[inputs], outputs=[outputs])
    model.summary()

    return model

def discriminator_model(img_size = img_size, channels = 1):
    inputs = Input((img_size, img_size, channels))

    conv1 = Conv2D(64, (5,5), padding='same')(inputs)
    conv1 = LeakyReLU(0.2)(conv1)
    pool1 = MaxPooling2D(pool_size=(2,2))(conv1)

    conv2 = Conv2D(128, (5,5), padding='same')(pool1)
    conv2 = LeakyReLU(0.2)(conv2)
    pool2 = MaxPooling2D(pool_size=(2,2))(conv2)

    fc1 = Flatten()(pool2)
    fc1 = Dense(1)(fc1)
    outputs = Activation('sigmoid')(fc1)

    model = Model(inputs=[inputs], outputs=[outputs])
    model.summary()

    return model

### d_on_g model for training generator
def generator_containing_discriminator(g, d, z_dim = z_dim):
    d.trainable = False

    ganInput = Input(shape=(z_dim, ))
    x = g(ganInput)
    ganOutput = d(x)
    gan = Model(inputs=ganInput, outputs=ganOutput)

    return gan

def load_model():
    d = discriminator_model()
    g = generator_model()
    d_optim = Adam()
    g_optim = Adam(lr=0.0001)
    g.compile(loss='binary_crossentropy', optimizer=g_optim)
    d.compile(loss='binary_crossentropy', optimizer=d_optim)
    d.load_weights('./weights/discriminator.h5')
    g.load_weights('./weights/generator.h5')
    return g, d

def anomaly_detection(test_img, img_size=img_size, g=None, d=None):
    model = anomaly_detector(g=g, d=d)
    ano_score, similar_img = compute_anomaly_score(model, test_img.reshape(1, img_size, img_size, 1), iterations=500, d=d)

    # anomaly area, 255 normalization
    np_residual = test_img.reshape(img_size,img_size,1) - similar_img.reshape(img_size,img_size,1)
    np_residual = (np_residual + 2)/4

    np_residual = (255*np_residual).astype(np.uint8)
    original_x = (test_img.reshape(img_size,img_size,1)*127.5+127.5).astype(np.uint8)
    similar_x = (similar_img.reshape(img_size,img_size,1)*127.5+127.5).astype(np.uint8)

    original_x_color = cv2.cvtColor(original_x, cv2.COLOR_GRAY2BGR)
    residual_color = cv2.applyColorMap(np_residual, cv2.COLORMAP_JET)
    show = cv2.addWeighted(original_x_color, 0.3, residual_color, 0.7, 0.)

    return ano_score, original_x, similar_x, show

### generate images
def generate(BATCH_SIZE, z_dim=z_dim):
    g = generator_model()
    g.load_weights('weights/generator.h5')
    noise = np.random.uniform(0, 1, (BATCH_SIZE, z_dim))
    # noise = np.random.uniform(0, 1, (BATCH_SIZE, 256))
    generated_images = g.predict(noise)
    return generated_images

### anomaly loss function 
def sum_of_residual(y_true, y_pred):
    return K.sum(K.abs(K.cast(y_true, dtype='float32') - K.cast(y_pred, dtype='float32')))

### discriminator intermediate layer feautre extraction
def feature_extractor(d=None):
    if d is None:
        d = discriminator_model()
        d.load_weights('weights/discriminator.h5') 
    intermidiate_model = Model(inputs=d.layers[0].input, outputs=d.layers[-7].output)
    intermidiate_model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    return intermidiate_model

### anomaly detection model define
def anomaly_detector(g=None, d=None, z_dim=z_dim):
    if g is None:
        g = generator_model()
        g.load_weights('weights/generator.h5')
    intermidiate_model = feature_extractor(d)
    intermidiate_model.trainable = False
    g = Model(inputs=g.layers[1].input, outputs=g.layers[-1].output)
    g.trainable = False
    # Input layer cann't be trained. Add new layer as same size & same distribution
    aInput = Input(shape=(z_dim,))
    gInput = Dense((10), trainable=True)(aInput)
    gInput = Activation('sigmoid')(gInput)
    
    # G & D feature
    G_out = g(gInput)
    D_out= intermidiate_model(G_out)    
    model = Model(inputs=aInput, outputs=[G_out, D_out])
    model.compile(loss=sum_of_residual, loss_weights= [0.90, 0.10], optimizer='rmsprop')
    
    # batchnorm learning phase fixed (test) : make non trainable
    K.set_learning_phase(0)
    
    return model


### anomaly detection
def compute_anomaly_score(model, x, iterations=500, d=None, z_dim=z_dim):
    z = np.random.uniform(0, 1, size=(1, z_dim))
    
    intermidiate_model = feature_extractor(d)
    d_x = intermidiate_model.predict(x)

    # learning for changing latent
    loss = model.fit(z, [x, d_x], batch_size=1, epochs=iterations, verbose=0)
    similar_data, _ = model.predict(z)
    
    loss = loss.history['loss'][-1]
    
    return loss, similar_data

@st.cache_data()
def load_discr():
	return tf.keras.models.load_model("Models/model_d.hdf5")
@st.cache_data()
def load_gen():
	return tf.keras.models.load_model("Models/model_g.hdf5")


model_d = load_discr()
model_g = load_gen()

### load file
uploaded_file = st.file_uploader("Choose a chest X-Ray image file (jpg or png)", type=["jpg", "png"])
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



if uploaded_file is not None:
  file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
  opencv_image = cv2.imdecode(file_bytes, 1)
  opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
  resized = cv2.resize(opencv_image,(256,256))
  
  col1, col2, col3 = st.columns([2,4,2])

  with col1:
  	st.write("")

  with col2:
    	st.image(opencv_image, channels="RGB")

  with col3:
    	st.write("")
  

  resized = mobilenet_v2_preprocess_input(resized)
  ### 2. test generator
  generated_img = generate(25)
  img = combine_images(generated_img)
  img = (img*127.5)+127.5
  img = img.astype(np.uint8)
  img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)

  col1, col2, col3 , col4, col5 = st.columns([0.75,1.1,3,.1,1])

  with col1:
  	pass
  with col2:
  	pass
  with col4:
  	pass
  with col5:
  	pass
  with col3 :
    Genrate_pred = st.button("Can patient have Tuberculosis?")
  
  check = st.checkbox('Show intermediate results')
  
  col1, col2 = st.columns([5, 1])

  with col2:
      st.text("")
      
  if Genrate_pred:
    with col1:
      st.text("Predicting...it may take few minutes")
  
    

  if Genrate_pred:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)
    # filebytes = bytes_data.decode("utf-8")
    img = Image.open(io.BytesIO(bytes_data)).convert('L')
    test_img = img.resize((256, 256))
    test_img = np.array(test_img).reshape(256, 256, 1)
    start = cv2.getTickCount()
    score, qurey, pred, diff = anomaly_detection(test_img)
    time = (cv2.getTickCount() - start) / cv2.getTickFrequency() * 1000
    col1, col2 = st.columns([5, 1])

    with col1:
        st.write("Done! See prediction below")
        
    with col2:
        st.write("")
    # Check for threshold and display the results    
    if score > 9500000:
      st.title("Patient may have Tuberculosis")
    else:
      st.title("Patient is healthy")
    
    # Show intermediate results
    
    
    if check:
        col1, col2, col3 = st.columns([2,2,2])

        with col1:
            st.image(qurey.reshape(256,256), channels="RGB")

        with col2:
            st.image(pred.reshape(256,256), channels="RGB")

        with col3:
            st.image(cv2.cvtColor(diff,cv2.COLOR_BGR2RGB))
        #st.image(qurey.reshape(256,256), channels="RGB")
        #st.image(pred.reshape(256,256), channels="RGB")
        #st.image(cv2.cvtColor(diff,cv2.COLOR_BGR2RGB))
        col4, col1, col2, col5, col3 = st.columns([0.4,1.6,1.4, .2,1.75])
        with col4:
            st.write("")
        with col1:
            st.write("Query image")

        with col2:
            st.write("Reconstructed pattern")
        with col5:
            st.write("")
        with col3:
            st.write("Difference with healthy patient")
        
    

    # random_image = np.random.uniform(0, 1, (100, 256, 256, 1))
    # print("random noise image")
    # plt.figure(4, figsize=(2, 2))
    # plt.title('random noise image')
    # plt.imshow(random_image[0].reshape(256,256), cmap=plt.cm.gray)
    # 
    # # Display the plot in Streamlit
    # st.pyplot(plt)
    # 
    # # intermidieate output of discriminator
    # model = feature_extractor()
    # feature_map_of_random = model.predict(random_image, verbose=1)
    # feature_map_of_minist = model.predict(X_test_original[:300], verbose=1)
    # feature_map_of_minist_1 = model.predict(X_test[:100], verbose=1)
    # 
    # # t-SNE for visulization
    # output = np.concatenate((feature_map_of_random, feature_map_of_minist, feature_map_of_minist_1))
    # output = output.reshape(output.shape[0], -1)
    # anomaly_flag = np.array([1]*100+ [0]*300)
    # 
    # X_embedded = TSNE(n_components=2).fit_transform(output)
    # plt.figure(5)
    # plt.title("t-SNE embedding on the feature representation")
    # plt.scatter(X_embedded[:100,0], X_embedded[:100,1], label='random noise(anomaly)')
    # plt.scatter(X_embedded[100:400,0], X_embedded[100:400,1], label='mnist(anomaly)')
    # plt.scatter(X_embedded[400:,0], X_embedded[400:,1], label='mnist(normal)')
    # plt.legend()
    # st.pyplot(plt)
    

### 2. test generator
# generated_img = generate(25)
# img = combine_images(generated_img)
# img = (img*127.5)+127.5
# img = img.astype(np.uint8)
# img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
