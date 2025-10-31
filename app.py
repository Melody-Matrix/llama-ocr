import streamlit as st
from PIL import Image, ImageEnhance
import easyocr

st.title("🦙 OCR with EasyOCR (Enhanced Accuracy)")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # 🔧 Preprocessing: Resize, enhance contrast, convert to grayscale
    image = image.resize((image.width * 2, image.height * 2))
    image = ImageEnhance.Contrast(image).enhance(2.0)
    image = image.convert("L")  # Grayscale

    st.image(image, caption="Preprocessed Image", use_column_width=True)

    st.write("🔍 Extracted Text with Confidence:")
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image, detail=1, paragraph=True)

    # 🧠 Show each detected line with confidence score
    for bbox, text, confidence in result:
        st.markdown(f"**{text}** — Confidence: `{confidence:.2f}`")

    # 📝 Combine all text into one block
    full_text = "\n".join([item[1] for item in result])
    st.text_area("📝 Full OCR Output", full_text, height=300)