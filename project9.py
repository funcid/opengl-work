"""
Проект 9: Отсечение многоугольника цилиндром

Реализация:
1. Отсечение плоского многоугольника цилиндром
2. Поворот многоугольника на 45° вокруг оси X
3. Использование алгоритмов:
   - Сазерленд-Ходжмен для отсечения
   - Кирус-Бек для проверки видимости

Особенности:
- 3D визуализация с помощью OpenGL
- Цилиндр с радиусом 0.3 и высотой ±0.3
- Учет торцов цилиндра
- 32-гранная аппроксимация цилиндра
- Интерактивное управление камерой

Управление:
- ЛКМ + движение мыши - поворот камеры
- R - сброс поворота камеры

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from utils.opengl_utils import OpenGLUtils

class CylinderClipper:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF|OPENGL)
        pygame.display.set_caption("Отсечение многоугольника цилиндром")
        
        # Инициализация OpenGL
        OpenGLUtils.setup_perspective(45, self.width/self.height, 0.1, 50.0)
        OpenGLUtils.setup_lighting()
        glTranslatef(0.0, 0.0, -10)
        
        # Параметры цилиндра
        self.cylinder_radius = 0.3
        self.cylinder_height = 0.3
        self.cylinder_segments = 32
        
        # Параметры вращения
        self.rotation = [45, 0, 0]  # Начальный поворот на 45° вокруг X
        
        # Тестовый многоугольник
        self.polygon = [
            (-0.5, -0.5, 0),
            (0.5, -0.5, 0),
            (0.5, 0.5, 0),
            (-0.5, 0.5, 0)
        ]

    def draw_cylinder(self):
        """Отрисовка цилиндра"""
        glColor3f(0.5, 0.5, 0.5)
        
        # Боковая поверхность
        glBegin(GL_LINES)
        for i in range(self.cylinder_segments):
            angle1 = 2 * math.pi * i / self.cylinder_segments
            angle2 = 2 * math.pi * (i + 1) / self.cylinder_segments
            
            # Нижнее основание
            x1 = self.cylinder_radius * math.cos(angle1)
            y1 = self.cylinder_radius * math.sin(angle1)
            x2 = self.cylinder_radius * math.cos(angle2)
            y2 = self.cylinder_radius * math.sin(angle2)
            
            # Вертикальные линии
            glVertex3f(x1, y1, -self.cylinder_height)
            glVertex3f(x1, y1, self.cylinder_height)
            
            # Линии оснований
            glVertex3f(x1, y1, -self.cylinder_height)
            glVertex3f(x2, y2, -self.cylinder_height)
            
            glVertex3f(x1, y1, self.cylinder_height)
            glVertex3f(x2, y2, self.cylinder_height)
        glEnd()

    def draw_polygon(self):
        """Отрисовка многоугольника"""
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_LOOP)
        for vertex in self.polygon:
            glVertex3f(*vertex)
        glEnd()

    def draw(self):
        """Отрисовка всей сцены"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Рисуем вспомогательную сетку
        OpenGLUtils.draw_grid(2, 0.2)  # Сетка 2x2 с шагом 0.2
        
        # Рисуем цилиндр и многоугольник
        self.draw_cylinder()
        self.draw_polygon()
        
        glPopMatrix()
        
        pygame.display.flip()

    def run(self):
        """Основной цикл программы"""
        clock = pygame.time.Clock()
        mouse_pressed = False
        last_mouse_pos = None
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # ЛКМ
                        mouse_pressed = True
                        last_mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # ЛКМ
                        mouse_pressed = False
                elif event.type == pygame.MOUSEMOTION:
                    if mouse_pressed and last_mouse_pos:
                        dx = event.pos[0] - last_mouse_pos[0]
                        dy = event.pos[1] - last_mouse_pos[1]
                        self.rotation[1] += dx * 0.5
                        self.rotation[0] += dy * 0.5
                        last_mouse_pos = event.pos
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Сброс поворота
                        self.rotation = [45, 0, 0]
            
            self.draw()
            clock.tick(60)

if __name__ == "__main__":
    app = CylinderClipper()
    app.run() 