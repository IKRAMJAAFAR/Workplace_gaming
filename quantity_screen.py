import pygame
import pandas as pd
global total_price, selected

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

# Fonts
font_text = pygame.font.Font(None, 36)

# Load Items from CSV
def load_items(csv_file):
    df = pd.read_csv(csv_file)
    return df.to_dict("records")

# Button Class
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
        return self.callback() if self.rect.collidepoint(pos) else None

# Quantity Selection Logic
def increase_quantity(index):
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
y_offset = 150
for i, item in enumerate(items):
    buttons.append(Button(500, y_offset, 40, 40, "-", lambda i=i: decrease_quantity(i)))
    buttons.append(Button(600, y_offset, 40, 40, "+", lambda i=i: increase_quantity(i)))
    y_offset += 50

# Play Button Callback
def prepare_results():
    global selected, total_price
    selected = [{"Item": items[i]["Item"], "Quantity": q} for i, q in enumerate(selected_quantities) if q > 0]
    total_price = calculate_total_price()
    return "gameplay"

play_button = Button(300, 500, 200, 50, "Play", prepare_results)

# Quantity Selection Screen
def quantity_screen():
    global selected, total_price
    selected = []  # Store selected items
    total_price = 0.0  # Store total price

    running = True
    while running:
        screen.fill(BACKGROUND)

        # Draw Items and Quantities
        y_offset = 150
        for i, item in enumerate(items):
            item_text = f"{item['Item']} (x{item['Quantity']})"
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
        screen.blit(total_price_surf, (50, 450))

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
                if play_button.check_click(event.pos) == "gameplay":
                    total_price = calculate_total_price()
                    selected = [
                        {"Item": items[i]["Item"], "Quantity": selected_quantities[i]}
                        for i in range(len(items))
                        if selected_quantities[i] > 0
                    ]
                    running = False

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)

    return total_price, selected

# Main Function
def main():
    total_price, selected = quantity_screen()
    print("Total Price:", total_price)
    print("Selected Items:", selected)
    return total_price, selected

if __name__ == "__main__":
    main()

