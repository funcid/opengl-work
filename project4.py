"""
Проект 4: Алгоритмы построения окружности

Реализация и сравнение алгоритмов:
1. Алгоритм Брезенхема для окружности
2. Метод вписанного многоугольника

Особенности:
- Размер растра: 32x32
- Радиус окружности: 15 единиц
- Настраиваемое количество сторон для многоугольника
- Визуализация процесса построения
- Сравнение точности аппроксимации
- Интерактивное управление

Управление:
- 1 - Алгоритм Брезенхема
- 2 - Метод многоугольника
- 4,8,6,3,7 - Количество сторон (4,8,16,32,128)
- C - Показать/скрыть координаты
- B - Тест производительности
- ЛКМ - Установить центр окружности

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import math
import time
import random
from utils.opengl_utils import OpenGLUtils
from utils.ui import UIManager

class CircleDrawer:
    def __init__(self):
        self.width = 32
        self.height = 32
        self.scale = 20
        self.center = (16, 16)
        self.buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.active_pixels = []
        self.radius = 15
        self.sides = 16  # Количество сторон для многоугольника
        
    def clear_buffer(self):
        self.buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.active_pixels = []

    def set_pixel(self, x, y):
        screen_x = int(x + self.center[0])
        screen_y = int(y + self.center[1])
        
        if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
            self.buffer[screen_y][screen_x] = 1
            self.active_pixels.append((screen_x, screen_y))

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

    def bresenham_circle(self):
        x = 0
        y = self.radius
        d = 3 - 2 * self.radius
        
        while x <= y:
            # Отражаем точки во все октанты
            self.set_pixel(x, y)
            self.set_pixel(-x, y)
            self.set_pixel(x, -y)
            self.set_pixel(-x, -y)
            self.set_pixel(y, x)
            self.set_pixel(-y, x)
            self.set_pixel(y, -x)
            self.set_pixel(-y, -x)
            
            if d < 0:
                d = d + 4 * x + 6
            else:
                d = d + 4 * (x - y) + 10
                y -= 1
            x += 1

    def polygon_circle(self, sides):
        points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            x = int(self.radius * math.cos(angle))
            y = int(self.radius * math.sin(angle))
            points.append((x, y))
        
        # Соединяем точки линиями
        for i in range(sides):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % sides]
            self.bresenham_line(x1, y1, x2, y2)

def main():
    pygame.init()
    window_size = (800, 800)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Алгоритмы построения окружности")
    
    drawer = CircleDrawer()
    clock = pygame.time.Clock()
    ui = UIManager()
    
    current_method = "bresenham"  # или "polygon"
    show_coordinates = False
    
    font = pygame.font.Font(None, 20)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_method = "bresenham"
                elif event.key == pygame.K_2:
                    current_method = "polygon"
                elif event.key == pygame.K_c:
                    show_coordinates = not show_coordinates
                elif event.key in [pygame.K_4, pygame.K_8, pygame.K_6, pygame.K_3, pygame.K_6, pygame.K_7]:
                    # Изменение количества сторон многоугольника
                    if event.key == pygame.K_4: drawer.sides = 4
                    elif event.key == pygame.K_8: drawer.sides = 8
                    elif event.key == pygame.K_6: drawer.sides = 16
                    elif event.key == pygame.K_3: drawer.sides = 32
                    elif event.key == pygame.K_6: drawer.sides = 64
                    elif event.key == pygame.K_7: drawer.sides = 128
        
        drawer.clear_buffer()
        
        if current_method == "bresenham":
            drawer.bresenham_circle()
        else:
            drawer.polygon_circle(drawer.sides)
        
        # Отрисовка
        screen.fill((0, 0, 0))
        
        # Рисуем активные пиксели и сетку
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
        
        # Отображение информации через UIManager
        info_text = [
            f"Метод: {'Брезенхем' if current_method == 'bresenham' else 'Многоугольник'}",
            f"Растр: 32x32",
            f"Радиус: {drawer.radius}",
            f"Стороны: {drawer.sides if current_method == 'polygon' else 'N/A'}"
        ]
        
        ui.draw_text_list(screen, info_text, 10, 10, 20)
        
        if show_coordinates:
            for pixel in drawer.active_pixels:
                coord_text = f"({pixel[0]-drawer.center[0]},{pixel[1]-drawer.center[1]})"
                text_surface = font.render(coord_text, True, (255, 255, 0))
                screen.blit(text_surface, 
                          (pixel[0] * drawer.scale, 
                           pixel[1] * drawer.scale - 15))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 