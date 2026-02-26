import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker Bar Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (180, 180, 180)
BLUE = (0, 120, 255)

# Bar settings
BAR_X = 100
BAR_Y = 180
BAR_WIDTH = 400
BAR_HEIGHT = 40
GREEN_ZONE_START = 0.4  # 40% of bar
GREEN_ZONE_END = 0.6    # 60% of bar

# Pointer settings
pointer_pos = 0.5  # Start in the middle (0.0 to 1.0)
velocity = 0.0

# Game settings
CLICK_POWER = 0.04
FRICTION = 0.008

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def draw_bar(pointer):
    # Draw bar
    pygame.draw.rect(screen, GRAY, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT))
    # Draw green zone
    green_x = BAR_X + int(GREEN_ZONE_START * BAR_WIDTH)
    green_w = int((GREEN_ZONE_END - GREEN_ZONE_START) * BAR_WIDTH)
    pygame.draw.rect(screen, GREEN, (green_x, BAR_Y, green_w, BAR_HEIGHT))
    # Draw pointer
    px = BAR_X + int(pointer * BAR_WIDTH)
    pygame.draw.circle(screen, BLUE, (px, BAR_Y + BAR_HEIGHT // 2), 18)
    # Draw border
    pygame.draw.rect(screen, BLACK, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 2)

def in_green_zone(pointer):
    return GREEN_ZONE_START <= pointer <= GREEN_ZONE_END

def main():
    global pointer_pos, velocity
    running = True
    last_click = 0
    game_over = False
    win = False
    time_in_zone = 0
    required_time = 15  # seconds in green zone to win
    start_time = time.time()
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                velocity += CLICK_POWER
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    velocity += CLICK_POWER
        # Apply friction
        if velocity > 0:
            velocity -= FRICTION
            if velocity < 0:
                velocity = 0
        elif velocity < 0:
            velocity += FRICTION
            if velocity > 0:
                velocity = 0
        # Pointer moves left unless clicked
        pointer_pos -= 0.25 * dt
        pointer_pos += velocity
        pointer_pos = max(0.0, min(1.0, pointer_pos))
        # Lose if pointer leaves bar
        if not in_green_zone(pointer_pos):
            time_in_zone = 0
        else:
            time_in_zone += dt
            if time_in_zone >= required_time:
                win = True
                game_over = True
        if pointer_pos <= 0.0 or pointer_pos >= 1.0:
            game_over = True
        screen.fill(WHITE)
        draw_bar(pointer_pos)
        if game_over:
            if win:
                msg = font.render("You Win!", True, GREEN)
            else:
                msg = font.render("Game Over!", True, RED)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 80))
        else:
            info = font.render(f"Stay in green: {required_time - time_in_zone:.1f}s", True, BLACK)
            screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 80))
        pygame.display.flip()

if __name__ == "__main__":
    main()
