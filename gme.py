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

from Stock_Alert import Stock 
    #List of functions in Stock
    #__init__(self,ticker)
    #getPrice()
    #getOpenPrice()
    #init_treshold()
    #stdTresh()
    #alertPercent()

############################################
#testing
GME = Stock("GME")
while True:
    print(GME.getPrice())

