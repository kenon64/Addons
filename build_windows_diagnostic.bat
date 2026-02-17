@echo off
REM ============================================================
REM Диагностический скрипт для DotaCoach сборки
REM Проверяет все компоненты и показывает что не работает
REM ============================================================

setlocal enabledelayedexpansion
color 0A

echo.
echo ============================================================
echo   🔍 ДИАГНОСТИКА СБОРКИ DotaCoach
echo ============================================================
echo.

REM 1. Проверка Python
echo 📋 1. Проверка Python...
python --version >tmp_python_version.txt 2>&1
type tmp_python_version.txt
if errorlevel 1 (
    echo ❌ Python ERROR
    del tmp_python_version.txt
    goto error_exit
) else (
    echo ✓ Python OK
)
del tmp_python_version.txt
echo.

REM 2. Проверка pip
echo 📋 2. Проверка pip...
python -m pip --version >tmp_pip_version.txt 2>&1
type tmp_pip_version.txt
if errorlevel 1 (
    echo ❌ pip ERROR
    del tmp_pip_version.txt
    goto error_exit
) else (
    echo ✓ pip OK
)
del tmp_pip_version.txt
echo.

REM 3. Проверка requirements.txt
echo 📋 3. Проверка requirements.txt...
if exist "requirements.txt" (
    echo ✓ requirements.txt найден
    echo    Содержимое:
    type requirements.txt
) else (
    echo ❌ requirements.txt НЕ НАЙДЕН!
    goto error_exit
)
echo.

REM 4. Установка зависимостей с логом
echo 📋 4. Установка зависимостей...
python -m pip install -r requirements.txt >tmp_pip_install.log 2>&1
if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей!
    echo    Лог ошибки:
    type tmp_pip_install.log
    del tmp_pip_install.log
    goto error_exit
) else (
    echo ✓ Зависимости установлены
    del tmp_pip_install.log
)
echo.

REM 5. Проверка PyInstaller
echo 📋 5. Проверка PyInstaller...
python -m pip install PyInstaller==6.1.0 >tmp_pyinstaller.log 2>&1
if errorlevel 1 (
    echo ❌ Ошибка при установке PyInstaller!
    type tmp_pyinstaller.log
    del tmp_pyinstaller.log
    goto error_exit
) else (
    echo ✓ PyInstaller установлен
    del tmp_pyinstaller.log
)
python -m PyInstaller --version >tmp_pi_version.txt 2>&1
type tmp_pi_version.txt
del tmp_pi_version.txt
echo.

REM 6. Проверка main.py
echo 📋 6. Проверка main.py синтаксис...
if exist "main.py" (
    echo ✓ main.py найден
    python -m py_compile main.py >tmp_compile.log 2>&1
    if errorlevel 1 (
        echo ❌ Ошибка в main.py:
        type tmp_compile.log
        del tmp_compile.log
        goto error_exit
    ) else (
        echo ✓ main.py синтаксис OK
        del tmp_compile.log
    )
) else (
    echo ❌ main.py НЕ НАЙДЕН!
    goto error_exit
)
echo.

REM 7. Проверка других python файлов
echo 📋 7. Проверка других файлов...
for %%f in (coach.py dota_advisor.py qwen_processor.py game_integration.py farming_optimizer.py voice_assistant.py config.py) do (
    if exist "%%f" (
        python -m py_compile %%f >tmp_compile.log 2>&1
        if errorlevel 1 (
            echo ❌ Ошибка в %%f:
            type tmp_compile.log
            del tmp_compile.log
            goto error_exit
        ) else (
            echo ✓ %%f OK
        )
    ) else (
        echo ⚠️  %%f не найден (может не требуется)
    )
)
del tmp_compile.log 2>nul
echo.

REM 8. Очистка старых сборок
echo 📋 8. Очистка старых файлов...
if exist "build" rmdir /s /q build >nul 2>&1
if exist "dist" rmdir /s /q dist >nul 2>&1
if exist "__pycache__" rmdir /s /q __pycache__ >nul 2>&1
echo ✓ Очищено
echo.

REM 9. Пробная сборка
echo 📋 9. СБОРКА EXE (это может занять 2-5 минут)...
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
    main.py >tmp_build.log 2>&1

if errorlevel 1 (
    echo ❌ ОШИБКА ПРИ СБОРКЕ!
    echo.
    echo 📋 Лог ошибки (последние 50 строк):
    echo ================================================
    for /f "skip=999" %%A in ('find /c /v "" ^< tmp_build.log') do set "lines=%%A"
    more +%lines% tmp_build.log 2>nul || type tmp_build.log
    del tmp_build.log
    goto error_exit
) else (
    echo ✓ Сборка успешна!
    del tmp_build.log
)
echo.

REM 10. Проверка результата
echo 📋 10. Проверка результата...
if exist "dist\DotaCoach.exe" (
    for %%A in (dist\DotaCoach.exe) do (
        set "size=%%~zA"
    )
    echo ✓ DotaCoach.exe создан успешно!
    echo    Размер: %size% байт
) else (
    echo ❌ dist\DotaCoach.exe НЕ НАЙДЕН!
    goto error_exit
)
echo.

echo ============================================================
echo   ✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!
echo ============================================================
echo.
echo 📁 Результат в папке: dist\DotaCoach.exe
echo.
if exist "dist\DotaCoach.exe" (
    start explorer dist
)
pause
exit /b 0

:error_exit
echo.
echo ============================================================
echo   ❌ ОШИБКА! Сборка не может быть завершена
echo ============================================================
echo.
echo 🆘 РЕШЕНИЯ:
echo    1. Проверь что Python 3.10+ установлен
echo    2. Убедись что все файлы на месте
echo    3. Проверь интернет (нужен для pip)
echo    4. Попробуй удалить папку venv (если есть) и запустить заново
echo    5. Скопируй содержимое экрана выще и создай Issue на GitHub
echo.
pause
exit /b 1
