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
import time

BASE_URL = "http://www.middlecoin.com/allusers.html"
HISTORY_JSON = "http://www.middlecoin.com/reports/{your btc wallet address}.json"
WALLET = "{Your wallet address}"
MTGOX = "http://data.mtgox.com/api/1/{your currency(example BTCSEK)}/ticker"

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
        amount = x['amount']
        print transid,"/", unixtime,"/", amount, "BTC"



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
print "Transaction ID: \t\t\t\t\t\t\t\t\t\t\t\t   Time:   \t\t\t\t\t  Amount:"
get_test_hist(HISTORY_JSON)
print "Total BTC:",get_total_btc(HISTORY_JSON)
print "\n"

print "BTC Stats:"
print "************************************************************************************************************"
print "Mtgox High:",get_mtgox_sek_high(MTGOX), "SEK"
print "Mtgox Low:",get_mtgox_sek_low(MTGOX), "SEK"
print "Mtgox Avg:",get_mtgox_sek_avg(MTGOX), "SEK"
print "\n"

print "Total:"
print "************************************************************************************************************"
print "High:",get_mtgox_sek_high(MTGOX) * get_total_btc(HISTORY_JSON), "SEK (MTGOX)"
print "Low:",get_mtgox_sek_low(MTGOX) * get_total_btc(HISTORY_JSON), "SEK (MTGOX)"
print "Avg:",get_mtgox_sek_avg(MTGOX) * get_total_btc(HISTORY_JSON), "SEK (MTGOX)"
