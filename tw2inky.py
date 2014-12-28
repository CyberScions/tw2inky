#!/usr/bin/python

import re, requests, urllib2
from bs4 import BeautifulSoup
from twython import Twython

#enter your twitter app details here
APP_KEY=''
APP_SECRET=''
OAUTH_TOKEN=''
OAUTH_TOKEN_SECRET=''

#enter twitter hashtags to search for
SEARCH_HASH = ['#BIGDATA', '#DEVOPS', '#CLOUD']

#sets the maximum number of twitter search results
SEARCH_LIMIT = '500'

class HashTagTweets(object):

	def __init__(self, tweet=None):
		self.tweet = tweet
		self.twitter = Twython(APP_KEY, APP_SECRET,
				OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	def queryHashtag(self, hashtag=None, count=SEARCH_LIMIT):
        	if not hashtag:
                	return None
        	tweets = self.twitter.search( q=( ('%s') % hashtag ), count=('%s' % count) )
        	return tweets['statuses']


	def getText(self):
		if not self.tweet:
			return None
		text = None
		try:
			text = self.tweet['text']
		except Exception as e:
			raise
		finally:
			return text

	def getScreenName(self):
		if not self.tweet:
			return None
		screen_name = self.tweet['user']['screen_name']
		return screen_name

        def getUserExpandedURL(self):
                if not self.tweet:
                        return None
                user_expanded_url = self.tweet['user']['entities']['url']['urls'][0]['expanded_url']
                return user_expanded_url

        def getPostedDate(self):
                if not self.tweet:
                        return None
                date = self.tweet['created_at']
                parts = date.split(' ')
                date = parts[0]+' '+parts[1]+' '+parts[2]+' '+parts[3]+' '+parts[5]
                return date

	def nicePrint(self):
		if not self.tweet:
			return None
		return ('%s @%s %s') % (self.getPostedDate(), 
			self.getScreenName() , repr(self.getText()) )

def isLinkedInURL(url=None):
        homepage = url
        if not homepage:
                return None
        search = re.compile(r"linkedin")
        found = search.findall(homepage)
        if found:
                return homepage
        return None


def scrapeLinkedInProfile(url=None):
        try:
		#header can be customized
		HEADER = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1;Trident/4.0; \
			SearchToolbar 1.2; BTRS103184; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; \
			.NET CLR 3.5.30729; InfoPath.1; AskTB5.6)"
            	request = urllib2.Request(url)
                request.add_header('User-Agent', HEADER)
                response = urllib2.urlopen(request)
                redditHtml = response.read()
                response.close()
                soup = BeautifulSoup(redditHtml)
        except Exception as e:
                raise

        name = soup.find("span", {'class': 'full-name'}).contents[0]
        headline = soup.find("div", {'id': 'headline'}).p.contents[0]
        locality = soup.find("span", {'class': 'locality'}).contents[0]
        industry = soup.find("dd", {'class': 'industry'}).contents[0]
        experience = soup.find("div", {'class': 'editable-item section-item current-position'})
	position = None
	employer = None
	try:
	        position = experience.header.h4.contents[0]
        	employer = experience.header.find("a", {'dir':'auto'}).contents[0]
	except:
		pass
        return {'name': name, 'headline': headline, 'locality': locality,
                'industry': industry, 'position': position, 'employer': employer}

def printLinkedInProfile(profile=None):
	if not profile:
		return None
	print 'Name: %s' % profile['name']
	print 'Headline: %s' % profile['headline']
	print 'Location: %s' % profile['locality']
	print 'Industry: %s' % profile['industry']
	print 'Position: %s' % profile['position']
	print 'Employer: %s' % profile['employer']


if __name__ == '__main__':
        try:
        	words = SEARCH_HASH
		H = HashTagTweets()
		for word in words:
			print "tw2inky: searching tweets for %s\n" % word
			statuses = H.queryHashtag(hashtag=word, count=SEARCH_LIMIT)
			for tweet in statuses:
				T = HashTagTweets(tweet=tweet)
				try:			
					homepage = T.getUserExpandedURL()
					if isLinkedInURL(url=homepage):
						try:
							print T.nicePrint()
							profile = scrapeLinkedInProfile(url=homepage)
							printLinkedInProfile(profile=profile)
							print
						except Exception as e:
							print 'tw2inky: exception scraping %s\n%s\n' % (homepage, e)
				except:
					#user does not have a homepage
					pass
	except Exception as e:
		print e

	print 'tw2inky: done'
