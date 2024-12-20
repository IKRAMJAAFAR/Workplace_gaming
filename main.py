import pygame
import cover_title as cover
import gameplay as game
import instruction as tutorial
import quantity_screen as inputting
import result as res

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cycle It Out!")
clock = pygame.time.Clock()

# Main function to test the title screen
def main():
    while True:
        cover.main()
        tutorial.main()
        total_price, selected_item = inputting.main()
        game.main(total_price)
        res.main() # Insert discounted_price and selected_item as parameters here


if __name__ == "__main__":
    main()


