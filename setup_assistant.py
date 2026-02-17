"""
Setup Assistant - помощник для первого запуска
Позволяет выбрать источник данных и настроить API
"""

import logging
import os
from typing import Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SetupAssistant:
    """Помощник для настройки приложения"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.config = {}
    
    def run_setup(self) -> dict:
        """Запустить интерактивную настройку"""
        print("\n" + "="*60)
        print("🎮 DOTA COACH - ПЕРВОНАЧАЛЬНАЯ НАСТРОЙКА")
        print("="*60 + "\n")
        
        # 1. Выбрать источник данных
        self.config['data_source'] = self._choose_data_source()
        
        # 2. Если выбран API - запросить конфиги
        if self.config['data_source'] == 'api':
            self.config['steam_id'] = self._get_steam_id()
            self.config['use_live'] = self._confirm("Использовать live данные из Dota 2 WebAPI?")
        
        # 3. Настроить Qwen AI (опционально)
        self.config['use_qwen'] = self._confirm("Настроить Qwen AI (для улучшенного анализа)?")
        if self.config['use_qwen']:
            self.config['qwen_api_key'] = self._get_qwen_key()
        
        # 4. Сохранить конфиг
        self._save_config()
        
        print("\n" + "="*60)
        print("✅ НАСТРОЙКА ЗАВЕРШЕНА!")
        print("="*60)
        print("\nПрограмма готова к работе. Запустите её еще раз.\n")
        
        return self.config
    
    def _choose_data_source(self) -> str:
        """Выбрать источник данных"""
        print("📊 ВЫБЕРИТЕ ИСТОЧНИК ДАННЫХ:")
        print("1️⃣  Локальная симуляция (нет требований) - БЫСТРО ⚡")
        print("2️⃣  Dota 2 WebAPI (реальные данные) - ТОЧНО 🎯")
        print("3️⃣  Оба (гибридный режим) - УНИВЕРСАЛЬНО 🔄\n")
        
        while True:
            choice = input("Выберите (1/2/3): ").strip()
            if choice == '1':
                print("✓ Выбрана локальная симуляция\n")
                return 'local'
            elif choice == '2':
                print("✓ Выбран Dota 2 WebAPI\n")
                return 'api'
            elif choice == '3':
                print("✓ Выбран гибридный режим\n")
                return 'hybrid'
            else:
                print("❌ Неверный выбор, попробуйте снова (1/2/3)\n")
    
    def _get_steam_id(self) -> str:
        """Получить Steam ID"""
        print("🔑 НАСТРОЙКА DOTA 2 WEBAPI")
        print("-" * 60)
        print("Нужен ваш Steam ID 32-bit формате")
        print("Узнать можно здесь: https://steamid.io/\n")
        
        while True:
            steam_id = input("Введите Steam ID (или пропустите нажав Enter): ").strip()
            if not steam_id:
                print("⏭️  Пропущено - будет использована локальная симуляция\n")
                return ""
            elif steam_id.isdigit() and len(steam_id) >= 6:
                print(f"✓ Steam ID сохранен: {steam_id}\n")
                return steam_id
            else:
                print("❌ Неверный формат Steam ID, попробуйте снова\n")
    
    def _get_qwen_key(self) -> str:
        """Получить Qwen API ключ"""
        print("\n🤖 НАСТРОЙКА QWEN AI")
        print("-" * 60)
        print("Для улучшенного анализа нужен ключ от Alibaba Qwen")
        print("Получить можно здесь: https://dashscope.aliyuncs.com/\n")
        
        key = input("Введите QWEN_API_KEY (или пропустите): ").strip()
        
        if key:
            print(f"✓ QWEN API ключ сохранен (первые 10 символов: {key[:10]}...)\n")
            return key
        else:
            print("⏭️  Пропущено - будет использован локальный анализ\n")
            return ""
    
    def _confirm(self, question: str) -> bool:
        """Получить подтверждение"""
        while True:
            response = input(f"\n{question} (да/нет): ").strip().lower()
            if response in ['да', 'yes', 'y', '1']:
                return True
            elif response in ['нет', 'no', 'n', '0']:
                return False
            else:
                print("❌ Ответьте 'да' или 'нет'")
    
    def _save_config(self):
        """Сохранить конфиг в .env"""
        print("\n💾 Сохраняю конфигурацию...")
        
        # Читать существующий .env
        env_content = ""
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r', encoding='utf-8') as f:
                env_content = f.read()
        
        # Обновить значения
        env_dict = self._parse_env(env_content)
        
        if self.config['data_source'] in ['api', 'hybrid']:
            if self.config.get('steam_id'):
                env_dict['STEAM_ID'] = self.config['steam_id']
            env_dict['USE_LIVE_GAME'] = 'true' if self.config.get('use_live') else 'false'
        
        env_dict['DATA_SOURCE'] = self.config['data_source']
        
        if self.config.get('qwen_api_key'):
            env_dict['QWEN_API_KEY'] = self.config['qwen_api_key']
        
        # Написать обновленный .env
        self._write_env(env_dict)
        print("✓ Конфиг сохранен в .env\n")
    
    def _parse_env(self, content: str) -> dict:
        """Парсить .env файл"""
        env_dict = {}
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_dict[key.strip()] = value.strip()
        return env_dict
    
    def _write_env(self, env_dict: dict):
        """Написать .env файл"""
        with open(self.env_file, 'w', encoding='utf-8') as f:
            for key, value in env_dict.items():
                f.write(f"{key}={value}\n")


def run_first_time_setup() -> bool:
    """Запустить setup если нужно"""
    # Проверить если .env существует и содержит конфиг
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'DATA_SOURCE' in content:
                return False  # Уже настроено
    
    # Запустить setup
    setup = SetupAssistant()
    setup.run_setup()
    return True

