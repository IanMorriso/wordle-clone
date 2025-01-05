import pygame
import sys
from PygameWordle import ScrabbleDict, Game

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
FONT_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
ORANGE_COLOR = (255, 165, 0)
RED_COLOR = (255, 0, 0)
FONT_SIZE = 32
GRID_SIZE = 5
CELL_SIZE = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Clone")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

def draw_grid():
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, GRID_COLOR, (100, 100 + i * CELL_SIZE), (100 + GRID_SIZE * CELL_SIZE, 100 + i * CELL_SIZE), 2)
        pygame.draw.line(screen, GRID_COLOR, (100 + i * CELL_SIZE, 100), (100 + i * CELL_SIZE, 100 + GRID_SIZE * CELL_SIZE), 2)

def draw_guess(guess, row, colors):
    for i, letter in enumerate(guess):
        text = font.render(letter.upper(), True, FONT_COLOR)
        color = GREEN_COLOR if colors[i] == 'green' else ORANGE_COLOR if colors[i] == 'orange' else RED_COLOR
        pygame.draw.rect(screen, color, (102 + i * CELL_SIZE, 102 + row * CELL_SIZE, CELL_SIZE-2, CELL_SIZE-2))
        screen.blit(text, (110 + i * CELL_SIZE, 110 + row * CELL_SIZE))

def main():
    clock = pygame.time.Clock()
    running = True
    current_guess = ""
    guesses = []

    # Initialize game
    wordle_dict = ScrabbleDict(5, "scrabble5.txt")
    game = Game(5, wordle_dict)

    while running:
        screen.fill(BG_COLOR)
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(current_guess) == GRID_SIZE:
                        colors = game.match(current_guess.lower())
                        game.add_guess((current_guess, colors))
                        current_guess = ""
                        if game.is_correct_guess() or len(game.get_guesses()) >= 5:
                            running = False
                elif event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                elif len(current_guess) < GRID_SIZE and event.unicode.isalpha():
                    current_guess += event.unicode

        for row, (guess, colors) in enumerate(game.get_guesses()):
            draw_guess(guess, row, colors)
        draw_guess(current_guess, len(game.get_guesses()), [''] * GRID_SIZE)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()