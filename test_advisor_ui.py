#!/usr/bin/env python3
"""
Простой тест UI - показывает различные типы советов
Не требует Dota 2, используется для проверки визуального интерфейса
"""

import time
import logging
from dota_advisor import DotaAdvisor, AdvisorType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_advisor():
    """Протестировать advisor UI с различными типами советов"""
    
    logger.info("=" * 60)
    logger.info("🎮 ТЕСТ ВИЗУАЛЬНОГО ПОМОЩНИКА")
    logger.info("=" * 60)
    
    # Создать помощника
    advisor = DotaAdvisor(position="top-right")
    advisor.start()
    
    logger.info("\n✓ Запущен UI помощник")
    logger.info("Окно должно появиться в верхнем правом углу экрана\n")
    
    time.sleep(1)
    
    # Установить героя
    advisor.set_hero("Legion Commander", "🗡️")
    logger.info("✓ Установлен герой: Legion Commander\n")
    
    time.sleep(1)
    
    # Тест 1: Совет по фарму
    logger.info("TEST 1: Совет по фарму (жёлтый)")
    advisor.show_advice(
        "🌾 Враги расходятся.\nПерейди на безопасное\nместо для фарма",
        AdvisorType.FARMING,
        priority=7,
        icon="🌾",
        duration=6.0
    )
    time.sleep(7)
    
    # Тест 2: Опасность
    logger.info("TEST 2: Опасность (оранжевый)")
    advisor.show_advice(
        "⚠️ ОПАСНО!\nВраг рядом с тобой!",
        AdvisorType.DANGER,
        priority=10,
        icon="!",
        duration=6.0
    )
    time.sleep(7)
    
    # Тест 3: Цель
    logger.info("TEST 3: Цель команды (голубой)")
    advisor.show_advice(
        "🐉 Рошан готов!\nВся команда собрана.",
        AdvisorType.OBJECTIVE,
        priority=9,
        icon="🐉",
        duration=6.0
    )
    time.sleep(7)
    
    # Тест 4: Предметы
    logger.info("TEST 4: Совет по предметам (фиолетовый)")
    advisor.show_advice(
        "✨ Собери Blink Dagger\nдля более гибкой игры.",
        AdvisorType.ITEM,
        priority=6,
        icon="✨",
        duration=6.0
    )
    time.sleep(7)
    
    # Тест 5: Позиция
    logger.info("TEST 5: Совет по позиции (жёлтый)")
    advisor.show_advice(
        "📍 Отойди из зоны\nпоражения врага!",
        AdvisorType.POSITIONING,
        priority=5,
        icon="📍",
        duration=6.0
    )
    time.sleep(7)
    
    # Тест 6: Стратегия
    logger.info("TEST 6: Стратегический совет (зелёный)")
    advisor.show_advice(
        "💡 Твоя команда может\nначать Рош сейчас!",
        AdvisorType.STRATEGY,
        priority=8,
        icon="💡",
        duration=6.0
    )
    time.sleep(7)
    
    # Тест мультипропиоритета
    logger.info("TEST 7: Множество советов (проверка очереди)")
    
    advisor.show_advice(
        "Низкий приоритет",
        AdvisorType.STRATEGY,
        priority=2,
        icon="💤",
        duration=3.0
    )
    
    advisor.show_advice(
        "Высокий приоритет\n(должен показаться первым)",
        AdvisorType.DANGER,
        priority=9,
        icon="🔴",
        duration=6.0
    )
    
    time.sleep(7)
    
    logger.info("\n")
    logger.info("=" * 60)
    logger.info("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
    logger.info("=" * 60)
    logger.info("\nОкно помощника сейчас закроется...\n")
    
    advisor.stop()
    time.sleep(1)


if __name__ == "__main__":
    try:
        test_advisor()
    except KeyboardInterrupt:
        logger.info("\n⏹️ Тест остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
