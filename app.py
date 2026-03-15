import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import gdown
import os

# 1. UI Configuration
st.set_page_config(page_title="Food Quality Inspector", page_icon="🥦")
st.title("Automated Food Freshness Detection")
st.write("Upload an image of a fruit or vegetable to inspect freshness before dispatch.")

# 2. Download model from Google Drive if not present
MODEL_PATH = 'defect_detector.h5'
FILE_ID = '1Cv9mhsecL9I59u4OGVD0zqJYPuQWaS4M'

if not os.path.exists(MODEL_PATH):
    with st.spinner("Loading model for the first time..."):
        gdown.download(f'https://drive.google.com/uc?id={FILE_ID}',
                      MODEL_PATH, quiet=False)

# 3. Load the Model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# 4. Image Processing Engine
def process_image(img):
    img = img.resize((128, 128))
    img_array = np.array(img.convert('RGB'))
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# 5. User Upload Component
uploaded_file = st.file_uploader("Choose an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    with st.spinner("Analyzing..."):
        processed_img = process_image(image)
        prediction = model.predict(processed_img)[0][0]

    st.divider()

    # stale = class index 1 → prediction > 0.5
    # fresh = class index 0 → prediction < 0.5
    if prediction > 0.5:
        st.error(f"🚨 **STALE — DO NOT DISPATCH** (Confidence: {prediction:.2%})")
        st.write("**Action:** Remove from active inventory. Flag for disposal.")
    else:
        st.success(f"✅ **FRESH — CLEAR FOR DISPATCH** (Confidence: {(1 - prediction):.2%})")
        st.write("**Action:** Proceed to packaging and dispatch.")
