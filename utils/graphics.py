"""
Общие графические утилиты для всех проектов
"""
import pygame
import numpy as np

class GraphicsBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = np.zeros((height, width))
        self.scale = 1
        self.offset = [0, 0]
        self.surface = pygame.Surface((width, height))

    def clear(self):
        self.buffer.fill(0)
        self.surface.fill((0, 0, 0))

    def set_pixel(self, x, y, value=1):
        screen_x = int(x + self.offset[0])
        screen_y = int(y + self.offset[1])
        if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
            self.buffer[screen_y, screen_x] = value
            color = (int(value * 255), int(value * 255), int(value * 255))
            self.surface.set_at((screen_x, screen_y), color)

    def get_pixel(self, x, y):
        screen_x = int(x + self.offset[0])
        screen_y = int(y + self.offset[1])
        if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
            return self.buffer[screen_y, screen_x]
        return 0

    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                value = self.buffer[y, x]
                color = (int(value * 255), int(value * 255), int(value * 255))
                self.surface.set_at((x, y), color)