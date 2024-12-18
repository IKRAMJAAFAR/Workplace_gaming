import pygame
from trashItem import TrashItem
from bins import create_bins, draw_bins, check_collision
from scoring import update_score
from customer import Customer


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

customers = [
    Customer("assets\\untitledcustomer1.png", (50, 100), 10000),  # Waits for 10 seconds
    Customer("assets\\untitledcustomer1.png", (50, 200), 15000),  # Waits for 15 seconds
]
def draw_customers_and_timers(screen, customers, font):
    for customer in customers:
        customer.draw(screen)
        customer.draw_timer(screen, font)

# Timer and score
start_time = pygame.time.get_ticks()
time_limit = 60000  # 1 minute
score = 0
font = pygame.font.Font(None, 36)

# Create trash items and bins
trash_items = [
    TrashItem("assets\\trash_item.png", 800, 600),
    TrashItem("assets\\untitled1.png", 800, 600),
]
bins = create_bins()

def draw_timer_and_score(screen, time_remaining, score):
    timer_text = font.render(f"Time: {time_remaining // 1000}s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 50))

running = True
level = 1

while running:
    screen.fill((255, 255, 255))  # Clear screen

    # Draw bins
    draw_bins(screen, bins)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for trash in trash_items:
            trash.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP and not trash.dragging:
                bin_index = check_collision(trash, bins)
                if bin_index != -1:
                    score = update_score(trash, bin_index, score)

    # Update customers and check for timeout
    for customer in customers:
        if customer.left:
            print("Customer left! Game over.")
            running = False  # End game if a customer leaves
        else:
            customer.update()

    # Draw customers and timers
    draw_customers_and_timers(screen, customers, font)

    # Check level progression
    if score >= level * 50:  # Level up every 50 points
        level += 1
        update_game_timer(level)
        print(f"Level up! Current level: {level}")

    # Draw trash items
    for trash in trash_items:
        trash.draw(screen)

    # Draw timer and score
    elapsed_time = pygame.time.get_ticks() - start_time
    time_remaining = max(0, time_limit - elapsed_time)
    draw_timer_and_score(screen, time_remaining, score)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
