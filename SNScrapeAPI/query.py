#!/usr/bin/env python3
# importing libraries and packages
import time
import snscrape.modules.twitter as sntwitter
import pandas as pd
from sentiment_analysis.sentiment import sentiment_analysis_polarity
from utils.utils import convert_timestamp_to_date, shift_by_date, clean_datetime_str
import datetime
from pathlib import Path
import re
import debugpy
import json
import numpy as np
import argparse
import sys
import logging


def setup_logger(formatter, name, log_file, level=logging.INFO):
    """
    To setup as many loggers as you want

    :NOTE: I am not sure if refactor setup_logger from train_self_supervised into utils will results in information being logged  and stoed correctly. lets run first and I will inspect the results.
    """

    Path(log_file).parent.absolute().mkdir(parents=True,exist_ok=True)

    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    # fh.terminator = ""

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARN)
    ch.setFormatter(formatter)
    # ch.terminator = ""

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

class Logger:
  def set_logger_params(self, formatter, logger_name, log_time, log_relative_path, log_file_name, log_level):
    self.formatter =  formatter
    self.logger_name =  logger_name
    self.log_file_name = log_file_name
    self.log_level = log_level
    self.log_time = log_time
    self.log_relative_path = log_relative_path

  def set_relative_path(self, relative_path):
    self.relative_path = relative_path

  def setup_logger(self):
    self.logger = setup_logger(self.formatter, self.logger_name, self.log_file_name, level=self.log_level)

class ArgsClass:
    def __init__(self, name):
        self.name = name

    def set_args(self):
        parser = self.set_parser(self.name)
        parser = self.original_arguments(parser)
        args = self.prep_args(parser)
        return args

    def set_parser(self, name):
        parser = argparse.ArgumentParser(name)
        return parser

    def original_arguments(self, parser):
        parser.add_argument('--n_days', type=int, help='number of days to be analyze', default=None)
        parser.add_argument('--list_of_coins_to_be_filtered', nargs="+", help='list of coins to be filtered', default=None)
        parser.add_argument('--is_collect_data', action='store_true', help='Do you want to collect data?')
        parser.add_argument('--is_report', action='store_true', help='Do you want to report data?')
        return parser

    def prep_args(self, parser):
        try:
            is_running_test = [True if 'pytest' in i else False for i in sys.argv]
            if any(is_running_test):
                args = parser.parse_args([])
            else:
                args = parser.parse_args()
        except:
            parser.print_help()
            sys.exit(0)
        return args


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
    query = f'${text} since:{date} -filter:retweets -filter:replies'
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
            query = get_query_option_1(self.user, str(self.date))
        elif option == 2:
            assert self.text is not None
            assert self.date is not None
            query = get_query_option_2(self.text, str(self.date))
        else:
            raise NotImplementedError()

        assert query is not None
        return query

    def get_query_as_suffix(self, query, option=None):
        """
        NOTE: name can't have : or = in the name. if there is
        """
        # query = f'from:{screen_name} since:{date} -filter:retweets -filter:replies'
        if option == 1:
            return query.replace(":", "=").replace(" ","_")
        elif option ==2:
            return query.replace(":", "=").replace(" ","_")
        else:
            raise NotImplementedError()

    def get_query_option_2(self, option=None):
        get_query_option_2(self.text, self.date)


def is_contained_number(txt):
    for i in range(10):
        if str(i) in txt:
            return True
    return False

def filter_crypto_symbol_from_tweet(txt):
    """
    :TODO: This has to be replaced with NLP.
    """
    cryptos = []
    for i in txt.split('$')[1:]:
        tmp  = i.strip(' ').split(' ')
        if len(tmp) > 0:
            if len(tmp[0]) > 0:
                tmp = tmp[0].splitlines()[0]
                # if re.match(r'.*[0-9].*', txt[0]) is None:
                if not is_contained_number(tmp):
                    # if '25' in txt[0]:
                    #     print(txt[0])
                    cryptos.append(tmp)

    return cryptos

