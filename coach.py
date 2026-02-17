"""
Виртуальный тренер - главный модуль для взаимодействия с игроком
"""

import logging
import time
import threading
from typing import Optional
from datetime import datetime, timedelta

from voice_assistant import VoiceAssistant
from qwen_processor import QwenStrategist
from local_strategist import LocalStrategist  # НОВОЕ: локальный анализатор
from dota2_api import HybridGameAnalyzer  # НОВОЕ: гибридный анализатор
from game_integration import GameAnalyzer
from farming_optimizer import FarmingOptimizer
from dota_advisor import DotaAdvisor, AdvisorType
from config import QWEN_API_KEY, DATA_SOURCE, STEAM_ID, USE_LIVE_GAME

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DotaCoach:
    def __init__(self):
        self.voice_assistant = VoiceAssistant(language="ru_RU")  # Теперь безопасна
        
        # НОВОЕ: выбрать анализатор в зависимости от конфига
        if DATA_SOURCE == 'api' or DATA_SOURCE == 'hybrid':
            logger.info(f"📊 Режим: {DATA_SOURCE.upper()}")
            if STEAM_ID:
                self.game_analyzer = HybridGameAnalyzer(steam_id=STEAM_ID, use_live=USE_LIVE_GAME)
                logger.info(f"✓ Используется API (Steam ID: {STEAM_ID})")
            else:
                logger.warning("Steam ID не установлен, использую локальную симуляцию")
                self.game_analyzer = GameAnalyzer()
        else:
            logger.info("📊 Режим: LOCAL")
            self.game_analyzer = GameAnalyzer()
            logger.info("✓ Используется локальная симуляция")
        
        # Выбрать стратега в зависимости от API ключа
        if QWEN_API_KEY:
            self.strategist = QwenStrategist()
            self.use_qwen = True
            logger.info("🤖 Используется Qwen AI (с API ключом)")
        else:
            self.strategist = LocalStrategist()
            self.use_qwen = False
            logger.info("🧠 Используется локальный анализ (без API ключа)")
        
        self.farming_optimizer = FarmingOptimizer()
        self.advisor = DotaAdvisor(position="top-right")  # Текстовой помощник
        self.is_running = False
        self.last_recommendation_time = None
        self.recommendation_cooldown = 30  # секунды
        self.last_farm_analysis_time = None
        self.farm_analysis_cooldown = 15  # анализировать фарм каждые 15 сек
        self.monitoring_thread = None
        self.enable_farming_tips = True  # Включить советы по фарму
        self.use_text_ui = True  # Новое: использовать текстовый UI вместо голоса

    def start(self):
        """Запустить тренера"""
        logger.info("🎮 Голосовой тренер Dota 2 запущен")
        
        # Новое: запустить текстовой помощник вместо озвучивания
        if self.use_text_ui:
            self.advisor.start()
            logger.info("✓ Текстовой UI помощник активирован")
        else:
            self.voice_assistant.speak("Виртуальный тренер активирован")
        
        self.is_running = True
        
        # Проверить, запущена ли игра
        if not self.game_analyzer.check_game_running():
            if self.use_text_ui:
                self.advisor.show_advice(
                    "Пожалуйста,\nзапустите Dota 2",
                    AdvisorType.DANGER,
                    priority=10,
                    icon="❌",
                    duration=5.0
                )
            else:
                self.voice_assistant.speak("Пожалуйста, запустите Dota 2")
            logger.warning("Dota 2 не запущена")
            return False
        
        return True

    def run(self):
        """Основной цикл работы"""
        if not self.start():
            return
        
        if self.use_text_ui:
            self.advisor.show_advice(
                "Игра обнаружена.\nЯ буду следить\nи давать советы",
                AdvisorType.STRATEGY,
                priority=8,
                icon="🎮",
                duration=4.0
            )
        else:
            self.voice_assistant.speak("Игра обнаружена. Я буду следить за ситуацией и давать советы")
        
        try:
            while self.is_running:
                # Получить состояние игры
                game_state = self.game_analyzer.get_current_game_state()
                
                if game_state is None:
                    time.sleep(2)
                    continue
                
                # Анализ ФАРМА
                if self.enable_farming_tips and self._should_analyze_farming():
                    self._analyze_and_recommend_farming(game_state)
                
                # Проверить, можно ли дать рекомендацию
                if self._should_give_recommendation():
                    self._analyze_and_recommend(game_state)
                
                # Проверить, просит ли игрок помощь
                self._check_for_user_input()
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Тренер остановлен пользователем")
            if self.use_text_ui:
                self.advisor.show_advice(
                    "До встречи\nна Доте! 👋",
                    AdvisorType.STRATEGY,
                    priority=5,
                    duration=3.0
                )
            else:
                self.voice_assistant.speak("До встречи на Доте!")
        except Exception as e:
            logger.error(f"Ошибка в основном цикле: {e}")
            if self.use_text_ui:
                self.advisor.show_advice(
                    "Произошла\nошибка ❌",
                    AdvisorType.DANGER,
                    priority=10,
                    duration=4.0
                )
            else:
                self.voice_assistant.speak("Произошла ошибка")
        finally:
            self.is_running = False

    def _should_give_recommendation(self) -> bool:
        """Проверить, можно ли давать рекомендацию (cooldown)"""
        if self.last_recommendation_time is None:
            return True
        
        elapsed = datetime.now() - self.last_recommendation_time
        return elapsed > timedelta(seconds=self.recommendation_cooldown)

    def _analyze_and_recommend(self, game_state: dict):
        """Анализировать ситуацию и дать рекомендацию"""
        logger.info("📊 Анализирую ситуацию...")
        
        # Получить анализ от стратега
        analysis = self.strategist.analyze_situation(game_state)
        
        if analysis["status"] == "success":
            self._voice_report_recommendation(analysis, game_state)
            self.last_recommendation_time = datetime.now()
        else:
            logger.warning(f"Ошибка анализа: {analysis.get('error')}")

    def _voice_report_recommendation(self, analysis: dict, game_state: dict):
        """Озвучить рекомендацию игроку (теперь через UI)"""
        try:
            # Получить рекомендации
            recommendations = analysis.get('recommendations', [])
            
            if not recommendations:
                return
            
            # Взять первую (самую важную) рекомендацию
            rec = recommendations[0]
            
            # Если используется LocalStrategist - структурированные рекомендации
            if not self.use_qwen:
                message = rec.get('advice', "Сосредоточься на игре")
                title = rec.get('title', '💡')
                
                # Определить тип советника по категории
                category = rec.get('category')
                if category:
                    category_str = str(category).lower()
                    if 'позиционирование' in category_str:
                        advice_type = AdvisorType.POSITIONING
                    elif 'фарм' in category_str:
                        advice_type = AdvisorType.FARMING
                    elif 'безопасность' in category_str or 'safety' in category_str:
                        advice_type = AdvisorType.DANGER
                    elif 'боевые' in category_str or 'teamfight' in category_str:
                        advice_type = AdvisorType.OBJECTIVE
                    elif 'предметы' in category_str or 'items' in category_str:
                        advice_type = AdvisorType.ITEM
                    else:
                        advice_type = AdvisorType.STRATEGY
                else:
                    advice_type = AdvisorType.STRATEGY
                
                priority = rec.get('priority', 5)
            else:
                # Если Qwen AI - текстовый анализ
                recommendation_text = analysis.get('analysis', '')
                
                # Простое преобразование в более короткий формат для озвучивания
                if "позиционирование" in recommendation_text.lower():
                    message = "Попробуй улучшить позицию на карте"
                    advice_type = AdvisorType.POSITIONING
                    priority = 6
                elif "фарм" in recommendation_text.lower():
                    message = "Сосредоточься на фарме, набирай предметы"
                    advice_type = AdvisorType.FARMING
                    priority = 7
                elif "безопасность" in recommendation_text.lower():
                    message = "Будь осторожнее, враги рядом"
                    advice_type = AdvisorType.DANGER
                    priority = 9
                elif "боевых цели" in recommendation_text.lower() or "офис" in recommendation_text.lower():
                    message = "Помоги команде с основной целью"
                    advice_type = AdvisorType.OBJECTIVE
                    priority = 7
                else:
                    message = "Обрати внимание на изменение ситуации"
                    advice_type = AdvisorType.STRATEGY
                    priority = 5
            
            logger.info(f"💬 Рекомендация: {message}")
            
            if self.use_text_ui:
                self.advisor.show_advice(
                    message,
                    advice_type,
                    priority=priority,
                    duration=6.0
                )
            else:
                self.voice_assistant.speak(message)
            
        except Exception as e:
            logger.error(f"Ошибка при озвучивании рекомендации: {e}")

    def _check_for_user_input(self):
        """Проверить, просит ли игрок помощь (без блокировки)"""
        # В полной реализации здесь можно слушать горячую клавишу
        # или слова-активаторы вроде "тренер" или "совет"
        pass

    def _should_analyze_farming(self) -> bool:
        """Проверить, пора ли анализировать фарм (cooldown)"""
        if self.last_farm_analysis_time is None:
            return True
        
        elapsed = datetime.now() - self.last_farm_analysis_time
        return elapsed > timedelta(seconds=self.farm_analysis_cooldown)

    def _analyze_and_recommend_farming(self, game_state: dict):
        """Анализировать фарм и дать рекомендацию по оптимальному маршруту"""
        logger.info("🌾 Анализирую оптимальный фарм...")
        
        try:
            # Получить текущую позицию героя
            hero_pos = game_state.get('hero_position', (500, 500))
            
            # Рассчитать опасность на карте
            danger_level = self._estimate_danger_level(game_state)
            
            # Рассчитать оптимальный маршрут фарма
            farm_route = self.farming_optimizer.calculate_farm_route(
                hero_position=hero_pos,
                team_danger_level=danger_level
            )
            
            if farm_route:
                # Получить информацию о следующем споте
                next_spot_info = self.farming_optimizer.get_next_spot()
                
                if next_spot_info['status'] == 'success':
                    rec = next_spot_info['recommendation']
                    logger.info(f"💬 Совет фарм: {rec}")
                    
                    # Новое: показать в UI вместо озвучивания
                    if self.use_text_ui:
                        self.advisor.show_advice(
                            f"🌾 {rec}\n\n💰 {next_spot_info['gold_per_minute']} GPM\n⏱️ {int(next_spot_info['time_to_clear'])}сек",
                            AdvisorType.FARMING,
                            priority=7,
                            icon="🌾",
                            duration=8.0
                        )
                    else:
                        self.voice_assistant.speak(rec)
                    
                    self.last_farm_analysis_time = datetime.now()
            
        except Exception as e:
            logger.error(f"Ошибка анализа фарма: {e}")

    def _estimate_danger_level(self, game_state: dict) -> float:
        """
        Оценить уровень опасности на карте
        
        Returns:
            Значение 0-1, где 1 = максимальная опасность
        """
        danger = 0.0
        
        # Враги поблизости
        enemies = game_state.get('enemies', [])
        visible_enemies = [e for e in enemies if e.get('visible', False)]
        
        if visible_enemies:
            danger += min(len(visible_enemies) * 0.2, 0.5)
        
        # Враги с большим преимуществом
        hero_level = game_state.get('level', 0)
        for enemy in enemies:
            if enemy.get('level', 0) > hero_level + 3:
                danger += 0.3
        
        return min(danger, 1.0)

    def ask_for_help(self):
        """Активная помощь по запросу игрока"""
        logger.info("🆘 Игрок запрашивает помощь")
        
        game_state = self.game_analyzer.get_current_game_state()
        if game_state is None:
            if self.use_text_ui:
                self.advisor.show_advice(
                    "Игра не\nобнаружена ❌",
                    AdvisorType.DANGER,
                    priority=10,
                    duration=3.0
                )
            else:
                self.voice_assistant.speak("Игра не обнаружена")
            return
        
        # Дать развёрнутый анализ
        if self.use_text_ui:
            self.advisor.show_advice(
                "🔍 Анализирую\nситуацию...",
                AdvisorType.STRATEGY,
                priority=8,
                duration=3.0
            )
        else:
            self.voice_assistant.speak("Анализирую ситуацию подробнее...")
        
        analysis = self.strategist.analyze_situation(game_state)
        if analysis["status"] == "success":
            self._voice_report_recommendation(analysis, game_state)
        else:
            if self.use_text_ui:
                self.advisor.show_advice(
                    "Не удалось\nпровести анализ ⚠️",
                    AdvisorType.DANGER,
                    priority=9,
                    duration=3.0
                )
            else:
                self.voice_assistant.speak("Не удалось провести анализ")

    def stop(self):
        """Остановить тренера"""
        logger.info("Остановка тренера...")
        self.is_running = False
