import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Circular Tycoon")
clock = pygame.time.Clock()

# Colors
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (50, 205, 50)

# Fonts
font_title = pygame.font.Font(None, 100)  # Title font
font_button = pygame.font.Font(None, 50)  # Button font

# Button Dimensions
button_width = 200
button_height = 80
button_x = (800 - button_width) // 2
button_y = 400


def show_cover_title():
    running = True
    while running:
        screen.fill(DARK_GREEN)  # Set background to dark green
        # Render title text
        title_text = font_title.render("Circular Tycoon", True, WHITE)
        title_rect = title_text.get_rect(center=(400, 200))  # Center the title
        screen.blit(title_text, title_rect)

        # Draw play button
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        in_button_x_region = button_x <= mouse_x <= button_x + button_width
        in_button_y_region = button_y <= mouse_y <= button_y + button_height

        # Check if mouse is over the button
        if in_button_x_region and in_button_y_region:
            button_color = LIGHT_GREEN  # Highlight button on hover
        else:
            button_color = WHITE

        # Draw the button
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        play_text = font_button.render("Play", True, DARK_GREEN)
        play_text_rect = play_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(play_text, play_text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_button_x_region and in_button_y_region:
                    running = False  # Exit cover title to start the game

        # Update the screen
        pygame.display.flip()
        clock.tick(60)


# Main function to test the title screen
def main():
    show_cover_title()


if __name__ == "__main__":
    main()
