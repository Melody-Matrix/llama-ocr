import streamlit as st
from PIL import Image, ImageEnhance
import easyocr
import numpy as np

# 🎯 App Title
st.markdown("<h1 style='text-align: center;'>🦙 OCR with EasyOCR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload an image to extract text with enhanced accuracy</p>", unsafe_allow_html=True)

# 🔄 Cache the OCR model
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], rotation_info=True)

reader = load_reader()

# 📤 File Upload
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # 🧪 Optional Enhancements
    with st.expander("🔧 Enhance image for better OCR"):
        enhance = st.checkbox("Apply brightness & contrast boost")
        if enhance:
            image = ImageEnhance.Brightness(image).enhance(1.5)
            image = ImageEnhance.Contrast(image).enhance(2.0)
            image = image.convert("L")

    # 📐 Resize if needed
    if image.width < 1000:
        image = image.resize((image.width * 2, image.height * 2))

    # 🖼️ Display image centered
    st.markdown("<h4 style='text-align: center;'>Processed Image</h4>", unsafe_allow_html=True)
    st.image(image, use_column_width=True)

    # 🔍 OCR Processing
    image_np = np.array(image)
    result = reader.readtext(image_np, detail=1)

    # 📋 Display results in columns
    st.markdown("### 🔍 Extracted Text")
    for bbox, text, confidence in result:
        if confidence > 0.5:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"<div style='font-size:16px;'>{text}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='background-color:#eee;border-radius:5px;padding:4px;text-align:center;'>Conf: {confidence:.2f}</div>", unsafe_allow_html=True)

    # 📝 Full Text Output
    full_text = "\n".join([item[1] for item in result])
    st.markdown("### 📝 Full OCR Output")
    st.text_area("Complete extracted text", full_text, height=300)