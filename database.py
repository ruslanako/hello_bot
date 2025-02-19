import sqlite3

# Подключение к базе данных (если файла нет, он будет создан)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Создание таблицы пользователей, если её нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        phone TEXT,
        location TEXT,
        birthday TEXT
    )
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных успешно создана и готова к использованию.")