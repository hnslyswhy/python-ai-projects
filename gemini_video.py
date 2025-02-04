from dotenv import load_dotenv  
from pathlib import Path
import os

import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# function to generate a video summary
def generate_video_summary(transcript, language):
    prompt = f'''You are a video summary generator for youtube food recipes videos
    which are likely not in English. 
    you are given a video transcript: {transcript} and a language: {language}.
    you need to generate a summary of the food recipe based on the transcript using the specified language
    make sure to include the ingredients the steps to make the recipe.
    for the ingredients, make sure to include the quantity and the unit of measurement.
    in a way that is easy to understand and follow in 300 words.
    '''
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text

# function to fetch a video transcript
def fetch_video_transcript(video_url):
    try:
        video_id = video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item["text"] for item in transcript])
        return transcript_text
    except Exception as e:
        st.error(f"Error fetching video transcript: {e}")
        return None

# streamlit app
st.title("Learn foreign food recipes made easy")
youtube_url = st.text_input("Enter the YouTube video URL")
specific_language = st.text_input("Enter the specific language of the transcript you want to generate") 
    
if st.button("Generate Summary") :
    if not youtube_url:
        st.error("Please enter a valid YouTube video URL")
    elif not specific_language:
        st.error("Please enter a valid language")
    else:
        transcript = fetch_video_transcript(youtube_url)
        if transcript:
            summary = generate_video_summary(transcript, specific_language)
            st.write(summary)
        else:
            st.error("Failed to fetch video transcript")

