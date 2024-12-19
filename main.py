import pygame
import cover_title as cover
import gameplay as game
import instruction as tutorial
import result as res



# Initialize Pygame
pygame.init()

# Main function to test the title screen
def main():
    while True:
        show_cover_title()
        items = read_csv_items("items.csv")  # Load items from CSV
        total_price = show_instructions(items)
        print("Game Starts!")  # Replace this with your actual game loop


if __name__ == "__main__":
    main()


