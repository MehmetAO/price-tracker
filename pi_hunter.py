#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import my_secrets
from twilio.rest import Client
import sys

price_url = "https://market.samm.com/raspberry-pi-zero-w"
test_price = 99

def setup_twilio_client():
    account_sid = my_secrets.TWILIO_ACCOUNT_SID
    auth_token = my_secrets.TWILIO_AUTH_TOKEN
    return Client(account_sid, auth_token)

def send_notification(text):
    twilio_client = setup_twilio_client()
    twilio_client.messages.create(
        body=text,
        from_=my_secrets.TWILIO_FROM_NUMBER,
        to=my_secrets.MY_PHONE_NUMBER
    )

def soup_maker(url):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")

        return soup

def price_grabber(soup):
    price = soup.find_all("span", class_= "product-price")[0].get_text()
    price = price.replace(",", ".")
    price = float(price)

    return price

def price_checker():
    price = price_grabber(soup_maker(price_url))
    if float(price) < float(test_price):
        output = "İndirim! Yeni fiyat: " + str(price)
        print(output)
        send_notification(output)
        sys.exit(1)
    else:
        print(price)

def main():
    while True:
        price_checker()
        time.sleep(1800)
        
if __name__== '__main__':
    main()