class Summary:
    def __init__(self):
        pass

    def summarize_sentiment_score(self, val_np):
        return val_np.sum()/ val_np.shape[0]

    def summarize(self, df, option_to_report="sentiment"):
        result = None
        if option_to_report == 'sentiment':
            result = self.summarize_sentiment_score(df['Sentiment Score'].to_numpy())
        else:
            raise NotImplementedError
        assert result is not None
        return result

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

    # def save_to_csv(self, tweets_list, columns, save_path):
    #     print(f'save to {save_path}')
    #     tweets_df = pd.DataFrame(tweets_list, columns=columns)
    #     tweets_df.to_csv(save_path)

    # def save_to_csv(self, tweets_dict, columns, save_path):
    def save_to_csv(self, tweets_df, save_path):
        print(f'save to {save_path}')
        # tweet_df = pd.DataFrame.from_dict(tweets_dict)
        tweets_df.to_csv(save_path)

    def get_tweets(self, query, limit=float("inf")):
        """return dict"""
        # tweets_list = []
        tweets = {
            'Date': [],
            'Datetime': [],
            'Tweet Id': [],
            'Sentiment Score': [],
            'Text': [],
            'Username': []
        }

        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query=query).get_items()):
            if i > limit:
                break

            tweets['Date'].append(tweet.date)
            tweets['Datetime'].append(tweet.date)
            tweets['Tweet Id'].append(tweet.id)
            tweets['Sentiment Score'].append(sentiment_analysis_polarity(tweet.content))
            tweets['Text'].append(tweet.content)
            tweets['Username'].append(tweet.user.username)
            # print(tweet.date, tweet.content)
            # print('----')

            # tweets_list.append([tweet.date, tweet.id, sentiment_analysis_polarity(tweet.content), tweet.content, tweet.user.username])
        # return tweets_list

        return tweets

    def get_tweets_from_text(self, text, date_dt, save_file=False):
        print(f'get tweets from text...')
        # query = get_query_option_1(user, date)
        get_query = GetQuery()
        get_query.set_variables(text=text, date=date_dt.date())
        query = get_query.get_query(option=2)
        get_tweets = GetTweets()
        df_cols =['Datetime', 'Tweet Id', 'Sentiment Score','Text', 'Username' ]

        suffix = get_query.get_query_as_suffix(query, option=2)
        get_path = GetPath()
        # save_path = str(get_path.get_data_path() / f'run-on={clean_datetime_str(str(date_dt))}_{suffix}.csv')
        save_path = str(get_path.get_data_path() / f'run-on={str(date_dt.date())}_text={suffix}.csv')

        # tweet_list = get_tweets.get_tweets(query)
        tweets_dict = get_tweets.get_tweets(query)
        tweet_df = pd.DataFrame.from_dict(tweets_dict)

        if save_file:
            # get_tweets.save_to_csv(tweet_list, df_cols, save_path=save_path)
            # get_tweets.save_to_csv(tweet_dict,save_path=save_path)

            get_tweets.save_to_csv(tweet_df,save_path=save_path)

    def get_tweets_from_user(self, user, date_dt, save_file=False):
        print(f'get tweets from {user}...')
        # query = get_query_option_1(user, date)
        get_query = GetQuery()
        get_query.set_variables(user=user, date=date_dt.date())
        query = get_query.get_query(option=1)
        get_tweets = GetTweets()
        df_cols =['Datetime', 'Tweet Id', 'Sentiment Score','Text', 'Username' ]

        suffix = get_query.get_query_as_suffix(query, option=1)
        get_path = GetPath()
        # save_path = str(get_path.get_data_path() / f'run-on={clean_datetime_str(str(date_dt))}_{suffix}.csv')
        save_path = str(get_path.get_data_path() / f'run-on={str(date_dt.date())}_{suffix}.csv')

        # tweet_list = get_tweets.get_tweets(query)
        tweets_dict = get_tweets.get_tweets(query)
        tweet_df = pd.DataFrame.from_dict(tweets_dict)

        if save_file:
            # get_tweets.save_to_csv(tweet_list, df_cols, save_path=save_path)
            # get_tweets.save_to_csv(tweet_dict,save_path=save_path)

            get_tweets.save_to_csv(tweet_df,save_path=save_path)

        return tweets_dict


def get_config():

    base_path = get_base_path()
    config_file = str(get_base_path() / 'SNScrapeAPI/config.json')
    with open(config_file) as json_file:
        config = json.load(json_file)
    return config

def is_social_media_platform_supported(social_media_platform):
    return social_media_platform in ["Twitter"]


