"""
Утилиты для работы с OpenGL
"""
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class OpenGLUtils:
    @staticmethod
    def setup_perspective(fov, aspect, near, far):
        """Настройка перспективной проекции"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fov, aspect, near, far)
        glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def setup_lighting():
        """Настройка освещения"""
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    @staticmethod
    def draw_grid(size, step):
        """Отрисовка вспомогательной сетки"""
        glBegin(GL_LINES)
        glColor3f(0.2, 0.2, 0.2)
        
        # Преобразуем size и step в целые числа для range
        size_int = int(size)
        step_int = int(step)
        if step_int < 1:
            step_int = 1
        
        # Горизонтальные линии
        for i in range(-size_int, size_int + 1, step_int):
            glVertex3f(float(i), 0, float(-size_int))
            glVertex3f(float(i), 0, float(size_int))
        
        # Вертикальные линии
        for i in range(-size_int, size_int + 1, step_int):
            glVertex3f(float(-size_int), 0, float(i))
            glVertex3f(float(size_int), 0, float(i))
        
        glEnd()

    @staticmethod
    def begin_2d():
        """Переключение в режим 2D"""
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 800, 600, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

    @staticmethod
    def end_2d():
        """Возврат в режим 3D"""
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()