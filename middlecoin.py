#!/usr/bin/env python

"""
@title: ...........middlecoinscraper
@author: ..........jonjez
@date: ............2014:01:27

--[Requirements]--
Please change the HISTORY_JSON and WALLET to match your wallet.

--[Description]--

This script could be used to scrape middlecoin from your stats
and history. it will also get the latest currency of your choice
value from mtgox in high/low/avg

please feel free to use and improve the script, if you like it you are more than
welcome to send me a donation.

BTC: 1EN27w1mMHp6mTaHk5RNoSVo7ZGwbMeH45

--[Future]--
Will change "get_mywallet()" function to retrieve the information from json instead.
hopefully he will implement a user specific json file instead of downloading a 3mb
json file for each iteration.

BASE_URL = "http://www.middlecoin.com/allusers.html"
HISTORY_JSON = "http://www.middlecoin.com/reports/{wallet}.json"
WALLET = "{wallet}"
MTGOX = "http://data.mtgox.com/api/1/BTCSEK/ticker"


"""

from bs4 import BeautifulSoup
from urllib2 import urlopen
import json
import time

BASE_URL = "http://www.middlecoin.com/allusers.html"
HISTORY_JSON = "http://www.middlecoin.com/reports/{wallet}.json"
WALLET = "{wallet}"
MTGOX = "http://data.mtgox.com/api/1/BTCSEK/ticker"

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

def get_test_hist(url):
    html = urlopen(url).read()
    test = json.loads(html)
    total = test['report']
    for x in total:
        transid = x['txid']
        unixtime = time.ctime(x['time'])
        amount = float(x['amount'])
        SEK_HIGH = amount * get_mtgox_sek_high(MTGOX)
        SEK_LOW = amount * get_mtgox_sek_low(MTGOX)
        SEK_AVG = amount * get_mtgox_sek_avg(MTGOX)
        #print transid,"/", unixtime,"/", amount, "BTC"
        print unixtime,"\t", amount, "BTC\t", SEK_HIGH,"SEK\t", SEK_LOW,"SEK\t", SEK_AVG,"SEK"


def get_mtgox_sek_high(url):
    html = urlopen(url).read()
    test = json.loads(html)
    return float(test['return']['high']['value'])

def get_mtgox_sek_low(url):
    html = urlopen(url).read()
    test = json.loads(html)
    return float(test['return']['low']['value'])

def get_mtgox_sek_avg(url):
    html = urlopen(url).read()
    test = json.loads(html)
    return float(test['return']['avg']['value'])

def get_total_btc(url):
    html = urlopen(url).read()
    test = json.loads(html)
    total = test['total']
    return float(total)



get_mywallet(BASE_URL)
print "Time:\t\t\t\t\t\tAmount\Day:\t\tMTGOX High:\t\t\tMTGOX Low:\t\t\tMTGOX Avg:"
get_test_hist(HISTORY_JSON)
print "Middlecoin Paid Out BTC:",get_total_btc(HISTORY_JSON)
print "\n"

print "BTC Stats:"
print "*"*101
print "Mtgox High:",get_mtgox_sek_high(MTGOX), "SEK"
print "Mtgox Low:",get_mtgox_sek_low(MTGOX), "SEK"
print "Mtgox Avg:",get_mtgox_sek_avg(MTGOX), "SEK"
print "\n"

print "Total:"
print "*"*101
print "High:",get_total_btc(HISTORY_JSON) * get_mtgox_sek_high(MTGOX), "SEK (MTGOX)"
print "Low:",get_total_btc(HISTORY_JSON) * get_mtgox_sek_low(MTGOX), "SEK (MTGOX)"
print "Avg:",get_total_btc(HISTORY_JSON) * get_mtgox_sek_avg(MTGOX), "SEK (MTGOX)"
