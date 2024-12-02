"""
Проект 5: Алгоритмы отсечения отрезков

Реализация алгоритмов:
1. Алгоритм Сазерленда-Коэна
2. Алгоритм разбиения средней точкой

Особенности:
- Отсечение отрезков по двумерному прямоугольному окну
- Определение полностью видимых и невидимых отрезков
- Визуализация процесса отсечения
- Интерактивное добавление отрезков
- Сравнение эффективности алгоритмов

Управление:
- 1 - Алгоритм Сазерленда-Коэна
- 2 - Алгоритм разбиения средней точкой
- I - Показать/скрыть информацию
- B - Тест производительности
- ЛКМ - Добавить отрезок

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import random
import math
import time
from utils.geometry import GeometryUtils
from utils.graphics import GraphicsBuffer
from utils.ui import UIManager
from utils.benchmark import Benchmark

class LineClipper:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Алгоритмы отсечения отрезков")
        
        self.buffer = GraphicsBuffer(self.width, self.height)
        self.ui = UIManager()
        self.geometry = GeometryUtils()
        
        # Параметры отображения
        self.scale = 1
        self.offset = [400, 300]  # Смещение для центрирования координат
        
        # Окно отсечения
        self.set_window(-100, -100, 100, 100)

    def get_circle_points(self, radius=150, num_points=16):
        """Генерация точек по окружности"""
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append((x, y))
        return points

    def draw_demo_lines(self):
        """Отрисовка демонстрационных линий"""
        # Генерируем точки по окружности
        points = self.get_circle_points()
        lines = []
        
        # Создаем линии от центра к точкам окружности
        for point in points:
            lines.append((0, 0, point[0], point[1]))
        
        return lines

    def set_window(self, xmin, ymin, xmax, ymax):
        self.window = [xmin, ymin, xmax, ymax]

    def get_code(self, x, y):
        """Вычисление кода точки для алгоритма Сазерленда-Коэна"""
        code = 0
        if x < self.window[0]:  # Слева
            code |= 1
        elif x > self.window[2]:  # Справа
            code |= 2
        if y < self.window[1]:  # Снизу
            code |= 4
        elif y > self.window[3]:  # Сверху
            code |= 8
        return code

    def cohen_sutherland(self, x1, y1, x2, y2):
        """Алгоритм Сазерленда-Коэна"""
        code1 = self.get_code(x1, y1)
        code2 = self.get_code(x2, y2)
        accept = False

        while True:
            if code1 == 0 and code2 == 0:  # Полностью видимый
                accept = True
                break
            elif code1 & code2 != 0:  # Полностью невидимый
                break
            else:
                # Частично видимый
                code = code1 if code1 != 0 else code2
                x, y = 0, 0

                if code & 1:  # Пересечение с левой границей
                    y = y1 + (y2 - y1) * (self.window[0] - x1) / (x2 - x1)
                    x = self.window[0]
                elif code & 2:  # Пересечение с правой границей
                    y = y1 + (y2 - y1) * (self.window[2] - x1) / (x2 - x1)
                    x = self.window[2]
                elif code & 4:  # Пересечение с нижней границей
                    x = x1 + (x2 - x1) * (self.window[1] - y1) / (y2 - y1)
                    y = self.window[1]
                elif code & 8:  # Пересечение с верхней границей
                    x = x1 + (x2 - x1) * (self.window[3] - y1) / (y2 - y1)
                    y = self.window[3]

                if code == code1:
                    x1, y1 = x, y
                    code1 = self.get_code(x1, y1)
                else:
                    x2, y2 = x, y
                    code2 = self.get_code(x2, y2)

        return accept, (x1, y1, x2, y2) if accept else None

    def midpoint_subdivision(self, x1, y1, x2, y2):
        """Алгоритм разбиения средней точкой"""
        code1 = self.get_code(x1, y1)
        code2 = self.get_code(x2, y2)

        # Если оба конца внутри окна
        if code1 == 0 and code2 == 0:
            return True, (x1, y1, x2, y2)
        
        # Если отрезок полностью невидим
        if code1 & code2 != 0:
            return False, None

        # Находим среднюю точку
        xm = (x1 + x2) / 2
        ym = (y1 + y2) / 2
        codem = self.get_code(xm, ym)

        # Рекурсивно проверяем обе половины
        if abs(x2 - x1) < 1 and abs(y2 - y1) < 1:
            return True, (x1, y1, x2, y2)

        # Проверяем первую половину
        accept1, line1 = self.midpoint_subdivision(x1, y1, xm, ym)
        # Проверяем вторую половину
        accept2, line2 = self.midpoint_subdivision(xm, ym, x2, y2)

        if accept1 and accept2:
            return True, (line1[0], line1[1], line2[2], line2[3])
        elif accept1:
            return True, line1
        elif accept2:
            return True, line2
        return False, None

    def benchmark(self, algorithm, iterations=100):
        """Тестирование производительности"""
        total_time = 0
        for _ in range(iterations):
            x1 = random.uniform(-150, 150)
            y1 = random.uniform(-150, 150)
            x2 = random.uniform(-150, 150)
            y2 = random.uniform(-150, 150)
            
            start_time = time.time()
            if algorithm == "cohen":
                self.cohen_sutherland(x1, y1, x2, y2)
            else:
                self.midpoint_subdivision(x1, y1, x2, y2)
            total_time += time.time() - start_time
            
        return total_time / iterations

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Алгоритмы отсечения отрезков")
    
    clipper = LineClipper()
    clock = pygame.time.Clock()
    
    current_algorithm = "cohen"  # или "midpoint"
    show_info = True
    lines = clipper.draw_demo_lines()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_algorithm = "cohen"
                elif event.key == pygame.K_2:
                    current_algorithm = "midpoint"
                elif event.key == pygame.K_i:
                    show_info = not show_info
                elif event.key == pygame.K_b:
                    # Запуск теста производительности
                    cohen_time = clipper.benchmark("cohen")
                    midpoint_time = clipper.benchmark("midpoint")
                    print(f"Cohen-Sutherland time: {cohen_time*1000:.6f} ms")
                    print(f"Midpoint time: {midpoint_time*1000:.6f} ms")
        
        # Отрисовка
        screen.fill((0, 0, 0))
        
        # Рисуем окно отсечения
        pygame.draw.rect(screen, (50, 50, 50),
                        (clipper.offset[0] + clipper.window[0] * clipper.scale,
                         clipper.offset[1] - clipper.window[3] * clipper.scale,
                         (clipper.window[2] - clipper.window[0]) * clipper.scale,
                         (clipper.window[3] - clipper.window[1]) * clipper.scale))
        
        # Рисуем все отрезки
        for line in lines:
            # Исходный отрезок (серым)
            pygame.draw.line(screen, (100, 100, 100),
                           (clipper.offset[0] + line[0] * clipper.scale,
                            clipper.offset[1] - line[1] * clipper.scale),
                           (clipper.offset[0] + line[2] * clipper.scale,
                            clipper.offset[1] - line[3] * clipper.scale))
            
            # Отсеченный отрезок (если видим)
            if current_algorithm == "cohen":
                accept, clipped = clipper.cohen_sutherland(line[0], line[1], line[2], line[3])
            else:
                accept, clipped = clipper.midpoint_subdivision(line[0], line[1], line[2], line[3])
                
            if accept and clipped:
                pygame.draw.line(screen, (255, 255, 255),
                               (clipper.offset[0] + clipped[0] * clipper.scale,
                                clipper.offset[1] - clipped[1] * clipper.scale),
                               (clipper.offset[0] + clipped[2] * clipper.scale,
                                clipper.offset[1] - clipped[3] * clipper.scale), 2)
        
        if show_info:
            info_text = [
                f"Алгоритм: {'Сазерленд-Коэн' if current_algorithm == 'cohen' else 'Разбиение средней точкой'}",
                "Управление:",
                "1 - Алгоритм Сазерленда-Коэна",
                "2 - Алгоритм разбиения средней точкой",
                "I - Показать/скрыть информацию",
                "B - Тест производительности",
                "ЛКМ - Добавить отрезок"
            ]
            
            clipper.ui.draw_text_list(screen, info_text, 10, 10)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 