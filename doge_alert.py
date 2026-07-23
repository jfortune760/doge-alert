import os
import requests

# ── Thresholds ──
ABOVE = 0.118   # alert if DOGE goes above this
BELOW = 0.0666   # alert if DOGE goes below this

# ── Telegram credentials (pulled from GitHub secrets) ──
TELEGRAM_TOKEN   = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def get_doge_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "dogecoin", "vs_currencies": "usd"}
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()["dogecoin"]["usd"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }, timeout=10)

def main():
    price = get_doge_price()
    print(f"DOGE price: ${price:.4f}")

    if price > ABOVE:
        send_telegram(
            f"🟢 <b>DOGE ALERT — ABOVE ${ABOVE}</b>\n\n"
            f"Current price: <b>${price:.4f}</b>\n"
            f"Crossed above your ${ABOVE} threshold."
        )
        print(f"Alert sent: above ${ABOVE}")

    elif price < BELOW:
        send_telegram(
            f"🔴 <b>DOGE ALERT — BELOW ${BELOW}</b>\n\n"
            f"Current price: <b>${price:.4f}</b>\n"
            f"Dropped below your ${BELOW} threshold."
        )
        print(f"Alert sent: below ${BELOW}")

    else:
        print(f"No alert. Price ${price:.4f} is between ${BELOW} and ${ABOVE}.")

if __name__ == "__main__":
    main()
