#!/usr/bin/env python3
from datetime import datetime, timedelta
import time

def clean_datetime_str(val):
    return val.replace(" ","_")

def shift_by_date(date_now, n_days):
    """
    date_now is datetime object

    return
    -----
    datetime object
    """
    # now = convert_timestamp_to_date(timestamp)
    delta = timedelta(n_days)

    # return (date_now - delta).date()
    return (date_now - delta)

def convert_timestamp_to_date(timestamp):
    """
    timestamp is time.time()
    """
    assert isinstance(timestamp,float)
    dt_object = datetime.fromtimestamp(timestamp)
    # return dir(dt_object)
    return dt_object

if __name__ == "__main__":

    # timestamp = 1545730073
    # dt_object = datetime.fromtimestamp(timestamp)
    # print("dt_object =", dt_object)
    # # print("type(dt_object) =", type(dt_object))

    # a_date = datetime.date(2015, 10, 10)
    # days = datetime. timedelta(5)
    # new_date = a_date - days
    # print(new_date)
    today = time.time()
    print(shift_by_date(today, 7))
