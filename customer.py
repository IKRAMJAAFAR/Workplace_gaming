import pygame

class Customer:
    def __init__(self, image_path, position, waiting_time):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.waiting_time = waiting_time  # Maximum waiting time in milliseconds
        self.start_time = pygame.time.get_ticks()
        self.left = False  # Whether the customer left due to timeout

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time >= self.waiting_time:
            self.left = True  # Customer leaves the queue
        return elapsed_time

    def draw_timer(self, screen, font):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        time_left = max(0, self.waiting_time - elapsed_time)
        timer_text = font.render(f"{time_left // 1000}s", True, (255, 0, 0))
        screen.blit(timer_text, (self.rect.centerx - 10, self.rect.bottom + 5))
