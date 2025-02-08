import os
import sys
import pickle

# script_dir = os.path.dirname(os.path.realpath(__file__))

# Paths
# modules_path = os.path.join(script_dir, "..", "modules")  # Parent dir contains "modules"
# model_path = os.path.join(script_dir, "stacking_model")  # Inside current dir



modules_path = os.path.abspath(os.path.join(os.getcwd(), ".")) + '\modules'
sys.path.append(modules_path)
from data_pre_processor import preprocess_text


model_path = os.path.abspath(os.path.join(os.getcwd(), ".")) + '\stacking_model\\'


def classify_text_domain(text):
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



