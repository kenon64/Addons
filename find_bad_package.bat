@echo off
setlocal enabledelayedexpansion
color 0A

echo.
echo ============================================================
echo   🔍 ПОИСК ПРОБЛЕМНОГО ПАКЕТА
echo ============================================================
echo.

REM Список пакетов из requirements.txt
set packages=^
SpeechRecognition==3.10.0 ^
pyttsx3==2.90 ^
requests==2.31.0 ^
psutil==5.9.0 ^
python-dotenv==1.0.0 ^
numpy==1.24.3 ^
pandas==2.0.3 ^
Pillow==10.0.0 ^
mss==9.0.1 ^
PyInstaller==6.1.0

echo 📋 Проверяю каждый пакет отдельно...
echo.

for %%p in (%packages%) do (
    echo Пытаюсь установить: %%p
    python -m pip install %%p >nul 2>&1
    if errorlevel 1 (
        echo   ❌ ОШИБКА! Пакет %%p не устанавливается!
        echo.
        echo   Подробный лог:
        python -m pip install %%p
        echo.
        goto problem_found
    ) else (
        echo   ✓ %%p установлен успешно
    )
)

echo.
echo ============================================================
echo   ✅ ВСЕ ПАКЕТЫ УСТАНОВИЛИСЬ!
echo ============================================================
pause
exit /b 0

:problem_found
echo.
echo ============================================================
echo   ⚠️  ПРОБЛЕМНЫЙ ПАКЕТ НАЙДЕН ВЫШЕ
echo ============================================================
echo.
echo 🆘 ВОЗМОЖНЫЕ РЕШЕНИЯ:
echo.
echo Если ошибка про "Microsoft Visual C++"
echo    → Скачай: https://visualstudio.microsoft.com/downloads/
echo    → Выбери "Desktop development with C++"
echo    → Переустанови
echo.
echo Если ошибка про "No such file or directory"
echo    → Проверь интернет соединение
echo    → Попробуй: python -m pip install --upgrade pip
echo.
echo Если ошибка про конкретный пакет
echo    → Попробуй: python -m pip install --upgrade %%p
echo.
pause
exit /b 1
