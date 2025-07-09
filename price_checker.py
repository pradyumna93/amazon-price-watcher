import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time

# Amazon product details
PRODUCT_URL = "https://www.amazon.in/Sony-Cancellation-Headphones-Multi-Point-Connection/dp/B0BS1QCFHX/ref=sr_1_3?crid=3KB40Z9BBS4W2&dib=eyJ2IjoiMSJ9.53MXxKu8Hee2hTX731sxBa4t9BaQpugTEsTpBgItlJpJluZXIrLEFrFO2yzC51yzevvAN1QvIdjjMtOPA-w69FHuTAgCJ7IViHztnbbX_lzJeHMYSoewggo8GFwi2ej4CZNoDDyiKgQWdgI7lYzCRyXf-9kdKGSoXFpjhjinnEsJxmNCngHNXB9UIVPLNrzciOrBwiyq-Kg8lXNvxZDtuTsoxLQf3zLVSdWPynAq7JM.x8Gqc3MTVyU2Y0_g-CUbbjiUSJ7B9u9rIUbD19HLA4I&dib_tag=se&keywords=sony%2Bheadphones%2Bover%2Bear&nsdOptOutParam=true&qid=1752029921&sprefix=sony%2Bhead%2Caps%2C348&sr=8-3&th=1"  # Replace with your product
TARGET_PRICE = 7999.0

# Request headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Twilio config
TWILIO_ACCOUNT_SID = "AC724444607f54751b98a09c2a632cf475"
TWILIO_AUTH_TOKEN = "adaa21ec60e45ef27bf87966a6285342"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+12185277496"  # Twilio sandbox number
TO_WHATSAPP_NUMBER = "whatsapp:+919337740362"      # Your verified number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def check_price():
    try:
        response = requests.get(PRODUCT_URL, headers=HEADERS)
        soup = BeautifulSoup(response.content, "lxml")

        title = soup.find(id="productTitle").get_text(strip=True)
        price_text = soup.find("span", {"class": "a-price-whole"}).get_text().replace(",", "").strip()
        price = float(price_text)

        print(f"Product: {title}")
        print(f"Current Price: ₹{price}")

        if price <= TARGET_PRICE:
            message = f"🔥 Price Drop Alert 🔔\n\n{title}\nPrice: ₹{price}\n\nBuy Now: {PRODUCT_URL}"
            send_whatsapp_message(message)
        else:
            print("Price is still above your target.\n")

    except Exception as e:
        print("Error:", e)


def send_whatsapp_message(message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=TO_WHATSAPP_NUMBER
        )
        print("✅ WhatsApp alert sent!")
    except Exception as e:
        print("Failed to send WhatsApp message:", e)


if __name__ == "__main__":
    while True:
        check_price()
        time.sleep(3600)  # Check every hour
