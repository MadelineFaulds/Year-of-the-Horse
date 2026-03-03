import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knock Sequence Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (180, 180, 180)

# Sounds
knock_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.get_init() and pygame.mixer.Sound(buffer=b'\x00'*1000) or None))
# replace above with a .wav file and load it for knock sound

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

SEQUENCE_LENGTH = 5
KNOCK_KEYS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
KNOCK_LABELS = ['A', 'S', 'D', 'F']


def play_sequence(seq):
    for idx in seq:
        pygame.draw.rect(screen, BLUE, (100 + idx*100, 150, 80, 80))
        label = font.render(KNOCK_LABELS[idx], True, WHITE)
        screen.blit(label, (100 + idx*100 + 25, 175))
        pygame.display.flip()
        knock_sound.play()
        pygame.time.wait(400)
        screen.fill(WHITE)
        draw_buttons()
        pygame.display.flip()
        pygame.time.wait(200)


def draw_buttons():
    for i in range(4):
        pygame.draw.rect(screen, GRAY, (100 + i*100, 150, 80, 80))
        label = font.render(KNOCK_LABELS[i], True, BLACK)
        screen.blit(label, (100 + i*100 + 25, 175))


def main():
    sequence = [random.randint(0, 3) for _ in range(SEQUENCE_LENGTH)]
    user_input = []
    step = 0
    showing = True
    win = False
    lose = False
    running = True
    while running:
        screen.fill(WHITE)
        draw_buttons()
        if showing:
            info = small_font.render("Listen to the knocks...", True, BLACK)
            screen.blit(info, (WIDTH//2 - info.get_width()//2, 80))
            pygame.display.flip()
            pygame.time.wait(800)
            play_sequence(sequence)
            showing = False
            continue
        if win:
            msg = font.render("You Gained Entry!", True, GREEN)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 60))
        elif lose:
            msg = font.render("Wrong Sequence!", True, RED)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 60))
        else:
            info = small_font.render("Repeat the sequence! (A S D F)", True, BLACK)
            screen.blit(info, (WIDTH//2 - info.get_width()//2, 80))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not (win or lose or showing):
                if event.key in KNOCK_KEYS:
                    user_input.append(KNOCK_KEYS.index(event.key))
                    idx = KNOCK_KEYS.index(event.key)
                    knock_sound.play()
                    # Visual feedback
                    pygame.draw.rect(screen, BLUE, (100 + idx*100, 150, 80, 80))
                    label = font.render(KNOCK_LABELS[idx], True, WHITE)
                    screen.blit(label, (100 + idx*100 + 25, 175))
                    pygame.display.flip()
                    pygame.time.wait(200)
                    if user_input[-1] != sequence[len(user_input)-1]:
                        lose = True
                    elif len(user_input) == len(sequence):
                        win = True
        if win or lose:
            pygame.time.wait(1500)
            running = False

if __name__ == "__main__":
    main()
