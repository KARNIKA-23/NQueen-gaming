import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color=(50, 50, 50), text_color=(255, 255, 255), hover_color=(70, 70, 70)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Draw shadow/3d effect
        pygame.draw.rect(screen, (30, 30, 30), self.rect.move(2, 2), border_radius=5)
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                return True
        return False

class Label:
    def __init__(self, x, y, text, font, color=(255, 255, 255), shadow_color=(0,0,0)):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.shadow_color = shadow_color

    def draw(self, screen):
        if self.shadow_color:
            # Draw outline/glow for better visibility
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                shadow_surf = self.font.render(self.text, True, self.shadow_color)
                screen.blit(shadow_surf, (self.x + dx, self.y + dy))
            
        text_surf = self.font.render(self.text, True, self.color)
        screen.blit(text_surf, (self.x, self.y))

    def set_text(self, text):
        self.text = text
