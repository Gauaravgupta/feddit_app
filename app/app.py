#!/usr/bin/env python
# coding: utf-8

# In[8]:


from flask import Flask, jsonify, request
from textblob import TextBlob
import requests

app = Flask(__name__)

# Feddit API base URL
FEDDIT_BASE_URL = "http://0.0.0.0:8080"

# Function to fetch comments from Feddit
def fetch_comments(subfeddit):
    response = requests.get(f"http://0.0.0.0:8080/{subfeddit}/comments")
    if response.status_code == 200:
        return response.json()['comments']
    else:
        return []

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Endpoint to fetch sentiment analyzed comments
@app.route('/sentiment/comments', methods=['GET'])
def get_sentiment_analyzed_comments():
    subfeddit=request.args.get('subfeddit','')
    comments = fetch_comments(subfeddit)


    # Sort comments by sentiment score (polarity)
    sort_by_sentiment = request.args.get('sort_by_sentiment')
    if sort_by_sentiment == 'true':
        comments.sort(key=lambda x: TextBlob(x['text']).sentiment.polarity, reverse=True)

    # Limit to 25 most recent comments
    recent_comments = comments[:25]

    # Analyze sentiment for each comment
    analyzed_comments = []
    for comment in recent_comments:
        sentiment = analyze_sentiment(comment['text'])
        analyzed_comment = {
            'comment_id': comment['id'],
            'text': comment['text'],
            'polarity_score': TextBlob(comment['text']).sentiment.polarity,
            'sentiment': sentiment
        }
        analyzed_comments.append(analyzed_comment)

    return jsonify({'comments': analyzed_comments})

if __name__ == '__main__':
    app.run(debug=False)


# In[ ]:




