import os
import sys
import pandas as pd
import pickle
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


modules_path = os.path.abspath(os.path.join(os.getcwd(), ".")) + '\modules'
sys.path.append(modules_path)
from classifier import classify_news
from data_pre_processor import preprocess_text


model_path = os.path.abspath(os.path.join(os.getcwd(), ".")) + '\stacking_model\\'


def classify_text_domain(text, category_keywords_dict):
    processed_text = preprocess_text(text)

    categories = {1: 'india', 4: 'world', 0: 'business', 3: 'tech', 2: 'sports'} 
    
    with open(f"{model_path}vectorizer_2.pkl", "rb") as file:
        vectorizer = pickle.load(file)
    
    text_vector = vectorizer.transform([processed_text])
    
    with open(f"{model_path}stack_model_2.pkl", "rb") as file:
        model = pickle.load(file)

    prediction = model.predict(text_vector)

    # prediction = classify_news(text, category_keywords_dict)
    
    return categories[prediction[0]].capitalize()



