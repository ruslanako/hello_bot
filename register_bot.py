import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("8024060225:AAEdy9B3MtP8plQG3-0N2iR54dWazfK6J-8")

# Подключение к базе данных
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы пользователей, если её нет
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY,
                  username TEXT,
                  phone TEXT,
                  location TEXT,
                  birthday TEXT)''')
conn.commit()

# Хранение данных пользователей перед сохранением в БД
user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    username = message.from_user.first_name if message.from_user.first_name else "Гость"
    user_data[message.chat.id] = {"username": username}
    bot.send_message(message.chat.id,
                     f"Привет, {username}! Давайте зарегистрируемся. Пожалуйста, отправьте свой номер телефона.",
                     reply_markup=request_contact())


# Запрос номера телефона
def request_contact():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton("Отправить номер", request_contact=True)
    markup.add(button)
    return markup


# Обработчик номера телефона
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_data[message.chat.id]['phone'] = message.contact.phone_number
    bot.send_message(message.chat.id, "Спасибо! Теперь отправьте вашу локацию.", reply_markup=request_location())


# Запрос локации
def request_location():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton("Отправить локацию", request_location=True)
    markup.add(button)
    return markup


# Обработчик локации
@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_data[message.chat.id]['location'] = f"{message.location.latitude}, {message.location.longitude}"
    bot.send_message(message.chat.id, "Спасибо! Теперь введите вашу дату рождения в формате ДД.ММ.ГГГГ.")
    bot.register_next_step_handler(message, handle_birthday)


# Обработчик даты рождения
def handle_birthday(message):
    user_id = message.chat.id
    user_data[user_id]['birthday'] = message.text

    # Сохранение данных в базу данных
    cursor.execute("INSERT INTO users (id, username, phone, location, birthday) VALUES (?, ?, ?, ?, ?)",
                   (user_id, user_data[user_id]['username'], user_data[user_id]['phone'],
                    user_data[user_id]['location'], user_data[user_id]['birthday']))
    conn.commit()

    bot.send_message(user_id, "Регистрация завершена! Ваши данные сохранены в системе.")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Список доступных команд:\n/start - Регистрация\n/help - Справка")


bot.polling()
