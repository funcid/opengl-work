"""
Проект 8: Алгоритм Сазерленда-Ходжмена

Реализация алгоритма отсечения многоугольников:
- Отсечение по прямоугольному окну
- Визуализация каждого этапа отсечения
- Тестовый многоугольник с координатами:
  (-4,2), (8,14), (8,2), (12,6), (12,-2), (4,-2), (4,6), (0,2)
- Окно отсечения: (0,0), (10,0), (10,10), (0,10)

Особенности:
- Пошаговая визуализация процесса
- Отображение исходного многоугольника
- Отображение окна отсечения
- Вывод результирующего многоугольника
- Интерактивное управление просмотром

Управление:
- Пробел - Показать/скрыть этапы
- Стрелки влево/вправо - Переключение этапов
- ЛКМ - Добавить новую точку

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import numpy as np
from utils.geometry import GeometryUtils
from utils.graphics import GraphicsBuffer
from utils.ui import UIManager
from utils.benchmark import Benchmark

class SutherlandHodgmanClipper:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Алгоритм Сазерленда-Ходжмена")
        
        self.buffer = GraphicsBuffer(self.width, self.height)
        self.ui = UIManager()
        self.geometry = GeometryUtils()
        
        self.scale = 30
        self.offset = [400, 300]
        
        # Тестовый многоугольник
        self.polygon = [
            (-4, 2), (8, 14), (8, 2), (12, 6),
            (12, -2), (4, -2), (4, 6), (0, 2)
        ]
        
        # Окно отсечения
        self.window = [(0, 0), (10, 0), (10, 10), (0, 10)]
        
        # История отсечения для визуализации этапов
        self.clipping_history = []

    def get_line_intersection(self, p1, p2, p3, p4):
        """Находит точку пересечения двух отрезков"""
        return self.geometry.get_line_intersection(p1, p2, p3, p4)

    def is_inside(self, point, edge_start, edge_end):
        """Проверяет, находится ли точка внутри относительно ребра"""
        edge_vector = (edge_end[0] - edge_start[0], edge_end[1] - edge_start[1])
        point_vector = (point[0] - edge_start[0], point[1] - edge_start[1])
        return self.geometry.dot_product((-edge_vector[1], edge_vector[0]), point_vector) >= 0

    def clip_polygon(self):
        """Алгоритм Сазерленда-Ходжмена"""
        input_polygon = self.polygon.copy()
        self.clipping_history = [input_polygon.copy()]
        
        for i in range(len(self.window)):
            edge_start = self.window[i]
            edge_end = self.window[(i + 1) % len(self.window)]
            
            output_polygon = []
            
            for j in range(len(input_polygon)):
                current = input_polygon[j]
                prev = input_polygon[j - 1]
                
                # Находим точку пересечения
                intersection = self.get_line_intersection(prev, current, edge_start, edge_end)
                
                # Если текущая точка внутри
                if self.is_inside(current, edge_start, edge_end):
                    # Если предыдущая точка снаружи, добавляем точку пересечения
                    if not self.is_inside(prev, edge_start, edge_end):
                        if intersection:
                            output_polygon.append(intersection)
                    output_polygon.append(current)
                # Если текущая точка снаружи, но предыдущая внутри
                elif self.is_inside(prev, edge_start, edge_end):
                    if intersection:
                        output_polygon.append(intersection)
            
            input_polygon = output_polygon
            if output_polygon:
                self.clipping_history.append(output_polygon.copy())
        
        return input_polygon

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Алгоритм Сазерленда-Ходжмена")
    
    clipper = SutherlandHodgmanClipper()
    clock = pygame.time.Clock()
    
    # Начальное отсечение
    clipped_polygon = clipper.clip_polygon()
    show_steps = False
    current_step = 0
    font = pygame.font.Font(None, 24)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_steps = not show_steps
                    current_step = 0
                elif event.key == pygame.K_RIGHT and show_steps:
                    current_step = (current_step + 1) % len(clipper.clipping_history)
                elif event.key == pygame.K_LEFT and show_steps:
                    current_step = (current_step - 1) % len(clipper.clipping_history)
        
        screen.fill((0, 0, 0))
        
        # Рисуем окно отсечения
        window_points = [(clipper.offset[0] + x * clipper.scale,
                         clipper.offset[1] - y * clipper.scale) for x, y in clipper.window]
        pygame.draw.polygon(screen, (50, 50, 50), window_points)
        pygame.draw.polygon(screen, (100, 100, 100), window_points, 1)
        
        # Рисуем исходный многоугольник
        polygon_points = [(clipper.offset[0] + x * clipper.scale,
                          clipper.offset[1] - y * clipper.scale) for x, y in clipper.polygon]
        pygame.draw.polygon(screen, (100, 100, 100), polygon_points, 1)
        
        # Рисуем текущий этап или финальный результат
        if show_steps and clipper.clipping_history:
            current_polygon = clipper.clipping_history[current_step]
            points = [(clipper.offset[0] + x * clipper.scale,
                      clipper.offset[1] - y * clipper.scale) for x, y in current_polygon]
            if points:
                pygame.draw.polygon(screen, (0, 255, 0), points, 2)
        else:
            # Рисуем отсеченный многоугольник
            clipped_points = [(clipper.offset[0] + x * clipper.scale,
                             clipper.offset[1] - y * clipper.scale) for x, y in clipped_polygon]
            if clipped_points:
                pygame.draw.polygon(screen, (255, 255, 255), clipped_points, 2)
        
        # Отображение информации
        info_text = [
            "Управление:",
            "Пробел - показать/скрыть этапы",
            "Стрелки влево/вправо - переключение этапов",
            f"Этап: {current_step + 1}/{len(clipper.clipping_history)}" if show_steps else "Финальный результат"
        ]
        
        y_offset = 10
        for text in info_text:
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 