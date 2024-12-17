#AIzaSyCVHWcCJu_HWatQyEAxyK5cbgBJPqCWsG8
import streamlit as st
from dotenv import load_dotenv

load_dotenv() #loads all the emvironment variables
import os 
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("API_KEY"))

prompt = """You are a youtube video summarizer you will be taking the transcript text and summarzing the entire video providing the important summary in points wihin 300 words. The transcript text will be appended here : """

#getting transcripts of the videos through their url
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        #splits the url in two parts at the '=' symbol and gets the video id from the second part 
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        #gets the transcript in the form of a list

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        #converts the list into a paragraph, appending each word witha space in between

        return transcript

    except Exception as e:
        raise e

#generates the summary of the transcript it is provided with following the prompt described above using the gemini model
def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text
    
st.title("Summify")
youtube_link = st.text_input("Enter the youtube video Link here:")
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
if st.button("Get Summary"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
         
        st.markdown("SUMMARY")
        st.write(summary)