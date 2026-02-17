#!/bin/bash
# Быстрый запуск DotaCoach для Linux/Mac (без сборки)

echo ""
echo "===================================="
echo "  🎮 DotaCoach - Быстрый запуск"
echo "===================================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен!"
    echo ""
    echo "Установи Python3:"
    echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  - Mac: brew install python3"
    echo "  - Или скачай с: https://www.python.org/"
    exit 1
fi

echo "✓ Python3 найден: $(python3 --version)"
echo ""

# Создание/использование виртуального окружения
if [ ! -d "venv" ]; then
    echo "🔧 Создаю виртуальное окружение..."
    python3 -m venv venv
fi

# Активация
source venv/bin/activate

echo "✓ Окружение активировано"
echo ""

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ Ошибка при установке зависимостей"
    deactivate
    exit 1
fi

echo "✓ Готово!"
echo ""
echo "🎮 Запускаю DotaCoach..."
echo ""

# Запуск
python main.py

echo ""
echo "✓ DotaCoach завершил работу"
