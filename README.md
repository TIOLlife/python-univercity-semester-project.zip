Telegram Bot Assistant for Students (MT-225)

Description

This project is a Telegram bot developed in Python for students of group MT-225.
The bot helps students manage tasks, reminders, and class schedules.

Main Features

- View class schedule
- Add reminders and deadlines
- Receive automatic notifications
- Delete completed tasks
- Store data locally in JSON format

The bot is built using the "pyTelegramBotAPI" library.

---

Project Structure

python-univercity-semester-project/
│
├── bot.py          # Main bot file
├── tasks.json       # JSON database for tasks
├── README.md         # Project documentation
├── requirments.txt           # Required libraries for project
---

Requirements

- Python 3.10+
- Internet connection
- Telegram Bot Token

---

Installation

1. Install Python

Download Python from the official website:

https://www.python.org/

---

2. Install Dependencies

Open terminal and run:

pip install -r requirments.txt

---

3. Create Telegram Bot

1. Open Telegram
2. Find @BotFather
3. Create a new bot
4. Copy your bot token

Create a file named "config.py":

BOT_TOKEN = "YOUR_BOT_TOKEN"

---

Running the Bot

Run the following command:

python bottt.py

If everything works correctly:

Бот успешно запущен и следит за дедлайнами...

---

Main Functions

Task Storage

Tasks are stored in "tasks1.json".

Example:

{
    "123456789": [
        {
            "text": "Submit Python project",
            "time": "18:00",
            "notified": false
        }
    ]
}

---

Bot Menu

Button| Description
📋 Мои задачи| Show all tasks
➕ Добавить задачу| Add new reminder
📅 Расписание занятий| Show class schedule
✅ Удалить выполненные| Delete completed task
ℹ️ Помощь| Help information

---

Schedule System

The bot contains a static schedule for MT-225 students.

Example:

SCHEDULE = {
    "mon": "Monday schedule...",
    "tue": "Tuesday schedule..."
}

Users select a day using inline buttons.

---

Adding Tasks

Step 1 — Task Text

User enters task description:

Submit database assignment

---

Step 2 — Reminder Time

User enters time in format:

HH:MM

Example:

18:30
09:00
14:05

The bot validates the time before saving.

---

Reminder System

The bot runs a background thread that checks reminders every 30 seconds.

If current time matches task time:

if task["time"] == now:

The bot sends a notification message.

---

Technologies Used

Technology| Purpose
Python| Main programming language
pyTelegramBotAPI| Telegram API
JSON| Data storage
Threading| Background reminder checking

---

Error Handling

The bot includes:

- Invalid input checking
- JSON protection
- Automatic reconnect on network failure
- Exception handling

---

Example Usage

Add Reminder

User:
➕ Добавить задачу

Bot:
Напиши текст задачи

User:
Submit physics lab

Bot:
Введи время

User:
18:00

Bot:
Напоминание установлено

---

Possible Improvements

Future improvements may include:

- SQLite database support
- Deadline dates
- Task categories
- Admin panel
- "/today" command
- Cloud deployment
- User authentication

---

Author

Educational Telegram bot project for managing student schedules and reminders.

Built with Python and Telegram Bot API.
