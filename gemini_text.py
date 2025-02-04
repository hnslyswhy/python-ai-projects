from dotenv import load_dotenv
load_dotenv() # load the variables from the .env file

import streamlit as st

import os
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load gemini model and get response
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text

# initialize streamlit app
st.set_page_config(page_title="Gemini Q&A Demo") #st.set_page_config() must be the first Streamlit command in the script
st.title("Gemini Q&A Demo")
st.header("Ask me anything about Gemini!")

# user input
user_input = st.text_input("Enter your prompt:", key="user_input")
submit_button = st.button("Submit Question", key="submit_button")

# get response
if user_input and submit_button:
    response = get_gemini_response(user_input)
    st.subheader("The response is:")
    st.write(response)