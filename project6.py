"""
Проект 6: Алгоритм Кируса-Бека

Реализация алгоритма Кируса-Бека для отсечения отрезков:
- Тестовый восьмиугольник с координатами:
  V1(1,0), V2(0,1), V3(0,2), V4(1,3), V5(2,3), V6(3,2), V7(3,1), V8(2,0)
- Тестовый отрезок: P1(-1,1) до P2(3,3)

Особенности:
- Вывод таблицы параметров для каждого ребра:
  * n (вектор нормали)
  * f (точка на ребре)
  * w (весовая функция)
  * w·n (скалярное произведение)
  * D·n (скалярное произведение директрисы)
  * t (параметр)

Управление:
- I - Показать/скрыть информацию
- B - Тест производительности
- ЛКМ - Добавить новый отрезок

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import numpy as np
import math
import time  # Добавляем импорт time для бенчмарка
from utils.geometry import GeometryUtils
from utils.graphics import GraphicsBuffer
from utils.ui import UIManager
from utils.benchmark import Benchmark

class CyrusBeckClipper:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Алгоритм Кируса-Бека")
        
        self.buffer = GraphicsBuffer(self.width, self.height)
        self.ui = UIManager()
        self.geometry = GeometryUtils()
        
        # Добавляем параметры отображения
        self.scale = 50
        self.offset = [400, 300]  # Смещение для центрирования координат
        
        # Координаты вершин восьмиугольника
        self.vertices = [
            (1, 0), (0, 1), (0, 2), (1, 3),
            (2, 3), (3, 2), (3, 1), (2, 0)
        ]
        
        # Вычисляем нормали и точки для каждого ребра
        self.edges = []
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            
            # Вычисляем вектор ребра
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            
            # Вычисляем нормаль (перпендикулярный вектор)
            normal = (-edge[1], edge[0])
            length = math.sqrt(normal[0]**2 + normal[1]**2)
            normal = (normal[0]/length, normal[1]/length)
            
            # Сохраняем ребро, его нормаль и точку на ребре
            self.edges.append({
                'p': p1,
                'normal': normal,
                'edge': edge
            })

    def get_line_intersection(self, p1, p2, p3, p4):
        return self.geometry.get_line_intersection(p1, p2, p3, p4)

    def dot_product(self, v1, v2):
        return self.geometry.dot_product(v1, v2)

    def cyrus_beck(self, p1, p2):
        """Алгоритм Кируса-Бека для отсечения отрезка"""
        # Вектор направления отрезка
        D = (p2[0] - p1[0], p2[1] - p1[1])
        
        t_enter = 0.0  # Максимальный параметр входа
        t_exit = 1.0   # Минимальный параметр выхода
        
        # Таблица для вывода результатов
        results = []
        
        # Проверяем каждое ребро многоугольника
        for edge in self.edges:
            n = edge['normal']  # Нормаль к ребру
            w = edge['p']       # Точка на ребре
            
            # Вычисляем скалярные произведения
            D_dot_n = self.dot_product(D, n)
            w_minus_p = (w[0] - p1[0], w[1] - p1[1])
            w_dot_n = self.dot_product(w_minus_p, n)
            
            # Сохраняем результаты для вывода
            results.append({
                'n': n,
                'f': w,
                'w·n': w_dot_n,
                'D·n': D_dot_n,
                't': -(w_dot_n / D_dot_n) if D_dot_n != 0 else None
            })
            
            if D_dot_n == 0:  # Отрезок параллелен ребру
                if w_dot_n < 0:
                    return False, None, results  # Отрезок снаружи
                continue
            
            t = -w_dot_n / D_dot_n
            
            if D_dot_n < 0:  # Входящее пересечение
                t_enter = max(t_enter, t)
            else:  # Выходящее пересечение
                t_exit = min(t_exit, t)
                
            if t_enter > t_exit:
                return False, None, results  # Отрезок невидим
        
        if t_enter <= t_exit:
            # Вычисляем точки пересечения
            x1 = p1[0] + D[0] * t_enter
            y1 = p1[1] + D[1] * t_enter
            x2 = p1[0] + D[0] * t_exit
            y2 = p1[1] + D[1] * t_exit
            return True, ((x1, y1), (x2, y2)), results
        
        return False, None, results

    def benchmark(self, iterations=100):
        """Тестирование производительности"""
        total_time = 0
        for _ in range(iterations):
            x1 = np.random.uniform(-5, 5)
            y1 = np.random.uniform(-5, 5)
            x2 = np.random.uniform(-5, 5)
            y2 = np.random.uniform(-5, 5)
            
            start_time = time.time()
            self.cyrus_beck((x1, y1), (x2, y2))
            total_time += time.time() - start_time
            
        return total_time / iterations

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Алгоритм Кируса-Бека")
    
    clipper = CyrusBeckClipper()
    clock = pygame.time.Clock()
    
    # Тестовый отрезок
    line = ((-1, 1), (3, 3))  # Начальные координаты тестового отрезка
    show_info = True
    font = pygame.font.Font(None, 20)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    show_info = not show_info
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ - задаем новый отрезок
                    mouse_x = (event.pos[0] - clipper.offset[0]) / clipper.scale
                    mouse_y = (clipper.offset[1] - event.pos[1]) / clipper.scale
                    line = ((-1, 1), (mouse_x, mouse_y))
        
        screen.fill((0, 0, 0))
        
        # Рисуем восьмиугольник
        points = [(clipper.offset[0] + v[0] * clipper.scale,
                  clipper.offset[1] - v[1] * clipper.scale) for v in clipper.vertices]
        pygame.draw.polygon(screen, (50, 50, 50), points)
        pygame.draw.polygon(screen, (100, 100, 100), points, 1)
        
        # Отсекаем отрезок
        visible, clipped, results = clipper.cyrus_beck(line[0], line[1])
        
        # Рисуем исходный отрезок
        pygame.draw.line(screen, (100, 100, 100),
                        (clipper.offset[0] + line[0][0] * clipper.scale,
                         clipper.offset[1] - line[0][1] * clipper.scale),
                        (clipper.offset[0] + line[1][0] * clipper.scale,
                         clipper.offset[1] - line[1][1] * clipper.scale))
        
        # Рисуем отсеченный отрезок, если он видим
        if visible and clipped:
            pygame.draw.line(screen, (255, 255, 255),
                           (clipper.offset[0] + clipped[0][0] * clipper.scale,
                            clipper.offset[1] - clipped[0][1] * clipper.scale),
                           (clipper.offset[0] + clipped[1][0] * clipper.scale,
                            clipper.offset[1] - clipped[1][1] * clipper.scale), 2)
        
        if show_info:
            # Выводим таблицу результатов
            y_offset = 10
            headers = ["Ребро", "n", "f", "w·n", "D·n", "t"]
            
            # Заголовки таблицы
            x_offset = 10
            for header in headers:
                text = font.render(header, True, (255, 255, 255))
                screen.blit(text, (x_offset, y_offset))
                x_offset += 100
            
            y_offset += 20
            
            # Данные таблицы
            for i, result in enumerate(results):
                x_offset = 10
                row_data = [
                    f"{i+1}",
                    f"({result['n'][0]:.2f}, {result['n'][1]:.2f})",
                    f"({result['f'][0]}, {result['f'][1]})",
                    f"{result['w·n']:.2f}",
                    f"{result['D·n']:.2f}",
                    f"{result['t']:.2f}" if result['t'] is not None else "∞"
                ]
                
                for data in row_data:
                    text = font.render(data, True, (255, 255, 255))
                    screen.blit(text, (x_offset, y_offset))
                    x_offset += 100
                y_offset += 20
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 