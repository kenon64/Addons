"""
Dota 2 WebAPI Integration
Получение реальных данных из OpenDota API и Stratz API
"""

import requests
import logging
from typing import Optional, Dict, List
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Dota2WebAPI:
    """Интеграция с Dota 2 WebAPI через OpenDota и Stratz"""
    
    def __init__(self, steam_id: Optional[str] = None, api_key: Optional[str] = None):
        """
        Args:
            steam_id: Steam ID игрока (32-bit format)
            api_key: Stratz API ключ (опционально)
        """
        self.steam_id = steam_id
        self.api_key = api_key
        
        # API endpoints
        self.opendota_base = "https://api.opendota.com/api"
        self.stratz_base = "https://api.stratz.com/graphql"
        
        self.cache_time = 30  # Кэш на 30 секунд
        self.last_fetch = 0
        self.cached_data = None
    
    def get_player_live_game(self) -> Optional[Dict]:
        """
        Получить информацию о текущей игре игрока
        Требует: Steam ID участника игры
        """
        if not self.steam_id:
            logger.warning("Steam ID не установлен, не могу получить live game")
            return None
        
        try:
            url = f"{self.opendota_base}/players/{self.steam_id}/recentMatches"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            matches = response.json()
            if matches and len(matches) > 0:
                match_id = matches[0]['match_id']
                logger.info(f"✓ Найдена матча: {match_id}")
                return self._parse_match_data(matches[0])
            
            return None
        except Exception as e:
            logger.error(f"Ошибка получения live game: {e}")
            return None
    
    def get_live_matches(self, hero_id: Optional[int] = None) -> List[Dict]:
        """
        Получить список текущих матчей
        Может фильтровать по герою
        """
        try:
            url = f"{self.opendota_base}/live"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            matches = response.json()
            logger.info(f"✓ Найдено live матчей: {len(matches)}")
            
            if hero_id:
                matches = [m for m in matches if self._hero_in_match(m, hero_id)]
            
            return matches[:10]  # Топ 10
        except Exception as e:
            logger.error(f"Ошибка получения live матчей: {e}")
            return []
    
    def get_hero_stats(self, hero_id: int) -> Optional[Dict]:
        """
        Получить статистику героя
        """
        try:
            url = f"{self.opendota_base}/heroStats"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            stats = response.json()
            hero_stat = next((h for h in stats if h['id'] == hero_id), None)
            
            if hero_stat:
                logger.info(f"✓ Статистика героя {hero_id} получена")
                return hero_stat
            
            return None
        except Exception as e:
            logger.error(f"Ошибка получения статистики героя: {e}")
            return None
    
    def get_hero_matchups(self, hero_id: int) -> Optional[Dict]:
        """
        Получить matchups героя (хорошие и плохие противники)
        """
        try:
            url = f"{self.opendota_base}/heroes/{hero_id}/matchups"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            matchups = response.json()
            logger.info(f"✓ Matchups для героя {hero_id} получены")
            
            return {
                "favorable": sorted(matchups, key=lambda x: x['wins'], reverse=True)[:5],
                "unfavorable": sorted(matchups, key=lambda x: x['wins'])[:5]
            }
        except Exception as e:
            logger.error(f"Ошибка получения matchups: {e}")
            return None
    
    def get_meta_heroes(self, limit: int = 10) -> List[Dict]:
        """
        Получить топ героев текущего meta
        """
        try:
            url = f"{self.opendota_base}/heroStats"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            stats = response.json()
            # Сортировать по win rate
            top_heroes = sorted(stats, key=lambda x: x.get('win', 0), reverse=True)[:limit]
            
            logger.info(f"✓ Получены топ {limit} героев meta")
            return top_heroes
        except Exception as e:
            logger.error(f"Ошибка получения meta: {e}")
            return []
    
    def _parse_match_data(self, match: Dict) -> Dict:
        """Преобразовать данные матчи в нужный формат"""
        return {
            "match_id": match.get('match_id'),
            "duration": match.get('duration', 0) // 60,  # В минуты
            "game_mode": match.get('game_mode'),
            "hero_id": match.get('hero_id'),
            "result": "win" if match.get('player_slot', 256) < 128 == match.get('radiant_win') else "loss",
            "kills": match.get('kills', 0),
            "deaths": match.get('deaths', 0),
            "assists": match.get('assists', 0),
            "last_hits": match.get('last_hits', 0),
            "gold": match.get('gold', 0),
            "xp_per_min": match.get('xp_per_min', 0),
            "gold_per_min": match.get('gold_per_min', 0),
        }
    
    def _hero_in_match(self, match: Dict, hero_id: int) -> bool:
        """Проверить если герой в матче"""
        players = match.get('players', [])
        return any(p.get('hero_id') == hero_id for p in players if p)


