"""
Проект 11: Исследование цветовых систем

Реализация:
1. Аддитивная (RGB) цветовая система
2. Субтрактивная (CMY) цветовая система
3. Эффекты смешивания цветов:
   - Сложение
   - Вычитание
   - Замена
   - Прозрачность

Особенности:
- Интерактивное управление цветами
- Визуализация эффекта одновременного контраста
- Линейная модель прозрачности
- Наглядная демонстрация результатов
- Сравнение RGB и CMY систем

Управление:
- R,G,B - базовые цвета RGB
- C,M,Y - базовые цвета CMY
- M - переключение режима (сложение/вычитание/замена)
- ↑↓ - изменение прозрачности
- Пробел - применить текущий цвет

Автор: Царюк Артём Владимирович
Дата: 02.12.2024
"""

import pygame
import numpy as np

class ColorExperiment:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Исследование цветовых систем")
        
        # Размеры квадратов
        self.square_sizes = [200, 100, 50]  # Большой, средний и маленький квадраты
        
        # Текущие цвета
        self.colors = {
            'current': (255, 0, 0),  # Текущий цвет
            'previous': (0, 0, 255),  # Предыдущий цвет
            'result': (255, 0, 255)   # Результирующий цвет
        }
        
        # Режимы работы
        self.modes = ['add', 'subtract', 'replace']  # Сложение, вычитание, замена
        self.current_mode = 'add'
        
        # Прозрачность
        self.alpha = 0.5
        
        # Шрифт для текста
        self.font = pygame.font.Font(None, 24)

    def rgb_to_cmy(self, rgb):
        """Преобразование из RGB в CMY"""
        return tuple(255 - c for c in rgb)

    def add_colors(self, color1, color2):
        """Сложение цветов в RGB"""
        return tuple(min(255, c1 + c2) for c1, c2 in zip(color1, color2))

    def subtract_colors(self, color1, color2):
        """Вычитание цветов в CMY"""
        cmy1 = self.rgb_to_cmy(color1)
        cmy2 = self.rgb_to_cmy(color2)
        result_cmy = tuple(max(0, c1 - c2) for c1, c2 in zip(cmy1, cmy2))
        return tuple(255 - c for c in result_cmy)

    def blend_colors(self, color1, color2, alpha):
        """Смешивание цветов с прозрачностью"""
        return tuple(int(c1 * (1 - alpha) + c2 * alpha) for c1, c2 in zip(color1, color2))

    def draw_square(self, x, y, size, color, alpha=1.0):
        """Отрисовка квадрата с возможной прозрачностью"""
        if alpha < 1.0:
            # Создаем поверхность с прозрачностью
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            alpha_color = (*color, int(255 * alpha))
            surface.fill(alpha_color)
            self.screen.blit(surface, (x, y))
        else:
            pygame.draw.rect(self.screen, color, (x, y, size, size))

    def draw_color_info(self, x, y, color, label):
        """Отображение информации о цвете"""
        text = f"{label}: RGB{color}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def handle_input(self):
        """Обработка пользовательского ввода"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Переключение режимов
                if event.key == pygame.K_m:
                    idx = (self.modes.index(self.current_mode) + 1) % len(self.modes)
                    self.current_mode = self.modes[idx]
                
                # Изменение прозрачности
                elif event.key == pygame.K_UP:
                    self.alpha = min(1.0, self.alpha + 0.1)
                elif event.key == pygame.K_DOWN:
                    self.alpha = max(0.0, self.alpha - 0.1)
                
                # Изменение текущего цвета
                elif event.key == pygame.K_r:
                    self.colors['current'] = (255, 0, 0)
                elif event.key == pygame.K_g:
                    self.colors['current'] = (0, 255, 0)
                elif event.key == pygame.K_b:
                    self.colors['current'] = (0, 0, 255)
                elif event.key == pygame.K_y:
                    self.colors['current'] = (255, 255, 0)
                elif event.key == pygame.K_c:
                    self.colors['current'] = (0, 255, 255)
                elif event.key == pygame.K_p:
                    self.colors['current'] = (255, 0, 255)
                
                # Применение текущего цвета
                elif event.key == pygame.K_SPACE:
                    self.colors['previous'] = self.colors['result']
                    if self.current_mode == 'add':
                        self.colors['result'] = self.add_colors(self.colors['previous'], self.colors['current'])
                    elif self.current_mode == 'subtract':
                        self.colors['result'] = self.subtract_colors(self.colors['previous'], self.colors['current'])
                    else:  # replace
                        self.colors['result'] = self.colors['current']
        
        return True

    def draw(self):
        """Отрисовка всех элементов"""
        self.screen.fill((30, 30, 30))
        
        # Отрисовка основных квадратов
        center_x = self.width // 2 - self.square_sizes[0] // 2
        center_y = self.height // 2 - self.square_sizes[0] // 2
        
        # Большой квадрат (результат)
        self.draw_square(center_x, center_y, self.square_sizes[0], self.colors['result'])
        
        # Средний квадрат (предыдущий цвет)
        self.draw_square(50, center_y, self.square_sizes[1], self.colors['previous'])
        
        # Маленький квадрат (текущий цвет)
        small_x = center_x + self.square_sizes[0] - self.square_sizes[2] - 50
        small_y = center_y + self.square_sizes[0] - self.square_sizes[2] - 50
        self.draw_square(small_x, small_y, self.square_sizes[2], self.colors['current'], self.alpha)
        
        # Отображение информации
        info_y = 20
        self.draw_color_info(20, info_y, self.colors['current'], "Текущий")
        self.draw_color_info(20, info_y + 30, self.colors['previous'], "Предыдущий")
        self.draw_color_info(20, info_y + 60, self.colors['result'], "Результат")
        
        # Режим работы и прозрачность
        mode_text = f"Режим: {self.current_mode}"
        alpha_text = f"Прозрачность: {self.alpha:.1f}"
        controls_text = "R,G,B,Y,C,P - цвета, M - режим, ↑↓ - прозрачность, Пробел - применить"
        
        mode_surface = self.font.render(mode_text, True, (255, 255, 255))
        alpha_surface = self.font.render(alpha_text, True, (255, 255, 255))
        controls_surface = self.font.render(controls_text, True, (255, 255, 255))
        
        self.screen.blit(mode_surface, (20, self.height - 80))
        self.screen.blit(alpha_surface, (20, self.height - 50))
        self.screen.blit(controls_surface, (20, self.height - 20))
        
        pygame.display.flip()

    def run(self):
        """Основной цикл программы"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_input()
            self.draw()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    experiment = ColorExperiment()
    experiment.run() 