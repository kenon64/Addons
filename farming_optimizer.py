"""
Оптимизатор фарма - рассчитывает оптимальный маршрут сбора золота
"""

import logging
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FarmingType(Enum):
    """Типы фарма"""
    LANE = "lane"           # На линии против крипов
    JUNGLE = "jungle"       # В лесу (древние, нейтралы)
    CAMP = "camp"           # Отдельный камп нейтралов
    STACK = "stack"         # Стакованный камп
    ROSHAN = "roshan"       # Рошан


@dataclass
class FarmSpot:
    """Точка фарма - место скопления мобов"""
    name: str                      # Название спота
    position: Tuple[float, float]  # (x, y) координаты на миникарте
    gold_per_minute: float         # Золото в минуту
    difficulty: float              # Сложность (0-1, где 1 = опасно)
    farm_type: FarmingType         # Тип фарма
    distance_to_base: float        # Расстояние до базы для отступления
    time_to_clear: float           # Время очистки в секундах


class FarmingOptimizer:
    """Оптимизатор маршрутов фарма"""
    
    def __init__(self):
        self.farm_spots = self._initialize_farm_spots()
        self.hero_position = (500, 500)  # Текущая позиция героя
        self.last_farm_route = None
        self.current_objective = None
        
    def _initialize_farm_spots(self) -> List[FarmSpot]:
        """Инициализировать известные споты фарма для Дота 2"""
        
        spots = [
            # LANE CREEPS (на линиях)
            FarmSpot(
                name="Боттом линия (крипы)",
                position=(100, 800),
                gold_per_minute=8,
                difficulty=0.3,
                farm_type=FarmingType.LANE,
                distance_to_base=400,
                time_to_clear=20
            ),
            FarmSpot(
                name="Мид линия (крипы)",
                position=(512, 512),
                gold_per_minute=8,
                difficulty=0.5,
                farm_type=FarmingType.LANE,
                distance_to_base=300,
                time_to_clear=20
            ),
            FarmSpot(
                name="Топ линия (крипы)",
                position=(900, 200),
                gold_per_minute=8,
                difficulty=0.4,
                farm_type=FarmingType.LANE,
                distance_to_base=500,
                time_to_clear=20
            ),
            
            # JUNGLE CAMPS (нейтральные джунгль-кампы)
            FarmSpot(
                name="Древние (красные)",
                position=(600, 650),
                gold_per_minute=15,
                difficulty=0.4,
                farm_type=FarmingType.JUNGLE,
                distance_to_base=200,
                time_to_clear=45
            ),
            FarmSpot(
                name="Нейтралы (саткейн)",
                position=(380, 580),
                gold_per_minute=10,
                difficulty=0.3,
                farm_type=FarmingType.JUNGLE,
                distance_to_base=150,
                time_to_clear=30
            ),
            FarmSpot(
                name="Нейтралы (ночной сад)",
                position=(650, 400),
                gold_per_minute=10,
                difficulty=0.3,
                farm_type=FarmingType.JUNGLE,
                distance_to_base=250,
                time_to_clear=30
            ),
            FarmSpot(
                name="Нейтралы (северный камп)",
                position=(300, 300),
                gold_per_minute=10,
                difficulty=0.4,
                farm_type=FarmingType.JUNGLE,
                distance_to_base=400,
                time_to_clear=30
            ),
            
            # STACKED CAMPS (стакованные кампы)
            FarmSpot(
                name="Стакованный камп мага",
                position=(450, 350),
                gold_per_minute=25,
                difficulty=0.6,
                farm_type=FarmingType.STACK,
                distance_to_base=300,
                time_to_clear=60
            ),
            
            # ROSHAN
            FarmSpot(
                name="Рошан",
                position=(700, 300),
                gold_per_minute=50,
                difficulty=0.9,
                farm_type=FarmingType.ROSHAN,
                distance_to_base=500,
                time_to_clear=120
            ),
        ]
        
        logger.info(f"✓ Инициализирован {len(spots)} спотов фарма")
        return spots

    def calculate_farm_route(self, hero_position: Tuple[float, float],
                           inventory_space: int = 6,
                           team_danger_level: float = 0.5) -> List[FarmSpot]:
        """
        Рассчитать оптимальный маршрут фарма
        
        Args:
            hero_position: Текущая позиция героя
            inventory_space: Свободные слоты в инвентаре
            team_danger_level: Уровень опасности (0-1)
            
        Returns:
            Список спотов в оптимальном порядке
        """
        self.hero_position = hero_position
        
        # Фильтровать опасные споты
        safe_spots = [
            spot for spot in self.farm_spots
            if spot.difficulty < (1.0 - team_danger_level)
        ]
        
        if not safe_spots:
            logger.warning("⚠️ Нет безопасных спотов для фарма")
            return []
        
        # Сортировать по эффективности (золото/расстояние)
        route = self._optimize_route(hero_position, safe_spots)
        self.last_farm_route = route
        
        logger.info(f"📍 Рассчитан маршрут фарма: {[s.name for s in route[:3]]}")
        return route

    def _optimize_route(self, current_pos: Tuple[float, float],
                       spots: List[FarmSpot]) -> List[FarmSpot]:
        """
        Оптимизировать порядок посещения спотов (TSP-like)
        
        Использует простую эвристику: ближайший непосещённый спот
        """
        route = []
        unvisited = spots.copy()
        current = current_pos
        
        while unvisited:
            # Найти ближайший спот
            nearest = min(
                unvisited,
                key=lambda s: self._distance(current, s.position)
            )
            
            # Рассчитать "эффективность" спота
            distance = self._distance(current, nearest.position)
            efficiency = (nearest.gold_per_minute / max(distance, 1)) * (1 - nearest.difficulty)
            
            nearest.efficiency = efficiency
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest.position
        
        # Сортировать по эффективности
        route.sort(key=lambda s: s.efficiency, reverse=True)
        
        return route

    def _distance(self, pos1: Tuple[float, float],
                 pos2: Tuple[float, float]) -> float:
        """Рассчитать расстояние между двумя точками"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def get_next_spot(self) -> Dict:
        """
        Получить следующий рекомендуемый спот для фарма
        
        Returns:
            Словарь с информацией о следующем споте
        """
        if not self.last_farm_route:
            return {"status": "no_route", "message": "Маршрут не рассчитан"}
        
        next_spot = self.last_farm_route[0]
        distance = self._distance(self.hero_position, next_spot.position)
        
        return {
            "status": "success",
            "spot_name": next_spot.name,
            "position": next_spot.position,
            "distance": distance,
            "gold_per_minute": next_spot.gold_per_minute,
            "time_to_clear": next_spot.time_to_clear,
            "difficulty": next_spot.difficulty,
            "type": next_spot.farm_type.value,
            "recommendation": self._generate_recommendation(next_spot, distance)
        }

    def _generate_recommendation(self, spot: FarmSpot, distance: float) -> str:
        """Генерировать текстовую рекомендацию"""
        if distance < 50:
            return f"Начни фарм в {spot.name}"
        elif distance < 200:
            return f"Направляйся в {spot.name} ({int(distance)}м)"
        else:
            return f"Отправляйся в {spot.name}, это оптимальный спот"

    def analyze_current_position(self, hero_pos: Tuple[float, float]) -> Dict:
        """
        Анализировать текущую позицию героя и дать совет
        
        Returns:
            Анализ текущей ситуации фарма
        """
        # Найти ближайший спот
        nearest_spot = min(
            self.farm_spots,
            key=lambda s: self._distance(hero_pos, s.position)
        )
        
        distance = self._distance(hero_pos, nearest_spot.position)
        
        analysis = {
            "nearest_spot": nearest_spot.name,
            "distance": distance,
            "spot_efficiency": nearest_spot.gold_per_minute / max(distance, 1),
            "recommendation": "",
            "warning": None
        }
        
        # Рекомендация
        if distance < 50:
            analysis["recommendation"] = f"Отличная позиция для фарма {nearest_spot.name}!"
        elif distance < 150:
            analysis["recommendation"] = f"Близко к {nearest_spot.name}"
        else:
            analysis["recommendation"] = f"Переместись в {nearest_spot.name}"
        
        # Предупреждение об опасности
        if nearest_spot.difficulty > 0.8:
            analysis["warning"] = "⚠️ ОПАСНАЯ ПОЗИЦИЯ!"
        elif nearest_spot.difficulty > 0.6:
            analysis["warning"] = "⚠️ Осторожно, враги рядом"
        
        return analysis

    def get_farm_statistics(self) -> Dict:
        """Получить статистику по фарму"""
        return {
            "total_spots": len(self.farm_spots),
            "lane_creeps_spots": len([s for s in self.farm_spots if s.farm_type == FarmingType.LANE]),
            "jungle_spots": len([s for s in self.farm_spots if s.farm_type == FarmingType.JUNGLE]),
            "stack_spots": len([s for s in self.farm_spots if s.farm_type == FarmingType.STACK]),
            "max_gpm": max(s.gold_per_minute for s in self.farm_spots),
            "dangerous_spots": len([s for s in self.farm_spots if s.difficulty > 0.7])
        }
