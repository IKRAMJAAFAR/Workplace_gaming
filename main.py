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
    id_player = 0 + 1 # Please change the first number that aligns with the number of rows in the leaderboard.csv
    id_order = 0 + 1 # Please change the first number that aligns with the number of rows in the order.csv
    while True:
        id = [id_order, id_player]
        cover.main()
        tutorial.main()
        total_price, selected_item, isPlaying = inputting.main()
        score, result_price = game.main(total_price) if isPlaying else 0,total_price
        res.main(score, result_price, selected_item, isPlaying) # Insert discounted_price and selected_item as parameters here
        id_player += 1
        id_order += 1


if __name__ == "__main__":
    main()


