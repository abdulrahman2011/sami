import os
import requests
import time
from datetime import datetime

# --- تحميل القيم من Secrets ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# الكلمات المفتاحية
KEYWORDS_MAP = {
    'patent': '📄 براءة اختراع',
    'FDA': '💊 موافقة FDA',
    'acquisition': '🤝 استحواذ',
    'merger': '🔗 اندماج',
    'approval': '✅ موافقة رسمية',
    'earnings': '💰 اعلان أرباح',
    'earnings announcement': '💰 اعلان أرباح',
    'quarter results': '📊 نتائج فصلية'
}

# تخزين الأخبار المرسلة لتجنب التكرار
sent_news_ids = set()

# --- إرسال رسالة إلى تيليجرام ---
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

# --- تحديد نوع الخبر ---
def detect_news_type(title):
    for keyword, label in KEYWORDS_MAP.items():
        if keyword.lower() in title.lower():
            return label
    return '📰 خبر عام'

# --- جلب الأخبار من Benzinga ---
def fetch_news():
    url = f'https://api.benzinga.com/api/v2/news?token={NEWS_API_KEY}&channels=stocks'
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

        if news_id not in sent_news_ids:
            sent_news_ids.add(news_id)
            message = f"{news_type} جديد: {title}\n{link}"
            filtered_news.append(message)

    return filtered_news

# --- تشغيل البوت بشكل متكرر كل 10 ثواني ---
if name == "__main__":
    print("🚀 البوت بدأ العمل، سيتم فحص الأخبار كل 10 ثواني...")
    while True:
        news_items = fetch_news()
        if news_items:
            for news in news_items:
                send_telegram_message(news)
        else:
            print(f"⏳ لا توجد أخبار جديدة ({datetime.now().strftime('%H:%M:%S')})")
        time.sleep(10)  # فحص كل 10 ثواني
