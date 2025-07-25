import requests
import time
import os
from datetime import datetime

# --- جلب القيم السرية من GitHub Secrets ---
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# --- الكلمات المفتاحية ---
KEYWORDS_MAP = {
    'patent': '📝 براءة اختراع',
    'FDA': '💊 FDA',
    'acquisition': '🤝 استحواذ',
    'merger': '🔗 اندماج',
    'approval': '✅ موافقة رسمية',
    'earnings': '💰 إعلان أرباح',
    'earnings announcement': '💰 إعلان أرباح',
    'quarter results': '📊 نتائج فصلية'
}

# --- تخزين الأخبار لتجنب التكرار ---
sent_news_ids = set()

# --- إرسال رسالة إلى تليجرام ---
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    r = requests.post(url, data=data)
    print(f"Test Message Status: {r.status_code}, Response: {r.text}")

# --- اختبار سريع للتأكد من أن البوت يعمل ---
def test_bot():
    send_telegram_message("🚀 اختبار ناجح! البوت متصل الآن.")

# --- تحديد نوع الخبر ---
def detect_news_type(title):
    for keyword, label in KEYWORDS_MAP.items():
        if keyword.lower() in title.lower():
            return label
    return '📢 خبر عام'

# --- جلب الأخبار من Benzinga ---
def fetch_news():
    url = f'https://api.benzinga.com/api/v2/news?token={NEWS_API_KEY}&channels=stocks&pageSize=50'
    response = requests.get(url)
    if response.status_code != 200:
        return []

    news_list = response.json()
    filtered_news = []

    for item in news_list:
        news_id = item.get("id")
        title = item.get("title", "")
        link = item.get("url", "")
        news_type = detect_news_type(title)

        if news_id not in sent_news_ids and any(kw.lower() in title.lower() for kw in KEYWORDS_MAP.keys()):
            sent_news_ids.add(news_id)
            message = f"{news_type}\n{title}\n{link}"
            filtered_news.append(message)

    return filtered_news

# --- تشغيل البوت ---
if name == "__main__":
    # تشغيل اختبار سريع قبل البدء
    test_bot()

    print("✅ البوت يعمل ويفحص الأخبار كل 10 ثواني...")
    while True:
        news_items = fetch_news()
        if news_items:
            for news in news_items:
                send_telegram_message(news)
        else:
            print("⏳ لا توجد أخبار جديدة الآن...")
        time.sleep(10)
