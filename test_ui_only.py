"""
Простой тест только UI компонента DotaAdvisor
"""

import time
from dota_advisor import DotaAdvisor, AdvisorType

def test_ui():
    """Тестировать UI помощника"""
    print("\n✅ Запуск простого теста UI...\n")
    
    # Создать помощника на верхнем右углу
    advisor = DotaAdvisor(position="top-right")
    
    # Запустить UI
    advisor.start()
    
    # Установить героя
    advisor.set_hero("Legion Commander", "🗡️")
    
    print("⏳ Показываю различные типы советов...\n")
    
    # Показать различные советы
    advisor.show_advice(
        "Враги расходятся.\nПерейди на линию",
        AdvisorType.FARMING,
        priority=7,
        icon="🌾",
        duration=5.0
    )
    time.sleep(6)
    
    advisor.show_advice(
        "⚠️ ОПАСНО!\nСень врага видна!",
        AdvisorType.DANGER,
        priority=10,
        icon="⚠️",
        duration=5.0
    )
    time.sleep(6)
    
    advisor.show_advice(
        "Рошан готов!\nВся команда собрна.",
        AdvisorType.OBJECTIVE,
        priority=8,
        icon="🐉",
        duration=5.0
    )
    time.sleep(6)
    
    advisor.show_advice(
        "Купи Blink Dagger\nдля гибкости.",
        AdvisorType.ITEM,
        priority=6,
        icon="✨",
        duration=5.0
    )
    time.sleep(6)
    
    advisor.show_advice(
        "Хорошая позиция.\nПродолжай!",
        AdvisorType.POSITIONING,
        priority=5,
        icon="📍",
        duration=5.0
    )
    time.sleep(6)
    
    print("\n✅ Тест завершён!")
    advisor.stop()

if __name__ == "__main__":
    try:
        test_ui()
    except KeyboardInterrupt:
        print("\n⏹️ Тест остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
