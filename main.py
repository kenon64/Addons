"""
Запуск стратегического помощника для Dota 2
"""

import logging
import sys
from setup_assistant import run_first_time_setup
from coach import DotaCoach

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Точка входа"""
    try:
        logger.info("=" * 60)
        logger.info("🎮 СТРАТЕГИЧЕСКИЙ ПОМОЩНИК DOTA 2")
        logger.info("Виртуальный тренер для анализа и рекомендаций")
        logger.info("=" * 60)
        
        # Запустить setup если первый запуск
        is_first_run = run_first_time_setup()
        if is_first_run:
            logger.info("\n✅ Первоначальная настройка завершена!")
            logger.info("Перезапустите приложение для загрузки конфигурации.\n")
            return
        
        coach = DotaCoach()
        coach.run()
        
    except KeyboardInterrupt:
        logger.info("\nПрограмма прервана пользователем")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

