"""
Dota 2 WebAPI Integration
Портирована логика из https://github.com/egger0a6/dota-web-api
Получение реальных данных из официального Steam API
"""

import requests
import logging
from typing import Optional, Dict, List
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Dota2WebAPI:
    """Полная интеграция с официальным Steam Dota 2 API"""
    
    # API Constants
    APP_ID = 570
    API_URL = "http://api.steampowered.com"
    STATIC_CDN = "http://cdn.dota2.com/apps/dota2/images"
    MATCH_INTERFACE = f"IDOTA2Match_{APP_ID}"
    ECONOMY_INTERFACE = f"IEconDOTA2_{APP_ID}"
    
    def __init__(self, steam_api_key: str):
        """
        Args:
            steam_api_key: Steam API ключ с https://steamcommunity.com/dev/apikey
        """
        self.api_key = steam_api_key
        self.heroes = {}
        self.items = {}
        
        # Загрузить статические данные
        self._load_heroes()
        self._load_items()
    
    def get_match_details(self, match_id: int) -> Optional[Dict]:
        """Получить полные детали матча по ID"""
        try:
            params = {
                'key': self.api_key,
                'match_id': match_id
            }
            url = f"{self.API_URL}/{self.MATCH_INTERFACE}/GetMatchDetails/v1"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('result'):
                logger.info(f"✓ Матча {match_id} загружена")
                return data['result']
            return None
        except Exception as e:
            logger.error(f"Ошибка получения матчи: {e}")
            return None
    
    def get_match_history(self, account_id: int, hero_id: Optional[int] = None, 
                         skill: Optional[int] = None, matches_requested: int = 20) -> Optional[List[Dict]]:
        """
        Получить историю матчей игрока
        
        Args:
            account_id: Account ID игрока (32-bit)
            hero_id: (опционально) Фильтр по герою
            skill: (опционально) Уровень - 0=Any, 1=Normal, 2=High, 3=VeryHigh
            matches_requested: Кол-во матчей
        """
        try:
            params = {
                'key': self.api_key,
                'account_id': account_id,
                'matches_requested': matches_requested
            }
            if hero_id:
                params['hero_id'] = hero_id
            if skill is not None:
                params['skill'] = skill
            
            url = f"{self.API_URL}/{self.MATCH_INTERFACE}/GetMatchHistory/v1"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('result', {}).get('matches'):
                logger.info(f"✓ История матчей {account_id} загружена ({len(data['result']['matches'])} матч)")
                return data['result']['matches']
            return None
        except Exception as e:
            logger.error(f"Ошибка получения истории матчей: {e}")
            return None
    
    def get_live_league_games(self) -> Optional[List[Dict]]:
        """Получить текущие live матчи лиги"""
        try:
            params = {'key': self.api_key}
            url = f"{self.API_URL}/{self.MATCH_INTERFACE}/GetLiveLeagueGames/v1"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('result', {}).get('games'):
                logger.info(f"✓ Загружено live матчей: {len(data['result']['games'])}")
                return data['result']['games']
            return None
        except Exception as e:
            logger.error(f"Ошибка получения live матчей: {e}")
            return None
    
    def get_team_info(self, start_team_id: Optional[int] = None, teams_requested: int = 20) -> Optional[List[Dict]]:
        """Получить информацию о профессиональных командах"""
        try:
            params = {
                'key': self.api_key,
                'teams_requested': teams_requested
            }
            if start_team_id:
                params['start_at_team_id'] = start_team_id
            
            url = f"{self.API_URL}/{self.MATCH_INTERFACE}/GetTeamInfoByTeamID/v1"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('result', {}).get('teams'):
                logger.info(f"✓ Информация о командах загружена")
                return data['result']['teams']
            return None
        except Exception as e:
            logger.error(f"Ошибка получения информации о командах: {e}")
            return None
    
    def get_hero_stats(self) -> Dict:
        """Получить статистику всех героев"""
        if self.heroes:
            return self.heroes
        self._load_heroes()
        return self.heroes
    
    def get_items(self) -> Dict:
        """Получить список всех предметов"""
        if self.items:
            return self.items
        self._load_items()
        return self.items
    
    def _load_heroes(self):
        """Загрузить список героев"""
        try:
            params = {'key': self.api_key}
            url = f"{self.API_URL}/{self.ECONOMY_INTERFACE}/GetHeroes/v1"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('result', {}).get('heroes'):
                for hero in data['result']['heroes']:
                    name = hero.get('name', '').replace('npc_dota_hero_', '')
                    hero['localized_name'] = name
                    hero['images'] = {
                        'sb': f"{self.STATIC_CDN}/heroes/{name}_sb.png",
                        'lg': f"{self.STATIC_CDN}/heroes/{name}_lg.png",
                        'full': f"{self.STATIC_CDN}/heroes/{name}_full.png",
                    }
                    self.heroes[name] = hero
                logger.info(f"✓ Загружено героев: {len(self.heroes)}")
        except Exception as e:
            logger.warning(f"⚠️  Не удалось загрузить героев: {e}")
    
    def _load_items(self):
        """Загрузить список предметов"""
        try:
            params = {'key': self.api_key}
            url = f"{self.API_URL}/{self.ECONOMY_INTERFACE}/GetGameItems/v1"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('result', {}).get('items'):
                for item in data['result']['items']:
                    name = item.get('name', '').replace('item_', '')
                    item['localized_name'] = name
                    item['images'] = {
                        'lg': f"{self.STATIC_CDN}/items/{name}_lg.png",
                    }
                    self.items[name] = item
                logger.info(f"✓ Загружено предметов: {len(self.items)}")
        except Exception as e:
            logger.warning(f"⚠️  Не удалось загрузить предметы: {e}")
    
    def player_summary(self, account_ids: List[int]) -> Dict[int, Dict]:
        """
        Получить краткую информацию об игроках из их профилей
        Требует дополнительного использования ISteamUser API
        """
        try:
            params = {
                'key': self.api_key,
                'steamids': ','.join(str(32 + aid) for aid in account_ids),  # Конвертировать в 64-bit
            }
            url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('response', {}).get('players'):
                logger.info(f"✓ Информация о {len(data['response']['players'])} игроках загружена")
                return {p.get('accountid'): p for p in data['response']['players']}
            return {}
        except Exception as e:
            logger.warning(f"⚠️  Ошибка получения информации об игроках: {e}")
            return {}


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

