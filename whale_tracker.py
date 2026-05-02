import praw
from groq import Groq
import requests
import time
import threading
from flask import Flask

# --- 1. BEÁLLÍTÁSOK ÉS KULCSOK ---

REDDIT_USER_AGENT = 'WhaleTrackerBot by u/REDDITUSER'
REDDIT_CLIENT_ID = 'YOUR_REDDIT_CLIENT_ID'
REDDIT_SECRET = 'YOUR_REDDIT_SECRET'
GROQ_API_KEY = 'YOUR_GROQ_API_KEY'
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

TARGET_USER = 'TARGETUSER'
# --- 2. RENDSZEREK INICIALIZÁLÁSA ---
client = Groq(api_key=GROQ_API_KEY)
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# --- 3. A WEBSZERVER (Hogy a felhő ne altassa el a botot) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "A Bálna Figyelő Bot aktív és fut 0-24-ben!"

def run_server():
    # A Render.com alapértelmezett portja a 10000-es
    app.run(host='0.0.0.0', port=10000)

# --- 4. A FŐ PROGRAM (A BOT AGYA) ---
def run_bot():
    print(f"Indítás... {TARGET_USER} figyelése folyamatban!")
    send_telegram_message("🤖 Bálna Figyelő Bot felhő üzemmódra felkészítve!")
    
    last_comment_id = None

    while True:
        try:
            redditor = reddit.redditor(TARGET_USER)
            latest_comment = next(redditor.comments.new(limit=1))

            if latest_comment.id != last_comment_id:
                print(f"Új aktivitás észlelve! Értelmezés...")
                
                prompt = f"""
                Te egy profi pénzügyi elemző vagy. A következő Reddit kommentet a(z) r/thetagang subreddit egyik opciós bálnája írta az imént. 
                1. Fordítsd le magyarra a lényeget.
                2. Magyarázd el egyszerűen a használt opciós/tőzsdei zsargont.
                3. Vond le a következtetést: spot részvénykereskedőként ez a lépés milyen jelzés (bika/emelkedést váró, vagy medve/esést váró) az adott részvényre nézve.
                
                Itt a komment szövege:
                "{latest_comment.body}"
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                
                ai_translation = chat_completion.choices[0].message.content
                
                final_message = f"🚨 **Új lépés {TARGET_USER}-től!**\n\n**Eredeti szöveg:**\n_{latest_comment.body}_\n\n**AI Elemzés:**\n{ai_translation}"
                send_telegram_message(final_message)
                
                last_comment_id = latest_comment.id
                print("Üzenet sikeresen elküldve a Telegramra.")

            time.sleep(300)

        except Exception as e:
            print(f"Hiba történt a bot futása közben: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # Párhuzamosan indítjuk a webszervert és a Reddit figyelőt
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    run_server()