#!/bin/bash

# Скрипт для запуска всех тестов ØccultoNG Pro

echo "🧪 Запуск тестов ØccultoNG Pro"
echo "================================"

# Создание виртуального окружения если нет
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install -q pytest pytest-cov pillow numpy pycryptodome scipy

# Запуск тестов
echo "🚀 Запуск тестов..."
pytest tests/ \
    --cov=. \
    --cov-report=html \
    --cov-report=term-missing \
    -v \
    --tb=short \
    -m "not slow"

# Проверка результата
if [ $? -eq 0 ]; then
    echo "✅ Все тесты пройдены!"
    echo "📊 Отчет о покрытии: htmlcov/index.html"
else
    echo "❌ Некоторые тесты не пройдены!"
    exit 1
fi

# Деактивация виртуального окружения
deactivate