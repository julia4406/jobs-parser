# 🤖 JobBot

A simple yet powerful application that parses job vacancies for **Junior** (or **Middle**) Python Developers and sends them directly to your Telegram via a **Telegram bot**.  
Job listings are fetched from **DOU** and **Djinni** websites.

---

## 🚀 Installation & Setup

1. **Clone this repository** to your local machine:

   ```bash
   git clone git@github.com:julia4406/jobs-parser.git
   cd jobs-parser
   ```

2. **Check your settings**:

   - 🛠️ You must have a Telegram bot (create one via [BotFather](https://telegram.me/botfather))
   - 🔑 You’ll need the following credentials:
     - `TELEGRAM_TOKEN`
     - `TELEGRAM_CHAT_ID`
   - 📁 In your project folder, create a `.env` file (use `.env.sample` as a template) and add your Telegram credentials there.

3. **Adjust the schedule (optional):**

   - Open `app/celery_app.py`
   - Find the `celery_app.conf.beat_schedule` section.
   - The parser is currently set to run **4 times a day**.
   - You can modify the `"schedule"` field to customize the frequency.

4. **Build and run the app using Docker** 🐳:

   ```bash
   docker-compose up --build
   ```

---

## ✅ Done!

Enjoy your personalized job feed delivered straight to Telegram!  
Good luck with your job hunting! 🍀

---

> 📌 Built with Python, Celery, BeautifulSoup, and a bit of ❤️
