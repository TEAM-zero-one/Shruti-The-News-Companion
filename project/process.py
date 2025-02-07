import os
import pandas as pd
from bs4 import BeautifulSoup
from news_summarizer import text_summarizer
from collect import categorize_articles
from pathlib import Path
from newspaper import Article
import csv


# Function to download and parse articles, and save data to CSV
def process_and_save_articles(links_list, csv_file):
    article_links = []
    article_text = []
    article_summary = []
    article_titles = []
    article_img = []
    total = 0
    print("=======================================")
    print("Inside Process and Save")

    for link in links_list:

        try:
            article = Article(link)
            article.download()
            article.parse()
            article.nlp()
            text = article.text
            print(text)
            print("Generating summary")
            summary = text_summarizer(text) #from gensum.py
            print(f"Generated summary: {summary}")

            # Find img src
            img_src = None
            img_tags = BeautifulSoup(article.html, 'html.parser').find_all('img')
            for img_tag in img_tags:
                src = img_tag.get('src', '')
                alt = img_tag.get('alt', '')
                fetchpriority = img_tag.get('fetchpriority', '')
                if "static.toiimg." in src and alt != "TOI logo" and fetchpriority == "high":
                    img_src = src
                    break

            # Check if all fields are valid and not null
            if all(article.title not in article_titles and field is not None and isinstance(field, str) and field.strip() for field in [link, text, summary, img_src]):
                print("Inside if")
                article_img.append(img_src)
                article_links.append(link)
                article_text.append(text)
                article_titles.append(article.title)  # Domain name as title
                article_summary.append(summary)
                print("Local Vars updated")
                total += 1
                print(total)

            if total >= 10:
                break

        except Exception as e:
            print(f"Error downloading article from {link}   : {e}")
            continue  # Continue with the next iteration of the loop

    # Save data to CSV
    print("Trying to save CSV")
    if article_titles:
        print("Inside Save if")
        if os.path.exists(csv_file):
            print("Path exists")
            file_size = os.path.getsize(csv_file)
            if file_size == 0:
                print("File size is zero")
                with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Article Title', 'Article Link', 'Article Text', 'Article Summary', 'Article Image'])
                    for i in range(len(article_titles)):
                        writer.writerow([article_titles[i], article_links[i], article_text[i], article_summary[i], article_img[i]])
                print("Data has been saved to:", csv_file)



# Define CSV file paths relative to the current file.
csv_folder = Path(__file__).resolve().parent
info_files = {
    "India": csv_folder / 'data/india.csv',
    "World": csv_folder / 'data/world.csv',
    "Business": csv_folder / 'data/business.csv',
    "Tech": csv_folder / 'data/tech.csv',
    "Sports": csv_folder / 'data/sports.csv'
}

# List of URLs to scrape.
all_links = [
    "https://timesofindia.indiatimes.com/india",
    "https://timesofindia.indiatimes.com/india/delhi",
    "https://timesofindia.indiatimes.com/india/maharashtra", 
    "https://timesofindia.indiatimes.com/india/tamil-nadu",

    "https://timesofindia.indiatimes.com/world",
    "https://timesofindia.indiatimes.com/world/uk",
    "https://timesofindia.indiatimes.com/world/us",
    "https://timesofindia.indiatimes.com/world/south-asia"
    "https://timesofindia.indiatimes.com/world/middle-east",
    
    "https://timesofindia.indiatimes.com/business",
    "https://timesofindia.indiatimes.com/business/stock-market",
    "https://timesofindia.indiatimes.com/business/financial-literacy",
    "https://timesofindia.indiatimes.com/business/india-business",
    "https://timesofindia.indiatimes.com/business/international-business"
    
    "https://timesofindia.indiatimes.com/technology",
    "https://timesofindia.indiatimes.com/technology/tech-news",
    
    "https://timesofindia.indiatimes.com/sports",
]


def load_category_keywords(file_path):

    df = pd.read_csv(file_path)
    # Assuming the CSV has two columns: 'keyword' and 'score'
    return df['keyword'].tolist()


keywords_path = os.path.abspath(os.path.join(os.getcwd(), ".")) + '\keyword_dataset\data'
# Load keywords for each category
india_keywords = load_category_keywords(f'{keywords_path}/india_keywords_tail_new.csv')

politics_keywords = load_category_keywords(f'{keywords_path}/politics_keywords_tail_new.csv')

business_keywords = load_category_keywords(f'{keywords_path}/business_keywords_tail_new.csv')

sports_keywords = load_category_keywords(f'{keywords_path}/sports_keywords_tail_new.csv')

entertainment_keywords = load_category_keywords(f'{keywords_path}/entertainment_keywords_tail_new.csv')

health_keywords = load_category_keywords(f'{keywords_path}/health_keywords_tail_new.csv')

world_keywords = load_category_keywords(f'{keywords_path}/world_keywords_tail_new.csv')

tech_keywords = load_category_keywords(f'{keywords_path}/tech_keywords_tail_new.csv')

category_keywords_dict = {
    'India': ' '.join(india_keywords[:500]),
    'Politics': ' '.join(politics_keywords[:250]),
    'Business': ' '.join(business_keywords[:500]),
    'Sports': ' '.join(sports_keywords[:500]),
    'Entertainment': ' '.join(entertainment_keywords[:250]),
    'Health': ' '.join(health_keywords[:500]),
    'World': ' '.join(world_keywords[:500]),
    'Tech': ' '.join(tech_keywords[:350]),
}

def start_new():
    # Get the categorized articles (each article has already been processed once).
    domain_lists = categorize_articles(all_links, category_keywords_dict)
    
    # For each category, process the articles and save to CSV.
    for category, filepath in info_files.items():
        if category in domain_lists:
            process_and_save_articles(domain_lists[category], filepath)

    print("\n\nApp ready for display")

# To run the process:
# if __name__ == "__main__":
#     start_new()
