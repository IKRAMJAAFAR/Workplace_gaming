# Leaderboard Screen
import pandas as pd
import csv
import pygame

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Leaderboard Screen")
clock = pygame.time.Clock()

BACKGROUND = (0,150,0)
BLACK = (0,0,0)
GRAY = (100,100,100)
WHITE = (255,255,255)
font_text = pygame.font.Font(None, 36)

def save_transaction(order_id, player_id, method_payment, money, remarks):
    with open("transaction.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([order_id, player_id, method_payment, money, remarks])

def save_order(order_id, selected_item):
    with open("order.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        for id, item_name, quantity in selected_item:
            writer.writerow([order_id, id, quantity])

def update_items(selected_item):
    df = pd.read_csv("items.csv")
    for id,item_name, quantity in selected_item:
        df.loc[df["Item_Id"] == id, "Quantity_Left"] -= quantity
    df.to_csv("items.csv", index=False)



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

# Payment Screen with additional parameters
def payment_screen(id_order, id_player, score, result_price, selected_item, isPlaying):
    id_player = None if not isPlaying else id_player
    running = True
    payment_method = "QR"  # Default payment method
    remarks = ""  # Text box for remarks
    input_active = False  # Input state for remarks box
    confirmed_payment = False
    while running:
        screen.fill(BACKGROUND)

        # Display Player Information
        text = [
            f"Order ID: {id_order}    Player ID: {id_player}",
            f"Score: {score}",
            f"Price: RM {result_price:.2f}",
            f"Selected Items: {', '.join([f'{item} (x{qty})' for _ ,item, qty in selected_item])}",
            f"Payment Method: {payment_method}",
        ]
        y_offset = 50
        for line in text:
            line_surf = font_text.render(line, True, BLACK)
            screen.blit(line_surf, (50, y_offset))
            y_offset += 50

        # Display Payment Method Buttons
        qr_button = Button(50, 300, 100, 50, "QR", lambda: "QR")
        cash_button = Button(200, 300, 100, 50, "Cash", lambda: "Cash")
        other_button = Button(350, 300, 100, 50, "Other", lambda: "Other")
        qr_button.active = payment_method == "QR"
        cash_button.active = payment_method == "Cash"
        other_button.active = payment_method == "Other"
        qr_button.draw()
        cash_button.draw()
        other_button.draw()

        # Display Remarks Input Box
        pygame.draw.rect(screen, WHITE, (50, 400, 500, 40), 0)
        pygame.draw.rect(screen, BLACK, (50, 400, 500, 40), 2)
        remarks_surf = font_text.render(remarks, True, BLACK)
        screen.blit(remarks_surf, (55, 410))

        # Confirm Payment Button
        confirm_button = Button(50, 500, 200, 50, "Confirm Payment", lambda: True)
        confirm_button.draw()

        # Done Button
        done_button = Button(300, 500, 200, 50, "Done", lambda: "done")
        done_button.draw()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check which payment method was clicked
                if qr_button.check_click(event.pos) == "QR":
                    payment_method = "QR"
                    input_active = False  # Disable remarks input
                elif cash_button.check_click(event.pos) == "Cash":
                    payment_method = "Cash"
                    input_active = False  # Disable remarks input
                elif other_button.check_click(event.pos) == "Other":
                    payment_method = "Other"
                    input_active = True  # Enable remarks input

                # Check if the remarks box is clicked
                if 50 <= event.pos[0] <= 550 and 400 <= event.pos[1] <= 440:
                    input_active = True  # Activate text input
                else:
                    input_active = False  # Deactivate text input if clicked outside

                # Check button clicks
                if confirm_button.check_click(event.pos):
                    confirmed_payment = True
                    print("Payment Confirmed!")
                elif done_button.check_click(event.pos) == "done" and confirmed_payment:
                    save_transaction(id_order, id_player, payment_method, result_price, remarks)
                    save_order(id_order, selected_item)
                    update_items(selected_item)
                    running = False

            # Handle keyboard input
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    remarks = remarks[:-1]
                else:
                    remarks += event.unicode

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)



def main(id_order, id_player, score, result_price, selected_item, isPlaying):
    # Step 1: Convert to a list of tuples
    tuples_list = [(item["Item_Id"], item["Item"], item["Quantity"]) for item in selected_item]
    payment_screen(id_order, id_player, score, result_price, tuples_list, isPlaying)

if __name__ == "__main__":
    id_order = 1
    id_player = 1
    score = 1
    result_price = 1
    selected_item = [
    {"Item_Id": 1, "Item": "Money", "Quantity": 2},
    {"Item_Id": 2, "Item": "Kali", "Quantity": 1},
    ]
    isPlaying = True
    main(id_order, id_player, score, result_price, selected_item, isPlaying)