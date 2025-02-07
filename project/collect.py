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



# import requests
# from bs4 import BeautifulSoup
# from newspaper import Article
# from categorize_text import classify_text_domain

# visited_links = {}

# def categorize_articles(all_links):
    
#     session = requests.Session()

#     #Define domain keywords for filtering once
#     domain_keywords = ["/india", "/city", "/elections", "/world", "/business", "/technology", "/sports"]

#     for url in all_links:
#         try:
#             response = session.get(url, timeout=10)
#             response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
#         except Exception as e:
#             print(f"Error fetching {url}: {e}")
#             continue

#         # Parse the fetched HTML content with BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Iterate through all anchor tags with an href attribute
#         for article_tag in soup.find_all('a', href=True):
#             link = article_tag['href']
#             # Filter: Link must be from Times of India, include "articleshow", and contain one of the domain keywords
#             if (link.startswith("https://timesofindia.indiatimes.com/") and 
#                 "articleshow" in link and 
#                 any(keyword in link for keyword in domain_keywords)):
                
#                 # Process the link only if not already visited
#                 if link not in visited_links:
#                     try:
#                         article = Article(link)
#                         article.download()
#                         article.parse()
#                         text = article.text
                        
#                         # Classify the article based on its text    
#                         domain = classify_text_domain(text)
                        
#                         # Save the article details in the visited_links dictionary
#                         visited_links[link] = {
#                             "url": link,
#                             "domain": domain,
#                             "text": text,
#                             "title": article.title,
#                             "top_image": article.top_image
#                         }
                        
#                         print(f"{link} → {domain}")
                    
#                     except Exception as e:
#                         print(f"Error processing article from {link}: {e}")
#                         continue  # Move to the next article

#     # 4. Use dictionary comprehension to initialize the domain lists
#     domain_lists = {category: [] for category in ['India', 'World', 'Business', 'Technology', 'Sports']}
    
#     # Organize the articles based on their classified domain
#     for article_data in visited_links.values():
#         domain = article_data["domain"]
#         if domain in domain_lists:
#             domain_lists[domain].append(article_data)
    
#     return domain_lists
