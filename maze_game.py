
import pygame
import sys

# Initialize pygame
pygame.init()

# Grid settings
GRID_SIZE = 10
CELL_SIZE = 50
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (180, 180, 180)

# Maze layout (0: empty, 1: wall, 2: start, 3: end)
MAZE = [
    [2,0,1,0,0,1,0,0,0,0],
    [1,0,1,0,1,1,0,1,1,0],
    [1,0,0,0,0,0,0,1,0,0],
    [1,1,1,1,1,1,0,1,0,1],
    [0,0,0,0,0,1,0,0,0,1],
    [0,1,1,1,0,1,1,1,0,1],
    [0,1,0,0,0,0,0,1,0,0],
    [0,1,0,1,1,1,0,1,1,0],
    [0,0,0,1,0,0,0,0,1,0],
    [1,1,0,1,0,1,1,0,1,3],
]

# Find start position
def find_start():
    for y, row in enumerate(MAZE):
        for x, cell in enumerate(row):
            if cell == 2:
                return x, y
    return 0, 0

def draw_maze(player_pos):
    for y, row in enumerate(MAZE):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == 1:
                pygame.draw.rect(screen, BLACK, rect)
            elif cell == 2:
                pygame.draw.rect(screen, GREEN, rect)
            elif cell == 3:
                pygame.draw.rect(screen, RED, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)
    # Draw player
    px, py = player_pos
    prect = pygame.Rect(px*CELL_SIZE+8, py*CELL_SIZE+8, CELL_SIZE-16, CELL_SIZE-16)
    pygame.draw.ellipse(screen, BLUE, prect)

def main():
    player_x, player_y = find_start()
    clock = pygame.time.Clock()
    won = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not won:
                dx, dy = 0, 0
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_UP:
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                nx, ny = player_x + dx, player_y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if MAZE[ny][nx] != 1:
                        player_x, player_y = nx, ny
        screen.fill(WHITE)
        draw_maze((player_x, player_y))
        if MAZE[player_y][player_x] == 3:
            won = True
            font = pygame.font.SysFont(None, 48)
            text = font.render("You Win!", True, (0, 128, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 24))
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
