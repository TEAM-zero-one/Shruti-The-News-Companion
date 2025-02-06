import streamlit as st
import pandas as pd
import time
from gtts import gTTS
import os
from pathlib import Path
from news_summarizer import text_summarizer  # Import summarization function


st.set_page_config(layout="wide")
vidno = 0

st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #333;
        }
        .category-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        .category-button {
            background-color: #007BFF;
            color: white;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            text-align: center;
            display: inline-block;
            width: 180px;
            transition: all 0.3s ease;
        }
        .category-button:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Shruti - Your AI-Powered News Summarizer</h1>", unsafe_allow_html=True)

# Define CSV file paths for each category
csv_folder = Path(__file__).resolve().parent  # Get the directory of the script
category_csv_files = {
    'India': csv_folder / 'data/india.csv',
    'World': csv_folder / 'data/world.csv',
    'Business': csv_folder / 'data/business.csv',
    'Technology': csv_folder / 'data/tech.csv',
    'Sports': csv_folder / 'data/sports.csv'
}

# Initialize session state variables if not set
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = None
if "filters" not in st.session_state:
    st.session_state["filters"] = {}
if "show_filters" not in st.session_state:
    st.session_state["show_filters"] = False

st.markdown("<div class='category-container'>", unsafe_allow_html=True)

cols = st.columns(len(category_csv_files) + 1)
for i, (category, file_path) in enumerate(category_csv_files.items()):
    if cols[i].button(category, key=f"btn_{category}"):
        st.session_state["selected_category"] = category
# Unique key for the Generate Summary button in the category container
if cols[-1].button("Generate Summary", key="btn_generate_summary_category"):
    st.session_state["selected_category"] = "Generate Summary"

st.markdown("</div>", unsafe_allow_html=True)

selected_category = st.session_state["selected_category"]

if not selected_category:
    st.write("## Welcome to Shruti!")
    st.write("### Explore the latest news or summarize your own content!")
    st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fperkupapp.com%2Fpost%2F20-of-the-best-welcome-to-the-team-memes&psig=AOvVaw2bfFcGnqvXWcfMH74lN2ot&ust=1738815513236000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCIju5PnWq4sDFQAAAAAdAAAAABAE", use_container_width=True)

elif selected_category and selected_category != "Generate Summary":
    st.write(f"## {selected_category}")
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
                st.write(f"[Read Full Article]({article_link})")
            with col2:
                st.write(f"### {article_title}")
                st.write(article_summary)
                
                convert_button_key = f"convert_button_{i}"
                if st.button("Convert to Audio", key=convert_button_key):
                    audio_filename = f"{vidno}_summary_audio.mp3"
                    vidno += 1
                    tts = gTTS(article_summary, lang='en-uk')
                    tts.save(audio_filename)
                    st.audio(audio_filename, format='audio/mp3')
                    if os.path.exists(audio_filename):
                        os.remove(audio_filename)

elif selected_category == "Generate Summary":
    st.write("## Generate a Custom Summary")
    user_input = st.text_area("Enter text to summarize:")

    if st.button("Show Advanced Settings", key="btn_show_advanced"):
        st.session_state["show_filters"] = not st.session_state["show_filters"]

    if st.session_state.get("show_filters", False):
        col1, col2 = st.columns(2)
        with col1:
            min_length = st.slider("Minimum Summary Length", 30, 500, 50)
            max_length = st.slider("Maximum Summary Length", 50, 1000, 150)
            quality_level = st.slider("Generation Quality", 1, 8, 4, 
                help="Higher values produce better results but take longer")
        with col2:
            detail_level = st.slider("Detail Level", 0.5, 3.0, 2.0, 0.1,
                help="Higher values produce more detailed summaries")
            repetition_control = st.slider("Repetition Control", 1.0, 2.5, 1.2, 0.1,
                help="Higher values reduce word repetition")

        st.session_state["filters"] = {
            "min_len": min_length,
            "max_len": max_length,
            "quality_level": quality_level,
            "detail_level": detail_level,
            "repetition_control": repetition_control
        }
    # Unique key for the Generate Summary button on the custom summary page
    if st.button("Generate Summary", key="btn_generate_summary_custom"):
        if user_input.strip():
            with st.spinner("Analyzing text and generating summary..."):
                start_time = time.time()
                filters = st.session_state.get("filters", {})
                summary = text_summarizer(user_input, **filters)
                
                st.write("### Generated Summary:")
                st.success(summary)
                
                # Audio Conversion
                audio_filename = f"summary_audio_{int(time.time())}.mp3"
                tts = gTTS(summary, lang='en')
                tts.save(audio_filename)
                st.audio(audio_filename)
                os.remove(audio_filename)
                
                st.write(f"Summary generated in {time.time()-start_time:.1f} seconds")
        else:
            st.warning("Please enter some text to summarize")

st.markdown("""
<p style='font-size: small; color: grey; text-align: center;'>
A NLP project. <a href='https://github.com/TEAM-zero-one/Shruti-The-News-Companion'>GitHub Link</a>.
Disclaimer: This project is intended for educational purposes only. Web scraping without proper authorization is not encouraged or endorsed.
</p>
""", unsafe_allow_html=True)