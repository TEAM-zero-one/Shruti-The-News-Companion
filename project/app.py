# import nltk
# nltk.download('punkt')
# nltk.download('punkt_tab')
# import streamlit as st
# import pandas as pd
# import os
# import tempfile
# from gtts import gTTS
# from pathlib import Path
# from news_summarizer import text_summarizer  # Import summarization function
# from QnA import answers  # Import the QA function
# from text_to_speech import generate_audio

import streamlit as st
import pandas as pd
from gtts import gTTS
import os
from pathlib import Path
import tempfile
from news_summarizer import text_summarizer
from QnA import answers
from pdf_utils import extract_text_from_pdf,generate_pdf

# Configuration
st.set_page_config(layout="wide")
AUDIO_TEMP_DIR = tempfile.TemporaryDirectory()  # For safe audio file handling

# UI Styles
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: white;
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
        .summary-box {
            padding: 20px;
            background-color: #f0f2f6;
            border-radius: 10px;
            margin: 15px 0;
        }
        .about-box {
            padding: 20px;
            background-color: black;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
SESSION_DEFAULTS = {
    "selected_category": None,
    "filters": {},
    "show_filters": False,
    "summary": None,
    "question": "",
    "answer": None,
    "audio_files": set()
}

for key, value in SESSION_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

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
def render_category_selector():
    """Render category selection buttons"""
    st.markdown("<h1 class='main-title'>📰 Shruti - The NEWS Companion 🤖</h1>", unsafe_allow_html=True)
    st.markdown("<div class='category-container'>", unsafe_allow_html=True)
    
    cols = st.columns(len(category_csv_files) + 1)
    for i, category in enumerate(category_csv_files):
        if cols[i].button(category, key=f"btn_{category}"):
            st.session_state.selected_category = category
            clean_audio_files()  # Clear previous audio files on category change
    
    if cols[-1].button("Generate Summary", key="btn_generate_summary_category"):
        st.session_state.selected_category = "Generate Summary"
        clean_audio_files()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_news_article(article_data, idx):
    """Render individual news article with Q&A"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(article_data['Article Image'], width=250)
        st.write(f"[Read Full Article]({article_data['Article Link']})")
    
    with col2:
        st.write(f"### {article_data['Article Title']}")
        st.write(article_data['Article Summary'])
        
        # Audio Conversion
        if st.button("Convert to Audio", key=f"convert_{idx}"):
            audio_path = create_audio(article_data['Article Summary'])
            if audio_path:
                st.session_state.audio_files.add(audio_path)
                st.audio(audio_path, format='audio/mp3')
        
        # Q&A Section
        with st.expander("Ask a question about this news article"):
            user_question = st.text_input("Your question:", key=f"qna_{idx}")
            if st.button("Get Answer", key=f"answer_{idx}"):
                if user_question.strip():
                    with st.spinner("Analyzing..."):
                        answer = answers(article_data['Article Summary'], user_question)
                        st.success(f"**Answer:** {answer}")
                else:
                    st.warning("Please enter a question.")

# Main App Logic
category_csv_files = get_csv_paths()
render_category_selector()
selected_category = st.session_state.selected_category

# Home Page
if not selected_category:
    st.write("## Welcome to Shruti!")
    st.write("### Explore the latest news, summarize content, or ask AI your questions!")
    # st.image("", use_container_width=True)
    
    # Added About Section
    st.markdown("""
        <div class='about-box'>
            <h3>📌 About Shruti - The News Companion</h3>
            <p>Shruti is an AI-powered news companion that helps you stay informed through:</p>
            <ul>
                <li>📰 Curated news categories</li>
                <li>🤖 AI-powered summarization</li>
                <li>🔍 Interactive Q&A with news content</li>
                <li>🔊 Audio conversions</li>
            </ul>
            <p>Developed by:</p>
            <ul>
                <li><a href='https://github.com/aryan2001atat' target='_blank'>Aaryan Pal</a></li>
                <li><a href='https://github.com/adrs3342' target='_blank'>Adarsh Sharma</a></li>
                <li><a href='https://github.com/ashutosh-awasthi23' target='_blank'>Ashutosh Awasthi</a></li>
                <li><a href='https://github.com/zwarriors2208' target='_blank'>Kumar Ankit</a></li>
                <li><a href='https://github.com/DkunalS' target='_blank'>Kunal Sahu</a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# News Category Pages
elif selected_category != "Generate Summary":
    st.write(f"## {selected_category}")
    df = pd.read_csv(category_csv_files[selected_category])
    
    for idx in range(min(50, len(df))):
        article_data = df.iloc[idx]
        if all(isinstance(article_data[field], str) and article_data[field].strip() 
               for field in ['Article Title', 'Article Summary', 'Article Link', 'Article Image']):
            render_news_article(article_data, idx)

# Custom Summary Page
else:
    st.write("## Generate a Custom Summary")
    input_type = st.radio("Choose Input Type:", ["Text Input", "Upload PDF"])
    if input_type == "Text Input":
    
        # Input Section
        user_input = st.text_area("Enter text to summarize:", key="user_input", 
                                on_change=lambda: st.session_state.update({"summary": None, "answer": None}))
        
        
        # Summary Generation
        if st.button("Generate Summary", key="btn_generate"):
            if user_input.strip():
                with st.spinner("Analyzing text..."):
                    summary = text_summarizer(user_input, **st.session_state.filters)
                    st.session_state.summary = summary
                    st.session_state.answer = None
            else:
                st.warning("Please enter text to summarize")
        
        # Display Summary
        if st.session_state.summary:
            st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
            st.write("### Generated Summary:")
            st.success(st.session_state.summary)
            
            # Audio Conversion
            audio_path = create_audio(st.session_state.summary)
            if audio_path:
                st.session_state.audio_files.add(audio_path)
                st.audio(audio_path)
            
            # Q&A Section
            st.write("### Ask a Question")
            user_question = st.text_input("Your question:", key="summary_question", 
                                        value=st.session_state.question)
            
            if st.button("Get Answer"):
                if user_input.strip() and user_question.strip():
                    with st.spinner("Finding answer..."):
                        answer = answers(user_input, user_question)
                        st.session_state.answer = answer
                else:
                    st.warning("Please enter both text and question")
            
            if st.session_state.answer:
                st.success(f"**Answer:** {st.session_state.answer}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    elif input_type == "Upload PDF":
        st.subheader("📂 Upload a PDF Document")

        uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_pdf is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_pdf.read())
                pdf_path = temp_file.name

            # Extract and summarize text
            with st.spinner("Extracting text from PDF..."):
                extracted_text = extract_text_from_pdf(pdf_path)

            if extracted_text:
                with st.spinner("Summarizing text..."):
                    pdf_summary = text_summarizer(extracted_text)
                    st.session_state.pdf_summary = pdf_summary

                # Generate and provide PDF download
                pdf_summary_path = generate_pdf(st.session_state.pdf_summary)
                st.success("### Summary Generated! Download below:")

                with open(pdf_summary_path, "rb") as pdf_file:
                    st.download_button(label="📥 Download Summary as PDF",
                                    data=pdf_file,
                                    file_name="summary.pdf",
                                    mime="application/pdf")
            else:
                st.error("Could not extract text from the uploaded PDF.")
    # Advanced Settings
    if st.button("Toggle Advanced Settings", key="btn_advanced"):
        st.session_state.show_filters = not st.session_state.show_filters
    
    if st.session_state.show_filters:
        col1, col2 = st.columns(2)
        with col1:
            min_length = st.slider("Minimum Length", 30, 500, 50)
            max_length = st.slider("Maximum Length", 50, 1000, 150)
            quality_level = st.slider("Quality Level", 1, 8, 4, help="Higher values produce better results but take longer")
        with col2:
            detail_level = st.slider("Detail Level", 0.5, 3.0, 2.0, 0.1, help="Higher values include more details")
            repetition_control = st.slider("Repetition Control", 1.0, 2.5, 1.2, 0.1, help="Higher values reduce repetition")
        
        st.session_state.filters = {
            "min_len": min_length,
            "max_len": max_length,
            "quality_level": quality_level,
            "detail_level": detail_level,
            "repetition_control": repetition_control
        }
                
# Footer
st.markdown("""
<p style='font-size: small; color: grey; text-align: center;'>
A NLP project. <a href='https://github.com/TEAM-zero-one/Shruti-The-News-Companion'>GitHub Link</a>.
Disclaimer: Educational use only. Web scraping without authorization is not endorsed.
</p>
""", unsafe_allow_html=True)

# Cleanup when done
AUDIO_TEMP_DIR.cleanup()




