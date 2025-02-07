
import streamlit as st
import pandas as pd
import time
from gtts import gTTS
import os
from pathlib import Path
from news_summarizer import text_summarizer  # Import summarization function
from nltk.tokenize import word_tokenize, sent_tokenize  # Assuming these are imported somewhere
from QnA import answers  # Import the QA function
from text_to_speech import generate_audio

st.set_page_config(layout="wide")
vidno = 0



st.markdown("<h1 class='main-title'>📰 Shruti - Your AI-Powered News Summarizer 🤖</h1>", unsafe_allow_html=True)

# Define CSV file paths for each category
csv_folder = Path(__file__).resolve().parent  # Get the directory of the script
category_csv_files = {
    'India': csv_folder / 'data/india.csv',
    'World': csv_folder / 'data/world.csv',
    'Business': csv_folder / 'data/business.csv',
    'Technology': csv_folder / 'data/tech.csv',
    'Sports': csv_folder / 'data/sports.csv'
}

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = None

cols = st.columns(len(category_csv_files))
for i, (category, file_path) in enumerate(category_csv_files.items()):
    if cols[i].button(f"{category} 🌍", key=f"btn_{category}"):
        st.session_state["selected_category"] = category

selected_category = st.session_state["selected_category"]

if selected_category:
    st.write(f"## {selected_category} 📰")
    csv_file = category_csv_files[selected_category]
    df = pd.read_csv(csv_file)

    for i in range(min(50, len(df))):
        article_title = df.iloc[i]['Article Title']
        article_summary = df.iloc[i]['Article Summary']
        article_link = df.iloc[i]['Article Link']
        article_image = df.iloc[i]['Article Image']
        
        if all(isinstance(field, str) and field.strip() for field in [article_title, article_summary, article_link, article_image]):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(article_image, width=250)
                st.write(f"🔗 [Read Full Article]({article_link})")
            with col2:
                st.write(f"### 🗞 {article_title}")
                st.write(f"📝 {article_summary}")
                
                question = st.text_input(f"🤔 Ask a question about this article (Q{i})", "")
                if question.strip():
                    answer = answers(article_summary, question)
                    st.write("**💡 Answer:**", answer)
                
                convert_button_key = f"convert_button_{i}"
                if st.button("🔊 Convert to Audio", key=convert_button_key):
                    audio_filename = f"{vidno}_summary_audio.mp3"
                    vidno += 1
                    tts = gTTS(article_summary, lang='en-uk')
                    tts.save(audio_filename)
                    st.audio(audio_filename, format='audio/mp3')
                    os.remove(audio_filename)
            
            st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
