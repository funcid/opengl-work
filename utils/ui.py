"""
Общие компоненты пользовательского интерфейса
"""
import pygame

class UIManager:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.buttons = []
        
    def draw_text(self, screen, text, pos, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        screen.blit(text_surface, pos)
        
    def draw_info_panel(self, screen, info_text, start_pos=(20, 20), line_height=25):
        y = start_pos[1]
        for text in info_text:
            self.draw_text(screen, text, (start_pos[0], y))
            y += line_height
            
    def add_button(self, text, callback, pos=(0, 0), size=(100, 30), color=(100, 100, 100)):
        self.buttons.append({
            'text': text,
            'callback': callback,
            'rect': pygame.Rect(pos, size),
            'color': color
        })
        
    def draw_buttons(self, screen):
        for button in self.buttons:
            pygame.draw.rect(screen, button['color'], button['rect'])
            text_surface = self.font.render(button['text'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
            
    def handle_click(self, pos):
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                button['callback']()
                return True
        return False

    def draw(self, screen):
        """Отрисовка всех элементов UI"""
        self.draw_buttons(screen)

    def draw_text_list(self, screen, text_list, x, y, line_height=25):
        """Отрисовка списка текста"""
        current_y = y
        for text in text_list:
            self.draw_text(screen, text, (x, current_y))
            current_y += line_height