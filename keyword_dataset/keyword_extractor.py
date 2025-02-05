import os
import pandas as pd
from keyword_extractor_functions import keyword_extract_and_save


"""# **Load Dataset**"""
dataset_path = os.path.abspath(os.path.join(os.getcwd(), '..')) + '/dataset/'
df = pd.read_csv(f'{dataset_path}india-news-headlines.csv')


keyword_extract_and_save(df, 'india')
keyword_extract_and_save(df, 'politics')
keyword_extract_and_save(df, 'business')
keyword_extract_and_save(df, 'sports')
keyword_extract_and_save(df, 'entertainment')
keyword_extract_and_save(df, 'health')
keyword_extract_and_save(df, 'world')
keyword_extract_and_save(df, 'tech')