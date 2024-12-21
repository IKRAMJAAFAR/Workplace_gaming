import pygame
import cover_title as cover
import gameplay as game
import instruction as tutorial
import quantity_screen as inputting
import result as res
import board_screen as board
import csv

def get_latest_id(file_name, id_column):
    try:
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)  # Read all rows into a list
            
            if not rows:  # If no rows, return 0 (file only has headers)
                return 0
            
            # Get the max ID from the specified column
            return max(int(row[id_column]) for row in rows)
    except FileNotFoundError:
        # If the file doesn't exist, assume no records
        return 0
    except ValueError:
        # If ID column values are not valid integers, assume no records
        return 0


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cycle It Out!")
clock = pygame.time.Clock()

# Main function to test the title screen
def main():
    while True:
        id_player = get_latest_id('leaderboard.csv', 'Player_Id') + 1
        id_order = get_latest_id('order.csv', 'Order_Id') + 1
        cover.main()
        tutorial.main()
        total_price, selected_item, isPlaying, initials = inputting.main()
        score, result_price = game.main(id_player,initials,total_price) if isPlaying else 0,total_price
        board.main()
        res.main(id_order, id_player, score, result_price, selected_item, isPlaying) 
        # Insert discounted_price and selected_item as parameters here
        # Player_ID is null when isPlaying is False

if __name__ == "__main__":
    main()


