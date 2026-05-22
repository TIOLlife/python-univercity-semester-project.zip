import telebot
from telebot import types
import json
import os
import datetime
import threading
import time

# Инициализируем бота
bot = telebot.TeleBot("8136946974:AAFVNVkpiPvusaYwKZLIA1YJY0D-26xZWjk")

# Файл для хранения задач
DATA_FILE = "tasks.json"

# --- ФУНКЦИИ РАБОТЫ С JSON ---
def load_tasks():
    """Загрузка задач из JSON файла."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return {}

def save_tasks(tasks):
    """Сохранение задач в JSON файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

# --- СТАТИЧНОЕ РАСПИСАНИЕ (МТ-225) ---
# Ты можешь изменить названия предметов и время прямо здесь
SCHEDULE = {
    "mon": "<b>Понедельник (МТ-225):</b>\n1. 09:00 — Высшая математика\n2. 10:45 — Программирование на Python (Лекция)\n3. 12:30 — Физика",
    "tue": "<b>Вторник (МТ-225):</b>\n1. 09:00 — Иностранный язык\n2. 10:45 — Программирование на Python (Практика)\n3. 14:00 — Физкультура",
    "wed": "<b>Среда (МТ-225):</b>\n1. 09:00 — История Казахстана\n2. 10:45 — Философия\n3. 12:30 — Базы данных",
    "thu": "<b>Четверг (МТ-225):</b>\n1. 10:45 — Высшая математика\n2. 12:30 — Операционные системы\n3. 14:15 — Дискретная математика",
    "fri": "<b>Пятница (МТ-225):</b>\n1. 09:00 — Программирование на Python (Лабораторные)\n2. 10:45 — Архитектура ЭВМ\n3. 12:30 — Военная подготовка / Электив",
    "sat": "<b>Суббота:</b>\n🎉 Выходной день! Занятий нет."
}

# --- КЛАВИАТУРА ИНТЕРФЕЙСА ---
def get_main_keyboard():
    """Создает кнопки основного меню."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_list = types.KeyboardButton("📋 Мои задачи")
    btn_add = types.KeyboardButton("➕ Добавить задачу")
    btn_sched = types.KeyboardButton("📅 Расписание занятий") # Новая кнопка
    btn_clear = types.KeyboardButton("✅ Удалить выполненные")
    btn_help = types.KeyboardButton("ℹ️ Помощь")
    
    markup.add(btn_list, btn_add)
    markup.add(btn_sched) # Разместим расписание на отдельной строке для красоты
    markup.add(btn_clear, btn_help)
    return markup

def get_schedule_keyboard():
    """Создает инлайн-кнопки для выбора дня недели."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_mon = types.InlineKeyboardButton("Пн", callback_data="sched_mon")
    btn_tue = types.InlineKeyboardButton("Вт", callback_data="sched_tue")
    btn_wed = types.InlineKeyboardButton("Ср", callback_data="sched_wed")
    btn_thu = types.InlineKeyboardButton("Чт", callback_data="sched_thu")
    btn_fri = types.InlineKeyboardButton("Пт", callback_data="sched_fri")
    btn_sat = types.InlineKeyboardButton("Сб", callback_data="sched_sat")
    markup.add(btn_mon, btn_tue, btn_wed, btn_thu, btn_fri, btn_sat)
    return markup

# --- ОБРАБОТЧИКИ КОМАНД И КНОПОК ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Привет, {user_name}! 👋\n"
        f"Я персональный бот-ассистент студента группы МТ-225.\n"
        f"Помогу следить за расписанием, задачами и дедлайнами! Используй меню ниже."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard())

@bot.message_handler(content_types=['text'])
def handle_menu(message):
    chat_id = str(message.chat.id)
    text = message.text.strip()

    if not text:
        bot.send_message(chat_id, "❌ Ошибка: Ввод не может быть пустым.")
        return

    tasks = load_tasks()

    if text == "📋 Мои задачи":
        user_tasks = tasks.get(chat_id, [])
        if not user_tasks:
            bot.send_message(chat_id, "🎉 У тебя нет активных задач! Отдыхай.")
        else:
            response = "<b>🔔 Твой список задач и дедлайнов:</b>\n\n"
            for i, task in enumerate(user_tasks, 1):
                response += f"{i}. 📌 {task['text']} — ⏰ <b>{task['time']}</b>\n"
            bot.send_message(chat_id, response, parse_mode="HTML")

    elif text == "➕ Добавить задачу":
        msg = bot.send_message(chat_id, "✍️ Напиши текст задачи (например: 'Сдать проект по Python'):")
        bot.register_next_step_handler(msg, process_task_text)

    elif text == "📅 Расписание занятий":
        bot.send_message(chat_id, "📅 Выбери интересующий день недели:", reply_markup=get_schedule_keyboard())

    elif text == "✅ Удалить выполненные":
        user_tasks = tasks.get(chat_id, [])
        if not user_tasks:
            bot.send_message(chat_id, "❌ Список задач пуст.")
        else:
            markup = types.InlineKeyboardMarkup()
            for i, task in enumerate(user_tasks):
                markup.add(types.InlineKeyboardButton(text=f"❌ {task['text']} ({task['time']})", callback_data=f"del_{i}"))
            bot.send_message(chat_id, "Выбери выполненную задачу для удаления:", reply_markup=markup)

    elif text == "ℹ️ Помощь":
        help_text = (
            "<b>Как пользоваться ботом:</b>\n\n"
            "• Кнопка <b>📅 Расписание занятий</b> — покажет пары для группы МТ-225.\n"
            "• Кнопка <b>➕ Добавить задачу</b> — создаст напоминание. Введи текст, а затем точное время (например, 15:30).\n"
            "• Бот автоматически пришлет уведомление в назначенную минуту!\n"
            "• Все дедлайны пишутся в локальную базу данных JSON."
        )
        bot.send_message(chat_id, help_text, parse_mode="HTML")
    
    else:
        bot.send_message(chat_id, "🤔 Я не знаю такой команды. Используй кнопки меню.")