def collect_data(config):
    print('collecting data ...')
    experts = config['is_collect_data']['list_of_experts']
    texts = config['is_collect_data']['list_of_text']
    n_days = config['is_collect_data']['n_days']
    save_file = bool(config['is_collect_data']['save_file'])
    query_option = config['is_collect_data']['query_option']
    list_of_social_media_platform_to_collect_data = config['is_collect_data']['list_of_social_media_platform_to_collect_data']

    for sc in list_of_social_media_platform_to_collect_data:
        assert is_social_media_platform_supported(sc)

    today = time.time()
    today_dt = convert_timestamp_to_date(today)
    date_dt = shift_by_date(today_dt, n_days)
    get_tweets = GetTweets()

    if query_option == 1:
        for i in experts:
            tweets_dict = get_tweets.get_tweets_from_user(i, date_dt, save_file=save_file)

    if query_option == 2:
        for i in texts:
            tweets_dict = get_tweets.get_tweets_from_text(i, date_dt, save_file=save_file)

def get_all_files_in_dir(dir_path):
    # p = Path(r'C:\Users\akrio\Desktop\Test').glob('**/*')
    p = Path(dir_path).glob('**/*')
    files = []
    for x in p:
        if x.is_file():
            dir_path = str(Path(dir_path) / x)
            logging.getLogger('first_logger').info(f'get files from {dir_path}')
            files.append(x)
    # files = [x for x in p if x.is_file()]
    return files

def get_file_from_suffix(files, suffix, option=None):
    """
    I expect this function to  be annoying af later on.
    """

    files_with_suffix = []
    random_text = '18jaskjdlfasdflsdfzzerztz'

    for f in files:
        since = random_text # :NOTE: this could be error prone.
        is_run_on = True if 'run-on' in str(f) else False
        is_user = True if 'from' in str(f) else False #
        is_since = True if 'since' in str(f) else False
        is_text = True if 'text=' in str(f) else False

        run_on = random_text
        user = random_text
        since = random_text
        text = random_text

        if is_run_on:
            run_on = str(f).split('run-on=')[-1].split('_')[0]
        if is_user:
            user = str(f).split('from=')[-1].split('_')[0]
            user_suffix = suffix.split('from=')[-1].split('_')[0]
        if is_since:
            since = str(f).split('since=')[-1].split('_')[0]
            since_suffix = suffix.split('since=')[-1].split('_')[0]
        if is_text:
            text = str(f).split('text=')[-1].split('_')[0]
            text_suffix = suffix.split('text=')[-1].split('_')[0]

        # :NOTE: this could be error prone.
        if option == 1:
            if since in since_suffix and not is_text and user in user_suffix:
                files_with_suffix.append(str(f))
        elif option == 2:
            if since in since_suffix and not is_user and text in text_suffix:
                files_with_suffix.append(str(f))


    return files_with_suffix

def is_filter_twitter_with_config_text(texts, is_filter=False):
    assert isinstance(is_filter, int)
    if is_filter:
        assert isinstance(texts, list)
        assert len(texts) > 0
    return is_filter

def apply_lower_cases(str_list):
    return [i.lower() for i in str_list]

