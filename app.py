import streamlit as st
from PIL import Image, ImageEnhance
import easyocr
import numpy as np

st.title("🦙 OCR with EasyOCR (Enhanced & Fast)")

# 🔄 Cache the OCR model to speed up reloads
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'], rotation_info=True)

reader = load_reader()

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # 🧪 Optional preprocessing toggle
    if st.checkbox("Enhance image for better OCR"):
        image = ImageEnhance.Brightness(image).enhance(1.5)
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image = image.convert("L")

    # Resize only if image is small
    if image.width < 1000:
        image = image.resize((image.width * 2, image.height * 2))

    st.image(image, caption="Processed Image", use_column_width=True)

    # Convert to NumPy array for easyocr
    image_np = np.array(image)

    st.write("🔍 Extracted Text with Confidence:")
    result = reader.readtext(image_np, detail=1)

    for bbox, text, confidence in result:
        if confidence > 0.5:  # Filter low-confidence results
            st.markdown(f"**{text}** — Confidence: `{confidence:.2f}`")

    full_text = "\n".join([item[1] for item in result])
    st.text_area("📝 Full OCR Output", full_text, height=300)