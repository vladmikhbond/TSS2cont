# Базовий образ з Python 3.12 + dev tools
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Встановлення системних пакетів (за потреби)
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*


# Встановлюємо залежності глобально (альтернативно: це робиться через postCreateCommand)
# RUN pip install fastapi[standard]
# RUN pip install sqlalchemy


# Копіюємо requirements.txt у контейнер (опціонально — VS Code і сам це зробить)
COPY requirements.txt /tmp/requirements.txt

# Встановлюємо Python-залежності
RUN pip install --no-cache-dir -r /tmp/requirements.txt
                                 
# Робоча директорія в контейнері
WORKDIR /app

# # Відкриваємо порт
# EXPOSE 8000


