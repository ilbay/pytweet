# -*- coding: utf-8 -*-
import tweepy
import os

class StreamListener(tweepy.StreamListener):
	#status_wrapper=TextWrapper(width=60,initial_indent='	',subsequent_indent='	')
	def __init__(self):
		super(StreamListener,self).__init__()
		if os.path.exists('twitter_data.txt'):
			self.twitter_file=open('twitter_data.txt','a')
		else:
			self.twitter_file=open('twitter_data.txt','w')
		self.retweet_list=[]
		self.tweet_counter=0
	def on_status(self,status):
		try:
			if self.tweet_counter>100:
				self.twitter_file.close()
				self.twitter_file.open('twitter_data.txt','a')
				self.tweet_counter=0
			if status.text.find('RT ')==0:
				if status.text not in self.retweet_list:
					self.twitter_file.write(status.text+"\n")
					self.retweet_list.append(status.text)
					self.tweet_counter+=1
			else:
				self.twitter_file.write(status.text+"\n")
				self.tweet_counter+=1
			print status.text
		except Exception,e:
			pass

while(True):
	authl=tweepy.auth.OAuthHandler('wGMTS455F4tFBthsY4WlQ','Mk6o7uq94ZrIdG4OQb4r5KdwznIjykCw96yJHpk')
	authl.set_access_token('246462414-qJ6okCAz9db26lft1D2aFtTV6evEYD7L3l3ebp6J','fp2WhOiTRjoEUQigtp5FAfed5hRXmbvE9fpFokWFTz0')

	streamListener=StreamListener()
	try:
		streamer=tweepy.Stream(auth=authl,listener=streamListener,timeout=1)
	except Exception,e:
		continue
	terms=['başka','geçen','gün','okul','arkadaş','dost','aşk','oha','sarkı','şarkı','arkadas','çok','için','içki','rakı','bir','galatasaray','fener','fenerbahçe','fenev','besiktas','beşiktaş','şike','fenerbahce','söz','fetih','sinema','diye','kadar','hoca','evet','hukumet','erkek','kadin','kadın','#benimzaafim','#olmakistiyorum']
	try:
		streamer.filter(None,terms)
	except Exception,e:
		continue
