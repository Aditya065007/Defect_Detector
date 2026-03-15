import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import gdown
import os

st.set_page_config(
    page_title="FreshCheck — Food Quality Inspector",
    page_icon="🥦",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&family=Poppins:wght@400;500;600&display=swap');

* { font-family: 'Poppins', sans-serif; }

.topbar {
    background: #E23744;
    padding: 16px 40px;
    margin: -1rem -1rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.topbar-logo {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 26px;
    color: white;
}
.topbar-logo span { color: #FFD700; }
.topbar-badge {
    background: rgba(255,255,255,0.2);
    color: white;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.3);
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 16px;
}

.hero {
    background: linear-gradient(135deg, #E23744, #c0182a);
    padding: 48px 40px;
    margin: 0 -1rem 32px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.hero-left { max-width: 600px; }
.hero-tag {
    background: rgba(255,255,255,0.2);
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.25);
}
.hero h1 {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 40px;
    line-height: 1.15;
    margin-bottom: 12px;
}
.hero p {
    font-size: 15px;
    opacity: 0.88;
    line-height: 1.6;
    max-width: 480px;
}
.hero-stats {
    display: flex;
    gap: 24px;
    margin-top: 28px;
}
.hero-stat {
    text-align: center;
}
.hero-stat-num {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 28px;
}
.hero-stat-label {
    font-size: 11px;
    opacity: 0.8;
    margin-top: 2px;
}

.main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
    padding: 0 8px;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.card-title {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 18px;
    color: #1C1C1C;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.card-title-dot {
    width: 10px;
    height: 10px;
    background: #E23744;
    border-radius: 50%;
}
.card-sub {
    font-size: 13px;
    color: #93959F;
    margin-bottom: 20px;
}

.result-fresh {
    background: #60B246;
    color: white;
    padding: 24px;
    border-radius: 14px;
    margin-bottom: 16px;
}
.result-stale {
    background: #E23744;
    color: white;
    padding: 24px;
    border-radius: 14px;
    margin-bottom: 16px;
}
.result-verdict {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 22px;
    margin-bottom: 4px;
}
.result-sub { font-size: 14px; opacity: 0.9; }

.action-fresh {
    background: #F0FBF0;
    border: 1px solid #cce8cc;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 16px;
}
.action-stale {
    background: #FFF5F5;
    border: 1px solid #fcc;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 16px;
}
.action-title {
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 4px;
    color: #1C1C1C;
}
.action-desc {
    font-size: 12px;
    color: #93959F;
    line-height: 1.5;
}

.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 16px;
}
.metric-box {
    background: #F5F5F5;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
}
.metric-val {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 16px;
    color: #1C1C1C;
}
.metric-label {
    font-size: 10px;
    color: #93959F;
    margin-top: 3px;
}

.info-card {
    background: white;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-top: 28px;
}
.info-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 12px 0;
    border-bottom: 1px solid #E9E9EB;
}
.info-row:last-child { border-bottom: none; padding-bottom: 0; }
.info-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 4px;
}
.info-text {
    font-size: 13px;
    color: #3D4152;
    line-height: 1.5;
}
.info-text strong { font-weight: 600; color: #1C1C1C; }

.produce-section {
    margin-top: 28px;
    background: white;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.produce-chips {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 14px;
}
.produce-chip {
    background: #F5F5F5;
    border: 1px solid #E9E9EB;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 600;
    color: #3D4152;
}

.stButton > button {
    background: #E23744 !important;
    color: white !important;
    border-radius: 25px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    border: none !important;
    width: 100% !important;
    padding: 14px 28px !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    background: #c0182a !important;
    transform: translateY(-1px);
}

.stFileUploader {
    border: 2px dashed #E9E9EB !important;
    border-radius: 12px !important;
}

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
</style>

<div class="topbar">
    <div class="topbar-logo">fresh<span>check</span></div>
    <div class="topbar-right">
        <div class="topbar-badge">Zomato QA Portal</div>
        <div class="topbar-badge">Dark Kitchen Inspector</div>
    </div>
</div>

<div class="hero">
    <div class="hero-left">
        <div class="hero-tag">AI-Powered Pre-Dispatch Inspection</div>
        <h1>Is your produce<br>fresh for delivery?</h1>
        <p>Automated food freshness detection for Zomato and Swiggy fulfilment centres. Upload a produce image and get an instant quality verdict powered by CNN.</p>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-num">99.6%</div>
                <div class="hero-stat-label">ROC-AUC</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">96%</div>
                <div class="hero-stat-label">Accuracy</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">17ms</div>
                <div class="hero-stat-label">Inference</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">0.927</div>
                <div class="hero-stat-label">Kappa Score</div>
            </div>
        </div>
    </div>
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

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title"><div class="card-title-dot"></div>Upload Produce Image</div>
        <div class="card-sub">Supports Apple, Banana, Orange, Tomato, Capsicum, Bitter Gourd</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        inspect_btn = st.button("Inspect Freshness")
    else:
        st.info("Upload a fruit or vegetable image to begin inspection.")
        inspect_btn = False

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title"><div class="card-title-dot"></div>Inspection Result</div>
        <div class="card-sub">Quality verdict will appear here after analysis</div>
    </div>
    """, unsafe_allow_html=True)

    if uploaded_file is not None and inspect_btn:
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
                <div class="action-title">Remove from active inventory</div>
                <div class="action-desc">Item is stale. Flag for disposal and log for supplier quality review. Do not dispatch to customer.</div>
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
                <div class="action-desc">Item cleared for dispatch. Route to packaging station and proceed with delivery.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metrics-row">
            <div class="metric-box"><div class="metric-val">CNN</div><div class="metric-label">Model</div></div>
            <div class="metric-box"><div class="metric-val">17ms</div><div class="metric-label">Latency</div></div>
            <div class="metric-box"><div class="metric-val">4.28M</div><div class="metric-label">Parameters</div></div>
            <div class="metric-box"><div class="metric-val">96%</div><div class="metric-label">Accuracy</div></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#F5F5F5;border-radius:14px;padding:48px;text-align:center;color:#93959F;">
            <div style="font-size:48px;margin-bottom:16px;">🔍</div>
            <div style="font-family:'Nunito',sans-serif;font-weight:800;font-size:18px;color:#3D4152;margin-bottom:8px;">No image uploaded yet</div>
            <div style="font-size:13px;">Upload a produce image on the left to get started</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="produce-section">
    <div class="card-title"><div class="card-title-dot"></div>Supported Produce Categories</div>
    <div class="produce-chips">
        <div class="produce-chip">Apple</div>
        <div class="produce-chip">Banana</div>
        <div class="produce-chip">Orange</div>
        <div class="produce-chip">Tomato</div>
        <div class="produce-chip">Capsicum</div>
        <div class="produce-chip">Bitter Gourd</div>
    </div>
</div>

<div class="info-card">
    <div class="card-title"><div class="card-title-dot"></div>Dispatch Guidelines</div>
    <div class="info-row">
        <div class="info-dot" style="background:#60B246;"></div>
        <div class="info-text"><strong>Fresh</strong> — Item is safe to dispatch. Route to packaging immediately.</div>
    </div>
    <div class="info-row">
        <div class="info-dot" style="background:#E23744;"></div>
        <div class="info-text"><strong>Stale</strong> — Remove from active inventory. Flag for disposal and supplier review.</div>
    </div>
    <div class="info-row">
        <div class="info-dot" style="background:#FF9A3C;"></div>
        <div class="info-text"><strong>Confidence below 70%</strong> — Flag for human re-inspection before dispatch decision.</div>
    </div>
</div>
""", unsafe_allow_html=True)
```

**requirements.txt — no change:**
```
streamlit
tensorflow-cpu
Pillow
numpy
gdown
