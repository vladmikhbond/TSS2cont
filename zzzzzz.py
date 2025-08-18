import bcrypt
from app import data_alch as db
from app.models.models import User

# Оригінальний пароль (введений користувачем)
password = "123456"
salt = bcrypt.gensalt()

# Генерація солі та хешування пароля
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)


# Зберігайте цей хеш у базі даних
print(hashed_password.decode())  # Хеш як рядок

# db.add_user(User(username="2Petrenko", password="123456", role=1))
# db.add_user(User(username="3Sydorenko", password="123456", role=1))

