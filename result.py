import pygame
import sys
import csv
import qrcode
from PIL import Image

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Result and Confirmation")
clock = pygame.time.Clock()

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
font_title = pygame.font.Font(None, 60)
font_text = pygame.font.Font(None, 36)

# Generate a QR Code
def generate_qr_code(total_price):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(f"Total Price: RM{total_price:.2f}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")  # Save the QR code locally
    return pygame.image.load("qr_code.png")

# Save order to CSV
def save_order_to_csv(filename, initials, score):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([initials, score])

# Result Screen Function
def show_result(score, total_price):
    # Generate QR code
    qr_code_image = generate_qr_code(total_price)
    qr_rect = qr_code_image.get_rect(center=(650, 300))

    running = True
    confirmed = False  # Track if the payment has been confirmed

    while running:
        screen.fill(WHITE)  # Background color

        # Display Title
        title_text = font_title.render("Order Summary", True, BLACK)
        screen.blit(title_text, (250, 50))

        # Show Score and Total Price
        score_text = font_text.render(f"Your Score: {score}", True, BLACK)
        price_text = font_text.render(f"Discounted Price: RM{total_price:.2f}", True, BLACK)
        screen.blit(score_text, (50, 150))
        screen.blit(price_text, (50, 200))

        # Translate Score into Real-Life Achievement
        achievement_text = font_text.render(
            "Great job! Your score contributes to reducing waste!",
            True,
            BLACK
        )
        screen.blit(achievement_text, (50, 250))

        # Display QR Code
        screen.blit(qr_code_image, qr_rect)

        # Leaderboard
        leaderboard_text = font_text.render("Leaderboard (Top 3):", True, BLACK)
        screen.blit(leaderboard_text, (50, 350))

        # Simulated leaderboard (fetch dynamically if needed)
        simulated_leaderboard = [("ABC", 300), ("DEF", 250), ("GHI", 200)]
        y_offset = 400
        for initials, leaderboard_score in simulated_leaderboard:
            lb_text = font_text.render(f"{initials}: {leaderboard_score}", True, BLACK)
            screen.blit(lb_text, (50, y_offset))
            y_offset += 30

        # Confirmation Button
        pygame.draw.rect(screen, GREEN if confirmed else RED, (300, 500, 200, 50))
        confirm_text = font_text.render("Confirm" if not confirmed else "Confirmed", True, WHITE)
        screen.blit(confirm_text, (340, 510))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Confirm Payment
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 300 <= mouse_x <= 500 and 500 <= mouse_y <= 550:
                    if not confirmed:  # On first click, save data and confirm
                        initials = input("Enter Customer's Initials (First 3 Letters): ")  # Replace with a text input box if needed
                        save_order_to_csv("order.csv", initials, score)
                        confirmed = True

        # Update Screen
        pygame.display.flip()
        clock.tick(60)

# Main Function to Test Result Screen
def main(score, result_price, selected_item, isPlaying):
    show_result(score, result_price)

if __name__ == "__main__":
    main()
