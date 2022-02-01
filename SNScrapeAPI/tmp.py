#!/usr/bin/env python3

from sentiment_analysis.sentiment import sentiment_analysis_polarity
content = 'Even if we capitulate on $BTC & altcoins most won’t be prepared to capitalise. Exchanges will be down. Panic will be real. Transfer times will be horrendous. You’ll get signed out your accounts. It’s all bollocks. Trust me.'
# content = 'bad bad bad bad'
# content = 'good good good'
print(sentiment_analysis_polarity(content))
