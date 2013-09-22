# A Twitter bot that replaces the word "Obama" with the word "Octopus".

import tweepy
import random
import time
from difflib import SequenceMatcher as seqm
import HTMLParser
import logging
import socket

class listener(tweepy.streaming.StreamListener):
    
    def on_status(self, status):
        if selector(status.text):
            message = status.text
            message = message.replace("Obama", "Octopus"). \
                              replace("obama", "octopus"). \
                              replace("OBAMA", "OCTOPUS")
            
            if validtweet(message):
                message = unescape(message)
                
                if not uniquetweet(message, 0.93):
                    return True
                
                print "Tweet " + status.id_str + " from @" + \
                      status.user.screen_name + " at " + \
                      time.strftime("%H:%M") + \
                      ":\n", message.encode("utf8"), "\n"
                
                api.update_status(message)

                t = (random.gauss(15, 4)) * 60
                print "[Wait", int(t/60), "minutes...]\n"
                time.sleep(t)

        return True

    def on_error(self, status):
        print status

def selector(tweet):
    if ((("RT" and "@") not in tweet) and
        ("barack" not in tweet.lower()) and
        ("obama" in tweet.lower())):
        return True
    else:
        return False

def metric(a, b):
    if "t.co" in (a and b):
        return seqm(None, a[:-10], b[:-10]).real_quick_ratio()
    else:
        return 0
        
def uniquetweet(a, d):
    for tweet in api.user_timeline(user):
        if metric(tweet.text, a) > d:
            return False
        else:
            return True

def validtweet(tweet):
    if len(tweet) > 140:
        return False
    elif tweet == (user.status.text or unescape(user.status.text)):
        return False
    else:
        return True

logging.basicConfig(filename = "error.log", 
                    format = "%(asctime)s %(levelname)s: %(message)s")

consumer = open("consumer.txt", "r").read().splitlines()
access = open("access.txt", "r").read().splitlines()

consumer_key = consumer[0]
consumer_secret = consumer[1]

access_token = access[0]
access_token_secret = access[1]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user("octopotus")

_htmlparser = HTMLParser.HTMLParser()
unescape = _htmlparser.unescape

stream = tweepy.Stream(auth, listener())


while True:
    try:
        stream.filter(track = ["obama"], languages = ["en"])
        break
    except socket.error as e:
        # Mitigate [Errno 104] Connection reset by peer (ssl.py)
        s = 60
        print "Socket Exception:", e, "\nReconnecting in", s, "seconds...\n"
        logging.warning(e)
        time.sleep(s)
    except Exception as e:
        s = 60
        print "Other Exception:", e, "\nReconnecting in", s, "seconds...\n"
        logging.error(e)
        time.sleep(s)

