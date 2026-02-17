"""
Анализатор состояния Dota 2
Получение и анализ информации об игре
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime
import psutil
import random  # НОВОЕ: случайные вариации

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameAnalyzer:
    def __init__(self, process_name: str = "dota2.exe"):
        self.process_name = process_name
        self.is_game_active = False
        self.game_state_history = []
        self.last_update = None
        self.game_time_offset = random.randint(10, 25)  # НОВОЕ: для вариативности

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

        # НОВОЕ: добавить вариативность
        game_time = self.game_time_offset + len(self.game_state_history) // 6  # растет со временем
        
        # Случайные вариации параметров
        hp_percent = random.randint(60, 100)
        max_hp = 500
        hp = int(max_hp * hp_percent / 100)
        
        gold = 2500 + (game_time * random.randint(150, 250))
        gold += random.randint(-300, 300)  # Небольшой шум
        
        last_hits = 40 + (game_time * 3) + random.randint(-5, 5)
        
        # Случайно враги поблизости
        nearby_enemy_count = random.randint(0, 2)
        
        # Примерное состояние игры (с вариациями!)
        game_state = {
            "game_time": game_time,  # Минуты - РАСТЕТ!
            "hero_name": "Anti-Mage",
            "hero_position": (420, 650),  # Позиция героя на миникарте
            "level": min(30, 5 + game_time // 3),  # Уровень растет
            "hp": hp,
            "max_hp": max_hp,
            "gold": gold,
            "items": ["Hand of Midas", "Power Treads"] if game_time > 10 else ["Boots"],
            "last_hits": last_hits,
            "denies": 3,
            "kills": 0,
            "deaths": 0,
            "assists": 2,
            "nearby_enemy_count": nearby_enemy_count,  # НОВОЕ
            
            "allies": [
                {"name": "Rubick", "level": max(5, 4 + game_time // 3), "position": "support", "hp_percent": 80},
                {"name": "Templar Assassin", "level": max(5, 5 + game_time // 3), "position": "midlane", "hp_percent": 100},
                {"name": "Tidehunter", "level": max(5, 4 + game_time // 3), "position": "offlane", "hp_percent": 70},
                {"name": "Shadow Shaman", "level": max(4, 3 + game_time // 3), "position": "support", "hp_percent": 60},
            ],
            
            "enemies": [
                {"name": "Phantom Assassin", "level": max(6, 5 + game_time // 3), "position": "carry", "visible": random.choice([True, False])},
                {"name": "Shadow Fiend", "level": max(7, 6 + game_time // 3), "position": "midlane", "visible": True},
                {"name": "Dark Seer", "level": max(5, 4 + game_time // 3), "position": "offlane", "visible": random.choice([True, False])},
                {"name": "Crystal Maiden", "level": max(4, 3 + game_time // 3), "position": "support", "visible": True},
                {"name": "Earthshaker", "level": max(5, 4 + game_time // 3), "position": "support", "visible": random.choice([True, False])},
            ],
            
            "team_gold": 12500 + (game_time * 800),
            "enemy_gold": 11800 + (game_time * 750),
            "recent_events": [
                "Ты получил First Blood" if game_time < 5 else "Идет мирный фарм",
                f"Anti-Mage получил {last_hits} последних удара",
                "Rubick использовал Telekinesis на Shadow Fiend" if random.random() > 0.5 else "Ганк отбит!",
                "Твоя команда контролирует карту" if random.random() > 0.5 else "Враги давят на линию",
            ],
            
            "timestamp": datetime.now().isoformat()
        }
        
        self.last_update = game_state
        self.game_state_history.append(game_state)
        
        logger.debug(f"Game State: Time={game_time}m, Gold={gold}, HP={hp_percent}%, Nearby enemies={nearby_enemy_count}")
        
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