class StratzAPI:
    """Альтернативный API - Stratz (GraphQL)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stratz.com/graphql"
    
    def get_player_profile(self, steam_id: str) -> Optional[Dict]:
        """Получить профиль игрока через Stratz"""
        try:
            query = """
            query {
                player(steamAccountId: %s) {
                    id
                    steamAccount {
                        name
                    }
                    stats {
                        matchCount
                        winCount
                    }
                }
            }
            """ % steam_id
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.base_url,
                json={"query": query},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            
            data = response.json()
            if "data" in data and "player" in data["data"]:
                logger.info("✓ Профиль игрока получен из Stratz")
                return data["data"]["player"]
            
            return None
        except Exception as e:
            logger.error(f"Ошибка Stratz API: {e}")
            return None


class HybridGameAnalyzer:
    """
    Гибридный анализатор
    Использует реальные данные из API когда доступно,
    иначе использует симуляцию
    """
    
    def __init__(self, steam_id: Optional[str] = None, use_live: bool = False):
        self.dota_api = Dota2WebAPI(steam_id=steam_id)
        self.use_live = use_live
        self.fallback = True  # Использовать fallback если API не работает
    
    def get_game_state(self) -> Optional[Dict]:
        """Получить состояние игры - сначала пытаемся API, потом fallback"""
        
        if self.use_live:
            try:
                # Пытаемся получить реальные данные
                live_game = self.dota_api.get_player_live_game()
                if live_game:
                    logger.info("✓ Используются данные из Dota 2 WebAPI")
                    return self._convert_api_to_game_state(live_game)
            except Exception as e:
                logger.warning(f"Не удалось получить данные WebAPI: {e}")
        
        # Fallback на локальную симуляцию
        if self.fallback:
            logger.info("↳ Используется локальная симуляция")
            from game_integration import GameAnalyzer
            analyzer = GameAnalyzer()
            return analyzer.get_current_game_state()
        
        return None
    
    def _convert_api_to_game_state(self, api_data: Dict) -> Dict:
        """Преобразовать API данные в формат game_state"""
        return {
            "game_time": api_data.get('duration', 15),
            "hero_name": self._get_hero_name(api_data.get('hero_id')),
            "level": self._estimate_level(api_data.get('xp_per_min', 0), api_data.get('duration', 15)),
            "gold": api_data.get('gold', 2500),
            "last_hits": api_data.get('last_hits', 40),
            "kills": api_data.get('kills', 0),
            "deaths": api_data.get('deaths', 0),
            "assists": api_data.get('assists', 0),
            "gpm": api_data.get('gold_per_min', 400),
            "xpm": api_data.get('xp_per_min', 400),
        }
    
    def _get_hero_name(self, hero_id: int) -> str:
        """Получить имя героя по ID"""
        # Миниатюрный словарь (в реальности нужна полная база)
        heroes = {
            1: "Anti-Mage",
            2: "Axe",
            3: "Bane",
            11: "Shadow Fiend",
            16: "Tidehunter",
            20: "Phantom Assassin",
            # ... и т.д.
        }
        return heroes.get(hero_id, f"Hero#{hero_id}")
    
    def _estimate_level(self, xpm: int, game_time: int) -> int:
        """Оценить уровень по XPM и времени"""
        total_xp = xpm * game_time
        # Примерная калькуляция: каждый уровень требует большше XP
        return min(30, 1 + total_xp // 250)

