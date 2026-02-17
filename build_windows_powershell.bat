@REM ============================================================
@REM DotaCoach Build Script - PowerShell версия
@REM Более надёжная версия с лучшей диагностикой
@REM ============================================================

@echo off
setlocal enabledelayedexpansion

REM Проверка наличия PowerShell
where powershell >nul 2>&1
if errorlevel 1 (
    echo ❌ PowerShell не найден в системе
    pause
    exit /b 1
)

REM Запуск PowerShell скрипта
echo 🔍 Запускаю диагностику системы...
powershell -NoProfile -ExecutionPolicy Bypass -Command "
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor [System.Net.SecurityProtocolType]::Tls12

# Проверка Python
\$pythonVersions = @(
    'C:\Python312\python.exe',
    'C:\Python311\python.exe',
    'C:\Python310\python.exe',
    'C:\Program Files\Python312\python.exe',
    'C:\Program Files\Python311\python.exe'
)

\$pythonFound = \$null

# Попытка 1: Поиск по PATH
try {
    \$pythonFound = (Get-Command python -ErrorAction Stop).Source
    Write-Host 'Python найден в PATH: ' -NoNewline
    Write-Host \$pythonFound -ForegroundColor Green
} catch {
    # Попытка 2: Поиск в стандартных местах
    foreach (\$path in \$pythonVersions) {
        if (Test-Path \$path) {
            \$pythonFound = \$path
            Write-Host 'Python найден: ' -NoNewline
            Write-Host \$path -ForegroundColor Green
            break
        }
    }
}

if (-not \$pythonFound) {
    Write-Host '❌ ОШИБКА: Python не найден в системе!' -ForegroundColor Red
    Write-Host ''
    Write-Host '📥 РЕШЕНИЕ:' -ForegroundColor Yellow
    Write-Host '1. Открой: https://www.python.org/downloads/' -ForegroundColor Yellow
    Write-Host '2. Скачай Python 3.10 или выше' -ForegroundColor Yellow
    Write-Host '3. ⭐ ПРИ УСТАНОВКЕ отметь: Add Python to PATH' -ForegroundColor Yellow
    Write-Host '4. Перезагрузи компьютер' -ForegroundColor Yellow
    Write-Host '5. Запусти этот скрипт снова' -ForegroundColor Yellow
    Write-Host ''
    Read-Host 'Нажми Enter для выхода'
    exit 1
}

# Проверка версии
Write-Host 'Проверяю версию Python...' 
\$version = & \$pythonFound --version 2>&1
Write-Host \$version -ForegroundColor Green

# Запуск основного скрипта сборки
Write-Host ''
Write-Host '=====================================' -ForegroundColor Cyan
Write-Host '  🎮 СБОРКА DotaCoach.exe' -ForegroundColor Cyan
Write-Host '=====================================' -ForegroundColor Cyan
Write-Host ''

# Установка pip
Write-Host '📦 Обновляю pip...' -ForegroundColor Yellow
& \$pythonFound -m pip install --upgrade pip

# Установка зависимостей
Write-Host '📦 Устанавливаю зависимости...' -ForegroundColor Yellow
& \$pythonFound -m pip install -r requirements.txt

if (\$LASTEXITCODE -ne 0) {
    Write-Host '❌ Ошибка при установке зависимостей!' -ForegroundColor Red
    Read-Host 'Нажми Enter для выхода'
    exit 1
}

Write-Host '✓ Зависимости установлены' -ForegroundColor Green

# Установка PyInstaller
Write-Host '🔍 Устанавливаю PyInstaller...' -ForegroundColor Yellow
& \$pythonFound -m pip install PyInstaller==6.1.0

Write-Host '✓ PyInstaller готов' -ForegroundColor Green

# Очистка старых сборок
Write-Host ''
Write-Host '🧹 Очищаю старые файлы...' -ForegroundColor Yellow
if (Test-Path 'build') { Remove-Item -Recurse -Force 'build' }
if (Test-Path 'dist') { Remove-Item -Recurse -Force 'dist' }
if (Test-Path '__pycache__') { Remove-Item -Recurse -Force '__pycache__' }
Write-Host '✓ Очищено' -ForegroundColor Green

# Сборка exe
Write-Host ''
Write-Host '🔨 Собираю exe файл...' -ForegroundColor Yellow
Write-Host '   (это может занять несколько минут)' -ForegroundColor Gray
Write-Host ''

& \$pythonFound -m PyInstaller --onefile `
    --windowed `
    --name 'DotaCoach' `
    --add-data '.env.example;.' `
    --hidden-import=speech_recognition `
    --hidden-import=pyttsx3 `
    --hidden-import=requests `
    --hidden-import=psutil `
    --hidden-import=dotenv `
    main.py

if (\$LASTEXITCODE -ne 0) {
    Write-Host ''
    Write-Host '❌ Ошибка при сборке!' -ForegroundColor Red
    Read-Host 'Нажми Enter для выхода'
    exit 1
}

Write-Host ''
Write-Host '=====================================' -ForegroundColor Green
Write-Host '   ✅ СБОРКА УСПЕШНО ЗАВЕРШЕНА!' -ForegroundColor Green
Write-Host '=====================================' -ForegroundColor Green
Write-Host ''
Write-Host '📁 Исполняемый файл: dist\DotaCoach.exe' -ForegroundColor Cyan
Write-Host ''
Write-Host '📝 Перед запуском:' -ForegroundColor Yellow
Write-Host '   1. Скопируй .env файл в папку с exe' -ForegroundColor Yellow
Write-Host '   2. Добавь QWEN_API_KEY в .env' -ForegroundColor Yellow
Write-Host '   3. Запусти DotaCoach.exe' -ForegroundColor Yellow
Write-Host ''

# Открыть папку
if (Test-Path 'dist\DotaCoach.exe') {
    Write-Host '📂 Открываю папку с результатом...' -ForegroundColor Cyan
    & explorer 'dist'
}

Write-Host ''
Read-Host 'Нажми Enter для выхода'
"