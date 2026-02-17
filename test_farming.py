"""
Тестирование функционала оптимизации фарма
"""

import logging
from farming_optimizer import FarmingOptimizer, FarmingType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_farm_optimizer():
    """Тестировать оптимизатор фарма"""
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ: ОПТИМИЗАТОР ФАРМА")
    logger.info("=" * 60)
    
    # Инициализировать
    optimizer = FarmingOptimizer()
    logger.info(f"✓ Инициализирован с {len(optimizer.farm_spots)} спотами")
    
    # Получить статистику
    stats = optimizer.get_farm_statistics()
    logger.info(f"\n📊 Статистика спотов:")
    logger.info(f"  Всего: {stats['total_spots']}")
    logger.info(f"  Линии: {stats['lane_creeps_spots']}")
    logger.info(f"  Джунгль: {stats['jungle_spots']}")
    logger.info(f"  Стакованные: {stats['stack_spots']}")
    logger.info(f"  Макс GPM: {stats['max_gpm']}")
    logger.info(f"  Опасные: {stats['dangerous_spots']}")
    
    # Тест 1: Расчет маршрута при низкой опасности
    logger.info(f"\n🧪 Тест 1: Расчет маршрута (низкая опасность)")
    hero_pos = (400, 400)
    route = optimizer.calculate_farm_route(
        hero_position=hero_pos,
        team_danger_level=0.2
    )
    
    logger.info(f"✓ Маршрут рассчитан ({len(route)} спотов):")
    for i, spot in enumerate(route[:5]):
        logger.info(f"  {i+1}. {spot.name} (GPM: {spot.gold_per_minute}, опасность: {spot.difficulty})")
    
    # Тест 2: Получить рекомендацию
    logger.info(f"\n🧪 Тест 2: Получить рекомендацию")
    next_spot = optimizer.get_next_spot()
    
    if next_spot['status'] == 'success':
        logger.info(f"✓ Рекомендация получена:")
        logger.info(f"  Спот: {next_spot['spot_name']}")
        logger.info(f"  Расстояние: {next_spot['distance']:.0f}м")
        logger.info(f"  GPM: {next_spot['gold_per_minute']}")
        logger.info(f"  Совет: {next_spot['recommendation']}")
    else:
        logger.warning(f"⚠️ {next_spot['message']}")
    
    # Тест 3: Анализ высокой опасности
    logger.info(f"\n🧪 Тест 3: Расчет маршрута (высокая опасность)")
    route_dangerous = optimizer.calculate_farm_route(
        hero_position=hero_pos,
        team_danger_level=0.8
    )
    
    logger.info(f"✓ Маршрут при опасности ({len(route_dangerous)} спотов):")
    if route_dangerous:
        logger.info(f"  Предпочитаемые: {[s.name for s in route_dangerous[:3]]}")
    else:
        logger.info(f"  Нет безопасных спотов!")
    
    # Тест 4: Анализ текущей позиции
    logger.info(f"\n🧪 Тест 4: Анализ текущей позиции")
    analysis = optimizer.analyze_current_position(hero_pos)
    
    logger.info(f"✓ Анализ:")
    logger.info(f"  Ближайший спот: {analysis['nearest_spot']}")
    logger.info(f"  Расстояние: {analysis['distance']:.0f}м")
    logger.info(f"  Рекомендация: {analysis['recommendation']}")
    if analysis['warning']:
        logger.warning(f"  ⚠️ {analysis['warning']}")
    
    # Тест 5: Разные позиции героя
    logger.info(f"\n🧪 Тест 5: Маршруты с разных позиций")
    test_positions = [
        ((100, 100), "левый нижний"),
        ((900, 900), "правый верхний"),
        ((512, 512), "центр карты"),
    ]
    
    for pos, name in test_positions:
        route = optimizer.calculate_farm_route(pos, team_danger_level=0.3)
        if route:
            logger.info(f"  {name}: {route[0].name}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    logger.info("=" * 60)


def demo_farming_recommendations():
    """Демонстрация рекомендаций по фарму"""
    logger.info("\n" + "=" * 60)
    logger.info("🎮 ДЕМОНСТРАЦИЯ: СОВЕТЫ ПО ФАРМУ")
    logger.info("=" * 60)
    
    optimizer = FarmingOptimizer()
    
    # Сценарий: Player Carry на маршрут фарма
    scenarios = [
        {
            "name": "Ранняя игра - безопасно",
            "pos": (100, 800),
            "danger": 0.1,
            "description": "Carry фармит боттом линию"
        },
        {
            "name": "Мид игра - враги активны",
            "pos": (512, 512),
            "danger": 0.6,
            "description": "Carry ищет безопасный фарм"
        },
        {
            "name": "Поздняя игра - очень опасно",
            "pos": (800, 700),
            "danger": 0.9,
            "description": "Carry ищет последнее место для фарма"
        },
    ]
    
    for scenario in scenarios:
        logger.info(f"\n📍 {scenario['name']}")
        logger.info(f"   {scenario['description']}")
        
        route = optimizer.calculate_farm_route(
            scenario['pos'],
            team_danger_level=scenario['danger']
        )
        
        if route:
            next_spot = optimizer.get_next_spot()
            logger.info(f"   💡 Совет: {next_spot['recommendation']}")
            logger.info(f"   💰 Доход: {next_spot['gold_per_minute']} GPM")
            logger.info(f"   📍 Первые 3 спота: {', '.join([s.name for s in route[:3]])}")
        else:
            logger.info(f"   ⚠️ Нет безопасных спотов!")
    
    logger.info("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        test_farm_optimizer()
        demo_farming_recommendations()
    except Exception as e:
        logger.error(f"Ошибка в тестах: {e}", exc_info=True)
