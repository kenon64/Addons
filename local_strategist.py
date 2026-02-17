"""
Локальный анализатор стратегии - работает БЕЗ API ключа
Анализирует Dota 2 ситуацию на основе правил и логики
"""

import logging
from typing import Dict, List, Optional
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdviceCategory(Enum):
    POSITIONING = "позиционирование"
    FARMING = "фарм" 
    SAFETY = "безопасность"
    TEAMFIGHT = "боевые действия"
    ITEMS = "предметы"
    ROAMING = "ротации"


class LocalStrategist:
    """Локальный анализатор игровой ситуации"""
    
    def __init__(self):
        self.hero_roles = {
            "carry": ["Anti-Mage", "Phantom Assassin", "Juggernaut", "Drow Ranger"],
            "midlaner": ["Shadow Fiend", "Puck", "Templar Assassin", "Storm Spirit"],
            "support": ["Crystal Maiden", "Lion", "Rubick", "Shadow Shaman"],
            "offlane": ["Tidehunter", "Centaur", "Dark Seer", "Underlord"],
        }
    
    def analyze_situation(self, game_state: Dict) -> Dict:
        """
        Анализировать текущую ситуацию и вернуть рекомендации
        """
        try:
            recommendations = []
            
            # Базовый анализ
            recommendations.extend(self._analyze_economy(game_state))
            recommendations.extend(self._analyze_safety(game_state))
            recommendations.extend(self._analyze_positioning(game_state))
            recommendations.extend(self._analyze_items(game_state))
            recommendations.extend(self._analyze_teamfight(game_state))
            
            # Сортировать по приоритету
            recommendations.sort(key=lambda x: x.get('priority', 0), reverse=True)
            
            return {
                "status": "success",
                "recommendations": recommendations[:3],  # Топ 3 совета
                "analysis": f"Анализировано {len(recommendations)} аспектов игры",
                "method": "local_analysis"
            }
        except Exception as e:
            logger.error(f"Ошибка анализа: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": []
            }
    
    def _analyze_economy(self, game_state: Dict) -> List[Dict]:
        """Анализ экономики (золото, фарм)"""
        advice = []
        gold = game_state.get('gold', 0)
        game_time = game_state.get('game_time', 0)
        last_hits = game_state.get('last_hits', 0)
        
        # Проверить золото
        expected_gpm = 400 + (game_time * 30)  # Примерно GPM
        if gold < expected_gpm * 0.8:
            advice.append({
                "type": "farming",
                "title": "Фарм отстает",
                "advice": "Фокусируйся на крипах. Ищи свободные линии или джунгль",
                "priority": 7,
                "category": AdviceCategory.FARMING
            })
        
        # Копить на предмет?
        if gold >= 1000 and not game_state.get('recently_shopped'):
            advice.append({
                "type": "items",
                "title": "Достаточно золота",
                "advice": "У тебя есть золото на важный предмет. Вернись в фонтан",
                "priority": 6,
                "category": AdviceCategory.ITEMS
            })
        
        return advice
    
    def _analyze_safety(self, game_state: Dict) -> List[Dict]:
        """Анализ безопасности (враги, hp)"""
        advice = []
        hp_percent = (game_state.get('hp', 0) / game_state.get('max_hp', 1)) * 100
        nearby_enemies = game_state.get('nearby_enemy_count', 0)
        
        # Низкий HP
        if hp_percent < 30:
            advice.append({
                "type": "safety",
                "title": "⚠️  Низкий HP!",
                "advice": "Отступи на безопасное расстояние и восстановись",
                "priority": 9,
                "category": AdviceCategory.SAFETY
            })
        
        # Враги поблизости
        if nearby_enemies >= 2 and hp_percent < 60:
            advice.append({
                "type": "safety",
                "title": "Враги приближаются",
                "advice": "Враги рядом. Отойди дальше или призови援助",
                "priority": 8,
                "category": AdviceCategory.SAFETY
            })
        
        return advice
    
    def _analyze_positioning(self, game_state: Dict) -> List[Dict]:
        """Анализ позиционирования"""
        advice = []
        game_time = game_state.get('game_time', 0)
        level = game_state.get('level', 1)
        hero = game_state.get('hero_name', '')
        
        # Ранняя игра
        if game_time < 10:
            advice.append({
                "type": "positioning",
                "title": "Раннее мидгейм",
                "advice": "Останавливайся на линии, рисуй опыт и золото для первого предмета",
                "priority": 5,
                "category": AdviceCategory.POSITIONING
            })
        
        # Видимо, Carry в раннюю кэрри время должен быть на линии
        if hero in self.hero_roles.get("carry", []) and game_time < 15:
            if game_state.get('position') != "lane":
                advice.append({
                    "type": "positioning",
                    "title": "Вернись на линию",
                    "advice": "Как кэрри, ты должен фармить на линии, а не роваться",
                    "priority": 6,
                    "category": AdviceCategory.POSITIONING
                })
        
        return advice
    
    def _analyze_items(self, game_state: Dict) -> List[Dict]:
        """Анализ покупки предметов"""
        advice = []
        items = game_state.get('items', [])
        hero = game_state.get('hero_name', '')
        level = game_state.get('level', 1)
        game_time = game_state.get('game_time', 0)
        
        # Предложить ранний предмет
        if game_time > 5 and len(items) == 0:
            advice.append({
                "type": "items",
                "title": "Купи первый предмет",
                "advice": "Попробуй Power Treads или Brown Boots для ускорения",
                "priority": 5,
                "category": AdviceCategory.ITEMS
            })
        
        return advice
    
    def _analyze_teamfight(self, game_state: Dict) -> List[Dict]:
        """Анализ групповых боев"""
        advice = []
        level = game_state.get('level', 1)
        heroes_nearby = len(game_state.get('allies', []))
        
        # Если рядом много героев
        if heroes_nearby >= 3:
            advice.append({
                "type": "teamfight",
                "title": "Возможен групповой бой",
                "advice": "Союзников много. Если враги покажутся - готовься к бою",
                "priority": 6,
                "category": AdviceCategory.TEAMFIGHT
            })
        
        return advice
    
    def get_hero_role_advice(self, hero_name: str, game_time: int) -> Optional[str]:
        """Рекомендация по ролям"""
        if game_time < 5:
            return "Получай опыт на стартовой позиции"
        elif game_time < 15:
            return "Фармишь линию или джунгль рядом"
        elif game_time < 35:
            return "Групповые бои и рошан"
        else:
            return "Ультимат игра - работай с командой"

