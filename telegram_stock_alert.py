import requests
import time
from datetime import datetime
import os

# --- إعدادات البوت من GitHub Secrets ---
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# --- إعدادات Benzinga API ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# الكلمات المفتاحية مع التصنيف
KEYWORDS_MAP = {
    'patent': '📜 براءة اختراع',
    'FDA': '💊 موافقة FDA',
    'acquisition': '🤝 استحواذ',
    'merger': '🔗 اندماج',
    'approval': '✅ موافقة رسمية',
    'earnings': '💰 إعلان أرباح',
    'earnings announcement': '💰 إعلان أرباح',
    'quarter results': '📊 نتائج فصلية'
}

# تخزين الأخبار المرسلة لتجنب التكرار
sent_news_ids = set()

# --- إرسال رسالة إلى تليجرام ---
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"❌ فشل الإرسال إلى تليجرام: {response.text}")

# --- تحديد نوع الخبر ---
def detect_news_type(title):
    for keyword, label in KEYWORDS_MAP.items():
        if keyword.lower() in title.lower():
            return label
    return '📰 خبر عام'

# --- جلب الأخبار من Benzinga ---
def fetch_news():
    url = f"https://api.benzinga.com/api/v2/news?token={NEWS_API_KEY}&channels=stocks"
    response = requests.get(url)
    print(f"🔍 Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"❌ خطأ من Benzinga API: {response.text}")
        return []
    return response.json()

# --- تشغيل البوت ---
    if __name__ == "__main__":
    send_telegram_message("✅ اختبار: البوت يعمل الآن!")  # رسالة اختبار

    print("🚀 بدء تشغيل البوت (يفحص الأخبار كل 10 ثوانٍ)...")
    while True:
        news_list = fetch_news()
        filtered_news = []

        for item in news_list:
            news_id = item.get("id")
            title = item.get("title", "")
            link = item.get("url", "")
            news_type = detect_news_type(title)

            # أرسل الأخبار الجديدة فقط
            if news_id not in sent_news_ids:
                sent_news_ids.add(news_id)
                message = f"{news_type}\n{title}\n{link}"
                send_telegram_message(message)
                filtered_news.append(message)

        time.sleep(10)  # الفحص كل 10 ثواني
