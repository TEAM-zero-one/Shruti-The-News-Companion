from newspaper import Article, build
import requests
from bs4 import BeautifulSoup
from categorize_text import classify_text_domain

# Dictionary to hold processed articles.
# Key: article URL, Value: dict with article details.
visited_links = {}

def categorize_articles(domain_links, category_keywords_dict):
    print("=======================================")
    print("Inside Categorize Articles\n")
    print("All Links:\n", domain_links)

    domain_lists = {
        'India': [],
        'World': [],
        'Business': [],
        'Tech': [],
        'Sports': []
    }

    # for link_list in domain_links:
    for url in domain_links:
        response = requests.get(url)
        web_page = response.text
        soup = BeautifulSoup(web_page, 'html.parser')
        news = soup.get_text()
        domain = classify_text_domain(news, category_keywords_dict)
        for article_tag in soup.find_all('a', href=True):
            link = article_tag['href']
            if link.startswith("https://timesofindia.indiatimes.com/") and "articleshow" in link:
                if any(i in url for i in domain_links):
                    if link not in visited_links:
                        try:
                            # domain = classify_text_domain(news, category_keywords_dict)
                            visited_links[link] = domain.capitalize()
                            domain_lists[domain.capitalize()].append(link)  # Append the link to the respective domain list
                            print(link, " is ", domain.capitalize()) 
                        except Exception as e:
                            print(f"Error downloading article from {link}  : {e}\n")
                            continue

    return domain_lists
