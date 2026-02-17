@echo off
REM Быстрый запуск DotaCoach для Windows (без сборки)

echo.
echo ====================================
echo   🎮 DotaCoach - Быстрый запуск
echo ====================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    echo.
    echo Скачай Python с: https://www.python.org/
    echo Не забудь отметить "Add Python to PATH"!
    pause
    exit /b 1
)

REM Проверка pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip не найден!
    pause
    exit /b 1
)

REM Установка зависимостей (если нужно)
echo 📦 Проверка зависимостей...
pip install -r requirements.txt -q

if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pause
    exit /b 1
)

echo ✓ Готово!
echo.
echo 🎮 Запускаю DotaCoach...
echo.

REM Запуск программы
python main.py

echo.
echo ✓ DotaCoach завершил работу
pause
