#!/usr/bin/python

import os, re, sys, urllib2

try:
	import requests
	from bs4 import BeautifulSoup
	from twython import Twython
	import ConfigParser
except Exception as e:
        print '[error] %s' % e
        print 'Please resolve import dependencies.'
        sys.exit(1)


class HashTagTweets(object):

	def __init__(self, tweet=None, config=None):
		self.tweet = tweet
		self.config = config
		self.max_results = '200'
		if self.config:
			self.max_results = self.config.max_results
			self.twitter = Twython(self.config.app_key, self.config.app_secret,
				self.config.oauth_token, self.config.oauth_token_secret)

	def queryHashtag(self, hashtag=None):
        	if not hashtag:
                	return None
        	tweets = self.twitter.search( q=( ('%s') % hashtag ), count=('%s' % self.max_results) )
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
                html = response.read()
                response.close()
                soup = BeautifulSoup(html)
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
                'industry': industry, 'position': position, 'employer': employer, 'url': url}

def printLinkedInProfile(profile=None):
	if not profile:
		return None
	print 'Name: %s' % profile['name']
	print 'Headline: %s' % profile['headline']
	print 'Location: %s' % profile['locality']
	print 'Industry: %s' % profile['industry']
	print 'Position: %s' % profile['position']
	print 'Employer: %s' % profile['employer']
	print 'URL: %s' % profile['url']


class tw2inkySetUp:
        def __init__(self):
                self.status = 0
                self.path = '/etc/tw2inky'
                try:
                    	os.makedirs(self.path)
                except OSError as e:
                        pass
                finally:
                        self.path = '%s/tw2inky.conf' % self.path
                        try:
                            	f = open(self.path, 'r').close()
                                print 'Found config file %s' % self.path
                                self.status = 0
                        except Exception as e:
                                print '[warning] %s' % e
				print 'Creating new config at /etc/tw2inky/tw2inky.conf'
                                f =  open(self.path, 'w')
                                f.write('[KEYS]\n')
                                f.write('APP_KEY=\n')
                                f.write('APP_SECRET=\n')
                                f.write('OAUTH_TOKEN=\n')
                                f.write('OAUTH_TOKEN_SECRET=\n\n')
                                f.write('[SEARCH]\n')
                                f.write('max_results=500\n')
                                f.write('include_twitter_hash=#bigdata, #cloudcomputing, #devops\n')
                                f.write('include_linkedin_locality=San Francisco, Los Angelas\n')
                                f.write('include_linkedin_position=Manager, Director, CIO, CTO, CSO, CEO, Founder, Owner, President, Partner, VP\n')
                                f.write('exclude_twitter_hash=#porn\n')
                                f.write('exclude_linkedin_company=IBM, HP\n\n')
                                f.close()
                                self.status = 1
                        if not self.parseConfig():
                                self.status = 1
                        else:
                             	self.status = 0

        def parseConfig(self):
                configParser = ConfigParser.RawConfigParser()
                configFilePath = (r'%s') % self.path
                configParser.read(configFilePath)
                self.app_key = str(configParser.get('KEYS', 'APP_KEY'))
                self.app_secret = str(configParser.get('KEYS', 'APP_SECRET'))
                self.oauth_token = str(configParser.get('KEYS', 'OAUTH_TOKEN'))
                self.oauth_token_secret = str(configParser.get('KEYS', 'OAUTH_TOKEN_SECRET'))
                self.include_twitter_hash = configParser.get('SEARCH', 'include_twitter_hash').split(',')
                self.include_linkedin_locality = configParser.get('SEARCH', 'include_linkedin_locality').split(',')
                self.include_linkedin_company = configParser.get('SEARCH', 'include_linkedin_position').split(',')
                self.exclude_twitter_hash = configParser.get('SEARCH', 'exclude_twitter_hash').split(',')
                self.exclude_linkedin_company = configParser.get('SEARCH', 'exclude_linkedin_company').split(',')
		self.include_linkedin_position = configParser.get('SEARCH', 'include_linkedin_position').split(',')
                self.max_results = str(configParser.get('SEARCH', 'max_results'))
                if not (len(self.app_key) or len(self.app_secret) or len(self.oauth_token) or len(self.oauth_token_secret)):
                        return False
                return True


if __name__ == '__main__':

        config = tw2inkySetUp()
        if config.status:
                print 'Setup config complete, please update app keys and search criteria.'
		sys.exit(0)
        else:
             	print 'Setup config complete, detected app keys and search criteria.'

        try:
        	words = config.include_twitter_hash
		exclude = config.exclude_twitter_hash

		H = HashTagTweets(config=config)
		for word in words:
			print "\nSearching tweets for %s\n" % word
			statuses = H.queryHashtag(hashtag=word)
			for tweet in statuses:
				T = HashTagTweets(tweet=tweet)

				# dont include tweets with exclude hashtags
				excludeTweet = False
				for e in exclude:
					if T.getText().lower().find(e.lower()) >=0:
						excludeTweet = True
				if excludeTweet:
					continue

				try:			
					homepage = T.getUserExpandedURL()
					if isLinkedInURL(url=homepage):
						try:
							profile = scrapeLinkedInProfile(url=homepage)

							# include only if profile matches positions
							if not profile['position']:
								continue
							includeProfile = False
							for position in config.include_linkedin_position:
								if includeProfile:
									continue
								positionParts = profile['position'].split()
								for pos in positionParts:
									#print position, pos
									if includeProfile:
										continue
									if pos.lower().find(position.lower().strip()) >= 0:
										includeProfile = True
							if not includeProfile:
								continue

							print T.nicePrint()
							printLinkedInProfile(profile=profile)
							print
						except Exception as e:
							pass
							#print '[error] %s' % e
							#print 'Exception scraping %s\n%s\n' % (homepage, e)
				except:
					#user does not have a homepage
					pass
	except Exception as e:
		print '[error] %s' % e

	print 'done!'
