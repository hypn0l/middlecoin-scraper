#!/usr/bin/env python

"""
Simple python script which scrapes your stats from middlecoin mining pool
and use mtgox to calculate total btc value to your currency of choice. 

please change (HISTORY_URL, WALLET, MTGOX to your needs)

if you like it send a donation
BTC: 1EN27w1mMHp6mTaHk5RNoSVo7ZGwbMeH45

"""

from bs4 import BeautifulSoup
from urllib2 import urlopen
import json

BASE_URL = "http://www.middlecoin.com/allusers.html"
HISTORY_URL = "http://www.middlecoin.com/reports/{your btc wallet address}.html"
WALLET = "{your btc wallet address}"
MTGOX = "http://data.mtgox.com/api/1/BTC{your currency(example BTCSEK)}/ticker"

def get_mywallet(url):
    GLOBAL = WALLET
    main = ['Accepted MH/s: ', 'Rejected MH/s: ', 'Immature: ', 'Unexchanged: ', 'Balance: ']
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    wallet = soup.find(text=WALLET)
    info = soup.find(text=WALLET).parent.findNextSiblings('td')
    print "Wallet: ",wallet
    for i, a in zip(main,info):
        print i,a.get_text()
    print "\n"

def get_history(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    tr = [a.get_text() for a in soup.find_all('tr')]
    for i in tr:
        i.replace(" ", '', 1)
        print i.replace("\n"," ")

def get_total_in_sek(url):
    data = {}
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    tr = [a.get_text() for a in soup.find_all('tr')]
    for i in tr:
        data.setdefault(i.replace("\n",""))
    for i in data:
        if i.startswith('Total'):
            return float(i.strip('Total'))

def get_mtgox(url):
    html = urlopen(url).read()
    test = json.loads(html)
    return float(test['return']['high']['value'])



get_mywallet(BASE_URL)
get_history(HISTORY_URL)
get_total_in_sek(HISTORY_URL)
print " Total",get_mtgox(MTGOX) * get_total_in_sek(HISTORY_URL), "SEK (MTGOX)"
