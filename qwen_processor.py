"""
Qwen Processor - анализ стратегии через Qwen AI
"""

import requests
import logging
import json
from typing import Optional, Dict, List
from config import QWEN_API_KEY, QWEN_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QwenStrategist:
    def __init__(self, api_key: Optional[str] = None, model: str = QWEN_MODEL):
        self.api_key = api_key or QWEN_API_KEY
        self.model = model
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    def analyze_situation(self, game_state: Dict) -> Dict:
        """
        Анализировать текущую игровую ситуацию и дать рекомендации
        
        Args:
            game_state: Словарь с информацией об игре
            
        Returns:
            Словарь с рекомендациями
        """
        try:
            prompt = self._build_analysis_prompt(game_state)
            response = self._call_qwen_api(prompt)
            
            recommendations = self._parse_recommendations(response)
            
            return {
                "status": "success",
                "recommendations": recommendations,
                "analysis": response,
                "timestamp": __import__('datetime').datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Ошибка анализа ситуации: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": []
            }

    def _build_analysis_prompt(self, game_state: Dict) -> str:
        """Построить промпт для анализа"""
        prompt = f"""
        Ты - опытный тренер по Dota 2. Твоя задача - анализировать игровую ситуацию 
        и давать стратегические рекомендации игроку.
        
        ТЕКУЩЕЕ СОСТОЯНИЕ ИГРЫ:
        ----------
        Время игры: {game_state.get('game_time', 'неизвестно')} минут
        Герой игрока: {game_state.get('hero_name', 'неизвестно')}
        Уровень: {game_state.get('level', 0)}
        Золото: {game_state.get('gold', 0)}
        HP: {game_state.get('hp', 0)}/{game_state.get('max_hp', 0)}
        
        ПРЕДМЕТЫ ИГРОКА: {', '.join(game_state.get('items', []))}
        
        ПОЗИЦИИ НА КАРТЕ:
        Союзники:
        {self._format_team(game_state.get('allies', []))}
        
        Враги:
        {self._format_team(game_state.get('enemies', []))}
        
        ПОСЛЕДНИЕ СОБЫТИЯ:
        {self._format_events(game_state.get('recent_events', []))}
        
        ----------
        
        Дай 2-3 конкретных стратегических рекомендации для игрока в следующем формате:
        
        РЕКОМЕНДАЦИЯ 1:
        Тип: [позиционирование/фарм/боевые цели/безопасность/другое]
        Совет: [конкретный совет]
        Обоснование: [почему это важно сейчас]
        
        РЕКОМЕНДАЦИЯ 2:
        [аналогично]
        
        Помни: не играй за игрока, давай рекомендации, которые помогут ему принять решение.
        """
        return prompt

    def _format_team(self, team_members: List[Dict]) -> str:
        """Форматировать информацию о команде"""
        result = []
        for member in team_members:
            result.append(f"  - {member.get('name', 'Unknown')}: уровень {member.get('level', 0)}, "
                         f"позиция {member.get('position', 'unknown')}")
        return "\n".join(result) if result else "  (информация отсутствует)"

    def _format_events(self, events: List[str]) -> str:
        """Форматировать события"""
        if not events:
            return "  (нет событий)"
        return "\n".join([f"  - {event}" for event in events[-5:]])  # Последние 5 событий

    def _call_qwen_api(self, prompt: str) -> str:
        """Вызвать API Qwen"""
        if not self.api_key:
            logger.warning("QWEN_API_KEY не установлен")
            return self._get_fallback_recommendation()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": {"messages": [{"role": "user", "content": prompt}]},
            "parameters": {"temperature": 0.7, "max_tokens": 500}
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            result = response.json()
            
            if "output" in result and "text" in result["output"]:
                return result["output"]["text"]
            
            logger.warning(f"Неожиданный формат ответа: {result}")
            return self._get_fallback_recommendation()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка API запроса: {e}")
            return self._get_fallback_recommendation()

    def _get_fallback_recommendation(self) -> str:
        """Базовая рекомендация без API"""
        return """
        РЕКОМЕНДАЦИЯ 1:
        Тип: позиционирование
        Совет: Остаёмся на линии и зарабатываем опыт
        Обоснование: Ранняя игра требует уровней
        
        РЕКОМЕНДАЦИЯ 2:
        Тип: безопасность
        Совет: Обращай внимание на миссинги в противоположных линиях
        Обоснование: Предотвращение ганков
        """

    def _parse_recommendations(self, text: str) -> List[Dict]:
        """Парсить рекомендации из текста"""
        recommendations = []
        # Простая обработка - можно улучшить
        if "РЕКОМЕНДАЦИЯ" in text:
            recommendations.append({
                "type": "strategy",
                "text": text,
                "confidence": 0.85
            })
        return recommendations
