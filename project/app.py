       
import streamlit as st
import pandas as pd
import os
import tempfile
from gtts import gTTS
from pathlib import Path
from news_summarizer import text_summarizer  # Import summarization function
from QnA import answers  # Import the QA function
from text_to_speech import generate_audio

# Configuration
st.set_page_config(layout="wide")
AUDIO_TEMP_DIR = tempfile.TemporaryDirectory()  # For safe audio file handling

# UI Styling
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #333;
        }
        .separator {
            height: 2px;
            background-color: #ddd;
            margin: 20px 0;
        }
        .summary-box, .about-box {
            padding: 20px;
            background-color: black;
            border-radius: 10px;
            margin: 15px 0;
            color: white;
        }
        .hidden {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = None
if "audio_files" not in st.session_state:
    st.session_state["audio_files"] = set()
if "show_about" not in st.session_state:
    st.session_state["show_about"] = True
if "summary" not in st.session_state:
    st.session_state["summary"] = ""

# File Path Configuration
def get_csv_paths():
    """Return configured CSV file paths for news categories"""
    csv_folder = Path(__file__).resolve().parent
    return {
        'India': csv_folder / 'data/india.csv',
        'World': csv_folder / 'data/world.csv',
        'Business': csv_folder / 'data/business.csv',
        'Technology': csv_folder / 'data/tech.csv',
        'Sports': csv_folder / 'data/sports.csv'
    }
category_csv_files = get_csv_paths()

# Audio Handling Utilities
def create_audio(text: str) -> str:
    """Generate and save audio file from text using gTTS"""
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False, dir=AUDIO_TEMP_DIR.name) as fp:
            tts = gTTS(text, lang='en', tld='co.uk')
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        return None

def clean_audio_files():
    """Clean up generated audio files"""
    for fpath in st.session_state.audio_files:
        try:
            if os.path.exists(fpath):
                os.remove(fpath)
        except Exception as e:
            st.error(f"Error cleaning audio files: {str(e)}")
    st.session_state.audio_files = set()

# UI Components
st.markdown("<h1 class='main-title'>🌟 Shruti - The NEWS Companion 🌟</h1>", unsafe_allow_html=True)

cols = st.columns(len(category_csv_files) + 2)
for i, (category, file_path) in enumerate(category_csv_files.items()):
    if cols[i].button(f"{category}", key=f"btn_{category}"):
        st.session_state["selected_category"] = category
        clean_audio_files()

if cols[-2].button("Generate Summary", key="btn_generate_summary_category"):
    st.session_state["selected_category"] = "Generate Summary"
    clean_audio_files()

if cols[-1].button("About", key="btn_about"):
    st.session_state["show_about"] = not st.session_state["show_about"]

# About Project Box
if st.session_state["show_about"]:
    st.markdown("""
        <div class='about-box'>
            <h3>About Shruti - The News Companion</h3>
            <p>Shruti is an innovative and comprehensive news companion that combines cutting-edge AI technologies to help users stay updated with the latest news, get quick summaries, and even interact with news content using question answering. 📰🤖</p>
            <p>GitHub Profiles:</p>
            <ul>
                <li><a href='https://github.com/aryan2001atat' target='_blank'>👨 Aryan Pal</a></li>
    <li><a href='https://github.com/adrs3342' target='_blank'>👨 Adarsh Sharma</a></li>
    <li><a href='https://github.com/ashutosh-awasthi23' target='_blank'>👨 Ashutosh Awasthi</a></li>
    <li><a href='https://github.com/zwarriors2208' target='_blank'>👨 Kumar Ankit</a></li>
    <li><a href='https://github.com/DkunalS' target='_blank'>👨 Kunal Sahu</a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

selected_category = st.session_state["selected_category"]

if selected_category and selected_category != "Generate Summary":
    st.write(f"## {selected_category} 📰")
    df = pd.read_csv(category_csv_files[selected_category])
    
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
                
                if st.button("🔊 Convert to Audio", key=f"convert_button_{i}"):
                    audio_path = generate_audio(article_summary)
                    if audio_path:
                        st.session_state.audio_files.add(audio_path)
                        st.audio(audio_path, format='audio/mp3')

            st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

elif selected_category == "Generate Summary":
    st.write("## Generate a Custom Summary")
    user_input = st.text_area("Enter text to summarize:", "")
    if st.button("Summarize"):
        if user_input.strip():
            with st.spinner("Generating summary..."):
                st.session_state["summary"] = text_summarizer(user_input)
    
    if st.session_state["summary"]:
        st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
        st.write("### Generated Summary:")
        st.success(st.session_state["summary"])
        
        audio_path = generate_audio(st.session_state["summary"])
        if audio_path:
            st.session_state.audio_files.add(audio_path)
            st.audio(audio_path, format='audio/mp3')

        question = st.text_input("Your question about this summary:", key="summary_question")
        if st.button("Get Answer"):
            if question.strip():
                with st.spinner("Finding answer..."):
                    answer = answers(user_input, question)
                    st.success(f"**Answer:** {answer}")
            else:
                st.warning("Please enter a question")
    
        
        st.markdown("</div>", unsafe_allow_html=True)



# Footer
st.markdown("""
<p style='font-size: small; color: grey; text-align: center;'>
A NLP project. <a href='https://github.com/TEAM-zero-one/Shruti-The-News-Companion'>GitHub Link</a>.
Disclaimer: Educational use only. Web scraping without authorization is not endorsed.
</p>
""", unsafe_allow_html=True)

AUDIO_TEMP_DIR.cleanup()




