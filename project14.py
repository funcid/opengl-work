"""
Проект 14: Растеризация эллипса

Реализация двух алгоритмов растеризации эллипса:
1. Алгоритм Брезенхема для эллипса
2. Полупиксельный алгоритм

Тестовые параметры:
- Размер псевдорастра: 32x32
- Полуоси эллипса: a=15, b=20
- Псевдобуфер в виде одномерного массива
- Вывод в формате "строка-колонка"

Особенности:
- Визуализация процесса растеризации
- Сравнение алгоритмов
- Тест производительности на 100 эллипсах
- Поддержка градаций серого
- Вывод координат точек

Управление:
- 1 - Алгоритм Брезенхема
- 2 - Полупиксельный алгоритм
- B - Тест производительности

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import numpy as np
from utils.graphics import GraphicsBuffer
from utils.ui import UIManager
from utils.benchmark import Benchmark
import sys

class EllipseRasterizer:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Алгоритмы растеризации эллипса")
        
        self.buffer = GraphicsBuffer(32, 32)
        self.ui = UIManager()
        
        # Размеры псевдорастра
        self.raster_size = 32
        self.cell_size = 20
        
        # Параметры эллипса
        self.a = 15  # Большая полуось
        self.b = 20  # Малая полуось
        
        # Список точек для вывода
        self.points = []
        
        # Текущий алгоритм
        self.current_algorithm = "bresenham"  # или "subpixel"

    def clear_buffer(self):
        """Очистка буфера"""
        self.buffer.clear()
        self.points = []

    def bresenham_ellipse(self):
        """Алгоритм Брезенхема для эллипса"""
        x = 0
        y = self.b
        
        # Начальные значения для облати 1
        d1 = (self.b * self.b) - (self.a * self.a * self.b) + (0.25 * self.a * self.a)
        dx = 2 * self.b * self.b * x
        dy = 2 * self.a * self.a * y
        
        # Первая область
        while dx < dy:
            self.plot_points(x, y)
            
            if d1 < 0:
                x += 1
                dx += 2 * self.b * self.b
                d1 += dx + self.b * self.b
            else:
                x += 1
                y -= 1
                dx += 2 * self.b * self.b
                dy -= 2 * self.a * self.a
                d1 += dx - dy + self.b * self.b
        
        # Начальные значения для области 2
        d2 = ((self.b * self.b) * ((x + 0.5) * (x + 0.5))) + \
             ((self.a * self.a) * ((y - 1) * (y - 1))) - \
             (self.a * self.a * self.b * self.b)
        
        # Вторая область
        while y >= 0:
            self.plot_points(x, y)
            
            if d2 > 0:
                y -= 1
                dy -= 2 * self.a * self.a
                d2 += self.a * self.a - dy
            else:
                y -= 1
                x += 1
                dx += 2 * self.b * self.b
                dy -= 2 * self.a * self.a
                d2 += dx - dy + self.a * self.a

    def subpixel_ellipse(self):
        """Полупиксельный алгоритм для эллипса"""
        # Создаем массив подпикселей (4x4 для каждого пикселя)
        subpixel_size = 4
        subpixel_buffer = np.zeros((self.raster_size * subpixel_size, 
                                  self.raster_size * subpixel_size))
        
        # Масштабируем параметры эллипса
        a_sub = self.a * subpixel_size
        b_sub = self.b * subpixel_size
        
        # Рисуем эллипс в подпиксельном буфере
        for x in range(-a_sub, a_sub + 1):
            y = int(b_sub * np.sqrt(1 - (x/a_sub)**2))
            for dy in [-1, 1]:
                sub_x = x + a_sub
                sub_y = y * dy + b_sub
                if 0 <= sub_x < self.raster_size * subpixel_size and \
                   0 <= sub_y < self.raster_size * subpixel_size:
                    subpixel_buffer[int(sub_y), int(sub_x)] = 1
        
        # Преобразуем подпиксельный буфер в обычный
        for y in range(self.raster_size):
            for x in range(self.raster_size):
                subpixels = subpixel_buffer[y*subpixel_size:(y+1)*subpixel_size,
                                          x*subpixel_size:(x+1)*subpixel_size]
                self.buffer.set_pixel(x, y, np.sum(subpixels) / (subpixel_size * subpixel_size))
                if self.buffer.get_pixel(x, y) > 0:
                    self.points.append((x - self.raster_size//2, 
                                     y - self.raster_size//2))

    def plot_points(self, x, y):
        """Отображение точек с учетом симметрии эллипса"""
        points = [
            (x, y), (-x, y), (x, -y), (-x, -y)
        ]
        
        for px, py in points:
            # Смещаем координаты к центру растра
            shifted_x = px + self.raster_size//2
            shifted_y = py + self.raster_size//2
            
            if 0 <= shifted_x < self.raster_size and 0 <= shifted_y < self.raster_size:
                self.buffer.set_pixel(shifted_x, shifted_y, 1)
                self.points.append((px, py))

    def benchmark(self):
        """Тестирование производительности"""
        def test_bresenham():
            self.clear_buffer()
            self.bresenham_ellipse()
            
        def test_subpixel():
            self.clear_buffer()
            self.subpixel_ellipse()
            
        bresenham_time = Benchmark.measure_time(test_bresenham)
        subpixel_time = Benchmark.measure_time(test_subpixel)
        
        # Выводим результаты в консоль на английском
        print("\nBenchmark results:")
        print(f"Bresenham: {bresenham_time*1000:.6f} ms")
        print(f"Subpixel: {subpixel_time*1000:.6f} ms")
                
        return {
            "bresenham": bresenham_time,
            "subpixel": subpixel_time
        }

    def draw(self):
        """Отрисовка всех элементов"""
        self.screen.fill((0, 0, 0))
        
        # Рисуем сетку и пиксели
        offset_x = 50
        offset_y = 50
        
        for y in range(self.raster_size):
            for x in range(self.raster_size):
                rect = pygame.Rect(
                    offset_x + x * self.cell_size,
                    offset_y + y * self.cell_size,
                    self.cell_size - 1,
                    self.cell_size - 1
                )
                
                if self.buffer.get_pixel(x, y) > 0:
                    # Для полупиксельного алгоритма используем градации серого
                    color = int(self.buffer.get_pixel(x, y) * 255)
                    pygame.draw.rect(self.screen, (color, color, color), rect)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)
        
        # Отображение информации
        info_text = [
            f"Алгоритм: {'Брезенхем' if self.current_algorithm == 'bresenham' else 'Полупиксельный'}",
            f"Размер растра: {self.raster_size}x{self.raster_size}",
            f"Полуоси: a={self.a}, b={self.b}",
            "Управление:",
            "1 - Алгоритм Брезенхема",
            "2 - Полупиксельный алгоритм",
            "B - Тест производительности",
            "Точки в формате (строка-колонка):"
        ]
        
        y_offset = 50
        for text in info_text:
            self.ui.draw_text(self.screen, text, (800, y_offset))
            y_offset += 25
        
        # Вывод оординат точек
        if len(self.points) > 0:
            points_text = [f"({x}, {y})" for x, y in sorted(set(self.points))]
            for i, text in enumerate(points_text[:20]):  # Ограничивм вывод 20 точками
                self.ui.draw_text(self.screen, text, (800, y_offset + i * 20), (200, 200, 200))

    def run(self):
        """Основной цикл программы"""
        clock = pygame.time.Clock()
        running = True
        
        # Начальная отрисовка
        self.clear_buffer()
        if self.current_algorithm == "bresenham":
            self.bresenham_ellipse()
        else:
            self.subpixel_ellipse()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.current_algorithm = "bresenham"
                        self.clear_buffer()
                        self.bresenham_ellipse()
                    elif event.key == pygame.K_2:
                        self.current_algorithm = "subpixel"
                        self.clear_buffer()
                        self.subpixel_ellipse()
                    elif event.key == pygame.K_b:
                        # Запуск теста производительности
                        results = self.benchmark()
                        print("\nBenchmark results:")
                        for alg, time in results.items():
                            print(f"{alg}: {time*1000:.6f} ms")
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

def main():
    rasterizer = EllipseRasterizer()
    rasterizer.run()

if __name__ == "__main__":
    main() 