# Добавление задачи: получаем текст
def process_task_text(message):
    chat_id = str(message.chat.id)
    task_text = message.text.strip() if message.text else ""

    if not task_text:
        bot.send_message(chat_id, "❌ Задача не может быть пустой. Попробуй заново.")
        return

    msg = bot.send_message(chat_id, "⏰ Теперь введи время напоминания в формате ЧЧ:ММ (например, 18:45 или 09:00):")
    bot.register_next_step_handler(msg, process_task_time, task_text)

# Добавление задачи: получаем время и валидируем его
def process_task_time(message, task_text):
    chat_id = str(message.chat.id)
    time_text = message.text.strip() if message.text else ""

    try:
        datetime.datetime.strptime(time_text, "%H:%M")
    except ValueError:
        bot.send_message(chat_id, "❌ Неверный формат времени! Нужно писать именно ЧЧ:ММ (например, 14:05). Задача не создана.")
        return

    tasks = load_tasks()
    if chat_id not in tasks:
        tasks[chat_id] = []
    
    new_task = {
        "text": task_text,
        "time": time_text,
        "notified": False
    }
    
    tasks[chat_id].append(new_task)
    save_tasks(tasks)
    
    bot.send_message(
        chat_id, 
        f"✅ Напоминание установлено!\n📌 <b>Что сделать:</b> {task_text}\n⏰ <b>Время:</b> {time_text}", 
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )

# --- ОБРАБОТКА CALLBACK-ЗАПРОСОВ (ИНЛАЙН КНОПКИ) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = str(call.message.chat.id)
    
    # Обработка удаления задач
    if call.data.startswith('del_'):
        task_index = int(call.data.split('_')[1])
        tasks = load_tasks()
        user_tasks = tasks.get(chat_id, [])
        
        if 0 <= task_index < len(user_tasks):
            removed_task = user_tasks.pop(task_index)
            tasks[chat_id] = user_tasks
            save_tasks(tasks)
            
            bot.answer_callback_query(call.id, text="Удалено!")
            bot.edit_message_text(
                chat_id=chat_id, 
                message_id=call.message.message_id, 
                text=f"🗑 Задача <b>\"{removed_task['text']}\"</b> успешно удалена!",
                parse_mode="HTML"
            )
        else:
            bot.answer_callback_query(call.id, text="Ошибка: задача не найдена.")
            
    # Обработка вывода расписания
    elif call.data.startswith('sched_'):
        day = call.data.split('_')[1]
        day_schedule = SCHEDULE.get(day, "Расписание не найдено.")
        
        bot.answer_callback_query(call.id)
        # Изменяем текст сообщения, добавляя выбранное расписание и сохраняя инлайн-кнопки
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=day_schedule,
            parse_mode="HTML",
            reply_markup=get_schedule_keyboard()
        )

# --- ФОНОВЫЙ ПОТОК НАПОМИНАНИЙ ---
def check_reminders():
    """Каждую минуту проверяет задачи и отправляет напоминания."""
    while True:
        try:
            now = datetime.datetime.now().strftime("%H:%M")
            tasks = load_tasks()
            changes_made = False

            for chat_id, user_tasks in tasks.items():
                if not isinstance(user_tasks, list):
                    continue

                for task in user_tasks:
                    if not isinstance(task, dict) or "time" not in task or "text" not in task:
                        continue

                    if task["time"] == now and not task.get("notified", False):
                        alert_text = f"⏰ <b>ВНИМАНИЕ! ДЕДЛАЙН / НАПОМИНАНИЕ:</b>\n\n🔔 {task['text']}"
                        try:
                            bot.send_message(chat_id, alert_text, parse_mode="HTML")
                            task["notified"] = True
                            changes_made = True
                        except Exception as send_error:
                            print(f"Не удалось отправить сообщение пользователю {chat_id}: {send_error}")
                    
                    if now == "00:00" and task.get("notified", False):
                        task["notified"] = False
                        changes_made = True

            if changes_made:
                save_tasks(tasks)

        except Exception as e:
            print(f"Ошибка в фоновом потоке напоминаний: {e}")
        
        time.sleep(30)

# --- ЗАПУСК БОТА ---
if __name__ == '__main__':
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()
    
    print("Бот успешно запущен и следит за дедлайнами...")
    
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            print(f"Сбой сети: {e}. Переподключение через 5 секунд...")
            time.sleep(5)
