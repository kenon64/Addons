@echo off
REM ============================================================
REM Скрипт сборки DotaCoach.exe для Windows
REM ============================================================

echo.
echo ====================================
echo   🎮 СБОРКА DotaCoach.exe
echo ====================================
echo.

REM Проверка python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Пожалуйста, установите Python.
    pause
    exit /b 1
)

echo ✓ Python найден

REM Установка зависимостей
echo.
echo 📦 Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pause
    exit /b 1
)

echo ✓ Зависимости установлены

REM Проверка PyInstaller
echo.
echo 🔍 Проверка PyInstaller...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyInstaller не установлен, устанавливаю...
    pip install PyInstaller==6.1.0
)

echo ✓ PyInstaller готов

REM Очистка старых сборок
echo.
echo 🧹 Очистка старых файлов...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "__pycache__" rmdir /s /q __pycache__
echo ✓ Очищено

REM Сборка exe
echo.
echo 🔨 Сборка exe файла...
echo    (это может занять несколько минут)
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "DotaCoach" ^
    --icon=icon.ico ^
    --add-data ".env.example;." ^
    --hidden-import=speech_recognition ^
    --hidden-import=pyttsx3 ^
    --hidden-import=requests ^
    --hidden-import=psutil ^
    --hidden-import=dotenv ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка при сборке!
    pause
    exit /b 1
)

echo.
echo ====================================
echo   ✅ СБОРКА УСПЕШНО ЗАВЕРШЕНА!
echo ====================================
echo.
echo 📁 Исполняемый файл: dist\DotaCoach.exe
echo.
echo 📝 Перед запуском:
echo    1. Скопируй .env файл в папку с exe
echo    2. Добавь QWEN_API_KEY в .env
echo    3. Запусти DotaCoach.exe
echo.

REM Открыть папку с результатом
if exist "dist\DotaCoach.exe" (
    echo 📂 Открываю папку с результатом...
    start explorer dist
)

pause
