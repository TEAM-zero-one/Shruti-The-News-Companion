import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from keyword_extractor_functions import extract_keywords_from_text



def classify_news(news, category_keywords_dict):

  article_keywords = extract_keywords_from_text(news)
  article_keywords_str = ' '.join(article_keywords)

  vectorizer = TfidfVectorizer()

  category_keywords_list = [''.join(keywords) for keywords in category_keywords_dict.values()]

  tfidf_matrix = vectorizer.fit_transform([article_keywords_str] + (category_keywords_list))

  similarities = cosine_similarity(tfidf_matrix[0].reshape(1, -1), tfidf_matrix[1:]).flatten()

  # print(list(category_keywords_dict.keys()), similarities, sep = '\n')
  best_match = list(category_keywords_dict.keys())[np.argmax(similarities)]
  # print(f"{news}\n{best_match}")
  return best_match

  # # Get non-zero similarity values and their indices
  # non_zero_indices = np.where(similarities > 0)[0]

  # if len(non_zero_indices) == 0:
  #     return 'other'
  # else:
  #     # Sort non-zero similarities in descending order
  #     sorted_indices = non_zero_indices[np.argsort(similarities[non_zero_indices])][::-1]

  #     # Select top 1 or 2 based on availability
  #     top_indices = sorted_indices[:2] if len(sorted_indices) > 1 else sorted_indices[:1]

  #     # Retrieve category names
  #     top_categories = [list(category_keywords_dict_1.keys())[i] for i in top_indices]

  #     # Print result
  #     print(f"{news}\nTop Categories: {', '.join(top_categories)}")
