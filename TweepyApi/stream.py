#!/usr/bin/env python3
import json
import os
import sys
import time
from datetime import datetime
from http.client import IncompleteRead  # Python 3
import logging
from pathlib import Path

from tweepy import OAuthHandler, Stream
import tweepy
# from tweepy.streaming import StreamListener

# import boto3
# from TwitterStreamWithAWS.global_params import kinesis_reddit_stream, kinesis_twitter_stream
#


# # Variables that contains the user credentials to access Twitter API
# CONSUMER_KEY = os.environ.get("TWITTER_API_CONSUMER_KEY")
# CONSUMER_SECRET = os.environ.get("TWITTER_API_CONSUMER_SECRET")
# ACCESS_TOKEN = os.environ.get("TWITTER_API_ACCESS_TOKEN")
# ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_API_ACCESS_TOKEN_SECRET")

CONSUMER_KEY =  "M2dcKnRZGqBWTrPBXeefFHHjZ"
CONSUMER_SECRET = "ktTB1WAJNsZBnKTddPqHMpzczj7ehZigXtN77YIFUdSlZ1EW7v"
ACCESS_TOKEN = "1140239819127365632-gnWnwYZmb6IxKCzOBdXcTWBEc0v1GU"
ACCESS_TOKEN_SECRET = "25wy0DsyD7yfzdKkRdvKTY3ILHbR4fF8t7vnVfRvkknym"

def setup_logger(formatter, name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

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

def get_user_id(screen_name):
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # set access to user's access key and access secret
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # calling the api
    api = tweepy.API(auth)

    # the screen name of the user

    # fetching the user
    user = api.get_user(screen_name=screen_name)

    # fetching the ID
    ID = user.id_str

    # print("The ID of the user is : " + ID)
    return ID


def save_str_data_to_json(data_str, file_path):
    logger.info(type(data_str))
    with open(file_path, 'w') as f:
        json.dump(json.loads(data_str), f)

# class TweetStreamListener(StreamListener):
class TweetStreamListener(Stream):
    print("runing..................")

    def on_data(self, data):
        # print(data)
        logger.info(type(data))
        # data_str = data.decode('utf-8')
        data_str = data.decode()
        # save_str_data_to_json(data_str, 'tmp.json')

    def on_connection_error(self):
            self.disconnect()

    # # on success
    # def on_data(self, data):
    #     print("streaming...")
    #     tweet = json.loads(data)
    #     try:
    #         if "text" in tweet.keys():
    #             message = json.dumps(tweet)
    #             message = (
    #                 message + ",\n"
    #             )  # NOTE: not sure what this is used for (could cause potential problem)
    #             print(message)

    #             timestamp_ms = tweet["timestamp_ms"]

    #             kinesis_input_data = bytes(message, "utf-8")

    #             response = kinesis_client.put_record(
    #                 # StreamName=stream_name,
    #                 # StreamName=kinesis_reddit_stream,
    #                 # StreamName=kinesis_twitter_stream,
    #                 StreamName=None,
    #                 Data=kinesis_input_data,
    #                 PartitionKey=timestamp_ms,
    #             )

    #             # print(response)
    #             print(datetime.fromtimestamp(int(timestamp_ms) / 1000.0))
    #             print("--------")

    #     except AttributeError as ae:
    #         print(ae)
    #     except Exception as ex:
    #         print(ex)

    #     print("work fine")
    #     return True

    # # on failure
    # def on_error(self, status):
    #     print(status)
    #     return True  # always runs and do not stop at any error

    # def on_exception(self, exception):
    #     """
    #        I am not sure how this is differnet from on_error.
    #     I also can't find info from Documentaion
    #     """
    #     print(exception)
    #     return


# fill the name of Kinesis data stream you created
# stream_name = "faucovidstream_input"
# stream_name = "faucovidstreamsentiment"


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    logger_name = "data_logger"
    log_time = str(time.time())
    log_file_name = 'logs/{}.log'.format(log_time)
    log_level = logging.DEBUG
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = setup_logger(formatter, logger_name, log_file_name, level=log_level)

    # # create kinesis client connection
    # kinesis_client = boto3.client(
    #     "kinesis",
    #     region_name="us-east-2",  # enter the region
    # )  # fill you aws secret access key

    # create instance of the tweepy tweet stream listener
    # listener = TweetStreamListener()

    # set twitter keys/tokens
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    # stream = Stream(auth, listener)

    # stream = Stream(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = TweetStreamListener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # search twitter for tags or keywords from cli parameters
    query = sys.argv[1:]  # list of CLI arguments
    query_fname = " ".join(query)  # string
    # print(query)
    # stream.filter()
    # stream.filter(track=query)
    while True:
        # stream.filter(track=query)
        # stream.filter(track=['bitcoin'], threaded=False)
        stream.filter(follow=[get_user_id("DocumentingBTC")], threaded=False)
        print('-------')

    # exit()

    # while True:

    #     try:
    #         stream.filter(track=query, stall_warnings=True)

    #     except IncompleteRead as ir:
    #         # reconnect and keep trucking
    #         print("the following error is caught..")
    #         print(ir)

    #         print("reconnect the network..")
    #         listener = TweetStreamListener()
    #         # set twitter keys/tokens
    #         auth = OAuthHandler(consumer_key, consumer_secret)
    #         auth.set_access_token(access_token, access_token_secret)
    #         # create instance of the tweepy stream
    #         stream = Stream(auth, listener)
    #         # search twitter for tags or keywords from cli parameters
    #         query = sys.argv[1:]  # list of CLI arguments
    #         query_fname = " ".join(query)  # string
    #         stream.filter(track=query, stall_warnings=True)

    #     except Exception as ex:
    #         print("the following error is caught..")
    #         print(ex)

    #         print("reconnect the network..")

    #         listener = TweetStreamListener()
    #         # set twitter keys/tokens
    #         auth = OAuthHandler(consumer_key, consumer_secret)
    #         auth.set_access_token(access_token, access_token_secret)
    #         # create instance of the tweepy stream
    #         stream = Stream(auth, listener)
    #         # search twitter for tags or keywords from cli parameters
    #         query = sys.argv[1:]  # list of CLI arguments
    #         query_fname = " ".join(query)  # string
    #         stream.filter(track=query, stall_warnings=True)
