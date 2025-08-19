 
# Базовий образ з Python 3.12 + dev tools
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Встановлюємо Node.js (наприклад, версії 18)
RUN apt-get update && apt-get install -y curl \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Перевіримо версії
RUN python --version && node --version && npm --version


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
COPY run.py /run.py
COPY app /app


# Встановлюємо Python-залежності
RUN pip install --no-cache-dir -r /tmp/requirements.txt
                                 
# Відкриваємо порт
EXPOSE 7000


# Робоча директорія в контейнері
WORKDIR /

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "run.py"]