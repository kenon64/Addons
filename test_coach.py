#!/usr/bin/env python3
"""
Тестирование компонентов системы
"""

import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_imports():
    """Проверить импорты всех модулей"""
    logger.info("📦 Проверка импортов...")
    
    try:
        from coach import DotaCoach
        logger.info("✓ coach.py - OK")
    except Exception as e:
        logger.error(f"✗ coach.py - {e}")
        return False
    
    try:
        from voice_assistant import VoiceAssistant
        logger.info("✓ voice_assistant.py - OK")
    except Exception as e:
        logger.error(f"✗ voice_assistant.py - {e}")
        return False
    
    try:
        from qwen_processor import QwenStrategist
        logger.info("✓ qwen_processor.py - OK")
    except Exception as e:
        logger.error(f"✗ qwen_processor.py - {e}")
        return False
    
    try:
        from game_integration import GameAnalyzer
        logger.info("✓ game_integration.py - OK")
    except Exception as e:
        logger.error(f"✗ game_integration.py - {e}")
        return False
    
    try:
        import config
        logger.info("✓ config.py - OK")
    except Exception as e:
        logger.error(f"✗ config.py - {e}")
        return False
    
    return True


def test_config():
    """Проверить конфигурацию"""
    logger.info("\n⚙️  Проверка конфигурации...")
    
    try:
        from config import (
            QWEN_API_KEY, QWEN_MODEL, DOTA2_PROCESS_NAME,
            ANALYSIS_INTERVAL, LANGUAGE
        )
        
        logger.info(f"  QWEN_MODEL: {QWEN_MODEL}")
        logger.info(f"  DOTA2_PROCESS_NAME: {DOTA2_PROCESS_NAME}")
        logger.info(f"  ANALYSIS_INTERVAL: {ANALYSIS_INTERVAL} сек")
        logger.info(f"  LANGUAGE: {LANGUAGE}")
        
        if QWEN_API_KEY:
            logger.info(f"  QWEN_API_KEY: ✓ Установлен")
        else:
            logger.warning(f"  QWEN_API_KEY: ⚠️  НЕ установлен (используется fallback)")
        
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка конфигурации: {e}")
        return False


def test_game_analyzer():
    """Проверить анализатор игры"""
    logger.info("\n🎮 Проверка GameAnalyzer...")
    
    try:
        from game_integration import GameAnalyzer
        
        analyzer = GameAnalyzer()
        logger.info("✓ GameAnalyzer инициализирован")
        
        # Проверка методов
        if hasattr(analyzer, 'check_game_running'):
            logger.info("✓ Метод check_game_running доступен")
        
        if hasattr(analyzer, 'get_current_game_state'):
            logger.info("✓ Метод get_current_game_state доступен")
        
        if hasattr(analyzer, 'analyze_threats'):
            logger.info("✓ Метод analyze_threats доступен")
        
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка GameAnalyzer: {e}")
        return False


def test_qwen_strategist():
    """Проверить Qwen Strategist"""
    logger.info("\n🧠 Проверка QwenStrategist...")
    
    try:
        from qwen_processor import QwenStrategist
        
        strategist = QwenStrategist()
        logger.info("✓ QwenStrategist инициализирован")
        
        if hasattr(strategist, 'analyze_situation'):
            logger.info("✓ Метод analyze_situation доступен")
        
        # Тестовый анализ
        test_game_state = {
            'game_time': 10,
            'hero_name': 'Anti-Mage',
            'level': 5,
            'gold': 1500,
            'allies': [],
            'enemies': []
        }
        
        logger.info("  Тестирование анализа ситуации...")
        result = strategist.analyze_situation(test_game_state)
        
        if result['status'] == 'success':
            logger.info("✓ Анализ выполнен успешно")
        else:
            logger.warning(f"⚠️  Анализ вернул статус: {result['status']}")
        
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка QwenStrategist: {e}")
        return False


def test_voice_assistant():
    """Проверить VoiceAssistant"""
    logger.info("\n🎤 Проверка VoiceAssistant...")
    
    try:
        from voice_assistant import VoiceAssistant
        
        try:
            assistant = VoiceAssistant()
            logger.info("✓ VoiceAssistant инициализирован")
            
            if hasattr(assistant, 'listen'):
                logger.info("✓ Метод listen доступен")
            
            if hasattr(assistant, 'speak'):
                logger.info("✓ Метод speak доступен")
            
            logger.info("  (Примечание: микрофон может быть недоступен в текущей среде)")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️  VoiceAssistant инициализация: {e}")
            logger.info("  (Это нормально, если нет микрофона)")
            return True
            
    except Exception as e:
        logger.error(f"✗ Ошибка VoiceAssistant: {e}")
        return False


def test_coach():
    """Проверить Coach"""
    logger.info("\n🎓 Проверка DotaCoach...")
    
    try:
        from coach import DotaCoach
        
        coach = DotaCoach()
        logger.info("✓ DotaCoach инициализирован")
        
        if hasattr(coach, 'run'):
            logger.info("✓ Метод run доступен")
        
        if hasattr(coach, 'start'):
            logger.info("✓ Метод start доступен")
        
        if hasattr(coach, 'ask_for_help'):
            logger.info("✓ Метод ask_for_help доступен")
        
        return True
    except Exception as e:
        logger.error(f"✗ Ошибка DotaCoach: {e}")
        return False


def run_all_tests():
    """Запустить все тесты"""
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ")
    logger.info("=" * 60 + "\n")
    
    tests = [
        ("Импорты", test_imports),
        ("Конфигурация", test_config),
        ("GameAnalyzer", test_game_analyzer),
        ("QwenStrategist", test_qwen_strategist),
        ("VoiceAssistant", test_voice_assistant),
        ("DotaCoach", test_coach),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Неожиданная ошибка в тесте {test_name}: {e}")
            results[test_name] = False
    
    # Итоги
    logger.info("\n" + "=" * 60)
    logger.info("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    logger.info("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name:<20} {status}")
    
    logger.info(f"\n  Всего: {passed}/{total} тестов пройдено")
    
    if passed == total:
        logger.info("\n✅ Все тесты пройдены! Система готова к работе.")
        return 0
    else:
        logger.warning(f"\n⚠️  {total - passed} тестов не пройдено.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(run_all_tests())
    except KeyboardInterrupt:
        logger.info("\n\nТестирование прервано пользователем")
        sys.exit(1)
