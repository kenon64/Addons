@echo off
REM ============================================================
REM Скрипт сборки DotaCoach.exe для Windows
REM Улучшенная версия с поиском Python
REM ============================================================

setlocal enabledelayedexpansion
set PYTHON_FOUND=0
set PYTHON_PATH=

echo.
echo ====================================
echo   🎮 СБОРКА DotaCoach.exe
echo ====================================
echo.

REM Попытка 1: проверить python в PATH
echo 🔍 Ищу Python в системе...
python --version >nul 2>&1
if errorlevel 0 (
    set PYTHON_FOUND=1
    echo ✓ Python найден в PATH
    goto python_found
)

REM Попытка 2: поиск Python в стандартных местах
for %%i in (
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Python39\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files (x86)\Python\python.exe"
) do (
    if exist %%i (
        set PYTHON_PATH=%%i
        set PYTHON_FOUND=1
        echo ✓ Python найден: !PYTHON_PATH!
        goto python_found
    )
)

REM Если Python не найден
if !PYTHON_FOUND! equ 0 (
    echo.
    echo ❌ ОШИБКА: Python не найден в системе!
    echo.
    echo 📥 РЕШЕНИЕ:
    echo 1. Открой https://www.python.org/downloads/
    echo 2. Скачай Python 3.10 или выше
    echo 3. ⭐ ВАЖНО! При установке отметь галочку:
    echo    "Add Python to PATH"
    echo 4. Перезагрузи компьютер
    echo 5. Запусти этот скрипт снова
    echo.
    pause
    exit /b 1
)

:python_found
REM Установка зависимостей
echo.
echo 📦 Установка зависимостей...
if !PYTHON_FOUND! equ 1 (
    if "!PYTHON_PATH!" neq "" (
        !PYTHON_PATH! -m pip install --upgrade pip
        !PYTHON_PATH! -m pip install -r requirements.txt
    ) else (
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
    )
) else (
    pip install -r requirements.txt
)

if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pause
    exit /b 1
)

echo ✓ Зависимости установлены

REM Проверка PyInstaller
echo.
echo 🔍 Проверка PyInstaller...
if "!PYTHON_PATH!" neq "" (
    !PYTHON_PATH! -m pip install PyInstaller==6.1.0
) else (
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

if "!PYTHON_PATH!" neq "" (
    !PYTHON_PATH! -m PyInstaller --onefile ^
        --windowed ^
        --name "DotaCoach" ^
        --add-data ".env.example;." ^
        --hidden-import=speech_recognition ^
        --hidden-import=pyttsx3 ^
        --hidden-import=requests ^
        --hidden-import=psutil ^
        --hidden-import=dotenv ^
        main.py
) else (
    python -m PyInstaller --onefile ^
        --windowed ^
        --name "DotaCoach" ^
        --add-data ".env.example;." ^
        --hidden-import=speech_recognition ^
        --hidden-import=pyttsx3 ^
        --hidden-import=requests ^
        --hidden-import=psutil ^
        --hidden-import=dotenv ^
        main.py
)

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
