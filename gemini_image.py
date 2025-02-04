from dotenv import load_dotenv
load_dotenv() # load the variables from the .env file

import streamlit as st
from PIL import Image

import os
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load gemini model and get response
model = genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(input, image):
    if input and image:
        response = model.generate_content([input, image])
    else:
        response = model.generate_content("Please add an input")
    return response.text

# initialize streamlit app
st.set_page_config(page_title="Your Diet Assistant")
st.title("Your Personal Diet Assistant")
st.header("Tell me about yourself")

# user input
user_info = st.text_input("Enter your age, gender, weight, height, and activity level:", key="user_info")
user_goal = st.text_input("Enter your goal (lose weight, gain weight, maintain weight):", key="user_goal")

uploaded_file = st.file_uploader("Show me your food...", type=["jpg", "jpeg", "png"])
submit_button = st.button("Submit", key="submit_button")

# get response
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


    
prompt = f'''
You are a dietitian, you are given a user's information {user_info}, user's goal {user_goal}, and a food image.
you need to give a food analysis based on the food image, include the calories, macronutrients, and micronutrients in your analysis, 
and give a suggestion for the user to adjust the food based on the image so that it is healthier and more nutritious and helps the user achieve their goal
and explain the reason for your suggestion in detail.
and make sure the food can easily be found in the market.
'''
if submit_button:
    if not user_info or not user_goal:
        st.error("Please fill in all fields")
        st.stop()
    else:
        response = get_gemini_response(prompt, image)
        st.subheader("Here is your food analysis, and diet plan:")
        st.write(response)