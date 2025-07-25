import requests
import time
from datetime import datetime
import os

# --- إعدادات البوت من GitHub Secrets ---
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# --- الكلمات المفتاحية مع التصنيف ---
KEYWORDS_MAP = {
    'patent': '📄 براءة اختراع',
    'FDA': '💊 موافقة FDA',
    'acquisition': '🤝 استحواذ',
    'merger': '🔗 اندماج',
    'approval': '✅ موافقة رسمية',
    'earnings': '💰 إعلان أرباح',
    'earnings announcement': '💰 إعلان أرباح',
    'quarter results': '📊 نتائج فصلية'
}

# --- تخزين الأخبار المرسلة لتجنب التكرار ---
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
        print(f"خطأ في جلب الأخبار: {response.status_code}")
        return []
    return response.json()

# --- تنفيذ البوت ---
if name == "__main__":
    print("🚀 بدء تشغيل البوت (يفحص الأخبار كل 10 ثوانٍ)...")
    while True:
        news_list = fetch_news()
        filtered_news = []
        for item in news_list:
            news_id = item.get("id")
            title = item.get("title", "")
            link = item.get("url", "")
            news_type = detect_news_type(title)

            # إرسال الأخبار الجديدة فقط
            if news_id not in sent_news_ids:
                sent_news_ids.add(news_id)
                message = f"{news_type}\n{title}\n{link}"
                send_telegram_message(message)
                filtered_news.append(message)

        if not filtered_news:
            print("⏳ لا توجد أخبار جديدة...")
        time.sleep(10)  # الفحص كل 10 ثوانٍ
