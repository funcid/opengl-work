"""
Проект 12: Дизеринг изображений

Реализация алгоритмов дизеринга:
1. Матричный дизеринг 2x2
2. Алгоритм Флойда-Стейнберга
3. Упорядоченное возмущение

Особенности:
- Поддержка разных размеров растра (32x32, 64x64, 128x128)
- Визуализация градиента серого цвета
- Сравнение результатов разных алгоритмов
- Анализ качества дизеринга
- Измерение производительности

Управление:
- 1 - растр 32x32
- 2 - растр 64x64
- 3 - растр 128x128
- Автоматическое применение:
  * Матричного дизеринга для всех размеров
  * Флойда-Стейнберга для 128x128
  * Упорядоченного возмущения для 128x128

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import numpy as np

class DitheringExperiment:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Дизеринг и сравнение алгоритмов")
        
        # Размеры растров
        self.sizes = [32, 64, 128]
        self.current_size = 128
        
        # Матрица дизеринга 2x2
        self.dither_matrix_2x2 = np.array([
            [0, 2],
            [3, 1]
        ]) / 4.0
        
        # Результаты для разных размеров
        self.results = {size: self.create_gradient(size) for size in self.sizes}
        
        # Применяем алгоритм Флойда-Стейнберга к растру 128x128
        self.floyd_result = self.apply_floyd_steinberg(self.create_gradient(128))
        
        # Добавляем упорядоченное возмущение
        self.ordered_result = self.apply_ordered_dithering(self.create_gradient(128))
        
        self.font = pygame.font.Font(None, 24)

    def create_gradient(self, size):
        """Создает градиент серого цвета слева направо"""
        gradient = np.zeros((size, size))
        for x in range(size):
            gradient[:, x] = x / size
        return gradient

    def apply_dithering_2x2(self, image):
        """Применяет дизеринг с матрицей 2x2"""
        height, width = image.shape
        result = np.zeros_like(image)
        
        for y in range(0, height, 2):
            for x in range(0, width, 2):
                for dy in range(2):
                    for dx in range(2):
                        if y + dy < height and x + dx < width:
                            threshold = self.dither_matrix_2x2[dy, dx]
                            result[y + dy, x + dx] = 1 if image[y + dy, x + dx] > threshold else 0
        
        return result

    def apply_floyd_steinberg(self, image):
        """Применяет алгоритм Флойда-Стейнберга"""
        height, width = image.shape
        result = image.copy()
        
        for y in range(height-1):
            for x in range(1, width-1):
                old_pixel = result[y, x]
                new_pixel = 1 if old_pixel > 0.5 else 0
                result[y, x] = new_pixel
                error = old_pixel - new_pixel
                
                result[y, x+1] += error * 7/16
                result[y+1, x-1] += error * 3/16
                result[y+1, x] += error * 5/16
                result[y+1, x+1] += error * 1/16
        
        return result

    def apply_ordered_dithering(self, image):
        """Применяет упорядоченное возмущение"""
        height, width = image.shape
        result = image.copy()
        
        # Создаем матрицу возмущения
        disturbance = np.random.uniform(-0.1, 0.1, (height, width))
        result = np.clip(result + disturbance, 0, 1)
        
        return result

    def draw_result(self, result, x_offset, y_offset, cell_size, label):
        """Отрисовка результата дизеринга"""
        # Рисуем заголовок
        text = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(text, (x_offset, y_offset - 30))
        
        # Рисуем результат
        for y in range(result.shape[0]):
            for x in range(result.shape[1]):
                rect = pygame.Rect(
                    x_offset + x * cell_size,
                    y_offset + y * cell_size,
                    cell_size - 1,
                    cell_size - 1
                )
                # Преобразуем значение пикселя в целое число для цвета
                color_value = min(255, max(0, int(result[y, x] * 255)))
                pygame.draw.rect(self.screen, (color_value, color_value, color_value), rect)

    def run(self):
        """Основной цикл программы"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.current_size = 32
                    elif event.key == pygame.K_2:
                        self.current_size = 64
                    elif event.key == pygame.K_3:
                        self.current_size = 128
            
            self.screen.fill((0, 0, 0))
            
            # Отрисовка результатов для разных размеров растра
            y_offset = 50
            for size in self.sizes:
                result = self.apply_dithering_2x2(self.results[size])
                cell_size = max(1, 400 // size)
                self.draw_result(result, 50, y_offset, cell_size,
                               f"Размер растра: {size}x{size}")
                y_offset += (size * cell_size) + 50
            
            # Отрисовка результатов разных алгоритмов для 128x128
            cell_size = 2
            x_offset = 500
            
            self.draw_result(self.floyd_result, x_offset, 50, cell_size,
                           "Алгоритм Флойда-Стейнберга (128x128)")
            
            self.draw_result(self.ordered_result, x_offset, 350, cell_size,
                           "Упорядоченное возмущение (128x128)")
            
            # Отображение информации
            info_text = [
                "Управление:",
                "1 - растр 32x32",
                "2 - растр 64x64",
                "3 - растр 128x128"
            ]
            
            y_offset = 650
            for text in info_text:
                text_surface = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (50, y_offset))
                y_offset += 25
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    experiment = DitheringExperiment()
    experiment.run() 