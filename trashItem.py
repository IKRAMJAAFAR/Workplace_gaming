import pygame
import random

class TrashItem:
    def __init__(self, image_path, screen_width, screen_height):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(
            topleft=(random.randint(50, screen_width - 50), random.randint(50, screen_height - 50))
        )
        self.dragging = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.mouse_offset = pygame.Vector2(self.rect.topleft) - pygame.Vector2(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.topleft = pygame.Vector2(event.pos) + self.mouse_offset
