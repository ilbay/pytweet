# -*- coding: utf-8 -*-
import mechanize
import cookielib
import re

class GoogleTranslateApi:
	def __init__(self):
		self.url="http://translate.google.com"
		self.seperators=("<span title=\"","\" onmouseover=\"this.style.backgroundColor='#ebeff9'\" onmouseout=\"this.style.backgroundColor='#fff'\">")
		self.form="text_form"
		self.browser=mechanize.Browser()
		
		#Firefox taklit ediliyor
		cookie=cookielib.LWPCookieJar()
		self.browser.set_cookiejar(cookie)
		
		self.browser.set_handle_equiv(True)
		self.browser.set_handle_gzip(True)
		self.browser.set_handle_redirect(True)
		self.browser.set_handle_referer(True)
		self.browser.set_handle_robots(False)

		self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; tr-TR; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

		self.browser.open(self.url)

	def isTurkish(self,sentence):
		correctedSentence=re.sub("[.!?&;]","",sentence) #.!? karakterleri siliniyor
		correctedSentence=re.sub(" +"," ",correctedSentence)
		correctedSentence=correctedSentence.strip()

		#Cümlenin çevirisi Google'ın önerdiği dilde çevirisi yapılıyor.
		self.browser.select_form(self.form)
		self.browser["sl"]=["auto"]
		self.browser["text"]=correctedSentence
		self.browser.submit()

		text=self.browser.response().read()
		seperator=self.seperators[0]+correctedSentence+self.seperators[1]
		start=text.find(seperator)
		#m=re.search(seperator,text,flags=re.IGNORECASE)
		if start==-1:
			#raise Exception("An unexpected error occured in auto translation for this sentence: "+sentence)
			print "An unexpected error occured in auto translation for this sentence: "+sentence
			return False

		#start=m.span()[0]
		text=text[start+len(seperator):]
		autoTranslatedSentence=text.split('</span>')[0]

		#Cümlenin Türkçe çevirisi yapılıyor
		self.browser.select_form(self.form)
		self.browser["sl"]=["tr"]
		self.browser["text"]=correctedSentence
		self.browser.submit()

		text=self.browser.response().read()
		seperator=self.seperators[0]+correctedSentence+self.seperators[1]
		start=text.find(seperator)		
		#m=re.search(seperator,text,flags=re.IGNORECASE)
		if start==-1:
			#raise Exception("An unexpected error occured in Turkish translation for this sentence: "+sentence)
			print "An unexpected error occured in Turkish translation for this sentence: "+sentence
			return False

		#start=m.span()[0]
		text=text[start+len(seperator):]
		translatedSentence=text.split('</span>')[0]

		#Eğer cümlenin hem Google'ın önerdiği dilde hem de Türkçede çevirisi aynı oluyorsa cümle Türkçedir
		if translatedSentence!=autoTranslatedSentence:
			return False
		return True
"""
gt=GoogleTranslateApi()
#Test
print gt.isTurkish("ich liebe dich")
print gt.isTurkish("seni seviyorum")
print gt.isTurkish("elma, karpuz, kiraz")
print gt.isTurkish("sarışın")

print "***************************"
print gt.isTurkish("@decupe Cok deprese oldugunu soylemek gerek. Bir film festivalinde acilis filmi olarak gosterildiginde salon birer birer terkedilmis...")
print gt.isTurkish("ti re bir njeriu !!!! beeee &lt;3")
"""
