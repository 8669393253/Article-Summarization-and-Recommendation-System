# Article-Summarization-and-Recommendation-System

This Python script allows users to input a URL of an article, which it will summarize using a transformer-based model. Additionally, it searches for similar articles using Google's Custom Search API and provides personalized article recommendations based on the user's reading history.
Certainly! Below is a **detailed README** for your project, with a more comprehensive explanation of each section, including setup instructions, example usage, and function descriptions.

## Overview

The **Article Summarization and Recommendation System** is a Python-based application that:

1. **Summarizes articles** from URLs provided by the user using Hugging Face's transformer-based model.
2. **Searches for similar articles** via the Google Custom Search API, using the summary of the article as the search query.
3. **Provides personalized recommendations** of articles based on the user's reading history by leveraging text similarity (TF-IDF and cosine similarity).

This project is designed to help users discover relevant content by summarizing articles and recommending similar articles based on their previous reading behavior.

## Features

- **Article Summarization**:  
  Summarize any article from a URL using the Hugging Face transformer-based model, which extracts the key points of the article.

- **Google Custom Search**:  
  Perform a Google search to find similar articles based on the summary of the article provided by the user. The search results exclude previously viewed articles.

- **User History Tracking**:  
  Maintain a record of previously viewed articles and their summaries in a local JSON file (`user_history.json`), enabling the system to track user preferences.

- **Personalized Recommendations**:  
  Recommend articles similar to the ones the user has read before, based on the similarity of their summaries using **TF-IDF** (Term Frequency-Inverse Document Frequency) and **Cosine Similarity**.


## Requirements

### Python Libraries

This script requires several Python libraries, which you can install using `pip`. You can use the following command to install the required dependencies:

pip install transformers requests_html beautifulsoup4 google-api-python-client scikit-learn


### Google API Setup

To use the **Google Custom Search API**, you will need to follow these steps:

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.

2. **Enable the Google Custom Search API**:
   - In your Google Cloud Console, navigate to the **API Library** and search for **Custom Search API**.
   - Enable the API for your project.

3. **Create an API Key**:
   - Navigate to the **Credentials** section of the Google Cloud Console.
   - Create an **API Key** for your project. This will be used for authenticating requests to the Google API.

4. **Create a Custom Search Engine (CSE)**:
   - Go to the [Google Custom Search Engine page](https://cse.google.com/cse/) and create a new search engine.
   - Set it up to search the entire web (or specific sites if needed).
   - Obtain the **CSE ID** from the Control Panel.

Once you have your **API Key** and **CSE ID**, you can use them in the script.


## Setup

1. **Download the Script**:  
   Clone or download this repository to your local machine.

2. **Create a Configuration File** (Optional):  
   If you want to store your API key and CSE ID separately, you can create a configuration file (`config.json`) like this:

   ```json
   {
     "api_key": "YOUR_GOOGLE_API_KEY",
     "cse_id": "YOUR_CUSTOM_SEARCH_ENGINE_ID"
   }
   ```

3. **Place the API Credentials**:  
   In the script, replace the `API_KEY` and `CSE_ID` values with the credentials you obtained from the Google Cloud Console.


## How to Use

### Step 1: Run the Script

After setting up your environment and entering your credentials, run the script:

python article_recommendation.py


### Step 2: Provide the Article URL

The script will prompt you to enter the **URL of an article** you'd like to summarize:

Enter the URL of the article: https://example.com/some-article


### Step 3: Article Summary

The script will fetch the content of the article from the URL, generate a summary using Hugging Face's transformer model, and display it.

Example output:

Article Summary:
This is the summarized text of the article that contains the key points and a condensed version of the content.


### Step 4: Add to User History

The script will save the article URL and summary to a local file (`user_history.json`). If you provide the same URL again, the script will recognize it as part of your history.

### Step 5: Google Search for Similar Articles

The script will use the generated summary to perform a Google Custom Search for articles related to the summary and display the search results.

Example output:

Similar Articles:
1. Article Title: https://example.com/similar-article-1
2. Article Title: https://example.com/similar-article-2


### Step 6: Personalized Recommendations

The script will recommend articles based on the user's reading history. It will use **TF-IDF** and **Cosine Similarity** to identify articles in the history that are most similar to the one just summarized.

Example output:

Personalized Article Recommendations:
Based on the article: https://example.com/some-article
  1. https://example.com/another-article
  2. https://example.com/yet-another-article


## File Structure

- **`article_recommendation.py`**:  
  The main Python script where the entire functionality resides. This script:
  - Fetches the article content.
  - Summarizes the article.
  - Searches for similar articles via Google Custom Search.
  - Provides recommendations based on past articles.

- **`user_history.json`**:  
  A JSON file that tracks the user’s article history and summaries. It is created automatically after the first run and updated with each new article.

- **`requirements.txt`**:  
  A text file containing the list of Python dependencies, which can be installed using `pip`:

  pip install -r requirements.txt

## Functions Overview

1. **`load_user_history()`**:  
   Loads the user’s reading history from the `user_history.json` file. If the file doesn’t exist, it initializes the history as an empty list.

2. **`save_user_history()`**:  
   Saves the user’s article history and summaries to `user_history.json`.

3. **`fetch_article_text(url)`**:  
   Fetches the article content from a given URL using the `requests_html` library and `BeautifulSoup`. Extracts the article text by pulling out `<p>` tags and concatenating them into a single string.

4. **`extract_summary_with_transformers(url)`**:  
   Summarizes the article fetched from the provided URL using Hugging Face's transformer-based summarization pipeline. The summary is generated with a max length of 100 characters and a min length of 50 characters.

5. **`google_search(query, api_key, cse_id, num_results)`**:  
   Uses the Google Custom Search API to search for articles related to the summary of the provided article. Returns a list of relevant articles (excluding previously fetched articles).

6. **`add_to_user_history(article_url, article_summary)`**:  
   Adds the article URL and its summary to the user's history, ensuring no duplicates are stored. Saves the updated history in `user_history.json`.

7. **`recommend_articles()`**:  
   Recommends articles based on the similarity of their summaries. Uses **TF-IDF** vectorization and **Cosine Similarity** to calculate the similarity between articles in the user’s history.

## Troubleshooting

- **Google API quota exceeded**:  
  If you hit your Google Custom Search API quota, you may need to wait until the next day or consider upgrading your API usage plan for higher limits.

- **Error fetching article**:  
  Ensure that the provided article URL is correct and accessible. Some websites may block scraping attempts, which could lead to failure in fetching content.

- **No Recommendations Available**:  
  If you are a new user and have not viewed enough articles, personalized recommendations may not be available. You’ll need to read more articles for the system to generate relevant recommendations.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
