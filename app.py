import streamlit as st
from PIL import Image, ImageEnhance
import easyocr
import numpy as np

# 🎯 Custom Headline
st.markdown("""
    <h1 style='text-align: center;'>🦙 Llama-OCR Project by John Jaskaran Singh(Team-DELTA)<br>
    <span style='font-size:18px;'>(Melody-Matrix)</span></h1>
    <p style='text-align: center;'>Upload an image to extract text with enhanced accuracy</p>
""", unsafe_allow_html=True)

# 🔄 Cache the OCR model
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = load_reader()

# 📤 File Upload
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        image = Image.open(uploaded_file)

        # ✅ Validate image dimensions
        if image.width == 0 or image.height == 0:
            st.error("Uploaded image is invalid or empty.")
            st.stop()

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

        if not result:
            st.warning("No text detected. Try enhancing the image or uploading a clearer one.")
            st.stop()

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

    except Exception as e:
        st.error(f"App crashed: {e}")
        st.stop()
