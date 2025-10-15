📘 README.md
# 🧠 MindBuy — Smart Telegram Bot for Marketplaces

MindBuy is an intelligent Telegram bot that helps users quickly find categories, search for products, compare prices, and get marketplace analytics — all directly inside Telegram.

---

## 📚 Navigation
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Usage Examples](#-usage-examples)
- [Future Plans](#-future-plans)

---

## 🎯 Features

| 📌 Feature | 🔍 Description |
|------------|----------------|
| 🤖 **Aiogram** | Powerful framework for creating Telegram bots |
| 🌐 **Selenium** | Automates browser and scrapes product data |
| 💾 **JSON** | Local storage for categories and products |
| 📊 **Analytics** | Tracks categories, prices, and trends |
| 🧱 **Modular architecture** | Easy to expand and maintain |

---

## 📽 Demo
Here’s how MindBuy works in Telegram 👇  

![MindBuy Demo](https://github.com/user-attachments/assets/393f72e0-ef52-4cb0-8670-d601f193838b)

---

## 🛠 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/behruzbekrizaviddinov-ai/mindbuy-bot.git
cd mindbuy-bot
```
### 2️⃣ Create and activate a virtual environment
Make sure Python 3.10+ is installed. Then create and activate a virtual environment:
```
python -m venv .venv
```

Windows:
```
.venv\Scripts\activate
```

macOS / Linux:
```
source .venv/bin/activate
```

### 3️⃣ Install dependencies
```
pip install aiogram
pip install selenium
pip install asyncio
```
### 4️⃣ Configure environment variables
```
Create a .env file in the project root:

TOKEN=8469918338:AAHvoFEjjzB0R7S8fQ0t5LDDerUsfx8m1to
CHROME_PATH=path_to_chromedriver.exe


TOKEN — Telegram bot token from @BotFather

CHROME_PATH — Full path to chromedriver.exe (used by Selenium)
```
### 5️⃣ Run the bot
```
python main.py
```
You should see:
```
INFO:aiogram:Bot polling has started
```

Then open your bot in Telegram (e.g., @MindBuyBot) and send /start.
## 🧩 Common Errors
```
Error	Cause	Solution
ValueError: The path is not a valid file	Invalid ChromeDriver path	Check CHROME_PATH in .env
telegram.error.Unauthorized	Invalid bot token	Get a new one from @BotFather

SessionNotCreatedException	Chrome/ChromeDriver mismatch	Install matching ChromeDriver
```
## 🧠 Tech Stack
```
Technology	Purpose
Python 3.10+	Core language
Aiogram	Telegram bot framework
Selenium	Web scraping and automation
Asyncio	Asynchronous operations
python-dotenv	Environment configuration
JSON	Local data storage
```

## 📂 Project Structure
```
mindbuy-bot/
│
├── main.py              # Bot entry point
├── handler/             # Command handlers
├── keyboard/            # Inline and reply keyboards
├── scraper/             # Marketplace data parser
└── README.md            # Project documentation
```
---

## 📄 **requirements.txt**
```txt
aiogram==3.3.0
selenium==4.20.0
asyncio
python-dotenv
requests
```
### ⚙️ .env.example

## Telegram bot token
```
8469918338:AAHvoFEjjzB0R7S8fQ0t5LDDerUsfx8m1to
```
## Full path to your ChromeDriver executable
```
CHROME_PATH=C:\path\to\chromedriver.exe
```
## Optional logging level
```
LOG_LEVEL=INFO
```
## 📌 Usage Examples

🏁 Start the bot
```
/start
```

💬 Show available commands
```
/help
```
## 🚀 Future Plans
```
📈 Product price history tracking

🌍 Support for more marketplaces

📊 Extended analytics and reports

🤖 AI-based product recommendations
```
## 📜 License
```
This project is licensed under the MIT License.
Feel free to use, modify, and share for educational or personal purposes.

Author: Bexruzbek Rizaviddinov & Sariev Doston
```
📧 For collaboration or support — feel free to reach out!
