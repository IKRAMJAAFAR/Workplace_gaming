import pygame
import sys
import csv

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Instructions")
clock = pygame.time.Clock()

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 139)
font_title = pygame.font.Font(None, 74)
font_text = pygame.font.Font(None, 36)

# Function to read items from a CSV file
def read_csv_items(filename):
    items = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append({"Item": row["Item"], "Price": float(row["Price"])})
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
            item_text = font_text.render(f"{item['Item']} - ${item['Price']:.2f}", True, BLACK)
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

# Main Function
def main():
    items = read_csv_items("items.csv")  # Load items from CSV
    total_price = show_instructions(items)  # Show instructions and calculate price
    print(f"Total Price: ${total_price:.2f}")  # Placeholder for gameplay transition

    # Proceed to gameplay with total price
    # replace with your game's main logic here

if __name__ == "__main__":
    main()
