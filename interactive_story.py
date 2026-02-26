
import pygame
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Story with Games")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 36)

def draw_text(text, y):
	lines = text.split('\n')
	for i, line in enumerate(lines):
		rendered = font.render(line, True, BLACK)
		screen.blit(rendered, (50, y + i * 40))

def intro():
	screen.fill(WHITE)
	draw_text("Welcome to the Interactive Story!\nPress SPACE to continue.", 200)
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				return

def story_segment(segment_number):
	screen.fill(WHITE)
	draw_text(f"[Story Segment {segment_number} goes here]\nPress SPACE to begin the game.", 200)
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				return

def ending():
	screen.fill(WHITE)
	draw_text("Thanks for playing the interactive story!\nPress ESC to quit.", 250)
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

def main():
	intro()
	# After each story segment, the game begins immediately.
	# After winning the game, the next story segment appears.
	story_segment(1)
	# --- First game call here ---
	# Wait for the player to win before continuing to the next segment.
	# e.g., guessing_game() or reaction_game()
	# (Insert game logic that blocks until the player wins)
	story_segment(2)
	# --- Second game call here ---
	# (Insert game logic that blocks until the player wins)
	story_segment(3)
	# --- Third game call here ---
	# (Insert game logic that blocks until the player wins)
	story_segment(4)
	# --- Fourth game call here ---
	# (Insert game logic that blocks until the player wins)
	story_segment(5)
	# --- Fifth game call here ---
	# (Insert game logic that blocks until the player wins)
	ending()

if __name__ == "__main__":
	main()
