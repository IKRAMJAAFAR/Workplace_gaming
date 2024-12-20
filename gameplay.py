import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trash Sorting Game")
clock = pygame.time.Clock()

# Colors
BACKGROUND_A = (173, 216, 230)  # Light Blue for gameplay
BACKGROUND_B = (255, 248, 220)  # Light Yellow for stats
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font_title = pygame.font.Font(None, 60)
font_text = pygame.font.Font(None, 36)

# Constants
SLOTS = 3
SLOTSCOORDINATE = [(10,10),(210,10),(410,10)]
BINS = 4
TIMER_LIMIT = 60  # In seconds

# Game Variables
score = 0
time_remaining = TIMER_LIMIT
trash_items = []
bins = []
dragging_item = None

# Load Images (replace placeholders with actual images)
bin_images = [pygame.Surface((100, 100)) for _ in range(BINS)]
for bin_img in bin_images:
    bin_img.fill(GREEN)

trash_images = [pygame.Surface((50, 50)) for _ in range(SLOTS)]
for trash_img in trash_images:
    trash_img.fill(RED)

# Rectangles
trash_slots = [pygame.Rect(50 + i * 60, 100 if i < 4 else 400, 50, 50) for i in range(SLOTS)]
bin_slots = [pygame.Rect(WIDTH // 2 - 150 + i * 100, HEIGHT // 2 - 50, 100, 100) for i in range(BINS)]

# Random Trash Assignment
def generate_trash_items():
    return [{"type": random.randint(0, BINS - 1), "rect": trash_slots[i]} for i in range(SLOTS)]

trash_items = generate_trash_items()

# Timer Function
def update_timer():
    global time_remaining
    if time_remaining > 0:
        time_remaining -= 1 / 60

# Game Loop
def game_loop(price_input):
    global score, price, dragging_item, trash_items
    price = price_input

    running = True
    while running:
        screen.fill(WHITE)

        # Split Screen Layout
        pygame.draw.rect(screen, BACKGROUND_A, (0, 0, WIDTH*3 // 4, HEIGHT))
        pygame.draw.rect(screen, BACKGROUND_B, (WIDTH*3 // 4, 0, WIDTH // 4, HEIGHT))

        # Display Score, Price, Timer
        score_text = font_text.render(f"Score: {score}", True, BLACK)
        timer_text = font_text.render(f"Time: {int(time_remaining)}s", True, BLACK)
        price_text = font_text.render(f"Price: RM{price:.2f}", True, BLACK)
        screen.blit(score_text, (WIDTH*3 // 4 + 10, 50))
        screen.blit(timer_text, (WIDTH*3 // 4 + 10, 100))
        screen.blit(price_text, (WIDTH*3 // 4 + 10, 150))

        # Update Timer
        update_timer()
        if time_remaining <= 0:
            running = False

        # Draw Bins
        for i, bin_slot in enumerate(bin_slots):
            screen.blit(bin_images[i], bin_slot)

        # Draw Trash Items
        for item in trash_items:
            if item != dragging_item:  # Don't draw the item being dragged
                screen.blit(trash_images[item["type"]], item["rect"])

        # Dragging Logic
        if dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dragging_item["rect"].center = (mouse_x, mouse_y)
            screen.blit(trash_images[dragging_item["type"]], dragging_item["rect"])

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any trash item is clicked
                for item in trash_items:
                    if item["rect"].collidepoint(event.pos):
                        dragging_item = item
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_item:
                    # Check if dropped over a bin
                    for i, bin_slot in enumerate(bin_slots):
                        if bin_slot.colliderect(dragging_item["rect"]):
                            if dragging_item["type"] == i:  # Correct bin
                                score += 10
                                price -= 1.00  # Example price deduction
                            else:  # Incorrect bin
                                score -= 5
                            # Reset the slot with a new item
                            dragging_item["type"] = random.randint(0, BINS - 1)
                            dragging_item["rect"].topleft = trash_slots[trash_items.index(dragging_item)].topleft
                            break
                    dragging_item = None

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)

def main(price_input):
    game_loop(price_input)
