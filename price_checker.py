import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# Load config from environment (GitHub Secrets)
PRODUCT_URL = os.getenv("PRODUCT_URL")
TARGET_PRICE = float(os.getenv("TARGET_PRICE"))

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}


def check_price():
    try:
        response = requests.get(PRODUCT_URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "lxml")

        title = soup.find(id="productTitle").get_text(strip=True)
        price_text = soup.find("span", {"class": "a-price-whole"}).get_text()
        price = float(price_text.replace(",", "").strip())

        print(f"Product: {title}")
        print(f"Current Price: ₹{price}")

        if price <= TARGET_PRICE:
            message_body = (
                f"🔥 Price Drop Alert!\n\n{title}\n"
                f"Current Price: ₹{price}\n\nBuy Now: {PRODUCT_URL}"
            )
            send_whatsapp(message_body)
        else:
            print("Price is still above the target.")
    except Exception as e:
        print("Error checking price:", e)


def send_whatsapp(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=TO_WHATSAPP_NUMBER
        )
        print("✅ WhatsApp message sent:", message.sid)
    except Exception as e:
        print("❌ Failed to send WhatsApp message:", e)


if __name__ == "__main__":
    check_price()
