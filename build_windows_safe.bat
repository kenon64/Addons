@echo off
REM ============================================================
REM DotaCoach Build Script - УЛУЧШЕННАЯ ВЕРСИЯ
REM Использует минимальные зависимости для надежности
REM ============================================================

setlocal enabledelayedexpansion
color 0A

echo.
echo ============================================================
echo   🎮 СБОРКА DotaCoach.exe (Улучшенная версия)
echo ============================================================
echo.

REM 1. Проверка Python
echo 📋 1. Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo.
    echo 🆘 РЕШЕНИЕ: Нужно установить Python
    echo.
    echo Сейчас откроется помощник для установки...
    timeout /t 3 /nobreak
    
    REM Запустить скрипт установки Python
    if exist "install_python.bat" (
        call install_python.bat
    ) else (
        echo.
        echo Установи Python вручную:
        echo   1. https://www.python.org/downloads/
        echo   2. ✓ "Add Python to PATH"
        echo   3. Перезагрузи компьютер
        pause
    )
    exit /b 1
)
python --version
echo ✓ Python найден
echo.

REM 2. Обновление pip
echo 📋 2. Обновление pip...
python -m pip install --upgrade pip >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ошибка при обновлении pip, продолжаю...
) else (
    echo ✓ pip обновлен
)
echo.

REM 3. Установка минимальных зависимостей
echo 📋 3. Установка зависимостей...
echo    (используются минимальные зависимости для надежности)
echo.

if exist "requirements-minimal.txt" (
    echo ✓ Использую requirements-minimal.txt
    python -m pip install -r requirements-minimal.txt
) else (
    echo ⚠️  requirements-minimal.txt не найден, используя requirements.txt
    python -m pip install -r requirements.txt
)

if errorlevel 1 (
    echo.
    echo ⚠️  Ошибка при установке зависимостей!
    echo.
    echo 🆘 ЧТО ДЕЛАТЬ:
    echo    1. Запусти: find_bad_package.bat
    echo       (найдет какой пакет не устанавливается)
    echo    2. Если ошибка про Visual C++:
    echo       → https://visualstudio.microsoft.com/downloads/
    echo       → Desktop development with C++
    echo    3. Если ошибка про интернет:
    echo       → Проверь соединение
    echo.
    pause
    exit /b 1
)

echo ✓ Зависимости установлены
echo.

REM 4. Установка PyInstaller
echo 📋 4. Установка PyInstaller...
python -m pip install PyInstaller==6.1.0 >nul 2>&1
if errorlevel 1 (
    echo ❌ Ошибка при установке PyInstaller!
    pause
    exit /b 1
)
echo ✓ PyInstaller готов
echo.

REM 5. Очистка старых сборок
echo 📋 5. Очистка старых файлов...
if exist "build" rmdir /s /q build >nul 2>&1
if exist "dist" rmdir /s /q dist >nul 2>&1
if exist "__pycache__" rmdir /s /q __pycache__ >nul 2>&1
if exist "*.spec" del /q *.spec >nul 2>&1
echo ✓ Очищено
echo.

REM 6. Сборка exe
echo 📋 6. СБОРКА EXE (это может занять 3-5 минут)...
echo    Пожалуйста, подожди...
echo.

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

if errorlevel 1 (
    echo.
    echo ❌ Ошибка при сборке!
    echo.
    echo 🆘 ЧТО ДЕЛАТЬ:
    echo    1. Запусти: build_windows_diagnostic.bat
    echo       (полная диагностика система)
    echo    2. Если ошибка про модули:
    echo       Запусти: find_bad_package.bat
    echo    3. Если всё равно не работает:
    echo       Скопируй сообщение об ошибке выше
    echo       Создай Issue на: https://github.com/kenon64/Addons
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   ✅ СБОРКА УСПЕШНО ЗАВЕРШЕНА!
echo ============================================================
echo.
echo 📁 Исполняемый файл: dist\DotaCoach.exe
echo.
echo 📝 Перед запуском:
echo    1. Сделай копию .env.example в .env
echo    2. Добавь QWEN_API_KEY в .env файл
echo    3. Запусти DotaCoach.exe
echo.

if exist "dist\DotaCoach.exe" (
    for %%A in (dist\DotaCoach.exe) do (
        set "size=%%~zA"
    )
    echo 📊 Размер файла: !size! байт
    echo.
    echo 📂 Открываю папку с результатом...
    start explorer dist
)

echo.
pause
exit /b 0
