import bs4
import requests
import datetime as dt
import pytz
import time
import smtplib
from bs4 import BeautifulSoup
from urllib.request import urlopen

# GME : url = https://finance.yahoo.com/quote/GME?p=GME&.tsrc=fin-srch

def check_market_open():
    NYC = pytz.timezone('America/New_York')
    current_time = dt.datetime.now(NYC)

    if (current_time.hour <= 10) or (current_time.hour < 16):
        return True
    else:
        return  False

def getPrice(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch"
    try:
        page = urlopen(url)
    except:
        print("Error opening the URL")

    soup = bs4.BeautifulSoup(page, "html.parser")
    price = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text

    return float(price)

def parsePrice(tickers):
    market_open = check_market_open()

    while market_open:
        for ticker in tickers:
            price = getPrice(ticker)
            print(f"Current Value of {ticker} is: {price}")

        print("-----------------------------------")
        time.sleep(60)

        market_open = check_market_open()

    return "THE MARKET IS NOW CLOSED"

def test(ticker):
    price = float(getPrice(ticker))
    return price

def sendEmail(message):
    sender_email = "PassGoCollect98@gmail.com"
    password = "M0neyBags777"
    receiver_email = "harrisspahic1190@gmail.com"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender_email, password)
        #print("Login Success")
    except:
        print("There was an error")

    server.sendmail(sender_email, receiver_email, message)

"""
Threshold --> (-lower $ amt, upper $ amt)
"""
def getOpenPrice(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch"
    try:
        page = urlopen(url)
    except:
        print("Error opening the URL")

    soup = bs4.BeautifulSoup(page, "html.parser")
    open_price = soup.find('td',{'data-test': 'OPEN-value'}).find('span').text
    return float(open_price)

def alertDollarEmail(ticker, threshold):
    open_price = float(getOpenPrice(ticker))
    threshold[0] = -1*(1 - ((open_price + threshold[0]) / open_price))
    threshold[1] = (((open_price + threshold[1]) / open_price) - 1)
    #print(f"Threshold = f{threshold[0]}, f{threshold[1]}")
    alertPercentEmail(ticker, [threshold[0], threshold[1]])

"""
Threshold --> (-lower %, upper %)
"""

def alertPercentEmail(ticker, threshold):
    start_ticks = False;
    ticks = 0;

    open_price = getOpenPrice(ticker)
    market_open = check_market_open()

    while market_open:
        # Get change in market
        delta = (getPrice(ticker) - open_price) / open_price

        # Check if meets threshold
        if start_ticks == False:
            if delta > threshold[1]:
                message = "My My good sir, what crispy tendies you have waiting. Go cash in!"
                sendEmail(message)
                start_ticks = True;


            elif delta < threshold[0]:
                message = "Dropped the tendies in bucket... Better go pick up what you can."
                sendEmail(message)
                start_ticks = True;

        else:
            ticks += 1

        if ticks == 24:
            ticks = 0
            start_ticks = False
            open_price = getPrice(ticker)

        print(f"Current Price is: {getPrice(ticker)}")
        time.sleep(5)
        market_open = check_market_open()

    return "THE MARKET IS NOW CLOSED"

if __name__ == "__main__":
    tickers = ["GME"]
    print(getOpenPrice(tickers[0]))
    print(getPrice(tickers[0]))
    #test = getOpenPrice(tickers[0])
    #print(parsePrice(tickers))
    alertDollarEmail(tickers[0] ,[-6, 6])
