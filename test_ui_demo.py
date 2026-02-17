"""
Демонстрация UI помощника для Dota Coach
"""

import time
from dota_advisor import DotaAdvisor, AdvisorType

def test_advisor_ui():
    """Тестировать UI помощника"""
    print("\n🎮 Запуск демонстрации текстового помощника...")
    print("=" * 50)
    
    # Создать помощника
    advisor = DotaAdvisor(position="top-right")
    
    # Запустить UI
    print("✓ Запускаю окно помощника...")
    advisor.start()
    time.sleep(1)
    
    # Установить героя
    print("✓ Выбираю героя...")
    advisor.set_hero("Legion Commander", "🗡️")
    time.sleep(1)
    
    # Показать советы
    print("✓ Показываю советы...")
    print("  - Фарм совет")
    time.sleep(1)
    
    advisor.show_advice(
        "🌾 Враги расходятся.\nПерейди на безопасное\nместо для фарма",
        AdvisorType.FARMING,
        priority=7,
        icon="🌾",
        duration=6.0
    )
    time.sleep(7)
    
    print("  - Опасность")
    advisor.show_advice(
        "⚠️ ОПАСНО!\nВраг рядом с тобой!",
        AdvisorType.DANGER,
        priority=10,
        icon="!",
        duration=6.0
    )
    time.sleep(7)
    
    print("  - Цель команды")
    advisor.show_advice(
        "🐉 Рошан готов!\nВся команда тут.",
        AdvisorType.OBJECTIVE,
        priority=9,
        icon="🐉",
        duration=6.0
    )
    time.sleep(7)
    
    print("✓ Закрываю помощника...")
    advisor.stop()
    print("\n✅ Демонстрация завершена!")

if __name__ == "__main__":
    try:
        test_advisor_ui()
    except KeyboardInterrupt:
        print("\n⏹️ Демонстрация остановлена")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
