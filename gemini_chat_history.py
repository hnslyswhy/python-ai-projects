from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

import streamlit as st

# initialize streamlit app
st.set_page_config(page_title="Your Chat Bot")
st.title("Hi, I'm your personal bot, botty!")
st.header("What's on your mind?")

# function to get gemini response
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

def get_gemini_response(prompt):
    response= chat.send_message(prompt, stream=True)
    return response

# initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# user input
user_input = st.text_input("Tell me what you want to chat about?", key="user_input")
submit_button = st.button("Let's chat!", key="submit_button")

# get response
if user_input and submit_button:
    response = get_gemini_response(user_input)
    # add user input and response to chat history
    st.session_state['chat_history'].append(("You", user_input))
    st.subheader("Botty:") 
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Botty", chunk.text))
st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")