def summarize_data(config):
    print('summarizing data....')
    n_days = config['is_report']['n_days']
    experts = config['is_report']['list_of_experts']
    is_filter_with_text = config['is_report']['is_filter_with_text']
    texts = config['is_report']['list_of_text']
    users = config['is_report']['list_of_experts']
    query_option = config['is_report']['query_option']
    is_expert_opinion = config['is_report']['is_expert_opinion']

    today = time.time()
    today_dt = convert_timestamp_to_date(today)
    date_dt = shift_by_date(today_dt, n_days)

    is_filter_with_text = is_filter_twitter_with_config_text(texts, is_filter_with_text)

    get_query = GetQuery()
    if query_option == 1:
        if is_expert_opinion:
            for user in users:
                get_query.set_variables(user=user, date=date_dt.date())
                query = get_query.get_query(option=query_option)
                suffix = get_query.get_query_as_suffix(query, option=query_option)

                dir_path = get_base_path() / 'SNScrapeAPI/data'
                files = get_all_files_in_dir(str(dir_path))
                files = get_file_from_suffix(files, suffix, option=query_option)

                if len(files) == 0:
                    print('no file with this suffix.')
                    return

                cryptos_sentiment_dict = {}
                for f in files:
                    df = pd.read_csv(str(dir_path / f))
                    summary = Summary()
                    for content, sentiment in zip(df['Text'], df['Sentiment Score']):
                        if is_filter_with_text:
                            cryptos = texts
                        else:
                            cryptos = filter_crypto_symbol_from_tweet(content)
                        if len(cryptos) > 0:
                            cryptos = apply_lower_cases(cryptos)
                        for c in cryptos:
                            cryptos_sentiment_dict.setdefault(c, []).append(sentiment)

                norm_val = []
                for xx in list(cryptos_sentiment_dict.values()):
                    norm_val.append(sum(xx)/len(xx))

                val = np.array(norm_val).reshape(-1)
                val_indx = np.argsort(val)
                val = val[val_indx]
                crypto = np.array(list(cryptos_sentiment_dict.keys())).reshape(-1)[val_indx]

                # df = pd.DataFrame.from_dict(cryptos_sentiment_dict)
                # for c,s in cryptos_sentiment_dict.items():
                for c,s in zip(crypto, val):
                    print(f'(user-crypto)={user}-{c} => {s}')
                #     print(f'(user-crypto)={user}-{c} => {sum(s)/len(s)}')

        else:
            raise NotImplementedError('forget what this do.')
            for user in users:
                get_query.set_variables(user=user, date=date_dt.date())
                query = get_query.get_query(option=query_option)
                suffix = get_query.get_query_as_suffix(query, option=query_option)

                dir_path = get_base_path() / 'SNScrapeAPI/data'
                files = get_all_files_in_dir(str(dir_path))
                files = get_file_from_suffix(files, suffix, option=query_option)

                if len(files) == 0:
                    print('no file with this suffix.')
                    return

                for f in files:
                    df = pd.read_csv(str(dir_path / f))
                    summary = Summary()
                    result = summary.summarize(df,option_to_report="sentiment")
                print(f'user={user} => {result}')

    if query_option == 2:
        for text in texts:
            get_query.set_variables(text=text, date=date_dt.date())
            query = get_query.get_query(option=query_option)
            suffix = get_query.get_query_as_suffix(query, option=query_option)

            dir_path = get_base_path() / 'SNScrapeAPI/data'
            files = get_all_files_in_dir(str(dir_path))
            files = get_file_from_suffix(files, suffix, option=query_option)

            if len(files) == 0:
                print('no file with this suffix.')
                return

            for f in files:
                df = pd.read_csv(str(dir_path / f))
                summary = Summary()
                result = summary.summarize(df,option_to_report="sentiment")
            print(f'text={text} => {result}')


    # summary = Summary()
    # result = summary.summarize(pd.DataFrame.to_dict(tweets_dict), option_to_report="sentiment")
    # print(result)

def convert_list_to_str(list_):
    return " ".join(list_)

def overwrite_config_with_args(config, args):
    ### overwrite config with args is provided
    if args.n_days is not None:
        print(f'overwriting config default of n_days to be {args.n_days}')
        config['is_collect_data']['n_days'] = args.n_days
        config['is_report']['n_days'] = args.n_days
    if args.list_of_coins_to_be_filtered is not None:
        print(f'overwriting config default of list_of_text to be {convert_list_to_str(args.list_of_coins_to_be_filtered)}')
        config['is_collect_data']['n_days'] = args.n_days
        config['is_report']['n_days'] = args.n_days
    if args.is_collect_data:
        config['is_collect_data']['is_flag_active'] = True
    else:
        config['is_collect_data']['is_flag_active'] = False
    if args.is_report:
        config['is_report']['is_flag_active'] = True
    else:
        config['is_report']['is_flag_active'] = False
    return config

def main(args):
    # experts = ['BITCOINTRAPPER', 'j0hnnyw00'] # screen name
    config = get_config()
    config = overwrite_config_with_args(config, args)

    is_collect_data_flag_active = bool(config['is_collect_data']['is_flag_active'])
    is_report_flag_active = bool(config['is_report']['is_flag_active'])

    if is_collect_data_flag_active:
        collect_data(config)
    else:
        logging.getLogger('first_logger').info('skip collecting data...')
        # print('skip collecting data...')
    if is_report_flag_active:
        summarize_data(config)
    else:
        logging.getLogger('first_logger').info('skip report data...')
    print('done')


if __name__ == "__main__":
    args_class = ArgsClass("Args")
    args = args_class.set_args()

    l_1  = Logger()
    logger_name = "first_logger"
    log_time = str(time.time())
    # base_path = '/home/awannaphasch2016/Documents/Working/CryptoExpertIdentification/SNScrapeAPI/'
    base_path = str(Path.cwd())
    # log_relative_path = 'log/'
    log_relative_path = str(Path(base_path) / 'log/')
    log_file_name = str(Path(log_relative_path) / '{}.log'.format(log_time))
    log_level = logging.INFO
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    l_1.set_logger_params(formatter, logger_name, log_time, log_relative_path, log_file_name, log_level)
    l_1.setup_logger()

    l_1.logger.info(args)
    main(args)
