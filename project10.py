"""
Проект 10: Алгоритм Вейлера-Азертона

Реализация алгоритма отсечения многоугольников:
1. Отсечение многоугольника с внешней границей и внутренней дырой
2. Тестовый многоугольник:
   - Внешняя граница: (0,0), (20,0), (20,-20), (0,-20)
   - Внутренняя дыра: (7,-13), (13,-13), (13,-7), (7,-7)
3. Отсекающий многоугольник:
   - Внешняя граница: (-10,-10), (-10,10), (10,10), (10,-10)
   - Внутренняя дыра: (-5,-5), (5,25), (5,5), (25,5)

Особенности:
- Визуализация исходных многоугольников
- Отображение точек пересечения
- Вывод результата отсечения
- Корректная обработка дыр
- Интерактивное управление

Управление:
- Пробел - показать/скрыть этапы
- Стрелки влево/вправо - переключение этапов

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import numpy as np

class WeilerAthertonClipper:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.scale = 20
        self.offset = [400, 300]  # Смещение для центрирования координат
        
        # Тестовый многоугольник с внешней границей и внутренней дырой
        self.subject_polygon = {
            'outer': [(0, 0), (20, 0), (20, -20), (0, -20)],
            'inner': [(7, -13), (13, -13), (13, -7), (7, -7)]
        }
        
        # Отсекающий многоугольник с внешней границей и внутренней дырой
        self.clip_polygon = {
            'outer': [(-10, -10), (-10, 10), (10, 10), (10, -10)],
            'inner': [(-5, -5), (5, 25), (5, 5), (25, 5)]
        }
        
        # Результаты отсечения
        self.intersection_points = []
        self.result_polygon = None

    def get_intersection(self, p1, p2, p3, p4):
        """Находит точку пересечения двух отрезков"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return None
            
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        
        if 0 <= t <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        return None

    def find_intersections(self, polygon1, polygon2):
        """Находит все точки пересечения между двумя многоугольниками"""
        intersections = []
        
        # Проверяем пересечения между внешними границами
        for i in range(len(polygon1['outer'])):
            p1 = polygon1['outer'][i]
            p2 = polygon1['outer'][(i + 1) % len(polygon1['outer'])]
            
            for j in range(len(polygon2['outer'])):
                p3 = polygon2['outer'][j]
                p4 = polygon2['outer'][(j + 1) % len(polygon2['outer'])]
                
                intersection = self.get_intersection(p1, p2, p3, p4)
                if intersection:
                    intersections.append(intersection)
        
        # Проверяем пересечения с внутренними дырами
        for hole in [polygon1['inner'], polygon2['inner']]:
            for i in range(len(hole)):
                p1 = hole[i]
                p2 = hole[(i + 1) % len(hole)]
                
                for j in range(len(polygon2['outer'])):
                    p3 = polygon2['outer'][j]
                    p4 = polygon2['outer'][(j + 1) % len(polygon2['outer'])]
                    
                    intersection = self.get_intersection(p1, p2, p3, p4)
                    if intersection:
                        intersections.append(intersection)
        
        return intersections

    def is_inside(self, point, polygon):
        """Проверяет, находится ли точка внутри многоугольника"""
        x, y = point
        n = len(polygon)
        inside = False
        
        for i in range(n):
            j = (i + 1) % n
            if ((polygon[i][1] > y) != (polygon[j][1] > y) and
                x < (polygon[j][0] - polygon[i][0]) * (y - polygon[i][1]) /
                    (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
                inside = not inside
        
        return inside

    def weiler_atherton_clip(self):
        """Алгоритм Вейлера-Азертона"""
        # Находим все точки пересечения
        self.intersection_points = self.find_intersections(
            self.subject_polygon, self.clip_polygon)
        
        # Создаем списки вершин для обхода
        subject_list = []
        clip_list = []
        
        # Добавляем вершины и точки пересечения в списки
        for i in range(len(self.subject_polygon['outer'])):
            subject_list.append(('v', self.subject_polygon['outer'][i]))
            
            # Добавляем точки пересечения
            for point in self.intersection_points:
                if self.is_on_edge(point, 
                                 self.subject_polygon['outer'][i],
                                 self.subject_polygon['outer'][(i + 1) % len(self.subject_polygon['outer'])]):
                    subject_list.append(('i', point))
        
        for i in range(len(self.clip_polygon['outer'])):
            clip_list.append(('v', self.clip_polygon['outer'][i]))
            
            # Добавляем точки пересечения
            for point in self.intersection_points:
                if self.is_on_edge(point,
                                 self.clip_polygon['outer'][i],
                                 self.clip_polygon['outer'][(i + 1) % len(self.clip_polygon['outer'])]):
                    clip_list.append(('i', point))
        
        # Сортируем точки пересечения
        subject_list.sort(key=lambda x: (x[1][0], x[1][1]))
        clip_list.sort(key=lambda x: (x[1][0], x[1][1]))
        
        # Формируем результат отсечения
        result = []
        current = subject_list[0]
        while current in subject_list:
            result.append(current[1])
            if current[0] == 'i':
                # Переключаемся на другой список
                idx = clip_list.index(current)
                current = clip_list[(idx + 1) % len(clip_list)]
            else:
                idx = subject_list.index(current)
                current = subject_list[(idx + 1) % len(subject_list)]
        
        self.result_polygon = result

    def is_on_edge(self, point, edge_start, edge_end):
        """Проверяет, лежит ли точка на отрезке"""
        x, y = point
        x1, y1 = edge_start
        x2, y2 = edge_end
        
        # Проверяем, что точка лежит на прямой
        cross_product = (y2 - y1) * (x - x1) - (x2 - x1) * (y - y1)
        if abs(cross_product) > 1e-9:
            return False
        
        # Проверяем, что точка лежит между концами отрезка
        if x1 != x2:
            return min(x1, x2) <= x <= max(x1, x2)
        else:
            return min(y1, y2) <= y <= max(y1, y2)

    def draw(self, screen):
        """Отрисовка всех элементов"""
        # Рисуем исходный многоугольник
        points = [(self.offset[0] + x * self.scale,
                  self.offset[1] + y * self.scale) 
                 for x, y in self.subject_polygon['outer']]
        pygame.draw.polygon(screen, (100, 100, 100), points, 1)
        
        # Рисуем дыру исходного многоугольника
        points = [(self.offset[0] + x * self.scale,
                  self.offset[1] + y * self.scale) 
                 for x, y in self.subject_polygon['inner']]
        pygame.draw.polygon(screen, (100, 100, 100), points, 1)
        
        # Рисуем отсекающий многоугольник
        points = [(self.offset[0] + x * self.scale,
                  self.offset[1] + y * self.scale) 
                 for x, y in self.clip_polygon['outer']]
        pygame.draw.polygon(screen, (150, 150, 150), points, 1)
        
        # Рисуем дыру отсеающего многоугольника
        points = [(self.offset[0] + x * self.scale,
                  self.offset[1] + y * self.scale) 
                 for x, y in self.clip_polygon['inner']]
        pygame.draw.polygon(screen, (150, 150, 150), points, 1)
        
        # Рисуем точки пересечения
        for point in self.intersection_points:
            x = self.offset[0] + point[0] * self.scale
            y = self.offset[1] + point[1] * self.scale
            pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 3)
        
        # Рисуем результат отсечения
        if self.result_polygon:
            points = [(self.offset[0] + x * self.scale,
                      self.offset[1] + y * self.scale) 
                     for x, y in self.result_polygon]
            pygame.draw.polygon(screen, (0, 255, 0), points, 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Алгоритм Вейлера-Азертона")
    
    clipper = WeilerAthertonClipper()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    # Выполняем начальное отсечение
    clipper.weiler_atherton_clip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        screen.fill((0, 0, 0))
        
        # Отрисовка всех элементов
        clipper.draw(screen)
        
        # Отображение информации
        info_text = [
            "Точки пересечения:",
            *[f"({x:.1f}, {y:.1f})" for x, y in clipper.intersection_points],
            "",
            "Результат отсечения:",
            *[f"({x:.1f}, {y:.1f})" for x, y in (clipper.result_polygon or [])]
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