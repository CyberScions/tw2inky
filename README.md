tw2inky
=======

Description: Maps tweets to linkedin profiles

Requires:

Python libraries installed: BeautifulSoup4, Requests, Twython

Twitter account to obtain application keys and Oauth tokens

Usage:

1) Run script to generate nececcary setup and config file

2) Enter Twitter apps keys in config /etc/tw2inky/tw2inky.conf

3) Update default config file with search criteria (see below)

4) Execute the script: ./tw2inky.py


Example Config (keys not shown):

[KEYS]
APP_KEY=''
APP_SECRET=''
OAUTH_TOKEN=''
OAUTH_TOKEN_SECRET=''

[SEARCH]
max_results=500
include_twitter_hash=#bigdata, #cloudcomputing, #devops, #PaaS, #IaaS, #AWS
include_linkedin_locality=San Francisco, Los Angelas
include_linkedin_position=Manager, Director, CEO, CIO, CTO, VP
exclude_twitter_hash=#porn
exclude_linkedin_company=IBM, HP
