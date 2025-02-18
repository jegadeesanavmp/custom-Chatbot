import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from io import BytesIO

load_dotenv()

st.set_page_config(
    page_title="AI assistant",
    page_icon="🤖",  # Favicon emoji representing fitness
    layout="centered",  # Page layout option
)

st.title("AI assistant for students 👾")

# Uploaded file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "csv"])
img = None
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, width=450, caption='Uploaded Image')
else:
    st.warning("Please upload an image file.")

# Set up Google Gemini-Pro AI model
genai.configure(api_key="AIzaSyCgojtUo9SMD9E5Xoq7i52An3fIM_K5Lvw")
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask your doubts:")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    
    try:
        # Check if image is defined before sending it to the model
        if img:
            gemini_response = st.session_state.chat_session.send_message([user_prompt, img])
        else:
            gemini_response = st.session_state.chat_session.send_message([user_prompt])

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
