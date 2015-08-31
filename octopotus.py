#!/usr/bin/env python3
# A Twitter bot that replaces the word "Obama" with the word "Octopus".

import tweepy # v3.3.0
from time import sleep, strftime
import socket
import creds
from html import unescape

auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
auth.set_access_token(creds.access_token, creds.access_token_secret)
api = tweepy.API(auth)
user = api.me()

class listener(tweepy.streaming.StreamListener):
    def on_status(self, status):
        message = unescape(octofy(status.text))
        if willtweet(message):
            print("Tweet", status.id_str,
                "from @" + status.user.screen_name,
                "at", strftime("%Y.%m.%d %H:%M") + ":")
            print(message)
            api.update_status(message)
            sleep(60 * 60)
        return True

def octofy(tweet):
    tweet = tweet.replace("Obama", "Octopus"). \
                  replace("obama", "octopus"). \
                  replace("OBAMA", "OCTOPUS"). \
                  replace("POTUS", "OCTOPOTUS")
    return tweet

def willtweet(tweet):
    if ((len(tweet) <= 140) and
        (("RT" and "@") not in tweet) and
        ("barack" not in tweet.lower()) and
        ("octopus" in tweet.lower()) and
        ("t.co" not in tweet) and
        (tweet != user.status.text)):
        return True
    else:
        return False

while True:
    t = 60
    try:
        stream = tweepy.Stream(auth, listener())
        stream.filter(track = ["obama"], languages = ["en"])
        break
    except Exception as e:
        print(e, "\nReconnecting in", t, "seconds...")
        sleep(t)

