"""
UI Помощник - текстовый оверлей с советами
Вместо голоса показывает текст на экране
"""

import logging
import threading
import time
from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import tkinter as tk
from tkinter import font as tkFont

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvisorType(Enum):
    """Типы советов"""
    STRATEGY = "strategy"      # Стратегия
    FARMING = "farming"        # Фарм
    DANGER = "danger"          # Опасность
    OBJECTIVE = "objective"    # Цели
    ITEM = "item"             # Предметы
    POSITIONING = "pos"        # Позиция


@dataclass
class Advice:
    """Совет для отображения"""
    text: str                  # Текст совета
    advisor_type: AdvisorType  # Тип
    priority: int              # Приоритет (1-10, где 10 = самый важный)
    icon: str                  # Иконка/эмодзи
    duration: float            # Длительность показа (сек)
    hero_name: str = ""        # Имя героя (опционально)


class DotaAdvisor:
    """Текстовый UI помощник для Dota 2"""
    
    def __init__(self, position: str = "top-right"):
        """
        Инициализировать помощника
        
        Args:
            position: Позиция на экране (top-right, top-left, bottom-right, bottom-left)
        """
        self.position = position
        self.advice_queue: List[Advice] = []
        self.current_advice: Optional[Advice] = None
        self.is_running = False
        self.window: Optional[tk.Tk] = None
        self.label: Optional[tk.Label] = None
        self.icon_label: Optional[tk.Label] = None
        self.priority_label: Optional[tk.Label] = None
        self.hero_label: Optional[tk.Label] = None  # Новое: отображение героя
        
        # Текущий герой
        self.current_hero_name = "Unknown Hero"
        self.current_hero_avatar = "🎮"
        
        # Стили
        self.bg_color = "#1a1a1a"      # Тёмный фон
        self.text_color = "#ffffff"    # Белый текст
        self.accent_color = "#00ff00"  # Зелёный акцент
        self.warning_color = "#ff6600" # Оранжевый для предупреждений
        
        self.window_width = 350
        self.window_height = 180
        
        logger.info(f"✓ DotaAdvisor инициализирован (позиция: {position})")

    def start(self):
        """Запустить помощника"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_window, daemon=True)
            self.thread.start()
            logger.info("🎤 Помощник запущен")

    def stop(self):
        """Остановить помощника"""
        self.is_running = False
        if self.window:
            try:
                self.window.quit()
            except:
                pass
        logger.info("⏹️ Помощник остановлен")

    def add_advice(self, advice: Advice):
        """
        Добавить совет в очередь
        
        Args:
            advice: Объект совета
        """
        self.advice_queue.append(advice)
        logger.info(f"💡 Совет добавлен: {advice.text[:50]}...")

    def show_advice(self, text: str, advice_type: AdvisorType = AdvisorType.STRATEGY,
                   priority: int = 5, icon: str = "💡", duration: float = 5.0):
        """
        Показать совет
        
        Args:
            text: Текст совета
            advice_type: Тип совета
            priority: Приоритет (1-10)
            icon: Иконка
            duration: Длительность показа
        """
        advice = Advice(
            text=text,
            advisor_type=advice_type,
            priority=priority,
            icon=icon,
            duration=duration,
            hero_name=self.current_hero_name
        )
        self.add_advice(advice)

    def set_hero(self, hero_name: str, hero_avatar: str = "🎮"):
        """
        Установить текущего героя
        
        Args:
            hero_name: Имя героя (например, "Legion Commander", "Marksmanship")
            hero_avatar: Аватар героя (emoji или текст)
        """
        self.current_hero_name = hero_name
        self.current_hero_avatar = hero_avatar
        logger.info(f"🎯 Герой выбран: {hero_avatar} {hero_name}")
        
        # Обновить UI если окно уже существует
        if self.hero_label:
            self.hero_label.config(text=f"{hero_avatar} {hero_name}")



    def _run_window(self):
        """Основной цикл окна"""
        try:
            self.window = tk.Tk()
            self.window.title("Dota Coach Assistant")
            self.window.geometry(f"{self.window_width}x{self.window_height}")
            self.window.configure(bg=self.bg_color)
            
            # Сделать окно всегда сверху
            self.window.attributes('-topmost', True)
            
            # Сделать окно прозрачным (пока не будем, это сложнее)
            # self.window.attributes('-alpha', 0.9)
            
            # Позиционировать окно
            self._position_window()
            
            # Убрать рамку окна
            self.window.overrideredirect(False)  # Можно сделать True для без-рамочного
            
            # UI элементы
            self._create_ui()
            
            # Запустить обновление советов
            self._update_advice()
            
            self.window.mainloop()
            
        except Exception as e:
            logger.error(f"❌ Ошибка окна: {e}")

    def _position_window(self):
        """Позиционировать окно на экране"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        padding = 20
        
        positions = {
            "top-right": (screen_width - self.window_width - padding, padding),
            "top-left": (padding, padding),
            "bottom-right": (screen_width - self.window_width - padding, 
                           screen_height - self.window_height - padding),
            "bottom-left": (padding, screen_height - self.window_height - padding),
        }
        
        x, y = positions.get(self.position, positions["top-right"])
        self.window.geometry(f"+{int(x)}+{int(y)}")

    def _create_ui(self):
        """Создать UI элементы"""
        # Заголовок с аватаром героя
        hero_frame = tk.Frame(self.window, bg="#0a0a0a")
        hero_frame.pack(fill=tk.X, padx=5, pady=3, side=tk.TOP)
        
        # Аватар героя
        self.hero_label = tk.Label(
            hero_frame,
            text=f"{self.current_hero_avatar} {self.current_hero_name}",
            font=("Arial", 9, "bold"),
            bg="#0a0a0a",
            fg="#00ff00"
        )
        self.hero_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Строка разделения
        sep = tk.Frame(self.window, bg="#333333", height=1)
        sep.pack(fill=tk.X)
        
        # Заголовок с типом совета
        header_frame = tk.Frame(self.window, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Иконка
        self.icon_label = tk.Label(
            header_frame,
            text="💡",
            font=("Arial", 20),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.icon_label.pack(side=tk.LEFT, padx=5)
        
        # Тип совета
        self.priority_label = tk.Label(
            header_frame,
            text="Совет",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.priority_label.pack(side=tk.LEFT, padx=5)
        
        # Основной текст совета
        self.label = tk.Label(
            self.window,
            text="Добро пожаловать в Dota Coach!",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=self.window_width - 20,
            justify=tk.LEFT,
            anchor=tk.NW
        )
        self.label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Нижняя строка статуса
        footer_frame = tk.Frame(self.window, bg="#0a0a0a")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_label = tk.Label(
            footer_frame,
            text="🔄 Ожидание советов...",
            font=("Arial", 8),
            bg="#0a0a0a",
            fg="#999999"
        )
        status_label.pack(side=tk.LEFT, padx=5, pady=3)

    def _update_advice(self):
        """Обновить текущий совет"""
        if not self.is_running:
            return
        
        # Если есть советы в очереди
        if self.advice_queue:
            # Сортировать по приоритету
            self.advice_queue.sort(key=lambda a: a.priority, reverse=True)
            self.current_advice = self.advice_queue.pop(0)
            
            self._display_advice(self.current_advice)
            
            # Запланировать очистку через duration
            self.window.after(
                int(self.current_advice.duration * 1000),
                self._clear_advice_after_delay
            )
        
        # Продолжить обновление
        if self.window:
            self.window.after(500, self._update_advice)

    def _display_advice(self, advice: Advice):
        """Отобразить совет в окне"""
        if not self.label:
            return
        
        # Обновить текст
        self.label.config(text=advice.text, fg=self._get_color_for_type(advice.advisor_type))
        
        # Обновить иконку
        if self.icon_label:
            self.icon_label.config(text=advice.icon)
        
        # Обновить тип
        if self.priority_label:
            type_name = advice.advisor_type.value.upper()
            self.priority_label.config(text=type_name)

    def _clear_advice_after_delay(self):
        """Очистить совет после задержки"""
        if self.label:
            self.label.config(text="")
        self.current_advice = None

    def _get_color_for_type(self, advisor_type: AdvisorType) -> str:
        """Получить цвет для типа совета"""
        colors = {
            AdvisorType.STRATEGY: "#00ff00",      # Зелёный
            AdvisorType.FARMING: "#ffff00",       # Жёлтый
            AdvisorType.DANGER: "#ff6600",        # Оранжевый
            AdvisorType.OBJECTIVE: "#00ccff",     # Голубой
            AdvisorType.ITEM: "#ff00ff",          # Фиолетовый
            AdvisorType.POSITIONING: "#ffcc00",   # Светло-жёлтый
        }
        return colors.get(advisor_type, self.text_color)

    def create_test_ui(self):
        """Создать тестовый UI"""
        logger.info("\n📊 ДЕМО: Советы помощника")
        logger.info("=" * 50)
        
        test_advices = [
            Advice(
                text="Враги расходятся😂\nСейчас оптимальный\nвремя для фарма линии!",
                advisor_type=AdvisorType.FARMING,
                priority=7,
                icon="🌾",
                duration=5.0
            ),
            Advice(
                text="⚠️ ВНИМАНИЕ!\nТень на мид -\nопасность!",
                advisor_type=AdvisorType.DANGER,
                priority=10,
                icon="⚠️",
                duration=6.0
            ),
            Advice(
                text="Рошан готов к\nнападению!\nВся команда собрана.",
                advisor_type=AdvisorType.OBJECTIVE,
                priority=8,
                icon="🐉",
                duration=5.0
            ),
            Advice(
                text="Твоё позиционирование\nидеально. Продолжай!",
                advisor_type=AdvisorType.POSITIONING,
                priority=3,
                icon="📍",
                duration=4.0
            ),
            Advice(
                text="Собери Blink Dagger\nдля более гибкой игры.",
                advisor_type=AdvisorType.ITEM,
                priority=5,
                icon="✨",
                duration=5.0
            ),
        ]
        
        for advice in test_advices:
            logger.info(f"\n{advice.icon} {advice.advisor_type.value.upper()}")
            logger.info(f"   Текст: {advice.text.replace(chr(10), ' ')}")
            logger.info(f"   Приоритет: {'🔴' * advice.priority}")
            
            self.add_advice(advice)
