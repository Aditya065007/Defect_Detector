import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# 1. UI Configuration
st.set_page_config(page_title="AVQA Defect Detector", page_icon="⚙️")
st.title("Automated Visual Quality Assurance")
st.write("Upload a frontal image of a casting product to inspect for defects.")

# 2. Load the Model (Cached for speed so it only loads once)
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('defect_detector.h5')

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# 3. Image Processing Engine
def process_image(img):
    img = img.resize((128, 128))             # Match Colab IMG_SIZE
    img_array = np.array(img.convert('RGB')) # Ensure 3 channels
    img_array = img_array / 255.0            # Normalize to [0,1]
    img_array = np.expand_dims(img_array, axis=0) # Create batch dimension (1, 128, 128, 3)
    return img_array

# 4. User Upload Component
uploaded_file = st.file_uploader("Choose an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    # Run Prediction
    with st.spinner("Analyzing..."):
        processed_img = process_image(image)
        prediction = model.predict(processed_img)[0][0]
    
    st.divider()
    
    # 5. Corrected Managerial Output Logic
    # Keras sorted folders alphabetically: def_front = 0, ok_front = 1
    if prediction < 0.5:
        # Closer to 0 means Defective
        st.error(f"🚨 **DEFECT DETECTED** (Confidence: {(1 - prediction):.2%})")
        st.write("**Action:** Route to human inspector.")
    else:
        # Closer to 1 means OK
        st.success(f"✅ **PRODUCT OK** (Confidence: {prediction:.2%})")
        st.write("**Action:** Clear for next assembly stage.")
