import streamlit as st
from PIL import Image
import pytesseract

st.title("🦙 Local OCR with Tesseract")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Extracted Text:")
    text = pytesseract.image_to_string(image)
    st.text(text)