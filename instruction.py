import pygame

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Instructions Screen")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (173, 216, 230)  # Light Blue
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font_title = pygame.font.Font(None, 60)
font_text = pygame.font.Font(None, 36)
font_button = pygame.font.Font(None, 50)  # Button font

# Button Class
x = """
class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = font_text.render(self.text, True, BLACK)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
"""

# Proceed Button Callback
def go_to_quantity_screen():
    return "quantity_screen"

# Create Button
button_x = 300
button_y = 500
button_width = 250
button_height = 50

# Instructions Screen Function
def instructions_screen():
    running = True
    while running:
        screen.fill(BACKGROUND)

        # Draw Instructions
        instructions = [
            "1. Follow the steps to play the game.",
            "2. Adjust quantities of items as needed.",
            "3. View the total price dynamically.",
            "4. Click checkbox if want to play the game.",
            "5. Click Play to begin the game.",
            "6. Have fun sorting trash items!",
            "Waste bin   (grey): Bananas, Plates, Gums",
            "Plastic bin (yellow): Straws, Bottles, Utensils",
            "Paper bin   (blue): Bags, Newspapers, Cups",
            "Aluminium bin (green): Cans, Caps"
        ]
        for i, line in enumerate(instructions):
            text_surf = font_text.render(line, True, BLACK)
            screen.blit(text_surf, (50, 50 + i * 40))

        mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
        in_button_x_region = button_x <= mouse_x <= button_x + button_width
        in_button_y_region = button_y <= mouse_y <= button_y + button_height

        # Draw the button
        button_color = WHITE 
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        play_text = font_button.render("I Understand", True, BLACK)
        play_text_rect = play_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(play_text, play_text_rect)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if in_button_x_region and in_button_y_region:
                    running = False  # Exit cover title to start the game

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)

def main():
    instructions_screen()

if __name__ == '__main__':
    main()
