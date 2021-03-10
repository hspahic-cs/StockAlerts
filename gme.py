#This python script is designed to display a live feed  of Gamestop's price
#Dominic Wojewodka
#03/09/2021
import bs4
import requests
import datetime as dt
import pytz
import time
import smtplib
from bs4 import BeautifulSoup
from urllib.request import urlopen

#a variation of Titan1190's getPrice function
def getPrice(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch"
    try:
        page = urlopen(url)
    except:
        print("Error opening the URL")

    soup = bs4.BeautifulSoup(page, "html.parser", from_encoding = "iso-8859-1")
    price = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span', {'class': "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text

    return float(price)

    '''
    returns open price of ticker & updates open price
    '''
############################################
#testing
while True:
    print(getPrice("GME"))

