"""
Проект 1: Платоновы тела (Куб, Тетраэдр, Октаэдр)

Реализация визуализации трех платоновых тел:
1. Куб (6 граней, 8 вершин, 12 ребер)
2. Тетраэдр (4 грани, 4 вершины, 6 ребер)
3. Октаэдр (8 граней, 6 вершин, 12 ребер)

Особенности:
- 3D визуализация с помощью OpenGL
- Каркасное отображение фигур
- Интерактивное управление
- Сохранение позиции при смене фигуры
- Плавная анимация вращения

Управление:
- 1,2,3 - выбор фигуры
- Стрелки - перемещение
- Q,W,E - поворот по осям
- +/- - масштабирование

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from utils.opengl_utils import OpenGLUtils
from utils.ui import UIManager

class PlatonicSolids:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF|OPENGL)
        pygame.display.set_caption("Платоновы тела: Куб, Тетраэдр, Октаэдр")
        
        # Инициализация OpenGL
        OpenGLUtils.setup_perspective(45, self.width/self.height, 0.1, 50.0)
        OpenGLUtils.setup_lighting()  # Добавляем освещение
        glTranslatef(0.0, 0.0, -10)
        
        # Инициализация UI и фигур
        self.solid = PlatonicSolid()
        self.ui = UIManager()
        
        # Добавляем параметры вращения
        self.rotation = [0, 0, 0]  # Углы поворота по X, Y, Z
        
        # Добавляем кнопки
        button_y = 10
        self.ui.add_button("Куб", self.select_cube, pos=(10, button_y))
        button_y += 40
        self.ui.add_button("Тетраэдр", self.select_tetrahedron, pos=(10, button_y))
        button_y += 40
        self.ui.add_button("Октаэдр", self.select_octahedron, pos=(10, button_y))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # ЛКМ
                        self.ui.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard(event)
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()

    def draw(self):
        # Очищаем буфер
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # Рисуем 3D объекты
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Рисуем сетку
        OpenGLUtils.draw_grid(10, 1)
        
        # Рисуем текущую фигуру
        self.solid.draw()
            
        glPopMatrix()
        
        # Переключаемся в режим 2D для отрисовки UI
        OpenGLUtils.begin_2d()
        self.ui.draw(self.screen)
        OpenGLUtils.end_2d()
        
        pygame.display.flip()

    def handle_keyboard(self, event):
        if event.key == pygame.K_1:
            self.select_cube()
        elif event.key == pygame.K_2:
            self.select_tetrahedron()
        elif event.key == pygame.K_3:
            self.select_octahedron()
        elif event.key == pygame.K_LEFT:
            self.solid.set_center(self.solid.center[0] - 0.1, self.solid.center[1], self.solid.center[2])
        elif event.key == pygame.K_RIGHT:
            self.solid.set_center(self.solid.center[0] + 0.1, self.solid.center[1], self.solid.center[2])
        elif event.key == pygame.K_UP:
            self.solid.set_center(self.solid.center[0], self.solid.center[1] + 0.1, self.solid.center[2])
        elif event.key == pygame.K_DOWN:
            self.solid.set_center(self.solid.center[0], self.solid.center[1] - 0.1, self.solid.center[2])
        elif event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:
            self.solid.set_edge_length(self.solid.edge_length + 0.1)
        elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
            self.solid.set_edge_length(self.solid.edge_length - 0.1)
        elif event.key == pygame.K_q:
            self.rotation[0] += 5
        elif event.key == pygame.K_w:
            self.rotation[1] += 5
        elif event.key == pygame.K_e:
            self.rotation[2] += 5

    def select_cube(self):
        self.solid.current_solid = "cube"

    def select_tetrahedron(self):
        self.solid.current_solid = "tetrahedron"

    def select_octahedron(self):
        self.solid.current_solid = "octahedron"

class PlatonicSolid:
    def __init__(self):
        self.center = [0, 0, 0]
        self.edge_length = 2.0
        self.rotation = [0, 0, 0]
        self.current_solid = "cube"  # По умолчанию куб

    def set_center(self, x, y, z):
        self.center = [x, y, z]

    def set_edge_length(self, length):
        self.edge_length = length

    def rotate(self, x, y, z):
        self.rotation[0] += x
        self.rotation[1] += y
        self.rotation[2] += z

    def draw_cube(self):
        vertices = [
            [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1],
            [1, -1, 1], [1, 1, 1], [-1, 1, 1], [-1, -1, 1]
        ]
        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                x = vertices[vertex][0] * self.edge_length/2 + self.center[0]
                y = vertices[vertex][1] * self.edge_length/2 + self.center[1]
                z = vertices[vertex][2] * self.edge_length/2 + self.center[2]
                glVertex3f(x, y, z)
        glEnd()

    def draw_tetrahedron(self):
        vertices = [
            [1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]
        ]
        edges = [
            (0,1), (1,2), (2,0),
            (0,3), (1,3), (2,3)
        ]
        
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                x = vertices[vertex][0] * self.edge_length/2 + self.center[0]
                y = vertices[vertex][1] * self.edge_length/2 + self.center[1]
                z = vertices[vertex][2] * self.edge_length/2 + self.center[2]
                glVertex3f(x, y, z)
        glEnd()

    def draw_octahedron(self):
        vertices = [
            [0, 1, 0], [0, -1, 0], [1, 0, 0],
            [-1, 0, 0], [0, 0, 1], [0, 0, -1]
        ]
        edges = [
            (0,2), (0,3), (0,4), (0,5),
            (1,2), (1,3), (1,4), (1,5),
            (2,4), (4,3), (3,5), (5,2)
        ]
        
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                x = vertices[vertex][0] * self.edge_length/2 + self.center[0]
                y = vertices[vertex][1] * self.edge_length/2 + self.center[1]
                z = vertices[vertex][2] * self.edge_length/2 + self.center[2]
                glVertex3f(x, y, z)
        glEnd()

    def draw(self):
        glPushMatrix()
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Рисуем вспомогательную сетку
        OpenGLUtils.draw_grid(10, 1)  # Сетка 10x10 с шагом 1
        
        if self.current_solid == "cube":
            self.draw_cube()
        elif self.current_solid == "tetrahedron":
            self.draw_tetrahedron()
        elif self.current_solid == "octahedron":
            self.draw_octahedron()
            
        glPopMatrix()

def main():
    app = PlatonicSolids()
    app.run()

if __name__ == "__main__":
    main() 