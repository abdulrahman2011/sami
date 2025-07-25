import requests
import time
from datetime import datetime

# --- إعدادات البوت ---
BOT_TOKEN = '7205683778:AAHq8xTqtY_ksnbvGLsYBFrk9BainB0vy04'
CHAT_ID = '665669452'

# --- إعدادات Benzinga API ---
NEWS_API_KEY = 'bz.V4WKHAJD3AQYLDGQIBUI72PXOTTZCEG4'

# الكلمات المفتاحية مع التصنيف
KEYWORDS_MAP = {
    'patent': '📜 براءة اختراع',
    'FDA': '💉 موافقة FDA',
    'acquisition': '🤝 استحواذ',
    'merger': '🔗 اندماج',
    'approval': '✅ موافقة رسمية',
    'earnings': '💰 إعلان أرباح',
    'earnings announcement': '💰 إعلان أرباح',
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
    url = f'https://api.benzinga.com/api/v2/news?token={NEWS_API_KEY}&channels=stocks&pagesize=20'
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

        # إرسال الأخبار المصنفة إذا لم ترسل سابقًا
        if news_id not in sent_news_ids and any(kw.lower() in title.lower() for kw in KEYWORDS_MAP.keys()):
            sent_news_ids.add(news_id)
            message = f"🔥 جديد: {news_type}\n{title}\n{link}"
            filtered_news.append(message)

    return filtered_news

# --- تشغيل البوت ---
if name == "__main__":
    print("✅ البوت شغال ويجلب الأخبار من Benzinga كل 10 ثواني...")
    while True:
        news_items = fetch_news()
        if news_items:
            for news in news_items:
                send_telegram_message(news)
                time.sleep(2)  # فاصل بين الرسائل
        else:
            print("🔍 لا توجد أخبار جوهرية الآن.")
        time.sleep(10)  # فحص الأخبار كل 10 ثواني
