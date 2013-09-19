# A Twitter bot that replaces the word "Obama" with the word "Octopus".

import tweepy
import random
import time
import HTMLParser

_htmlparser = HTMLParser.HTMLParser()
unescape = _htmlparser.unescape

consumer = open("consumer.txt", "r").read().splitlines()
access = open("access.txt", "r").read().splitlines()

consumer_key = consumer[0]
consumer_secret = consumer[1]

access_token = access[0]
access_token_secret = access[1]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user('octopotus')

class listener(tweepy.streaming.StreamListener):
	
	def on_status(self, status):
		if (("RT" and "@") not in status.text) and ("barack" not in status.text.lower()) and (status.user.screen_name != "octopotus"): 
			message = status.text
			message = message.replace("Obama", "Octopus").replace("obama", "octopus").replace("OBAMA", "OCTOPUS")
			if (len(message) <= 140) and ("octopus" in message.lower()) and (message != (user.status.text or unescape(user.status.text))):
				message = unescape(message)
				api.update_status(message)
				print "Tweet from @" + status.user.screen_name + " at " + time.strftime("%H:%M") + ":\n", message.encode("utf8"), "\n"
				t = (random.gauss(15, 4)) * 60
				print "[Wait", int(t/60), "minutes...]\n"
				time.sleep(t)
		return True

	def on_error(self, status):
		print status

stream = tweepy.Stream(auth, listener())
stream.filter(track=['obama'], languages = ["en"])

