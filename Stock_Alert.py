import bs4
import requests
import datetime as dt
import pytz
import time
import smtplib
from bs4 import BeautifulSoup
from urllib.request import urlopen

# TIMEZONE defaults to NYC
TIMEZONE = pytz.timezone('America/New_York')

# GME : url = https://finance.yahoo.com/quote/GME?p=GME&.tsrc=fin-srch

def changeTIMEZONE():
    print("Timezne must be in the form found in pytz.all_timezones")
    TIMEZONE = input("PLEASE INPUT TIMEZONE: ")
    TIMEZONE = pytz.timezone(TIMEZONE)

def openUrl(url):
    Success = False
    count = 0
    while not Success:
        if count > 100:
            print("There seems to be an issue connecting with the site")
            return null
        try:
            page = urlopen(url)
            Success = True
        except:
            count+=1
            time.sleep(.5)

    return page

class Stock_Portfolio:
    '''
    [str] ptfl --> Portfolio containing ticker symbols, of all stocks you'd like to monitor
    (str) email --> email you'd like alerts to be sent to
    (str) timezone --> your timezone (must be in form found in pytz.all_timezones)

    '''

    def __init__(self, ptfl, email):
        self.ptfl = []
        for ticker in ptfl:
            self.ptfl.append(Stock(ticker))

        self.email = email
        self.time = dt.datetime.now(TIMEZONE)


    '''
    checkMarketOpen: returns boolean if the market is currently open & updates current time
    '''

    def checkMarketOpen(self):
        self.time = dt.datetime.now(TIMEZONE)
        if (self.time.hour >= 10) and (self.time.hour < 16):
            return True
        else:
            return False

    '''
    parsePrice: Continuously prints current price of tickers in portfolio until market closed
    '''

    def parsePrice(self):
        market_open = self.checkMarketOpen()

        while market_open:
            for stock in self.ptfl:
                stock.getPrice()
                print(f"Current Value of {stock.ticker} is: {stock.current_price}")

            print("-----------------------------------")
            time.sleep(60)

            market_open = self.checkMarketOpen()

        return "THE MARKET IS NOW CLOSED"

    '''
    sendEmail: Sends email from a burner account to your email
    ## NEEDS YOU TO INPUT BURNER EMAIL & PASSWORD ##
    '''

    def sendEmail(self, message):
        sender_email = "PassGoCollect98@gmail.com"
        password = "M0neyBags777"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        try:
            server.login(sender_email, password)
            #print("Login Success")
        except:
            print("There was an error")

        server.sendmail(self.email, self.email, message)

    '''
    emailAlert: Initializes thresholds, then continuously monitors stock prices,
                and sends email if any threshold is reached
    '''

    def emailAlert(self):
        market_open = self.checkMarketOpen()

        # Initializes & standardizes thresholds to %
        print("For dollar thresholds --> input int$ | For % change thresholds --> input int%")
        print("Note: Upper and Lower thresholds can be different types & should both be POSITIVE \n")

        for stock in self.ptfl:
            stock.stdThresh()

        while market_open:
            messages = []

            for stock in self.ptfl:
                if not stock.delay:
                    messages.append(stock.alertPercent())
                else:
                    # Waits 2 minutes, then resets open_price = current price of stock
                    # so that new high or low, is checked for % change
                    if (self.time - stock.time).seconds >= 120:
                        stock.delay = False
                        stock.open_price = stock.getPrice()

            # Only keeps string messages
            string_msg = [x for x in messages if isinstance(x, str)]

            if string_msg:
                string_msg = " \n ".join(string_msg)
                self.sendEmail(string_msg)

            time.sleep(5)
            market_open = self.checkMarketOpen()

        return print("MARKET IS NOW CLOSED")

