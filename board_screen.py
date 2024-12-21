# Leaderboard Screen
import pandas as pd
import pygame
import pygame.image


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


def leaderboard_screen():
    running = True

    # Load Leaderboard Data
    try:
        df = pd.read_csv("leaderboard.csv")
        #df = df.drop("Player_Id", axis = 1)
        leaderboard_data = df.sort_values(by="Score", ascending=False).head(10).to_dict("records")
    except FileNotFoundError:
        leaderboard_data = []

    while running:
        screen.fill(BACKGROUND)

        # Display Leaderboard Title
        title_surf = font_text.render("Leaderboard", True, BLACK)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))


        # Display Top 10 Leaderboard Entries
        y_offset = 100
        for i, entry in enumerate(leaderboard_data):
            text = f"{i + 1}. {entry['Initials']} - Score: {entry['Score']}"
            entry_surf = font_text.render(text, True, BLACK)
            screen.blit(entry_surf, (50, y_offset))
            y_offset += 40

        # Exit Button
        exit_button = Button(50, 500, 200, 50, "Exit", lambda: "exit")
        exit_button.draw()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.check_click(event.pos) == "exit":
                    running = False

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)

def main():
    leaderboard_screen()

if __name__ == '__main__':
    main()
