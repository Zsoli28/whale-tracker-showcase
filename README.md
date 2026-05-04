# 🐋 WhaleTracker-AI: Reddit Options Sentiment Bot

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg)
![Groq](https://img.shields.io/badge/AI-Groq%20Llama%203.3-orange.svg)
![Telegram](https://img.shields.io/badge/Alerts-Telegram%20Bot-blue.svg)
![Deployment](https://img.shields.io/badge/Deployment-Render.com-purple.svg)

## 📌 Overview
An automated, real-time tracking bot designed to monitor high-net-worth ("whale") options traders on Reddit. The system scrapes real-time comments using the official Reddit API, processes the complex financial jargon through an LLM (Large Language Model), and delivers translated, actionable spot-trading signals directly to a mobile device via Telegram.

Built with an emphasis on low latency and 24/7 cloud availability.

## 🚀 Key Features
* **Real-Time Monitoring:** Polls specific subreddits/users (e.g., `r/thetagang`) for new activity using `PRAW` (Python Reddit API Wrapper).
* **AI-Powered Sentiment Analysis:** Integrates the Groq API (utilizing the blazing-fast `llama-3.3-70b-versatile` model) to instantly translate English options jargon into native language and deduce bullish/bearish signals for spot trading.
* **Instant Push Notifications:** Dispatches formatted markdown alerts to a private Telegram channel via the Telegram Bot API.
* **Cloud-Native Architecture:** Wrapped in a lightweight Flask server to enable 24/7 zero-downtime deployment on Render.com, kept alive via automated external HTTP pings (UptimeRobot).

## 🛠️ Tech Stack
* **Language:** Python 3
* **APIs:** Reddit API (PRAW), Telegram Bot API, Groq AI API
* **Web Framework:** Flask (for health-check endpoint)
* **Infrastructure:** Render.com (Cloud Hosting), UptimeRobot (Keep-alive)
* **Concurrency:** `threading` module for parallel execution of the web server and the scraping loop.

## ⚙️ How It Works (Architecture Flow)
1. **Scraper Thread:** Wakes up every 5 minutes to check for new comments from target users.
2. **AI Processing:** If a new comment is found, the raw text is sent to the Groq LLM with a strict prompt structure.
3. **Alert Dispatcher:** The LLM's response (Translation + Jargon Explanation + Market Sentiment) is routed to the Telegram API.
4. **Health Server:** Concurrently, a Flask server listens on port 10000 to respond to external pings, preventing the cloud instance from sleeping.

## 💻 Local Setup (For Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/Zsoli28/whale-tracker-showcase.git
   cd whale-tracker-showcase
