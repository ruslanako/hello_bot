import telebot
from telebot import types

bot = telebot.TeleBot("7833445990:AAGCp90YDZRYpEceCNDqSan2Sj5y8_cFLDk")
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    username = message.from_user.username if message.from_user.username else "гость"
    bot.send_message(message.chat.id, f"Привет, {username}! Я ваш Telegram-бот. Чем могу помочь?")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Список доступных команд:\n/start - Приветствие\n/help - Справка")

bot.polling()
