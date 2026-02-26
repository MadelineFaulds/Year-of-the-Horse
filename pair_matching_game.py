import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game settings
ROWS, COLS = 4, 4
CARD_SIZE = 100
GAP = 10
WIDTH = COLS * (CARD_SIZE + GAP) + GAP
HEIGHT = ROWS * (CARD_SIZE + GAP) + GAP
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pair Matching Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Card values (pairs)
values = list(range(1, (ROWS * COLS) // 2 + 1)) * 2
random.shuffle(values)

# Card state: 0 = face down, 1 = face up, 2 = matched
card_states = [[0 for _ in range(COLS)] for _ in range(ROWS)]
card_values = [[0 for _ in range(COLS)] for _ in range(ROWS)]
for i in range(ROWS * COLS):
    card_values[i // COLS][i % COLS] = values[i]

font = pygame.font.SysFont(None, 48)


def draw_board():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(GAP + x * (CARD_SIZE + GAP), GAP + y * (CARD_SIZE + GAP), CARD_SIZE, CARD_SIZE)
            state = card_states[y][x]
            if state == 2:
                pygame.draw.rect(screen, GREEN, rect)
            elif state == 1:
                pygame.draw.rect(screen, BLUE, rect)
                value = str(card_values[y][x])
                text = font.render(value, True, WHITE)
                screen.blit(text, (rect.x + CARD_SIZE // 2 - text.get_width() // 2, rect.y + CARD_SIZE // 2 - text.get_height() // 2))
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)


def get_card_at_pos(pos):
    mx, my = pos
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(GAP + x * (CARD_SIZE + GAP), GAP + y * (CARD_SIZE + GAP), CARD_SIZE, CARD_SIZE)
            if rect.collidepoint(mx, my):
                return x, y
    return None, None


def main():
    first = None
    second = None
    matched_pairs = 0
    running = True
    waiting = False
    wait_time = 0
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not waiting:
                x, y = get_card_at_pos(event.pos)
                if x is not None and card_states[y][x] == 0:
                    card_states[y][x] = 1
                    if first is None:
                        first = (x, y)
                    elif second is None and (x, y) != first:
                        second = (x, y)
                        waiting = True
                        wait_time = pygame.time.get_ticks()
        if waiting:
            if pygame.time.get_ticks() - wait_time > 800:
                x1, y1 = first
                x2, y2 = second
                if card_values[y1][x1] == card_values[y2][x2]:
                    card_states[y1][x1] = 2
                    card_states[y2][x2] = 2
                    matched_pairs += 1
                else:
                    card_states[y1][x1] = 0
                    card_states[y2][x2] = 0
                first = None
                second = None
                waiting = False
        screen.fill(WHITE)
        draw_board()
        if matched_pairs == (ROWS * COLS) // 2:
            win_text = font.render("You Win!", True, RED)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
