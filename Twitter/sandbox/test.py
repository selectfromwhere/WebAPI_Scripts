#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-

import json, config
from requests_oauthlib import OAuth1Session

CK = config.Consumer_Key
CS = config.Consumer_Secret
AT = config.Access_Token
ATS = config.Access_Token_Secret

twitter = OAuth1Session(CK, CS, AT, ATS)

def ConsoleInput():
    print("====================")
    print("Home TL  : press '0'")
    print("My TL    : press '1'")
    print("Search TL: press '2'")
    print("====================")

    i = int(input("Which do you want to get?："))
    return i


# https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-home_timeline
def GetHomeTimelines():
    url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
    params = {'count':'5'}
    return twitter.get(url, params=params)


# https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
def GetUserTimelines():
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'count':'5'}
    return twitter.get(url, params=params)


# https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
def SearchTweets(word):
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {
        "q" : word,
        "lang": 'ja',
        "result_type": 'recent',
        "count": '5'
        }
    return twitter.get(url, params=params)


def ConsoleOutput(i,res):
    if res.status_code == 200:
        timelines = json.loads(res.text)
        if i in (0,1):
            for line in timelines:
                print("--------------------------------------------------")
                print("User     : "+line['user']['screen_name']+" ["+line['user']['name']+"]")
                print("Date     : "+line['created_at'])
                print("Location : "+line['user']['location'])
                print("Tweet    : "+line['text'])
        elif i == 2:
            for line in timelines['statuses']:
                print("--------------------------------------------------")
                print("User     : "+line['user']['screen_name']+" ["+line['user']['name']+"]")
                print("Date     : "+line['created_at'])
                print("Location : "+line['user']['location'])
                print("Tweet    : "+line['text'])

    else:
        print("Failed: " + res.status_code)

    # f = open('test.json', 'w')
    # json.dump(json.loads(res.text), f)

def main():
    i = ConsoleInput()

    if i == 0:
        res = GetHomeTimelines()
    elif i == 1:
        res = GetUserTimelines()
    elif i == 2:
        word = input("What do you want to search?：")
        res = SearchTweets(word)

    ConsoleOutput(i,res)

if __name__ == "__main__":
    main()