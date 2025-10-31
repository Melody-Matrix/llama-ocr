import streamlit as st
from PIL import Image
import easyocr

st.title("🦙 OCR with EasyOCR (Streamlit Cloud Compatible)")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Extracted Text:")
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    text = "\n".join([item[1] for item in result])
    st.text_area("OCR Output", text, height=300)