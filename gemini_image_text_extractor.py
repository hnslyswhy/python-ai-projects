from dotenv import load_dotenv
load_dotenv()

import os
import io
import streamlit as st
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# function to extract text from image
def extract_text(input, image, prompt):
    response = model.generate_content([input, image[0], prompt]) # image[0] is the first image in the list
    return response.text

# function to setup the image
def setup_image(uploaded_file):
    if uploaded_file is not None:
        try:
            # Handle image files only
            image = Image.open(uploaded_file)
            image_bytes = uploaded_file.getvalue()
            
            image_parts = [{
                "mime_type": uploaded_file.type,
                "data": image_bytes
            }]
            return image_parts
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.error("Please upload an image file (e.g., PNG, JPG, JPEG)")
            return None
    
    return None

# initialize streamlit app
st.title("Text Extractor")
st.header("Multi-language extract text from an image")
# user input
user_input = st.text_input("Enter your text", key="input")
# image uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key="image")
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
# prompt input
prompt = """
You are a text extractor. You are given an image and a text. You need to extract the text from the image, and answer any questions related to the text.
"""
# submit button
submit_button = st.button("Extract Text", key="submit_button")

# get response
if submit_button:
    image_data = setup_image(uploaded_file)
    response = extract_text(user_input, image_data, prompt)
    st.subheader("The Response is: ")
    st.write(response)