#!/usr/bin/env python3

# importing libraries and packages
import time
import snscrape.modules.twitter as sntwitter
import pandas as pd
from sentiment_analysis.sentiment import sentiment_analysis_polarity
from utils.utils import convert_timestamp_to_date, shift_by_date
import datetime
from pathlib import Path
import re
import debugpy
import json

def get_query_option_1(screen_name, date):
    """
    return list of tweets tweeted by the specified user account.
    """
    query = f'from:{screen_name} since:{date} -filter:retweets -filter:replies'
    return query

def get_query_option_2(text, date):
    """
    return list of tweets containing coins symbol.
    """
    # query = f'$ANKR since:{date} -filter:retweets -filter:replies'
    query = f'{text} since:{date} -filter:retweets -filter:replies'
    return query


class GetQuery:
    def __init__(self):
        pass

    def set_variables(self, user=None, date=None, text=None):
        self.user = user # str
        self.date = date # datetime
        self.text = text # str

    def get_query(self, option=None):
        query = None
        if option == 1:
            assert self.user is not None
            assert self.date is not None
            query = get_query_option_1(self.user, self.date)
        elif option == 2:
            assert self.text is not None
            assert self.date is not None
            query = get_query_option_2(self.text, self.date)
        else:
            raise NotImplementedError()

        assert query is not None
        return query

    def get_query_as_suffix(self, query):
        # query = f'from:{screen_name} since:{date} -filter:retweets -filter:replies'
        return query.replace(":", "=").replace(" ","_")


    # def get_query_option_2(self. option=None):
    #     get_query_option_2(self.text, self.date)


class Report:
    def __init__(self):
        pass
    def report_last_week():
        pass

def is_contained_number(txt):
    for i in range(10):
        if str(i) in txt:
            return True
    return False

def filter_crypto_symbol_from_tweet(txt):
    cryptos = []
    for i in txt.split('$')[1:]:
        tmp  = i.split(' ')
        if len( tmp ) > 0:

            tmp = tmp[0].splitlines()[0]
            # if re.match(r'.*[0-9].*', txt[0]) is None:
            if not is_contained_number(tmp):
                # if '25' in txt[0]:
                #     print(txt[0])
                cryptos.append(tmp)

    return cryptos

class Report:
    def __init__(self):
        pass

    def summary_sentiment_score(self, val_np):
        return val_np.sum()/ val_np.shape[0]

class GetPath():
    """must always return Path object."""

    def get_base_path(self):
        return get_base_path()

    def get_data_path(self):
        return Path(self.get_base_path() / 'SNScrapeAPI/data/')


def get_normlize_score(file_path):
    df = pd.read_csv(file_path)
    total_val = df['Sentiment Score'].sum()
    n_count = df['Sentiment Score'].shape
    return total_val[0] / n_count



def get_base_path():
    return Path('/home/awannaphasch2016/Documents/Working/CryptoExpertIdentification/')

class GetTweets:
    def __init__(self):

        pass

    def save_to_csv(self, tweets_list, columns, save_path):
        print(f'save to {save_path}')
        tweets_df = pd.DataFrame(tweets_list, columns=columns)
        tweets_df.to_csv(save_path)

    def get_tweets(self, query, limit=float("inf")):
        tweets_list = []
        # tweets = {}
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query=query).get_items()):
            if i > limit:
                break

            # tweets['date'] = tweet.date
            # tweets['Datetime'] = tweet.date
            # tweets['Tweet Id'] =  tweet.id
            # tweets['Sentiment Score'] = sentiment_analysis_polarity(tweet.content)
            # tweets['Text'] = tweet.content
            # tweets['Username'] = tweet.user.username
            # print(tweet.user.username, tweet.date)

            print(tweet.date, tweet.content)
            print('----')
            tweets_list.append([tweet.date, tweet.id, sentiment_analysis_polarity(tweet.content), tweet.content, tweet.user.username])

        return tweets_list

    def get_tweets_from_user(self, user, date, save_file=False):
        print(f'get tweets from {user}...')
        # query = get_query_option_1(user, date)
        get_query = GetQuery()
        get_query.set_variables(user=user, date=date)
        query = get_query.get_query(option=1)
        get_tweets = GetTweets()
        df_cols =['Datetime', 'Tweet Id', 'Sentiment Score','Text', 'Username' ]

        tweet_list = get_tweets.get_tweets(query)
        if save_file:
            suffix = get_query.get_query_as_suffix(query)
            get_path = GetPath()
            save_path = str(get_path.get_data_path() / f'{suffix}.csv')
            get_tweets.save_to_csv(tweet_list, df_cols, save_path=save_path)


def get_config():

    base_path = get_base_path()
    config_file = str(get_base_path() / 'SNScrapeAPI/config.json')
    with open(config_file) as json_file:
        config = json.load(json_file)
    return config


def main():
    experts = ['BITCOINTRAPPER', 'j0hnnyw00'] # screen name
    config = get_config()
    today = time.time()
    today_dt = convert_timestamp_to_date(today)
    date = shift_by_date(today_dt, 7)
    get_tweets = GetTweets()

    for i in experts:
        get_tweets.get_tweets_from_user(i, date, save_file=config['save_file'])

if __name__ == "__main__":
    main()

