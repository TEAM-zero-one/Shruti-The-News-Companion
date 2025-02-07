import os
import sys
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


modules_path = os.path.abspath(os.path.join(os.getcwd(), ".")) + '\modules'
sys.path.append(modules_path)
from classifier import classify_news
from data_pre_processor import preprocess_text





def classify_text_domain(text, category_keywords_dict):
    processed_text = preprocess_text(text)
    
    prediction = classify_news(text, category_keywords_dict)
    
    return prediction.capitalize()

