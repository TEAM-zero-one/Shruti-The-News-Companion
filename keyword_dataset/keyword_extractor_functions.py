from keybert import KeyBERT
import os
import sys
import pandas as pd
from data_pre_processor import preprocess_text



"""# **KeyBERT Extraction**"""
model = KeyBERT()

def extract_keywords_from_df(df_1, num_keywords = 100):
  full_text = ' '.join(df_1['processed_text'])
  keywords = model.extract_keywords(full_text,
                                    # keyphrase_ngram_range = (1, 2),
                                    top_n=num_keywords)
  return [kw[0] for kw in keywords]

def extract_keywords_from_text(news, num_keywords = 100):
  keywords = model.extract_keywords(news,
                                    # keyphrase_ngram_range = (1, 2),
                                    top_n=num_keywords)
  return [kw[0] for kw in keywords]



"""# **Extract & Save**"""
def keyword_extract_and_save(df, categ):

  category_df = df[df["headline_category"].str.contains(categ, case=False, na=False)].tail(1000)

  category_df['processed_text'] = category_df['headline_text'].apply(preprocess_text)

  category_key = extract_keywords_from_df(category_df, 500)

  keywords_path = os.path.abspath(os.path.join(os.getcwd(), ".")) + '/keywords'

  pd.DataFrame(category_key, columns = ['keyword']).to_csv(f'{keywords_path}/{categ}_keywords_tail_new.csv')