class Stock:

    '''
    (str) ticker --> Ticker of particular stock
    (float) current_price --> current price of stock
    (float) open_price --> open price of stock
    (bool) delay --> set to true if stock reaches threshold, starting a 2 minute delay before
                     automatically resetting to a larger threshold
    '''

    def __init__(self, ticker):
        self.ticker = ticker
        self.current_price = self.getPrice()
        self.open_price = self.getOpenPrice()
        self.delay = False
        self.threshold = []
        self.time = 0

    '''
    getPrice: returns current price of stock & updates current_price
    '''

    def getPrice(self):
        url = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}&.tsrc=fin-srch"
        page = openUrl(url)

        soup = bs4.BeautifulSoup(page, "html.parser", from_encoding = "iso-8859-1")
        price = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})

        if price is None:
            time.sleep(1)
            price = self.getPrice()

        else:
            price = price.find('span', {'class': "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text

        self.current_price = float(price)
        return float(price)

    '''
    getAfterMarketPrice: gets the post/premarket prices and updates current price
    '''
    def getAfterMarketPrice(self):
        url = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}&.tsrc=fin-srch"
        page = openUrl(url)

        soup = bs4.BeautifulSoup(page, "html.parser", from_encoding = "iso-8859-1")
        price = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})

        if price is None:
            time.sleep(1)
            price = self.getAfterMarketPrice()
        else:
            price = price.find('span',{'class':"C($primaryColor) Fz(24px) Fw(b)"}).text

        self.current_price = float(price)
        return float(price)


    '''
    getOpenPrice: returns open price of ticker & updates open price
    '''

    def getOpenPrice(self):
        url = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}&.tsrc=fin-srch"
        page = openUrl(url)

        soup = bs4.BeautifulSoup(page, "html.parser", from_encoding = "iso-8859-1")
        open_price = soup.find('td',{'data-test': 'OPEN-value'})

        if open_price is None:
            time.sleep(1)
            open_price = self.getOpenPrice()

        else:
            open_price = open_price.find('span').text

        self.open_price = float(open_price)
        return float(open_price)

    '''
    init_thresh: Initializes an alert threshold for a stock
    # Asks for upper & lower bound inputs
    # Form of input: num$ or num% (lower bound is automatically converted to negative, if not already)
    '''

    def init_threshold(self):
        valid = False
        while not valid:
            try:
                upper = input(f"Please input upper_bound for {self.ticker} : ")
                lower = input(f"Please input lower_bound for {self.ticker} : ")

                if (not upper[-1] == "$") and (not lower[-1] == "%"):
                    raise ValueError

                if (not upper[-1] == "$") and (not lower[-1] == "%"):
                    raise ValueError

                valid = True
            except ValueError:
                print("\nInput should be in the form 'num$' or 'num%'")

        self.threshold = [upper, lower]

    "stdThresh: Standardizes all thresholds to %"

    def stdThresh(self):
        self.init_threshold()

        if self.threshold[0][-1] == "$":
            self.threshold[0] = float(self.threshold[0][:-1])
            self.threshold[0] = 1*(1 - ((self.open_price + self.threshold[0]) / self.open_price))

        else:
            self.threshold[0] = float(self.threshold[0][:-1])
            self.threshold[0] = (-1*self.threshold[0]) / 100

        # Makes sure threshold is negative
        if self.threshold[0] > 0:
            self.threshold[0] *= -1

        if self.threshold[1][-1] == "$":
            self.threshold[1] = float(self.threshold[1][:-1])
            self.threshold[1] = (((self.open_price + self.threshold[1]) / self.open_price) - 1)

        else:
            self.threshold[1] = float(self.threshold[1][:-1])
            self.threshold[1] = (self.threshold[1]) / 100

        print(self.threshold)

    """
    alertPercent: Checks if threshold is reached at current price,
                  if true returns message; otherwise returns false
    """

    def alertPercent(self):
        # Updates current market price
        self.getPrice()

        # Calculates % change in price from open
        delta = (self.current_price - self.open_price) / self.open_price
        print(f"Current Price of {self.ticker}: {self.current_price}")

        # Returns message if threshold reached and starts delay, otherwise returns false
        if delta > self.threshold[1]:
            message = f"My My good sir, what crispy tendies you have waiting for {self.ticker}. Go cash in!"
            self.delay = True
            self.time = dt.datetime.now(TIMEZONE)

        elif delta < self.threshold[0]:
            message = f"Dropped the tendies in a bucket for {self.ticker}... Better go pick up what you can."
            self.delay = True
            self.time = dt.datetime.now(TIMEZONE)

        else:
            return False;

        return message

if __name__ == "__main__":
    # Add your own tickers below
    ptfl = ["GME"]

    #Add your email below
    ptfl = Stock_Portfolio(ptfl, "harrisspahic1190@gmail.com")
    ptfl.emailAlert()
