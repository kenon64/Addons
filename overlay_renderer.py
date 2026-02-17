"""
Визуализатор оверлея - рисует маршруты фарма на экран
Использует PIL для рисования и работает без вмешательства в игру
"""

import logging
import threading
import time
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import mss
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OverlayRenderer:
    """Рендерер оверлея для визуализации маршрутов"""
    
    def __init__(self, monitor_index: int = 0):
        """
        Инициализировать рендерер оверлея
        
        Args:
            monitor_index: Индекс монитора для захвата (0 = основной)
        """
        self.sct = mss.mss()
        self.monitor_index = monitor_index
        self.monitors = self.sct.monitors
        self.current_monitor = self.monitors[monitor_index] if len(self.monitors) > monitor_index else self.monitors[1]
        
        self.is_running = False
        self.render_thread = None
        self.farm_route = []
        self.hero_position = None
        self.overlay_alpha = 0.7
        self.enable_arrows = True
        self.enable_text = True
        
        logger.info(f"✓ OverlayRenderer инициализирован (монитор {monitor_index})")

    def start(self):
        """Запустить отрендеринг оверлея"""
        if not self.is_running:
            self.is_running = True
            self.render_thread = threading.Thread(target=self._render_loop, daemon=True)
            self.render_thread.start()
            logger.info("🎨 Оверлей запущен")

    def stop(self):
        """Остановить отрендеринг"""
        self.is_running = False
        if self.render_thread:
            self.render_thread.join(timeout=2)
        logger.info("⏹️ Оверлей остановлен")

    def set_farm_route(self, route: List, hero_pos: Tuple[float, float]):
        """
        Установить маршрут фарма для отрисовки
        
        Args:
            route: Список объектов FarmSpot
            hero_pos: Позиция героя (x, y)
        """
        self.farm_route = route
        self.hero_position = hero_pos

    def _render_loop(self):
        """Главный цикл отрендеринга"""
        try:
            while self.is_running:
                if self.farm_route and self.hero_position:
                    self._draw_overlay()
                time.sleep(0.05)  # ~20 FPS
        except Exception as e:
            logger.error(f"❌ Ошибка в цикле отрендеринга: {e}")

    def _draw_overlay(self):
        """Нарисовать оверлей на экран"""
        try:
            # Захватить скриншот
            screenshot = self.sct.grab(self.current_monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            draw = ImageDraw.Draw(img, 'RGBA')
            
            # Рисовать маршрут
            self._draw_farm_route(draw, img.size)
            
            # Рисовать текст
            if self.enable_text:
                self._draw_info_panel(draw, img.size)
            
            # Показать изображение (пока просто будем логировать, в реальной жизни нужен оверлей WIndow)
            logger.debug("🎨 Оверлей отрисован")
            
        except Exception as e:
            logger.error(f"Ошибка при отрисовке: {e}")

    def _draw_farm_route(self, draw: ImageDraw.ImageDraw, screen_size: Tuple[int, int]):
        """Рисовать маршрут между спотами"""
        if len(self.farm_route) < 2:
            return
        
        # Масштаб: преобразование координат маршрута в пиксели экрана
        # Допустим, игровая карта 1024x1024, а экран 1920x1080
        scale_x = screen_size[0] / 1024
        scale_y = screen_size[1] / 1024
        
        # Текущая позиция героя
        if self.hero_position:
            hero_x = int(self.hero_position[0] * scale_x)
            hero_y = int(self.hero_position[1] * scale_y)
            
            # Рисовать героя (большой кружок)
            r = 15
            draw.ellipse(
                [hero_x - r, hero_y - r, hero_x + r, hero_y + r],
                fill=(0, 255, 0, 150),  # Зелёный цвет
                outline=(0, 200, 0, 255)
            )
            
            # Рисовать стрелки к каждому споту
            for i, spot in enumerate(self.farm_route[:5]):  # Показать первые 5 спотов
                spot_x = int(spot.position[0] * scale_x)
                spot_y = int(spot.position[1] * scale_y)
                
                # Цвет в зависимости от типа спота
                color = self._get_spot_color(spot, i)
                
                # Рисовать спот (кружок)
                r = 10
                draw.ellipse(
                    [spot_x - r, spot_y - r, spot_x + r, spot_y + r],
                    fill=(*color[:3], 100),
                    outline=(*color[:3], 255)
                )
                
                # Рисовать стрелку от героя/предыдущего спота
                if i == 0:
                    self._draw_arrow(draw, hero_x, hero_y, spot_x, spot_y, color, 3)
                else:
                    prev_spot = self.farm_route[i - 1]
                    prev_x = int(prev_spot.position[0] * scale_x)
                    prev_y = int(prev_spot.position[1] * scale_y)
                    self._draw_arrow(draw, prev_x, prev_y, spot_x, spot_y, color, 2)
                
                # Рисовать номер поряда
                draw.text(
                    (spot_x - 5, spot_y - 5),
                    str(i + 1),
                    fill=(255, 255, 255, 200),
                    font=None
                )

    def _get_spot_color(self, spot, index: int) -> Tuple[int, int, int]:
        """Получить цвет для спота в зависимости от типа и приоритета"""
        if index == 0:
            return (0, 255, 0)  # Зелёный - приоритетный
        elif index == 1:
            return (255, 200, 0)  # Жёлтый
        elif index == 2:
            return (255, 100, 0)  # Оранжевый
        else:
            return (200, 100, 255)  # Фиолетовый
    
    def _draw_arrow(self, draw: ImageDraw.ImageDraw, 
                   x1: int, y1: int, x2: int, y2: int,
                   color: Tuple[int, int, int], width: int = 2):
        """
        Нарисовать стрелку от (x1, y1) к (x2, y2)
        
        Args:
            draw: Объект ImageDraw
            x1, y1: Начальная точка
            x2, y2: Конечная точка
            color: RGB цвет
            width: Толщина линии
        """
        import math
        
        # Рисовать линию
        draw.line([(x1, y1), (x2, y2)], fill=(*color, 200), width=width)
        
        # Рисовать стрелку (треугольник на конце)
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_size = 15
        
        # Три точки для треугольника
        tip_x = x2
        tip_y = y2
        
        left_x = int(x2 - arrow_size * math.cos(angle - math.pi / 6))
        left_y = int(y2 - arrow_size * math.sin(angle - math.pi / 6))
        
        right_x = int(x2 - arrow_size * math.cos(angle + math.pi / 6))
        right_y = int(y2 - arrow_size * math.sin(angle + math.pi / 6))
        
        # Рисовать треугольник стрелки
        draw.polygon(
            [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)],
            fill=(*color, 200),
            outline=(*color, 255)
        )

    def _draw_info_panel(self, draw: ImageDraw.ImageDraw, screen_size: Tuple[int, int]):
        """Рисовать информационную панель"""
        try:
            # Координаты панели (верхний левый угол)
            panel_x = 20
            panel_y = 20
            panel_width = 300
            panel_height = 150
            
            # Полупрозрачный фон панели
            draw.rectangle(
                [(panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height)],
                fill=(0, 0, 0, 100),
                outline=(200, 200, 200, 200)
            )
            
            # Текст информации
            info_lines = [
                "📍 МАРШРУТ ФАРМА",
                f"Спотов: {len(self.farm_route)}",
            ]
            
            if self.farm_route:
                next_spot = self.farm_route[0]
                info_lines.append(f"Первый: {next_spot.name}")
                info_lines.append(f"GPM: {next_spot.gold_per_minute}")
            
            # Рисовать текст
            y_offset = panel_y + 10
            for line in info_lines:
                draw.text(
                    (panel_x + 10, y_offset),
                    line,
                    fill=(0, 255, 0, 255),
                    font=None
                )
                y_offset += 30
                
        except Exception as e:
            logger.error(f"Ошибка при рисовании панели: {e}")

    def create_overlay_window(self):
        """
        Создать прозрачное окно оверлея (использует tkinter)
        Это экспериментальная функция для Windows
        """
        try:
            import tkinter as tk
            from PIL import ImageTk
            
            self.overlay_window = tk.Tk()
            self.overlay_window.attributes('-topmost', True)
            self.overlay_window.attributes('-alpha', self.overlay_alpha)
            
            logger.info("💻 Окно оверлея создано (экспериментально)")
            return self.overlay_window
            
        except Exception as e:
            logger.warning(f"⚠️ Оверлей окно не поддерживается: {e}")
            return None
