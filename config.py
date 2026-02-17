import os
from dotenv import load_dotenv

load_dotenv()

# Qwen Configuration
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-max")

# Dota 2 Configuration
DOTA2_PROCESS_NAME = os.getenv("DOTA2_PROCESS_NAME", "dota2.exe")
GAME_DETECTION_ENABLED = os.getenv("GAME_DETECTION_ENABLED", "true").lower() == "true"

# Voice Configuration
VOICE_ENGINE = os.getenv("VOICE_ENGINE", "google")
LANGUAGE = os.getenv("LANGUAGE", "ru_RU")

# Coach Configuration
ANALYSIS_INTERVAL = 30  # Интервал анализа в секундах
RECOMMENDATION_THRESHOLD = 0.7  # Минимальная уверенность для рекомендации

# Game State Monitoring
HERO_ROLES = {
    "carry": ["Anti-Mage", "Phantom Assassin", "Juggernaut"],
    "midlaner": ["Shadow Fiend", "Puck", "Templar Assassin"],
    "support": ["Crystal Maiden", "Lion", "Rubick"],
    "offlane": ["Tidehunter", "Centaur", "Dark Seer"],
}

# Recommendation types
RECOMMENDATION_TYPES = {
    "positioning": "Позиционирование",
    "farming": "Фарм",
    "teamfight": "Участие в боях",
    "objectives": "Боевые цели",
    "items": "Закупка предметов",
    "escape": "Безопасность",
}
