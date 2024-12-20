import random
import pygame
from objects import Trash, Bin

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trash Sorting Game")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (173, 216, 230)  # Light Blue
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font_text = pygame.font.Font(None, 36)

# Fixed Bin Coordinates
BIN_COORDINATES = [
    (300, 400),  # Bin 1
    (400, 400),  # Bin 2
    (300, 500),  # Bin 3
    (400, 500),  # Bin 4
]

# Randomized Trash Placement within Screen Bounds
def generate_random_coordinates():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 150)  # Keep trash away from bottom UI area
    return x, y

# Initialize Bins
bins = [
    Bin("Plastic"),
    Bin("Aluminium"),
    Bin("Paper"),
    Bin("Waste"),
]

# Place bins at fixed coordinates
for i, bin_obj in enumerate(bins):
    bin_obj.x, bin_obj.y = BIN_COORDINATES[i]  # Add x, y attributes to Bin objects

# Initialize Trash
trash_categories = ["Plastic", "Aluminium", "Paper", "Waste"]
trash_objects = [
    Trash(category, wait_time=random.randint(3, 6)) for category in trash_categories
]

# Assign random coordinates to trash objects
for trash in trash_objects:
    trash.x, trash.y = generate_random_coordinates()  # Add x, y attributes to Trash objects

# Gameplay Function
def gameplay(player_id, original_price):
    score = 0
    timer = 60  # 60 seconds timer
    running = True

    while running:
        screen.fill(BACKGROUND)

        # Timer Countdown
        timer -= 1 / 60  # Reduce by ~1 second per frame at 60 FPS
        if timer <= 0:
            running = False  # End game when timer reaches 0

        # Draw Trash
        for trash in trash_objects:
            pygame.draw.rect(screen, (255, 105, 97), (trash.x, trash.y, 40, 40))  # Draw trash as red squares
            trash_label = font_text.render(trash.catergory, True, BLACK)
            screen.blit(trash_label, (trash.x, trash.y - 20))

        # Draw Bins
        for bin_obj in bins:
            pygame.draw.rect(screen, (144, 238, 144), (bin_obj.x, bin_obj.y, 60, 60))  # Draw bins as green squares
            bin_label = font_text.render(bin_obj.catergory, True, BLACK)
            screen.blit(bin_label, (bin_obj.x, bin_obj.y - 20))

        # Draw UI
        score_text = f"Score: {score}"
        timer_text = f"Timer: {int(timer)}s"
        price_text = f"Price: RM {original_price:.2f}"
        screen.blit(font_text.render(score_text, True, BLACK), (600, 450))
        screen.blit(font_text.render(timer_text, True, BLACK), (600, 500))
        screen.blit(font_text.render(price_text, True, BLACK), (600, 550))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check for trash-bin collisions
                for trash in trash_objects:
                    trash_rect = pygame.Rect(trash.x, trash.y, 40, 40)
                    for bin_obj in bins:
                        bin_rect = pygame.Rect(bin_obj.x, bin_obj.y, 60, 60)
                        if trash_rect.colliderect(bin_rect):
                            if bin_obj.check_trash(trash):  # Correct bin
                                score += 10
                                trash.x, trash.y = generate_random_coordinates()  # Respawn trash
                            else:
                                score -= 5  # Penalty for wrong bin

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)

    return score

def main(player_id, original_price):
    return gameplay(player_id, original_price)

# Main Function
if __name__ == "__main__":
    player_id = "Player01"
    original_price = 50.0
    final_score = main(player_id, original_price)
    print(f"Final Score: {final_score}")
