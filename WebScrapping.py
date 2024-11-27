import json
from transformers import pipeline
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

# Your Google API credentials (replace with your own)
API_KEY = 'xxxxxxxxxxxxxxxxxx'  # Replace with your API key
CSE_ID = 'xxxxxxxxxxxxxxxxxxx'  # Replace with your CSE ID

# A set to track already fetched articles by URL
fetched_articles = set()
# A list to store the user's article history (URL and summary)
user_history = []

# Initialize a TfidfVectorizer for similarity calculation
vectorizer = TfidfVectorizer(stop_words='english')

def load_user_history():
    """Load user history from a file."""
    global user_history
    try:
        with open('user_history.json', 'r') as f:
            user_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        user_history = []  # If file doesn't exist or is empty, start with an empty list

def save_user_history():
    """Save user history to a file."""
    with open('user_history.json', 'w') as f:
        json.dump(user_history, f, indent=4)  # Use indent for better readability

def fetch_article_text(url):
    """Fetch article text from a given URL."""
    session = HTMLSession()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        
        article_text = ' '.join([para.get_text() for para in paragraphs])
        return article_text
    else:
        raise Exception(f"Failed to retrieve the article, status code: {response.status_code}")

def extract_summary_with_transformers(url):
    """Fetch the article and summarize it using a transformer model."""
    try:
        article_text = fetch_article_text(url)
        summary = summarizer(article_text, max_length=100, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"An error occurred: {str(e)}"

def google_search(query, api_key, cse_id, num_results=10):
    """Function to perform Google search using Google API."""
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
    
    search_results = []
    for item in res.get('items', []):
        if item['link'] not in fetched_articles and item['link'].startswith("http"):
            search_results.append({'title': item['title'], 'link': item['link']})
            fetched_articles.add(item['link'])
    
    return search_results

def add_to_user_history(article_url, article_summary):
    """Add the article and its summary to the user history."""
    # Check if the article URL already exists in history
    for entry in user_history:
        if entry['url'] == article_url:
            print(f"Article already exists in history: {article_url}")
            return  # Don't add the duplicate article
    
    # Add new article to history if it's not already there
    user_history.append({'url': article_url, 'summary': article_summary})
    print(f"Article added to history: {article_url}")
    
    # Save updated user history to the file
    save_user_history()

def recommend_articles():
    """Provide article recommendations based on the user's history."""
    if len(user_history) < 2:
        return "Not enough articles in the history to recommend."
    
    summaries = [entry['summary'] for entry in user_history]
    tfidf_matrix = vectorizer.fit_transform(summaries)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    recommendations = []
    for idx, entry in enumerate(user_history):
        similar_indices = similarity_matrix[idx].argsort()[-4:-1][::-1]  # Top 3 most similar articles
        similar_articles = [(user_history[i]['url'], user_history[i]['summary']) for i in similar_indices]
        recommendations.append({'current_article': entry['url'], 'similar_articles': similar_articles})
    
    return recommendations

# Main execution
def main():
    # Load history from the file
    load_user_history()
    
    # Get URL input from the user
    url = input("Enter the URL of the article: ")
    
    # Step 1: Summarize the provided article
    summary = extract_summary_with_transformers(url)
    print("\nArticle Summary:")
    print(summary)

    # Add the article and summary to user history
    add_to_user_history(url, summary)

    # Step 2: Search for similar articles based on the summary
    search_query = summary  # Using the extracted summary as the search query
    similar_articles = google_search(search_query, API_KEY, CSE_ID, num_results=10)

    # Print similar articles
    print("\nSimilar Articles:")
    for idx, article in enumerate(similar_articles, 1):
        print(f"{idx}. {article['title']}: {article['link']}")

    # Step 3: Provide article recommendations based on user history
    print("\nPersonalized Article Recommendations:")
    recommendations = recommend_articles()
    if isinstance(recommendations, str):
        print(recommendations)  # If not enough articles for recommendations
    else:
        for rec in recommendations:
            print(f"Based on the article: {rec['current_article']}")
            for idx, (url, _) in enumerate(rec['similar_articles'], 1):
                print(f"  {idx}. {url}")

# Run the main function
if __name__ == "__main__":
    main()

