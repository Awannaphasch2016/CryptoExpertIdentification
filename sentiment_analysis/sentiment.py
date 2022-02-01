#!/usr/bin/env python3

from textblob import TextBlob

def sentiment_analysis_polarity(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    return sentiment_polarity
