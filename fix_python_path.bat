@echo off
REM ============================================================
REM FIX_PYTHON_PATH.bat - Добавление Python в PATH
REM ============================================================

setlocal enabledelayedexpansion
color 0A

echo.
echo ============================================================
echo   🔧 ДОБАВЛЕНИЕ PYTHON В PATH
echo ============================================================
echo.

REM Поиск Python в стандартных местах
set "PYTHON_FOUND=0"
set "PYTHON_PATH="

REM 1. Проверить если Python уже в PATH
python --version >nul 2>&1
if errorlevel 0 (
    REM Получить полный путь к Python
    for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i"
    if not "!PYTHON_PATH!"=="" (
        echo ✓ Python уже найден в PATH:
        echo   !PYTHON_PATH!
        python --version
        set "PYTHON_FOUND=1"
    )
)

REM 2. Если нет - ищем в стандартных местах
if "!PYTHON_FOUND!"=="0" (
    echo 🔍 Ищу Python в стандартных местах установки...
    echo.
    
    REM Проверяем C:\Python312
    if exist "C:\Python312\python.exe" (
        set "PYTHON_PATH=C:\Python312"
        echo ✓ Найден Python 3.12 в C:\Python312
        set "PYTHON_FOUND=1"
    )
    
    REM Проверяем C:\Python311
    if "!PYTHON_FOUND!"=="0" if exist "C:\Python311\python.exe" (
        set "PYTHON_PATH=C:\Python311"
        echo ✓ Найден Python 3.11 в C:\Python311
        set "PYTHON_FOUND=1"
    )
    
    REM Проверяем C:\Python310
    if "!PYTHON_FOUND!"=="0" if exist "C:\Python310\python.exe" (
        set "PYTHON_PATH=C:\Python310"
        echo ✓ Найден Python 3.10 в C:\Python310
        set "PYTHON_FOUND=1"
    )
    
    REM Проверяем AppData (для локальной установки)
    if "!PYTHON_FOUND!"=="0" if exist "%APPDATA%\Python\Python312\python.exe" (
        set "PYTHON_PATH=%APPDATA%\Python\Python312"
        echo ✓ Найден Python в AppData
        set "PYTHON_FOUND=1"
    )
)

REM 3. Результат
echo.
if "!PYTHON_FOUND!"=="0" (
    echo ❌ Python НЕ НАЙДЕН
    echo.
    echo 💾 Установи Python отсюда:
    echo    https://www.python.org/downloads/
    echo.
    echo ⚠️  ЭТО ВАЖНО:
    echo    1. Запусти установщик python-3.12.*.exe
    echo    2. В первом окне ОТМЕТЬ галочку:
    echo       ✓ "Add Python 3.12 to PATH"
    echo    3. Выбери "Install Now"
    echo    4. Подожди завершения
    echo    5. ПЕРЕЗАГРУЗИ компьютер
    echo    6. Запусти этот скрипт еще раз
    echo.
    pause
    exit /b 1
)

REM 4. Добавить в PATH если нужно
echo.
echo 📝 Добавляю Python в PATH...

REM Проверить еще раз
python --version >nul 2>&1
if errorlevel 0 (
    echo ✓ Python работает в PATH!
    python --version
    echo.
    echo ✅ ВСЕ В ПОРЯДКЕ - готово к сборке EXE
    pause
    exit /b 0
) else (
    echo.
    echo Нужно добавить Python в PATH вручную:
    echo.
    echo 1. Нажми WIN+X и выбери "Параметры"
    echo 2. Перейди в: Система ^> О системе ^> Дополнительные параметры системы
    echo 3. Нажми "Переменные окружения"
    echo 4. В разделе "Переменные среды пользователя" нажми "Изменить"
    echo 5. Добавь путь: !PYTHON_PATH!
    echo 6. Нажми OK три раза
    echo 7. ПЕРЕЗАГРУЗИ компьютер
    echo.
    pause
    exit /b 1
)

endlocal
