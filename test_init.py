#!/usr/bin/env python3
"""
Проверить инициализацию DotaCoach со всеми новыми изменениями
"""

print("Проверка инициализации...")

try:
    from coach import DotaCoach
    print("✓ Импорт coach успешен")
    
    coach = DotaCoach()
    print("✓ DotaCoach инициализирован")
    
    # Проверить advisor
    print(f"✓ Advisor создан: {coach.advisor}")
    print(f"✓ Text UI mode: {coach.use_text_ui}")
    
    print("\n✅ Все проверки прошли успешно!")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
