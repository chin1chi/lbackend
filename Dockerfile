# Используем официальный образ Python в качестве базового
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

RUN apt-get update 

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . .

# Открываем порт
EXPOSE 8000

CMD ["alembic", "upgrade", "head"]

