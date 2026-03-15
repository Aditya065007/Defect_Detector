import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import gdown
import os

st.set_page_config(
    page_title="FreshCheck — Food Quality Inspector",
    page_icon="🥦",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&family=Poppins:wght@400;500;600&display=swap');
* { font-family: 'Poppins', sans-serif; }
.main { background: #F5F5F5; }
.block-container { padding-top: 0 !important; max-width: 480px !important; }

.topbar {
    background: #E23744; padding: 14px 20px;
    border-radius: 0 0 0 0; margin: -1rem -1rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.topbar-logo {
    font-family: 'Nunito', sans-serif; font-weight: 900;
    font-size: 22px; color: white;
}
.topbar-logo span { color: #FFD700; }
.topbar-badge {
    background: rgba(255,255,255,0.2); color: white;
    font-size: 11px; font-weight: 600;
    padding: 4px 12px; border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.3);
}
.hero {
    background: linear-gradient(135deg, #E23744, #c0182a);
    padding: 24px 20px 40px; margin: 0 -1rem;
    color: white;
}
.hero-tag {
    background: rgba(255,255,255,0.2); display: inline-block;
    padding: 4px 12px; border-radius: 20px;
    font-size: 11px; font-weight: 600; margin-bottom: 10px;
}
.hero h2 {
    font-family: 'Nunito', sans-serif; font-weight: 900;
    font-size: 24px; line-height: 1.2; margin-bottom: 6px;
}
.hero p { font-size: 13px; opacity: 0.85; }

.stats-row {
    display: flex; gap: 10px;
    margin: -20px 0 16px; position: relative; z-index: 2;
}
.stat-card {
    flex: 1; background: white; border-radius: 12px;
    padding: 12px; text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stat-num {
    font-family: 'Nunito', sans-serif; font-weight: 900;
    font-size: 18px; color: #E23744;
}
.stat-label { font-size: 10px; color: #93959F; margin-top: 2px; }

.result-fresh {
    background: #60B246; color: white;
    padding: 20px; border-radius: 14px;
    font-family: 'Nunito', sans-serif;
}
.result-stale {
    background: #E23744; color: white;
    padding: 20px; border-radius: 14px;
    font-family: 'Nunito', sans-serif;
}
.result-verdict { font-weight: 900; font-size: 20px; margin-bottom: 4px; }
.result-sub { font-size: 13px; opacity: 0.9; }

.action-fresh {
    background: #F0FBF0; border: 1px solid #cce8cc;
    border-radius: 12px; padding: 12px 14px; margin-top: 12px;
}
.action-stale {
    background: #FFF5F5; border: 1px solid #fcc;
    border-radius: 12px; padding: 12px 14px; margin-top: 12px;
}
.action-title { font-weight: 700; font-size: 13px; margin-bottom: 3px; }
.action-desc { font-size: 11px; color: #93959F; }

.stButton button {
    background: #E23744 !important; color: white !important;
    border-radius: 25px !important; font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important; font-size: 16px !important;
    border: none !important; width: 100% !important;
    padding: 12px !important;
}
.stButton button:hover { background: #c0182a !important; }
</style>

<div class="topbar">
    <div class="topbar-logo">fresh<span>check</span></div>
    <div class="topbar-badge">QA Portal</div>
</div>

<div class="hero">
    <div class="hero-tag">AI-Powered Inspection</div>
    <h2>Is your produce<br>fresh for delivery?</h2>
    <p>Instant freshness detection for Zomato & Swiggy fulfilment centres.</p>
</div>

<div class="stats-row">
    <div class="stat-card"><div class="stat-num">99.6%</div><div class="stat-label">ROC-AUC</div></div>
    <div class="stat-card"><div class="stat-num">96%</div><div class="stat-label">Accuracy</div></div>
    <div class="stat-card"><div class="stat-num">17ms</div><div class="stat-label">Per image</div></div>
</div>
""", unsafe_allow_html=True)

MODEL_PATH = 'defect_detector.h5'
FILE_ID = '1Cv9mhsecL9I59u4OGVD0zqJYPuQWaS4M'

if not os.path.exists(MODEL_PATH):
    with st.spinner("Loading model for the first time..."):
        gdown.download(
            f'https://drive.google.com/uc?id={FILE_ID}',
            MODEL_PATH, quiet=False
        )

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

def process_image(img):
    img = img.resize((128, 128))
    img_array = np.array(img.convert('RGB'))
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

st.markdown("### Upload Produce Image")
uploaded_file = st.file_uploader(
    "Supported: Apple, Banana, Orange, Tomato, Capsicum, Bitter Gourd",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    if st.button("Inspect Freshness"):
        with st.spinner("Analyzing produce..."):
            processed_img = process_image(image)
            prediction = model.predict(processed_img)[0][0]

        if prediction > 0.5:
            confidence = prediction * 100
            st.markdown(f"""
            <div class="result-stale">
                <div class="result-verdict">STALE — DO NOT DISPATCH</div>
                <div class="result-sub">Confidence: {confidence:.1f}%</div>
            </div>
            <div class="action-stale">
                <div class="action-title">Flag for disposal</div>
                <div class="action-desc">Remove from active inventory and log for supplier review.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            confidence = (1 - prediction) * 100
            st.markdown(f"""
            <div class="result-fresh">
                <div class="result-verdict">FRESH — CLEAR FOR DISPATCH</div>
                <div class="result-sub">Confidence: {confidence:.1f}%</div>
            </div>
            <div class="action-fresh">
                <div class="action-title">Proceed to packaging</div>
                <div class="action-desc">Item cleared for dispatch. Route to packaging station immediately.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Model", "CNN")
        col2.metric("Latency", "17ms")
        col3.metric("Parameters", "4.28M")
else:
    st.info("Upload a fruit or vegetable image to begin inspection.")

st.markdown("""
---
**Supported produce:** Apple · Banana · Orange · Tomato · Capsicum · Bitter Gourd
""")
