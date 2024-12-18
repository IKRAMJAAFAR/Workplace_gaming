import pygame
import sys
import csv
import pandas as pd


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Circular Tycoon")
clock = pygame.time.Clock()

# Colors
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (50, 205, 50)
DARK_BLUE = (0,0,139)
BLACK = (0,0,0)

# Fonts
font_title = pygame.font.Font(None, 100)  # Title font
font_button = pygame.font.Font(None, 50)  # Button font
font_text = pygame.font.Font(None, 36)

# Button Dimensions
button_width = 200
button_height = 80
button_x = (800 - button_width) // 2
button_y = 400

# Function to read items from a CSV file
def read_csv_items(filename):
    items = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append({
                "Item": row["Item"], 
                "Quantity": int(row["Quantity"]), 
                "Price": float(row["Price_(RM)"])
            })
    return items


# Tutorial/Instruction Screen Function
def show_instructions(items):
    running = True
    selected_items = {}  # To store user's selections
    total_price = 0  # Initialize total price

    while running:
        screen.fill(WHITE)  # Background color

        # Display Title
        title_text = font_title.render("Instructions", True, DARK_BLUE)
        screen.blit(title_text, (250, 50))

        # Placeholder for instructions (can add pictures later)
        instructions_text = font_text.render("1. Choose items to buy.", True, BLACK)
        instructions_text2 = font_text.render("2. Press ENTER to calculate total.", True, BLACK)
        screen.blit(instructions_text, (50, 150))
        screen.blit(instructions_text2, (50, 200))

        # Display Available Items
        y_offset = 250
        for item in items:
            item_text = font_text.render(
                f"{item['Item']} (x{item['Quantity']}) - RM{item['Price']:.2f}",
                True,
                BLACK
            )
            screen.blit(item_text, (50, y_offset))
            y_offset += 40


        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # On Enter, calculate total price
                    total_price = sum(count * item['Price'] for item, count in selected_items.items())
                    running = False  # Exit the instructions screen

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Placeholder: Detect clicks to select items (future enhancement)
                pass

        # Input logic (for item quantities)
        # Example: (future improvement can include better UI for item selection)
        for item in items:
            if item['Item'] not in selected_items:
                selected_items[item['Item']] = 1  # Default quantity for now

        # Update Screen
        pygame.display.flip()
        clock.tick(60)

    return total_price

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

        # Check if mouse is over the button
        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
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
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    running = False  # Exit cover title to start the game

        # Update the screen
        pygame.display.flip()
        clock.tick(60)


# Main function to test the title screen
def main():
    while True:
        show_cover_title()
        items = read_csv_items("items.csv")  # Load items from CSV
        total_price = show_instructions(items)
        print("Game Starts!")  # Replace this with your actual game loop


if __name__ == "__main__":
    main()


