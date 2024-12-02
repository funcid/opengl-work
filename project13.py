"""
Проект 13: Устранение ступенчатого эффекта (антиалиасинг)

Реализация методов устранения ступенчатости:
1. Равномерная фильтрация
2. Взвешенная фильтрация
3. Рекурсивная фильтрация
4. Свертка с прямоугольным ядром

Особенности:
- Размер псевдорастра: 64x64
- Размер подпикселя: 4x4
- Угловой коэффициент линии: 3/8
- Визуализация всех методов
- Увеличенное отображение фрагментов
- Сравнение результатов

Методы:
- Эвристический подход к площадной интерпретации
- Математическое обоснование с помощью свертки
- Рекурсивная и нерекурсивная фильтрация
- Равномерная и взвешенная фильтрация

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import numpy as np
from scipy.signal import convolve2d

class AntialiasExperiment:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Устранение ступенчатого эффекта")
        
        # Размер псевдорастра
        self.raster_size = 64
        self.subpixel_size = 4  # Размер подпикселя (2x2 или 4x4)
        
        # Угловой коэффициент для линии (3/8)
        self.slope = 3/8
        
        # Создаем базовое изображение линии
        self.base_image = self.create_line_image()
        
        # Применяем разные методы антиалиасинга
        self.uniform_filtered = self.apply_uniform_filter()
        self.weighted_filtered = self.apply_weighted_filter()
        self.recursive_filtered = self.apply_recursive_filter()
        self.convolution_filtered = self.apply_convolution_filter()
        
        self.font = pygame.font.Font(None, 24)

    def create_line_image(self):
        """Создает изображение линии на псевдорастре"""
        image = np.zeros((self.raster_size * self.subpixel_size,
                         self.raster_size * self.subpixel_size))
        
        for x in range(image.shape[1]):
            y = int(x * self.slope)
            if 0 <= y < image.shape[0]:
                image[y, x] = 1
        
        return image

    def apply_uniform_filter(self):
        """Применяет равномерную фильтрацию"""
        result = np.zeros((self.raster_size, self.raster_size))
        sub_size = self.subpixel_size
        
        for y in range(self.raster_size):
            for x in range(self.raster_size):
                # Считаем среднее значение в области подпикселей
                subpixels = self.base_image[y*sub_size:(y+1)*sub_size,
                                          x*sub_size:(x+1)*sub_size]
                result[y, x] = np.mean(subpixels)
        
        return result

    def apply_weighted_filter(self):
        """Применяет взвешенную фильтрацию"""
        result = np.zeros((self.raster_size, self.raster_size))
        sub_size = self.subpixel_size
        
        # Создаем матрицу весов
        weights = np.array([
            [1, 2, 2, 1],
            [2, 4, 4, 2],
            [2, 4, 4, 2],
            [1, 2, 2, 1]
        ]) / 36.0
        
        for y in range(self.raster_size):
            for x in range(self.raster_size):
                subpixels = self.base_image[y*sub_size:(y+1)*sub_size,
                                          x*sub_size:(x+1)*sub_size]
                result[y, x] = np.sum(subpixels * weights)
        
        return result

    def apply_recursive_filter(self):
        """Применяет рекурсивную фильтрацию"""
        result = self.apply_uniform_filter()  # Начальное приближение
        
        # Рекурсивный фильтр
        alpha = 0.5
        filtered = np.zeros_like(result)
        
        # Прямой проход
        filtered[0, 0] = result[0, 0]
        for y in range(result.shape[0]):
            for x in range(result.shape[1]):
                if x == 0 and y == 0:
                    continue
                elif x == 0:
                    filtered[y, x] = alpha * filtered[y-1, x] + (1-alpha) * result[y, x]
                else:
                    filtered[y, x] = alpha * (filtered[y, x-1] + filtered[y-1, x])/2 + (1-alpha) * result[y, x]
        
        return filtered

    def apply_convolution_filter(self):
        """Применяет свертку с прямоугольным ядром"""
        kernel = np.ones((4, 4)) / 16
        return convolve2d(self.apply_uniform_filter(), kernel, mode='same')

    def draw_result(self, image, x, y, cell_size, label):
        """Отрисовывает результат с подписью"""
        height, width = image.shape
        surface = pygame.Surface((width * cell_size, height * cell_size))
        surface.fill((30, 30, 30))
        
        for py in range(height):
            for px in range(width):
                color = int(image[py, px] * 255)
                pygame.draw.rect(surface, (color, color, color),
                               (px * cell_size, py * cell_size, cell_size - 1, cell_size - 1))
        
        self.screen.blit(surface, (x, y))
        
        # Отрисовка подписи
        text = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(text, (x, y - 25))

    def run(self):
        """Основной цикл программы"""
        clock = pygame.time.Clock()
        running = True
        cell_size = 8
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill((0, 0, 0))
            
            # Отрисовка результатов разных методов
            self.draw_result(self.apply_uniform_filter(), 50, 50, cell_size,
                           "Равномерная фильтрация")
            
            self.draw_result(self.weighted_filtered, 50, 250, cell_size,
                           "Взвешенная фильтрация")
            
            self.draw_result(self.recursive_filtered, 50, 450, cell_size,
                           "Рекурсивная фильтрация")
            
            self.draw_result(self.convolution_filtered, 50, 650, cell_size,
                           "Свертка с прямоугольным ядром")
            
            # Отображение увеличенного фрагмента
            zoomed_size = 16
            zoomed_x = 600
            for i, (result, label) in enumerate([
                (self.apply_uniform_filter(), "Равномерная фильтрация"),
                (self.weighted_filtered, "Взвешенная фильтрация"),
                (self.recursive_filtered, "Рекурсивная фильтрация"),
                (self.convolution_filtered, "Свертка с ядром")
            ]):
                # Берем центральный фрагмент 8x8
                center = result.shape[0] // 2
                fragment = result[center-4:center+4, center-4:center+4]
                self.draw_result(fragment, zoomed_x, 50 + i * 200, zoomed_size,
                               f"{label} (увеличено)")
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    experiment = AntialiasExperiment()
    experiment.run() 