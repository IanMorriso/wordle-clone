import pygame
import sys
from PygameWordle import ScrabbleDict, Game

pygame.init()

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


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Clone")

font = pygame.font.Font(None, FONT_SIZE)

def draw_grid():
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, GRID_COLOR, (100, 100 + i * CELL_SIZE), (100 + GRID_SIZE * CELL_SIZE, 100 + i * CELL_SIZE), 2)
        pygame.draw.line(screen, GRID_COLOR, (100 + i * CELL_SIZE, 100), (100 + i * CELL_SIZE, 100 + GRID_SIZE * CELL_SIZE), 2)

def draw_guess(guess, row, colors):
    for i, letter in enumerate(guess):
        text = font.render(letter.upper(), True, FONT_COLOR)
        color = BG_COLOR
        if len(colors) > 1:
            color = GREEN_COLOR if colors[i] == 'green' else ORANGE_COLOR if colors[i] == 'orange' else RED_COLOR
        pygame.draw.rect(screen, color, (102 + i * CELL_SIZE, 102 + row * CELL_SIZE, CELL_SIZE-2, CELL_SIZE-2))
        screen.blit(text, (110 + i * CELL_SIZE, 110 + row * CELL_SIZE))

def play_again_prompt(message):
    prompt_font = pygame.font.Font(None, 48)
    prompt_text = message + "\nPlay again? (Y/N)"
    render_text(screen, prompt_text, (WIDTH // 2 - 100, HEIGHT // 2), prompt_font, FONT_COLOR)
    pygame.display.flip()

    waiting_for_response = True
    while waiting_for_response:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False
                
def render_text(screen, text, position, font, color=(255,0,0)):
    text = font.render(text, True, color)
    screen.blit(text, position)

def main():
    clock = pygame.time.Clock()
    running = True
    current_guess = ""
    guesses = []
    alert = ""
    game_result = ""

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
                    alert = game.inputValidator(current_guess)
                    if not alert:
                        if len(current_guess) == GRID_SIZE:
                            colors = game.match(current_guess.lower())
                            game.add_guess((current_guess, colors))
                            current_guess = ""
                            if game.is_correct_guess() or len(game.get_guesses()) >= 5:
                                game_result = "You lose!"
                                if game.is_correct_guess():
                                    game_result = "You win!"
                                running = False
                elif event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                elif len(current_guess) < GRID_SIZE and event.unicode.isalpha():
                    current_guess += event.unicode

        for row, (guess, colors) in enumerate(game.get_guesses()):
            draw_guess(guess, row, colors)
        draw_guess(current_guess, len(game.get_guesses()), [])
        
        if alert:
            render_text(screen, alert, (100, 500), font)

        pygame.display.flip()
        clock.tick(60)

        # Ask if the user wants to play again
    if play_again_prompt(game_result):
        main()  # Restart the game

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()