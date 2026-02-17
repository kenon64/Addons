@echo off
REM ============================================================
REM УСТАНОВКА PYTHON - Простейший способ
REM ============================================================

setlocal enabledelayedexpansion
color 0A

echo.
echo ============================================================
echo   ЁЯУЪ УСТАНОВКА PYTHON 3.12
echo ============================================================
echo.

REM Проверка если Python уже установлен
python --version >nul 2>&1
if errorlevel 0 (
    echo тЬУ Python уже установлен!
    python --version
    echo.
    pause
    exit /b 0
)

echo.
echo ПОШАГОВАЯ ИНСТРУКЦИЯ:
echo.
echo 1️⃣  Откроется сайт Python в браузере
echo    Жди загрузки...
echo.
echo 2️⃣  Нажми кнопку "Download Python 3.12"
echo    (большая синяя кнопка посередине)
echo.
echo 3️⃣  Когда файл скачается, двойной клик на него
echo    (обычно: C:\Users\ТвоеИмя\Downloads\python-3.12.*.exe)
echo.
echo 4️⃣  ⭐⭐⭐ ОЧЕНЬ ВАЖНО ⭐⭐⭐
echo    В первом окне установщика ОТМЕТЬ ГАЛОЧКУ:
echo    ┌─────────────────────────────────────┐
echo    │ ✓ Add Python 3.12 to PATH           │  ← ВОТ СЮДА!
echo    │                                     │
echo    │ [Install Now]  [Customize install]  │
echo    └─────────────────────────────────────┘
echo.
echo 5️⃣  Дождись завершения установки
echo    (может занять 1-2 минуты)
echo.
echo 6️⃣  Перезагрузи компьютер
echo    (ОБЯЗАТЕЛЬНО!)
echo.
echo 7️⃣  После перезагрузки запусти:
echo    build_windows_safe.bat
echo.

echo.
echo Открываю сайт Python...
timeout /t 2 /nobreak

REM Открыть браузер на странице Python
start https://www.python.org/downloads/

echo.
echo Нажми любую клавишу когда закончишь с установкой и перезагрузкой...
pause

REM Проверить еще раз
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Python ЕЩЕ НЕ УСТАНОВЛЕН
    echo.
    echo тнР Убедись что:
    echo    1. Ты установил Python с https://www.python.org/
    echo    2. Отметил галочку "Add Python to PATH"
    echo    3. Перезагрузил компьютер
    echo.
    pause
    exit /b 1
)

echo.
echo тЬУ Python успешно установлен!
python --version
echo.
echo Теперь можешь запустить:
echo   build_windows_safe.bat
echo.
pause
