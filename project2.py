"""
Проект 2: Платоновы тела (Икосаэдр и Додекаэдр)

Реализация визуализации двух платоновых тел:
1. Икосаэдр (20 граней, 12 вершин, 30 ребер)
2. Додекаэдр (12 граней, 20 вершин, 30 ребер)

Особенности:
- 3D визуализация с помощью OpenGL
- Каркасное отображение фигур
- Использование золотого сечения
- Правильная геометрия граней
- Оптимизированные вычисления

Управление:
- 1,2 - выбор фигуры
- Стрелки - перемещение
- Q,W,E - поворот по осям
- +/- - масштабирование

Математические константы:
- Золотое сечение φ = (1 + √5) / 2 ≈ 1.618033989
- Двойственность фигур (вершины одной - центры граней другой)

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils.opengl_utils import OpenGLUtils
from utils.ui import UIManager

class PlatonicSolids2:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF|OPENGL)
        pygame.display.set_caption("Платоновы тела: Икосаэдр и Додекаэдр")
        
        self.ui = UIManager()
        OpenGLUtils.setup_perspective(45, self.width/self.height, 0.1, 50.0)
        OpenGLUtils.setup_lighting()
        glTranslatef(0.0, 0.0, -10)
        
        self.center = [0, 0, 0]
        self.edge_length = 2.0
        self.rotation = [0, 0, 0]
        self.current_solid = "icosahedron"  # По умолчанию икосаэдр

    def set_center(self, x, y, z):
        self.center = [x, y, z]

    def set_edge_length(self, length):
        self.edge_length = length

    def rotate(self, x, y, z):
        self.rotation[0] += x
        self.rotation[1] += y
        self.rotation[2] += z

    def draw_icosahedron(self):
        phi = (1 + math.sqrt(5)) / 2
        vertices = [
            [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
            [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
            [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
        ]
        
        edges = [
            (0,1), (0,4), (0,5), (0,8), (0,9),
            (1,6), (1,7), (1,8), (1,9),
            (2,3), (2,4), (2,5), (2,10), (2,11),
            (3,6), (3,7), (3,10), (3,11),
            (4,8), (4,10), (5,9), (5,11),
            (6,8), (6,10), (7,9), (7,11),
            (8,10), (9,11)
        ]
        
        scale = self.edge_length / 4
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                x = vertices[vertex][0] * scale + self.center[0]
                y = vertices[vertex][1] * scale + self.center[1]
                z = vertices[vertex][2] * scale + self.center[2]
                glVertex3f(x, y, z)
        glEnd()

    def draw_dodecahedron(self):
        phi = (1 + math.sqrt(5)) / 2
        inv_phi = 1/phi
        
        vertices = [
            [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
            [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
            [0, inv_phi, phi], [0, inv_phi, -phi], [0, -inv_phi, phi], [0, -inv_phi, -phi],
            [inv_phi, phi, 0], [inv_phi, -phi, 0], [-inv_phi, phi, 0], [-inv_phi, -phi, 0],
            [phi, 0, inv_phi], [phi, 0, -inv_phi], [-phi, 0, inv_phi], [-phi, 0, -inv_phi]
        ]
        
        edges = [
            (0,16), (0,8), (0,12), (1,16), (1,9), (1,13),
            (2,17), (2,10), (2,12), (3,17), (3,11), (3,13),
            (4,18), (4,8), (4,14), (5,18), (5,9), (5,15),
            (6,19), (6,10), (6,14), (7,19), (7,11), (7,15),
            (8,9), (10,11), (12,14), (13,15), (16,17), (18,19)
        ]
        
        scale = self.edge_length / 3
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                x = vertices[vertex][0] * scale + self.center[0]
                y = vertices[vertex][1] * scale + self.center[1]
                z = vertices[vertex][2] * scale + self.center[2]
                glVertex3f(x, y, z)
        glEnd()

    def draw(self):
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        OpenGLUtils.draw_grid(10, 1)  # Добавляем сетку для лучшей ориентации
        
        if self.current_solid == "icosahedron":
            self.draw_icosahedron()
        elif self.current_solid == "dodecahedron":
            self.draw_dodecahedron()
            
        glPopMatrix()

def main():
    solid = PlatonicSolids2()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    solid.current_solid = "icosahedron"
                elif event.key == pygame.K_2:
                    solid.current_solid = "dodecahedron"
                elif event.key == pygame.K_LEFT:
                    solid.set_center(solid.center[0] - 0.1, solid.center[1], solid.center[2])
                elif event.key == pygame.K_RIGHT:
                    solid.set_center(solid.center[0] + 0.1, solid.center[1], solid.center[2])
                elif event.key == pygame.K_UP:
                    solid.set_center(solid.center[0], solid.center[1] + 0.1, solid.center[2])
                elif event.key == pygame.K_DOWN:
                    solid.set_center(solid.center[0], solid.center[1] - 0.1, solid.center[2])
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    solid.set_edge_length(solid.edge_length + 0.1)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    solid.set_edge_length(solid.edge_length - 0.1)
                elif event.key == pygame.K_q:
                    solid.rotate(5, 0, 0)
                elif event.key == pygame.K_w:
                    solid.rotate(0, 5, 0)
                elif event.key == pygame.K_e:
                    solid.rotate(0, 0, 5)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        solid.draw()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main() 