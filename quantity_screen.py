import pygame
import pandas as pd

# Global Variables
global total_price, selected, play_game

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantity Selection Screen")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (200, 255, 200)  # Light Green
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Fonts
font_text = pygame.font.Font(None, 36)
font_input = pygame.font.Font(None, 32)

# Load Items from CSV
def load_items(csv_file):
    df = pd.read_csv(csv_file)
    return df.to_dict("records")

# Button Class
class Button:
    def __init__(self, x, y, w, h, text, callback, toggle=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.toggle = toggle
        self.active = False

    def draw(self):
        color = GRAY if self.toggle and self.active else WHITE
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        if self.text:
            text_surf = font_text.render(self.text, True, BLACK)
            screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.toggle:
                self.active = not self.active
            return self.callback()

# Quantity Selection Logic
def increase_quantity(index):
    if selected_quantities[index] < items[index]["Quantity_Left"]:
        selected_quantities[index] += 1

def decrease_quantity(index):
    if selected_quantities[index] > 0:
        selected_quantities[index] -= 1

# Calculate Total Price
def calculate_total_price():
    return sum(item["Price_(RM)"] * quantity for item, quantity in zip(items, selected_quantities))

# Load Items and Initialize Quantities
items = load_items("items.csv")
selected_quantities = [0] * len(items)

# Create Buttons
buttons = []
y_offset = 150 - 100
for i, item in enumerate(items):
    buttons.append(Button(500, y_offset, 40, 40, "-", lambda i=i: decrease_quantity(i)))
    buttons.append(Button(600, y_offset, 40, 40, "+", lambda i=i: increase_quantity(i)))
    y_offset += 50

# Play Game Checkbox
play_game = False
def toggle_play_game():
    global play_game
    play_game = not play_game

checkbox_button = Button(50, 500 - 100, 30, 30, "", toggle_play_game, toggle=True)
checkbox_label = "Check to play the game"

# Play Button Callback
def prepare_results():
    global selected, total_price
    selected = [{"Item_Id": items[i]["Item_Id"], "Quantity": q} for i, q in enumerate(selected_quantities) if q > 0]
    total_price = calculate_total_price()
    return "gameplay"

play_button = Button(300, 550 - 50, 200, 50, "Play", prepare_results)

# Input Box for Initials
input_box = pygame.Rect(90, 540, 200, 40)
input_text = ""
input_active = False

# Quantity Selection Screen
def quantity_screen():
    global selected, total_price, play_game, input_text, input_active
    selected = []  # Store selected items
    total_price = 0.0  # Store total price
    play_game = False  # Initialize play game as False
    input_text = ""  # Reset input text
    input_active = False  # Input box is inactive initially

    running = True
    while running:
        screen.fill(BACKGROUND)

        # Draw Items and Quantities
        y_offset = 150 - 100
        for i, item in enumerate(items):
            item_text = f"{item['Item']} (x{item['Quantity_Left']})"
            item_surf = font_text.render(item_text, True, BLACK)
            screen.blit(item_surf, (50, y_offset))
            quantity_text = font_text.render(str(selected_quantities[i]), True, BLACK)
            screen.blit(quantity_text, (550, y_offset))
            y_offset += 50

        # Draw Buttons
        for button in buttons:
            button.draw()

        # Draw Total Price
        total_price_text = f"Total Price: RM {calculate_total_price():.2f}"
        total_price_surf = font_text.render(total_price_text, True, BLACK)
        screen.blit(total_price_surf, (50, 450 - 100))

        # Draw Checkbox and Label
        checkbox_button.draw()
        checkbox_label_surf = font_text.render(checkbox_label, True, BLACK)
        screen.blit(checkbox_label_surf, (90, 500 - 100))

        # Draw Input Box if Checkbox is Checked
        if play_game:
            pygame.draw.rect(screen, WHITE, input_box)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            input_text_surf = font_input.render(input_text, True, BLACK)
            screen.blit(input_text_surf, (input_box.x + 5, input_box.y + 5))

        # Draw Play Button
        play_button.draw()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(event.pos)
                checkbox_button.check_click(event.pos)
                if input_box.collidepoint(event.pos) and play_game:
                    input_active = True
                else:
                    input_active = False
                if play_button.check_click(event.pos) == "gameplay":
                    total_price = calculate_total_price()
                    selected = [
                        {
                            "Item_Id": items[i]["Item_Id"], 
                            "Item": items[i]["Item"],       # Include item name for clarity
                            "Quantity": selected_quantities[i]
                        }
                        for i in range(len(items))
                        if selected_quantities[i] > 0
                    ]
                    running = False
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)

    return total_price, selected, play_game, input_text

# Main Function
def main():
    total_price, selected, play_game, initials = quantity_screen()
    print("Total Price:", total_price)
    print("Selected Items:", selected)
    print("Play Game:", play_game)
    print("Initials:", initials)
    return total_price, selected, play_game, initials

if __name__ == "__main__":
    main()
