import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Получение всех записей
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Вывод данных в консоль
print("Список пользователей в базе данных:")
for row in rows:
    print(row)

# Закрытие соединения
conn.close()