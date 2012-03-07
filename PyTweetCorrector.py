# -*- coding: utf-8 -*-
import os
import re
import GoogleTranslateApi

gta=GoogleTranslateApi.GoogleTranslateApi()
recordedTweetFile=open("twitter_data.txt","r")

turkishTweetFile=open("turkish_twitter_data.txt","w")
nonturkishTweetFile=open("nonturkish_twitter_data.txt","w")

for line in recordedTweetFile:
	line=re.sub(" +"," ",line)
	line=line.strip()
	if line=='' or line=='\n':
		continue		
	changedLine=line.replace("\'","&#39;").replace("\"","&quot;")
	changedLine=re.sub("http:[a-zA-Z0-9/\.]*","",changedLine)

	fails=True #Eğer bağlantı problemi oluşursa, bu değişken True olarak değiştirilir
	counter=0 #Yaşanan bağlantı problemi sayısını tutar
	while fails and counter<3:
		try:
			if counter>0:
				gta=GoogleTranslateApi.GoogleTranslateApi()

			if gta.isTurkish(changedLine):
				turkishTweetFile.write(line+"\n")
			else:
				nonturkishTweetFile.write(line+"\n")
			fails=False
			counter=0
		except Exception,e:
			print "Error-"+str(counter)+": "+line
			fails=True
			counter+=1
	
	if counter==3:
		nonturkishTweetFile.write(line+"\n")
		counter=0
		fails=False

turkishTweetFile.close()
nonturkishTweetFile.close()
recordedTweetFile.close()
