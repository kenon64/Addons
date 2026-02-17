@echo off
REM ============================================================
REM DotaCoach Build Script - ПРЯМОЕ ИСПОЛЬЗОВАНИЕ PYTHON
REM Использует полный путь к Python, не зависит от PATH
REM ============================================================

setlocal enabledelayedexpansion
color 0A

echo.
echo ============================================================
echo   🎮 СБОРКА DotaCoach.exe (Прямой способ)
echo ============================================================
echo.

REM 1. Поиск Python в известных местах
echo 📋 1. Поиск Python...
set "PYTHON_PATH="

REM Проверяем C:\Users\%USERNAME%\AppData\Local\Python (альтернативная установка)
if exist "%APPDATA%\Local\Python\pythoncore-3.14-64\python.exe" (
    set "PYTHON_PATH=%APPDATA%\Local\Python\pythoncore-3.14-64\python.exe"
    echo ✓ Найден Python 3.14 в AppData\Local\Python
)

REM Проверяем C:\Python312
if "!PYTHON_PATH!"=="" if exist "C:\Python312\python.exe" (
    set "PYTHON_PATH=C:\Python312\python.exe"
    echo ✓ Найден Python 3.12
)

REM Проверяем C:\Python311
if "!PYTHON_PATH!"=="" if exist "C:\Python311\python.exe" (
    set "PYTHON_PATH=C:\Python311\python.exe"
    echo ✓ Найден Python 3.11
)

REM Проверяем C:\Python310
if "!PYTHON_PATH!"=="" if exist "C:\Python310\python.exe" (
    set "PYTHON_PATH=C:\Python310\python.exe"
    echo ✓ Найден Python 3.10
)

REM Если все еще не найден - проверяем PATH
if "!PYTHON_PATH!"=="" (
    for /f "delims=" %%i in ('where python 2^>nul') do set "PYTHON_PATH=%%i"
)

if "!PYTHON_PATH!"=="" (
    echo ❌ Python НЕ НАЙДЕН!
    echo.
    echo 🆘 РЕШЕНИЕ:
    echo   1. Запустите: fix_python_path.bat
    echo   2. После завершения - ПЕРЕЗАГРУЗИТЕ компьютер
    echo   3. Затем запустите этот скрипт заново
    echo.
    pause
    exit /b 1
)

echo   Полный путь: !PYTHON_PATH!
"!PYTHON_PATH!" --version
echo.

REM 2. Обновление pip
echo 📋 2. Обновление pip...
"!PYTHON_PATH!" -m pip install --upgrade pip >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ошибка при обновлении pip, продолжаю...
) else (
    echo ✓ pip обновлен
)
echo.

REM 3. Установка зависимостей (минимальные)
echo 📋 3. Установка зависимостей...
echo   Установка: SpeechRecognition, pyttsx3, requests, psutil, python-dotenv, Pillow, mss, PyInstaller

"!PYTHON_PATH!" -m pip install --upgrade -r requirements-minimal.txt
if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей!
    echo.
    echo 💡 Попробуйте:
    echo    1. Удалите папку: dist/
    echo    2. Удалите папку: build/
    echo    3. Запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)
echo ✓ Зависимости установлены
echo.

REM 4. Проверка PyInstaller
echo 📋 4. Проверка PyInstaller...
"!PYTHON_PATH!" -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ❌ PyInstaller не установлен!
    echo   Переустанавливаю...
    "!PYTHON_PATH!" -m pip install PyInstaller==6.1.0
)
echo ✓ PyInstaller готов
echo.

REM 5. Сборка EXE
echo 📋 5. Сборка DotaCoach.exe...
echo   Это может занять 2-5 минут...
echo.

"!PYTHON_PATH!" -m PyInstaller DotaCoach.spec --noconfirm

if errorlevel 1 (
    echo.
    echo ❌ ОШИБКА ПРИ СБОРКЕ!
    echo.
    echo Попробуйте:
    echo   1. Закройте все копии DotaCoach.exe
    echo   2. Удалите папки: dist/ и build/
    echo   3. Запустите скрипт заново
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   ✅ СБОРКА УСПЕШНО ЗАВЕРШЕНА!
echo ============================================================
echo.
echo 📁 Файл: dist\DotaCoach.exe
echo 📦 Размер: примерно 200-300 МБ
echo.
echo 🚀 Следующие шаги:
echo   1. Откройте папку dist/
echo   2. Скопируйте .env файл в dist/ папку
echo   3. Добавьте QWEN_API_KEY в .env
echo   4. Дважды кликните на DotaCoach.exe
echo.

REM Открыть папку с результатом
if exist "dist" (
    echo 📂 Открываю папку dist...
    start dist
)

echo.
echo Для продолжения нажмите любую клавишу . . .
pause

endlocal
