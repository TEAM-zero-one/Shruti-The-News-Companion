from news_summarizer import text_summarizer
from collect import categorize_articles
from pathlib import Path

# Function to process already-downloaded articles, generate summaries, and save to CSV.
def process_and_save_articles(articles_data, csv_file):
    article_links = []
    article_text = []
    article_summary = []
    article_titles = []
    article_img = []
    total = 0

    for article in articles_data:
        try:
            text = article["text"]
            # Generate summary using gensum's text_summarizer.
            summary = text_summarizer(text)
            
            # Validate fields (here you can add further validations if needed).
            if all([article["url"], text, summary, article["top_image"]]) and article["title"] not in article_titles:
                article_links.append(article["url"])
                article_text.append(text)
                article_titles.append(article["title"])
                article_img.append(article["top_image"])
                article_summary.append(summary)
                total += 1
                print(f"Collected {total}: {article['title']}")

            if total >= 20:  # Stop after collecting 20 articles per category.
                break

        except Exception as e:
            print(f"Error processing article {article['url']}: {e}")
            continue


    # Create a DataFrame and save the data to CSV.
    df = pd.DataFrame({
        'Article Title': article_titles,
        'Article Link': article_links,
        'Article Text': article_text,
        'Article Summary': article_summary,
        'Article Image': article_img
    })
    df.to_csv(csv_file, index=False, encoding='utf-8')
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
    "https://timesofindia.indiatimes.com/world",
    "https://timesofindia.indiatimes.com/business",
    "https://timesofindia.indiatimes.com/technology",
    "https://timesofindia.indiatimes.com/sports"
]

def start_new():
    # Getting the categorized and processed articles 
    domain_lists = categorize_articles(all_links)
    
    # For each category, process the articles and save to CSV.
    for category, filepath in info_files.items():
        if category in domain_lists:
            process_and_save_articles(domain_lists[category], filepath)

    print("\n\nApp ready for display")
