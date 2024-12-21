import random
import pygame
import csv
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
RED = (255, 0, 0)

# Fonts
font_large = pygame.font.Font(None, 72)
font_text = pygame.font.Font(None, 36)

# Fixed Bin Coordinates
offset = 40
BIN_COORDINATES = [
    (WIDTH//2 - offset, HEIGHT//2 - offset),  # Bin 1
    (WIDTH//2 - offset, HEIGHT//2 + offset),  # Bin 2
    (WIDTH//2 + offset, HEIGHT//2 - offset),  # Bin 3
    (WIDTH//2 + offset, HEIGHT//2 + offset),  # Bin 4
]

# Region Boundary
BIN_REGION = pygame.Rect(250, 350, 300, 250)
UI_REGION = pygame.Rect(600, 400, 200, 200)

# Randomized Trash Placement
def generate_random_coordinates():
    while True:
        x = random.randint(30, WIDTH - 50)
        y = random.randint(0, HEIGHT - 150)  # Keep trash away from bottom UI
        if not UI_REGION.collidepoint(x,y) and not BIN_REGION.collidepoint(x, y):  # Ensure trash avoids bin region
            return x, y

# Initialize Bins
bins = [
    Bin("Plastic"),
    Bin("Aluminium"),
    Bin("Paper"),
    Bin("Waste"),
]

# Assign bins to fixed coordinates
for i, bin_obj in enumerate(bins):
    bin_obj.x, bin_obj.y = BIN_COORDINATES[i]

# Initialize Trash
trash_categories = ["Plastic", "Aluminium", "Paper", "Waste"]
trash_objects = []

# Append Data to Leaderboard
def append_to_leaderboard(player_id,initials, original_price, score, reduced_price):
    with open("leaderboard.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([player_id,initials, original_price, score, reduced_price])

# Gameplay Function
def gameplay(player_id,initials, original_price):
    score = 0
    timer = 10  # 60 seconds timer
    running = True
    countdown = 3  # 3-second countdown
    trash_spawn_time = 0  # Time to spawn the next trash
    selected_trash = None  # Trash being dragged

    # Add initial trash
    for _ in range(4):
        category = random.choice(trash_categories)
        x, y = generate_random_coordinates()
        trash_objects.append(Trash(category, wait_time=0))
        trash_objects[-1].x, trash_objects[-1].y = x, y

    while running:
        screen.fill(BACKGROUND)

        # Countdown at Start
        if countdown > 0:
            countdown_text = font_large.render(str(countdown), True, BLACK)
            screen.blit(countdown_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.delay(1000)
            countdown -= 1
            continue

        # Timer Countdown
        timer -= 1 / 60  # Reduce by ~1 second per frame at 60 FPS
        if timer <= 0:
            running = False  # End game when timer reaches 0
            break

        # Spawn New Trash Every 2 Seconds
        trash_spawn_time += 1 / 60  # Increment time
        if trash_spawn_time >= 2:  # Every 2 seconds
            category = random.choice(trash_categories)
            x, y = generate_random_coordinates()
            trash_objects.append(Trash(category, wait_time=0))
            trash_objects[-1].x, trash_objects[-1].y = x, y
            trash_spawn_time = 0  # Reset spawn timer

        # Calculate Discounted Price
        reduced_price = round(min(original_price, original_price * max(0.5, 1 - score * 0.01)),2)

        # Draw Bins
        for bin_obj in bins:
            sprite_path = bin_obj.sprites
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (60, 60))  # Adjust size
            screen.blit(sprite, (bin_obj.x, bin_obj.y))

        # Draw Trash
        for trash in trash_objects:
            sprite_path = trash.sprites
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (40, 40))  # Adjust size
            screen.blit(sprite, (trash.x, trash.y))

        # Draw UI
        score_text = f"Score: {score}"
        timer_text = f"Timer: {int(timer)}s"
        price_text = f"Price: RM {reduced_price:.2f}"
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
                for trash in trash_objects:
                    trash_rect = pygame.Rect(trash.x, trash.y, 40, 40)
                    if trash_rect.collidepoint(pos):
                        selected_trash = trash  # Select trash for dragging
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_trash:
                    # Check for bin collision
                    trash_rect = pygame.Rect(selected_trash.x, selected_trash.y, 40, 40)
                    correct_bin = False
                    for bin_obj in bins:
                        bin_rect = pygame.Rect(bin_obj.x, bin_obj.y, 60, 60)
                        if trash_rect.colliderect(bin_rect):
                            if bin_obj.check_trash(selected_trash):  # Correct bin
                                correct_bin = True
                                break
                    trash_objects.remove(selected_trash)  # Remove trash        
                    score += 10 if correct_bin else -5
                    score = 0 if score < 0 else score
                    selected_trash = None  # Deselect trash
            elif event.type == pygame.MOUSEMOTION:
                if selected_trash:
                    selected_trash.x, selected_trash.y = event.pos  # Update position

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)

    # Show "Game Over" Screen
    screen.fill(BACKGROUND)
    game_over_rect = pygame.Rect(WIDTH // 2 - 150 - 30, HEIGHT // 2 - 50, 300 + 50, 100)
    pygame.draw.rect(screen, RED, game_over_rect)
    game_over_text = font_large.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 25))
    pygame.display.flip()
    pygame.time.delay(3000)
    
    # Append to Leaderboard
    append_to_leaderboard(player_id,initials, round(original_price,2), score, round(reduced_price,2))

    return score, reduced_price

def main(player_id,initials,original_price):
    return gameplay(player_id,initials,original_price)

# Main Function
if __name__ == "__main__":
    player_id = "Player01"
    initials = "AKJ"
    original_price = 50.0
    final_score, discount_price = main(player_id,initials, original_price)
    print(f"Final Score: {final_score}")
    print(f"Discount Price: {discount_price}")
