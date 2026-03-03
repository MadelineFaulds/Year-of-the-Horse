import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Runner: Out of the Woods")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BROWN = (139, 69, 19)
BLUE = (0, 120, 255)

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 80
PLAYER_X = 100
GROUND_Y = HEIGHT - 80
JUMP_VEL = -15
GRAVITY = 1
SLIDE_HEIGHT = 40
SLIDE_TIME = 30  # frames

# Obstacle settings
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 70
OBSTACLE_LOW = GROUND_Y + PLAYER_HEIGHT - OBSTACLE_HEIGHT
OBSTACLE_HIGH = GROUND_Y + PLAYER_HEIGHT - 120
OBSTACLE_SPEED = 8
SPAWN_INTERVAL = 60  # frames

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = PLAYER_X
        self.y = GROUND_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_y = 0
        self.jumping = False
        self.sliding = False
        self.slide_timer = 0
    def update(self):
        if self.jumping:
            self.y += self.vel_y
            self.vel_y += GRAVITY
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.jumping = False
                self.vel_y = 0
        if self.sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.sliding = False
    def jump(self):
        if not self.jumping and not self.sliding:
            self.jumping = True
            self.vel_y = JUMP_VEL
    def slide(self):
        if not self.jumping and not self.sliding:
            self.sliding = True
            self.slide_timer = SLIDE_TIME
    def rect(self):
        if self.sliding:
            return pygame.Rect(self.x, self.y + (self.height - SLIDE_HEIGHT), self.width, SLIDE_HEIGHT)
        else:
            return pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self, surface):
        r = self.rect()
        pygame.draw.rect(surface, BLUE, r)

class Obstacle:
    def __init__(self, kind):
        self.kind = kind  # 'high' or 'low'
        self.x = WIDTH
        if kind == 'low':
            self.y = OBSTACLE_LOW
            self.height = OBSTACLE_HEIGHT
        else:
            self.y = OBSTACLE_HIGH
            self.height = 40
        self.width = OBSTACLE_WIDTH
        self.passed = False
    def update(self):
        self.x -= OBSTACLE_SPEED
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self, surface):
        pygame.draw.rect(surface, BROWN, self.rect())

def main():
    player = Player()
    obstacles = []
    frame_count = 0
    score = 0
    running = True
    game_over = False
    win = False
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        player.jump()
                    if event.key == pygame.K_DOWN:
                        player.slide()
                else:
                    # Restart game if 'R' is pressed
                    if event.key == pygame.K_r:
                        # Reset all game variables
                        player = Player()
                        obstacles = []
                        frame_count = 0
                        score = 0
                        game_over = False
                        win = False
        if not game_over:
            player.update()
            # Spawn obstacles
            if frame_count % SPAWN_INTERVAL == 0:
                kind = random.choice(['low', 'high'])
                obstacles.append(Obstacle(kind))
            # Update obstacles
            for obs in obstacles:
                obs.update()
            # Remove off-screen obstacles
            obstacles = [obs for obs in obstacles if obs.x + obs.width > 0]
            # Check collisions and scoring
            for obs in obstacles:
                if not obs.passed and obs.x + obs.width < player.x:
                    score += 5
                    obs.passed = True
                if player.rect().colliderect(obs.rect()) and not obs.passed:
                    game_over = True
            if score >= 100:
                win = True
                game_over = True
            frame_count += 1
        # Draw
        screen.fill(WHITE)
        # Draw ground
        pygame.draw.rect(screen, GREEN, (0, GROUND_Y + PLAYER_HEIGHT, WIDTH, HEIGHT - (GROUND_Y + PLAYER_HEIGHT)))
        # Draw player
        player.draw(screen)
        # Draw obstacles
        for obs in obstacles:
            obs.draw(screen)
        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        # Draw win/lose
        if game_over:
            if win:
                msg = font.render("You Escaped the Woods!", True, GREEN)
            else:
                msg = font.render("Game Over!", True, RED)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 80))
            restart_msg = font.render("Press R to Restart", True, BLACK)
            screen.blit(restart_msg, (WIDTH // 2 - restart_msg.get_width() // 2, 140))
        pygame.display.flip()

if __name__ == "__main__":
    main()
