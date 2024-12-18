import pygame

def create_bins():
    # Define bin positions and sizes
    return [
        pygame.Rect(100, 500, 100, 100),  # Example bin 1
        pygame.Rect(600, 500, 100, 100),  # Example bin 2
    ]

def draw_bins(screen, bins):
    for bin_rect in bins:
        pygame.draw.rect(screen, (0, 255, 0), bin_rect)  # Green bins

def check_collision(item, bins):
    for i, bin_rect in enumerate(bins):
        if item.rect.colliderect(bin_rect):
            return i  # Return the index of the bin
    return -1  # No collision
