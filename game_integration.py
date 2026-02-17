"""
Анализатор состояния Dota 2
Получение и анализ информации об игре
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime
import psutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameAnalyzer:
    def __init__(self, process_name: str = "dota2.exe"):
        self.process_name = process_name
        self.is_game_active = False
        self.game_state_history = []
        self.last_update = None

    def check_game_running(self) -> bool:
        """Проверить, запущена ли Dota 2"""
        try:
            for proc in psutil.process_iter(['name']):
                if self.process_name.lower() in proc.info['name'].lower():
                    self.is_game_active = True
                    logger.info("✓ Dota 2 запущена")
                    return True
            self.is_game_active = False
            logger.warning("✗ Dota 2 не запущена")
            return False
        except Exception as e:
            logger.error(f"Ошибка при проверке процесса: {e}")
            return False

    def get_current_game_state(self) -> Optional[Dict]:
        """
        Получить текущее состояние игры
        
        В полной реализации здесь будет:
        - Чтение из Dota 2 API
        - Парсинг информации с экрана
        - Анализ логов игры
        
        Returns:
            Словарь с состоянием игры или None
        """
        if not self.check_game_running():
            return None

        # Примерное состояние игры (в реальности будет получаться из API/экрана)
        game_state = {
            "game_time": 15,  # Минуты
            "hero_name": "Anti-Mage",
            "hero_position": (420, 650),  # Позиция героя на миникарте
            "level": 7,
            "hp": 450,
            "max_hp": 500,
            "gold": 2500,
            "items": ["Hand of Midas", "Power Treads"],
            "last_hits": 45,
            "denies": 3,
            "kills": 0,
            "deaths": 0,
            "assists": 2,
            
            "allies": [
                {"name": "Rubick", "level": 6, "position": "support", "hp_percent": 80},
                {"name": "Templar Assassin", "level": 7, "position": "midlane", "hp_percent": 100},
                {"name": "Tidehunter", "level": 6, "position": "offlane", "hp_percent": 70},
                {"name": "Shadow Shaman", "level": 5, "position": "support", "hp_percent": 60},
            ],
            
            "enemies": [
                {"name": "Phantom Assassin", "level": 7, "position": "carry", "visible": False},
                {"name": "Shadow Fiend", "level": 8, "position": "midlane", "visible": True},
                {"name": "Dark Seer", "level": 6, "position": "offlane", "visible": True},
                {"name": "Crystal Maiden", "level": 5, "position": "support", "visible": True},
                {"name": "Earthshaker", "level": 6, "position": "support", "visible": False},
            ],
            
            "team_gold": 12500,
            "enemy_gold": 11800,
            "recent_events": [
                "Ты получил First Blood",
                "Anti-Mage получил 2 последних удара",
                "Rubick использовал Telekinesis на Shadow Fiend",
                "Твоя команда захватила Roshan Pit",
            ],
            
            "timestamp": datetime.now().isoformat()
        }
        
        self.last_update = game_state
        self.game_state_history.append(game_state)
        
        return game_state

    def analyze_threats(self, game_state: Dict) -> List[Dict]:
        """
        Анализировать угрозы на карте
        
        Args:
            game_state: Текущее состояние игры
            
        Returns:
            Список угроз с приоритетами
        """
        threats = []
        
        for enemy in game_state.get('enemies', []):
            if enemy.get('visible'):
                threat_level = self._calculate_threat(game_state, enemy)
                if threat_level > 0.5:
                    threats.append({
                        "hero": enemy['name'],
                        "position": enemy.get('position', 'unknown'),
                        "threat_level": threat_level,
                        "description": self._threat_description(threat_level)
                    })
        
        # Сортировать по приоритету
        threats.sort(key=lambda x: x['threat_level'], reverse=True)
        return threats

    def _calculate_threat(self, game_state: Dict, enemy: Dict) -> float:
        """Рассчитать уровень угрозы от героя"""
        threat = 0.0
        
        # Враги с большим преимуществом
        if enemy.get('level', 0) > game_state.get('level', 0):
            threat += 0.3
        
        # Враги с опасными льготами
        dangerous_heroes = ["Phantom Assassin", "Shadow Fiend", "Earthshaker"]
        if enemy.get('name') in dangerous_heroes:
            threat += 0.2
        
        return min(threat, 1.0)

    def _threat_description(self, threat_level: float) -> str:
        """Описание уровня угрозы"""
        if threat_level > 0.7:
            return "Критическая угроза!"
        elif threat_level > 0.5:
            return "Серьёзная угроза"
        return "Минимальная угроза"

    def get_current_objectives(self, game_state: Dict) -> List[str]:
        """Определить текущие стратегические цели"""
        objectives = []
        game_time = game_state.get('game_time', 0)
        
        if game_time < 10:
            objectives.append("Зарабатывай уровни на линии")
            objectives.append("Не совершай рискованных движений")
        elif game_time < 20:
            objectives.append("Завершай предметы")
            objectives.append("Помогай команде с ганками")
        elif game_time < 30:
            objectives.append("Участвуй в командных боях")
            objectives.append("Захватывай Roshan")
        else:
            objectives.append("Координируйся с командой")
            objectives.append("Защищай барраки")
        
        return objectives
