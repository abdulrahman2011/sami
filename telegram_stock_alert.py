import requests
import time
from datetime import datetime

# --- إعدادات البوت ---
BOT_TOKEN = '7205683778:AAHq8xTqtY_ksnbvGLsYBFrk9BainB0vy04'
CHAT_ID = '665669452'

# --- إعدادات مصادر الأخبار ---
NEWS_API_KEY = 'e7f9a32bda6b452db0d514afaf3c5999'
SEARCH_KEYWORDS = ['patent', 'FDA', 'acquisition', 'merger', 'approval', 'earnings']
MIN_PRICE = 3
MAX_PRICE = 20

# --- إرسال رسالة إلى تليجرام ---
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

# --- الحصول على أخبار من NewsAPI ---
def fetch_news():
    url = f'https://newsapi.org/v2/everything?q={" OR ".join(SEARCH_KEYWORDS)}&language=en&sortBy=publishedAt&pageSize=20&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    return response.json().get('articles', [])

# --- الحصول على سعر السهم ---
def get_stock_price(symbol):
    url = f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}'
    try:
        res = requests.get(url).json()
        price = res['quoteResponse']['result'][0]['regularMarketPrice']
        return price
    except:
        return None

# --- الفلترة والإرسال ---
def check_and_alert():
    articles = fetch_news()
    for article in articles:
        title = article['title']
        url = article['url']

        for word in SEARCH_KEYWORDS:
            if word.lower() in title.lower():
                for word in title.split():
                    if word.isupper() and 1 <= len(word) <= 5:
                        symbol = word.strip('().,')
                        price = get_stock_price(symbol)
                        if price and MIN_PRICE <= price <= MAX_PRICE:
                            msg = f'📢 خبر عن {symbol}:\n{title}\n💰 السعر: ${price}\n🔗 {url}'
                            send_telegram_message(msg)
                        break

# --- تنفيذ ---
if __name__ == '__main__':
    check_and_alert()
    send_telegram_message("🚨 تم إرسال هذه الرسالة كاختبار للتأكد من عمل البوت.")
