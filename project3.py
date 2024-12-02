"""
Проект 3: Алгоритмы рисования линий

Реализация и сравнение алгоритмов:
1. Цифровой дифференциальный анализатор (ЦДА)
2. Алгоритм Брезенхема

Особенности:
- Размер растра: 32x32
- Визуализация процесса построения
- Два режима работы: демо и тест
- Отображение координат точек
- Сравнение производительности
- Интерактивное управление

Управление:
- 1 - Алгоритм ЦДА
- 2 - Алгоритм Брезенхема
- Пробел - Переключение режима
- C - Показать/скрыть координаты
- B - Тест производительности
- ЛКМ - Установить центр в демо-режиме

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import random
import math
import time
from utils.opengl_utils import OpenGLUtils

class LineDrawer:
    def __init__(self):
        self.width = 32
        self.height = 32
        self.scale = 20  # Размер одного пикселя на экране
        self.center = (16, 16)  # Центр координат
        self.buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.active_pixels = []  # Для хранения активированных пикселей
        
    def clear_buffer(self):
        self.buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.active_pixels = []

    def set_pixel(self, x, y):
        # Преобразование координат в координаты растра
        screen_x = int(x + self.center[0])
        screen_y = int(y + self.center[1])
        
        if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
            self.buffer[screen_y][screen_x] = 1
            self.active_pixels.append((screen_x, screen_y))

    def dda_line(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            self.set_pixel(x1, y1)
            return
            
        x_increment = dx / steps
        y_increment = dy / steps
        
        x = x1
        y = y1
        
        for _ in range(int(steps) + 1):
            self.set_pixel(x, y)
            x += x_increment
            y += y_increment

    def bresenham_line(self, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        x, y = x1, y1
        
        step_x = 1 if x2 > x1 else -1
        step_y = 1 if y2 > y1 else -1
        
        if dx > dy:
            err = dx / 2
            while x != x2:
                self.set_pixel(x, y)
                err -= dy
                if err < 0:
                    y += step_y
                    err += dx
                x += step_x
        else:
            err = dy / 2
            while y != y2:
                self.set_pixel(x, y)
                err -= dx
                if err < 0:
                    x += step_x
                    err += dy
                y += step_y
                
        self.set_pixel(x, y)

    def draw_circle_points(self, center, points=16):
        result = []
        for i in range(points):
            angle = 2 * math.pi * i / points
            x = int(8 * math.cos(angle))
            y = int(8 * math.sin(angle))
            result.append((x, y))
        return result

    def benchmark(self, algorithm, iterations=100):
        total_time = 0
        for _ in range(iterations):
            x1 = random.randint(-15, 15)
            y1 = random.randint(-15, 15)
            x2 = random.randint(-15, 15)
            y2 = random.randint(-15, 15)
            
            start_time = time.time()
            if algorithm == "dda":
                self.dda_line(x1, y1, x2, y2)
            else:
                self.bresenham_line(x1, y1, x2, y2)
            total_time += time.time() - start_time
            
            self.clear_buffer()
            
        return total_time / iterations

def main():
    pygame.init()
    window_size = (800, 800)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Алгоритмы рисования линий")
    
    drawer = LineDrawer()
    clock = pygame.time.Clock()
    
    # Флаги для выбора алгоритма и режима
    current_algorithm = "dda"  # или "bresenham"
    demo_mode = True  # True - демо с кругом, False - тестовая линия
    show_coordinates = False
    center_x, center_y = 0, 0
    
    # Создаем шрифт для отобржения текста
    font = pygame.font.Font(None, 24)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_algorithm = "dda"
                elif event.key == pygame.K_2:
                    current_algorithm = "bresenham"
                elif event.key == pygame.K_SPACE:
                    demo_mode = not demo_mode
                elif event.key == pygame.K_c:
                    show_coordinates = not show_coordinates
                elif event.key == pygame.K_b:
                    # Запуск бенчмарка
                    dda_time = drawer.benchmark("dda")
                    bresenham_time = drawer.benchmark("bresenham")
                    print(f"DDA average time: {dda_time*1000:.6f} ms")
                    print(f"Bresenham average time: {bresenham_time*1000:.6f} ms")
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    mouse_x = (event.pos[0] // drawer.scale) - drawer.center[0]
                    mouse_y = (event.pos[1] // drawer.scale) - drawer.center[1]
                    center_x, center_y = mouse_x, mouse_y
        
        drawer.clear_buffer()
        
        if demo_mode:
            # Рисуем 16 линий из центра к точкам окружности
            points = drawer.draw_circle_points((center_x, center_y))
            for point in points:
                if current_algorithm == "dda":
                    drawer.dda_line(center_x, center_y, center_x + point[0], center_y + point[1])
                else:
                    drawer.bresenham_line(center_x, center_y, center_x + point[0], center_y + point[1])
        else:
            # Рисуем тестовую линию (0,0) -> (-8,-3)
            if current_algorithm == "dda":
                drawer.dda_line(0, 0, -8, -3)
            else:
                drawer.bresenham_line(0, 0, -8, -3)
        
        # Отрисовка
        screen.fill((0, 0, 0))
        
        # Рисуем сетку
        for x in range(drawer.width):
            for y in range(drawer.height):
                rect = pygame.Rect(
                    x * drawer.scale, 
                    y * drawer.scale, 
                    drawer.scale - 1, 
                    drawer.scale - 1
                )
                if drawer.buffer[y][x]:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                else:
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)
        
        # Отображение минимальной информации
        info_text = [
            f"Алгоритм: {'ЦДА' if current_algorithm == 'dda' else 'Брезенхем'}",
            f"Режим: {'Демо' if demo_mode else 'Тест'}",
            f"Растр: 32x32"
        ]
        
        # Смещаем текст в левый верхний угол и уменьшаем шрифт
        font = pygame.font.Font(None, 20)  # Уменьшаем размер шрифта
        y_offset = 10
        x_offset = 10  # Отступ слева
        for text in info_text:
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (x_offset, y_offset))
            y_offset += 20  # Уменьшаем межстрочный интервал
        
        # Отображение координат активных пикселей
        if show_coordinates:
            for pixel in drawer.active_pixels:
                coord_text = f"({pixel[0]-drawer.center[0]},{pixel[1]-drawer.center[1]})"
                text_surface = font.render(coord_text, True, (255, 255, 0))
                screen.blit(text_surface, 
                          (pixel[0] * drawer.scale, 
                           pixel[1] * drawer.scale - 15))  # Уменьшаем отступ для координат
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 