import pygame
import sys
import time
import random
import os

# Initialize pygame
pygame.init()

# Default screen settings (story mode)
STORY_WIDTH, STORY_HEIGHT = 800, 600

# Image directory (relative to this script)
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'yohassets')
MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sounds', 'music')
screen = pygame.display.set_mode((STORY_WIDTH, STORY_HEIGHT))
pygame.display.set_caption("Year of the Horse — Interactive Story with Games")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (180, 180, 180)
BLUE = (0, 120, 255)
BROWN = (139, 69, 19)

# Fontsco


FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts')
dandelion_path = os.path.join(FONT_DIR, 'Dandelion.otf')
averia_path = os.path.join(FONT_DIR, 'AveriaSerifLibre-Light.ttf')
lasiren_path = os.path.join(FONT_DIR, 'LaSiren.otf')
font = pygame.font.Font(averia_path, 36)
title_font = pygame.font.Font(lasiren_path, 64)
story_font = pygame.font.Font(averia_path, 28)
poet_font = pygame.font.Font(averia_path, 36)
poet_font_big = pygame.font.Font(averia_path, 56)
small_font = pygame.font.Font(averia_path, 32)
big_font = pygame.font.Font(averia_path, 48)

clock = pygame.time.Clock()


def resize_screen(width, height):
    global screen
    screen = pygame.display.set_mode((width, height))


def show_image(filename):
    """Display an image centered on screen. Press SPACE to continue."""
    path = os.path.join(IMAGE_DIR, filename)
    img = pygame.image.load(path).convert_alpha()
    w, h = screen.get_size()
    # Scale image to fit within the screen with some margin
    max_w, max_h = w - 60, h - 100
    iw, ih = img.get_size()
    scale = min(max_w / iw, max_h / ih, 1.0)
    if scale < 1.0:
        img = pygame.transform.smoothscale(img, (int(iw * scale), int(ih * scale)))
    iw, ih = img.get_size()
    screen.fill(WHITE)
    screen.blit(img, (w // 2 - iw // 2, h // 2 - ih // 2 - 20))
    prompt = small_font.render("Press SPACE to continue.", True, BLACK)
    screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h - 50))
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})


# ─── Story helper functions ───────────────────────────────────────────────────

def wrap_text(text, max_width, text_font):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if text_font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def draw_wrapped_text(text, y, text_font=None, x=50, max_width=700, line_gap=40):
    if text_font is None:
        text_font = font
    wrapped_lines = []
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            wrapped_lines.append("")
            continue
        wrapped_lines.extend(wrap_text(paragraph, max_width, text_font))
    for i, line in enumerate(wrapped_lines):
        rendered = text_font.render(line, True, BLACK)
        screen.blit(rendered, (x, y + i * line_gap))


def wait_for_key(valid_keys):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in valid_keys:
                return


def show_title_card(title):
    w, h = screen.get_size()
    screen.fill(WHITE)
    rendered = title_font.render(title, True, BLACK)
    screen.blit(
        rendered,
        (w // 2 - rendered.get_width() // 2, h // 2 - rendered.get_height() // 2),
    )
    prompt = font.render("Press SPACE to continue.", True, BLACK)
    screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h - 90))
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})


def fade_to_white(duration=1000):
    """Fade the current screen contents to solid white."""
    snapshot = screen.copy()
    white = pygame.Surface(screen.get_size())
    white.fill((255, 255, 255))
    steps = 30
    for i in range(1, steps + 1):
        screen.blit(snapshot, (0, 0))
        white.set_alpha(int(255 * i / steps))
        screen.blit(white, (0, 0))
        pygame.display.flip()
        pygame.time.wait(duration // steps)


def show_paragraphs_over_image(paragraphs, bg_filename):
    """Show paragraphs one at a time over a background image. SPACE advances."""
    w, h = screen.get_size()
    path = os.path.join(IMAGE_DIR, bg_filename)
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.smoothscale(bg, (w, h))
    # Semi-transparent dark overlay for readability
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))

    margin_x = 120  # Increased margin for narrower text box
    max_width = w - margin_x * 2
    line_gap = 36

    for para in paragraphs:
        screen.blit(bg, (0, 0))
        screen.blit(overlay, (0, 0))
        lines = wrap_text(para, max_width, story_font)
        total_h = len(lines) * line_gap
        start_y = h // 2 - total_h // 2
        for i, line in enumerate(lines):
            rendered = story_font.render(line, True, WHITE)
            line_x = w // 2 - rendered.get_width() // 2
            screen.blit(rendered, (line_x, start_y + i * line_gap))
        prompt = small_font.render("Press SPACE to continue.", True, (200, 200, 200))
        screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h - 45))
        pygame.display.flip()
        wait_for_key({pygame.K_SPACE})


# ─── Story segments ──────────────────────────────────────────────────────────

def intro():
    show_paragraphs_over_image([
        "Welcome to the Interactive Story!",
    ], 'tent.png')


def story_segment_1():
    show_paragraphs_over_image([
        "You feel the hot sun on your face, warm and inviting. You stretch a tentative limb out "
        "of your sleeping bag, prying your eyelids open. It smells like rain. Mom isn't in the "
        "tent, how strange.. Looking around, it seems as if her things aren't thrown around the "
        "groundsheet like they were last night. You call out, confident she is just beyond the thin "
        "sheet of nylon. When no response comes, you unzip the flap and take a peak outside. Her old "
        "white car is gone, its left pieces of rust behind, and deep tire marks in the mud. Mom is "
        "gone, but perhaps she'll come back. You can wait.",
    ], 'tent.png')


    # Show warbler title card with warbler.png as background
    w, h = screen.get_size()
    path = os.path.join(IMAGE_DIR, 'warbler.png')
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.smoothscale(bg, (w, h))
    screen.blit(bg, (0, 0))
    rendered = title_font.render("The Warbler", True, WHITE)
    screen.blit(rendered, (w // 2 - rendered.get_width() // 2, h // 2 - rendered.get_height() // 2))
    prompt = font.render("Press SPACE to continue.", True, WHITE)
    screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h - 90))
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

    show_paragraphs_over_image([
        "As you sit cross legged at the foot of a large elm tree, a warbler lands just above your "
        "head. You feel as if he's looking at you, playfully tilting his head. You are beyond "
        "surprised when the warbler begins to sing, and you begin to understand him…",
        "\u201cWhat are you waiting for?\u201d he asks, he sounds eager and excited. "
        "\u201cIt's a beautiful day, no use in sitting around.\u201d",
        "\u201cI'm waiting for Mom\u201d you reply, looking longingly back towards your tent, and the "
        "empty spot where her car was last night.",
        "\u201cI've waited before. But I find I'm quite impatient. Have you tried going to search "
        "for her? Maybe she's waiting for you!\u201d he offers.",
        "\u201cI haven't. I'm not sure I'd be able to find my way back…\u201d",
        "\u201cSometimes we spend our whole lives waiting, and only when we reach the end do we "
        "realize our mistake \u2013 life is out there-\u201d he points his wings out generally towards the woods "
        "\u201cyou'll only find it if you take the risk. You know what they say, the early bird gets the worm.\u201d",
        "You think over the Warbler's advice carefully. He's right, sometimes action needs to be taken. "
        "But on the other hand, Mom always told you not to wander off…",
        "How often does a bird speak? Doesn't the significance of this magical moment mean the advice given to you by the Warbler should be heeded?",
        "You stand, wobbly in your yellow rainboots. You look at the woods that surround you, considering which direction would be most fruitful. "
        "You remember the river was towards the rising sun, so you begin to put one foot after the other.",
    ], 'warbler.png')


def story_segment_2():

    # Show beaver title card with beaver.png as background
    w, h = screen.get_size()
    path = os.path.join(IMAGE_DIR, 'beaver.png')
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.smoothscale(bg, (w, h))
    screen.blit(bg, (0, 0))
    rendered = title_font.render("The Beaver", True, WHITE)
    screen.blit(rendered, (w // 2 - rendered.get_width() // 2, h // 2 - rendered.get_height() // 2))
    prompt = font.render("Press SPACE to continue.", True, WHITE)
    screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h - 90))
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

    show_paragraphs_over_image([
        "You can hear the faint sound of rushing water, but before you can lay eyes on the river, you notice a very large tree in the verge of falling over. "
        "Gnaw marks have eaten away the trunk into a point at one end, how curious…",
        '"Admiring my work?" you hear a voice ask. A head, peeking out from behind the trunk, stares at you proudly.',
        '"Oh! Yes, it\'s… lovely." You return, looking at the beaver. His teeth are very large, and as result, he has a lisp.',
        '"I\'ve been gnawing away at this big oak tree for a week now. I\'ve been laughed at and ridiculed by my woodland peers, but I know that reaching one\'s goals isn\'t easy." '
        'He stands now, admiring his own work with his hands on his… hips?',
        '"that\'s a nice thought…" You nod politely, looking towards the sound of the river, hinting to the beaver that you\'d like to be moving along.',
        '"Trust me, you will face large obstacles in life, and they will feel insurmountable, but a breakthrough is always possible." He looks at his handy \u2013 or toothy - work and turns back to look at you. '
        '"The next time you walk through this clearing, this will be but a stump."',
    ], 'beaver.png')

    show_paragraphs_over_image([
        "Finally, you find the river. It's wider than you remember, and it looks very cold this morning. "
        "You stand, with your toes a mere meter away from the rushing water. You recall the beaver's advice and decide this is one of those moments where a breakthrough must be made.",
        "You look to your left, and then your right, as if crossing a road. At this moment, you're wishing the beaver had built his damn right here. "
        "But in the distance, you notice a curved tree stretching over the water, like its reaching for the bank on the other side.",
        "You've climbed trees before. They were smaller, and more approachable, and not suspended over a river… but still, all it would take was a hop, skip, and a jump!",
    ], 'river.png')


def post_game_2_text():
    show_paragraphs_over_image([
        "You make it to the base of the tree, digging your heels into the dirt. You reach out and latch onto a branch and begin your ascent.",
        "Finally, you are at the edge of the curving tree, you take a deep, brave breath, and launch yourself towards the riverbank. You made it!",
    ], 'river.png')


def story_segment_3():

    # Show fox title card with fox.png as background
    w, h = screen.get_size()
    path = os.path.join(IMAGE_DIR, 'fox.png')
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.smoothscale(bg, (w, h))
    screen.blit(bg, (0, 0))
    rendered = title_font.render("The Fox", True, WHITE)
    screen.blit(rendered, (w // 2 - rendered.get_width() // 2, h // 2 - rendered.get_height() // 2))
    prompt = font.render("Press SPACE to continue.", True, WHITE)
    screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h - 90))
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

    show_paragraphs_over_image([
        "As you stand up, finding your footing once more, you realize you're tired, hungry, and sore. "
        "It's been a long day of walking, and you just want to sit down… As you let your eyelids close gently, and allow your head to lull to the side, you hear a rustle in the nearby leaves.",
        '"You are doing very well." A voice says. You startle awake, the fatigue leaving your body almost immediately.',
        '"You\'ve been following me?" You ask tentatively towards the bush.',
        '"Not following, we just happened to be moving in the same direction." It replies, finally emerging from the bush. A fox! How special, Mom always told you that a fox sighting symbolized adaptability and intelligence.',
        '"Okay, what do I do know?" You ask, believing Mom that this fox must be wise.',
        '"You keep going. Stagnancy is the antithesis of growth. If you want to become better and reach your desired outcome, you must continue to move forward."',
        'You stand up, searching the woods for some clear path. There is none. You turn back to the fox, she nods her head, "forge your own path."',
    ], 'fox.png')


def show_mole_title_card():
    w, h = screen.get_size()
    path = os.path.join(IMAGE_DIR, 'mole.png')
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.smoothscale(bg, (w, h))
    screen.blit(bg, (0, 0))
    rendered = title_font.render("The Mole", True, WHITE)
    screen.blit(rendered, (w // 2 - rendered.get_width() // 2, h // 2 - rendered.get_height() // 2))
    prompt = font.render("Press SPACE to continue.", True, WHITE)
    screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h - 90))
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

def story_segment_4():
    show_paragraphs_over_image([
        "Now covered in thorns and leaves, you are feeling exhausted. You can see a break in the tree line, but you can't find the will to keep moving your feet. Your boots feel so heavy, your hands feel so cold. As you continue to glance longingly to the break in the tree line, a mole pops out of the ground at your feet.",
        '"Oh, pardon me! Sometimes I have no idea where I\'ll breach the surface!" It says, patting your boot apologetically where it had careened into you.',
        '"No problem." You say, the exasperation coming through in your voice.',
        '"What\'s wrong?" It asks, turning back towards you. Evidently, it couldn\'t see you, but you surmised it must have been able to smell you.',
        '"Oh.. well. I guess I just can\'t find the strength to keep going. Every time it feels like my journey should be ending, a new challenge appears." You reply, crouching down to get closer to the mole.',
        '"Ahh. I know this dilemma well! Sometimes, I get away from myself and I dig far too deep into the soil. When I realize my mistake, I\'m so far underground and so tired, that finding the surface seems impossible, I dig, and I dig, and I dig, and it feels like I\'ll never reach the surface. The important part… I keep digging!" He exclaims, nose twitching. "Perseverance is about what you do in those moments where you can\'t see the light at the end of the tunnel. Do you stop, letting the cold soil surround you, or do you keep digging until your find the warm sun?"',
        'The mole waves goodbye, and burrows back into the ground. You stand up and begin to march towards that break in the treeline.',
    ], 'mole.png')

def story_segment_5():

    # Show horse title card with horse.png as background
    w, h = screen.get_size()
    path = os.path.join(IMAGE_DIR, 'horse.png')
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.smoothscale(bg, (w, h))
    screen.blit(bg, (0, 0))
    rendered = title_font.render("The Horse", True, WHITE)
    screen.blit(rendered, (w // 2 - rendered.get_width() // 2, h // 2 - rendered.get_height() // 2))
    prompt = font.render("Press SPACE to continue.", True, WHITE)
    screen.blit(prompt, (w // 2 - prompt.get_width() // 2, h - 90))
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

    show_paragraphs_over_image([
        "It's a field of long, soft grass, a pasture. The field is painted with the soft warm glow of the setting sun, and you see a farmhouse in the distance. "
        "You walk through the grass, dancing your fingers through it as you breathe in the evening air. You close your eyes, seeing the light come through your eyelids magnificently.",
    ], 'horse.png')

    show_paragraphs_over_image([
        '"Well done, Artemis." Your eyes open, you stop in your tracks. A big horse with long flowing blonde hair stands in front of you. She looks like she\'s on fire, but it\'s just the sunlight.',
        '"How did you know my name?" You ask, amazed that an animal so beautiful would ever concern herself with the likes of you.',
        '"Artemis, we\'ve been waiting for you!" She laughs, her tail swishing gently. "You\'ve been very brave so far, and I admire how you take advice in stride. But now, you must confront the most difficult of challenges." She adds.',
        'You lower your head with dread, you thought it was over.',
        '"You have to ask for help." She says, playfully nudging you on your shoulder with her head. "In that house over there-" she nods to the farmhouse, "there is a kind, old couple. They\'ve taken very good care of me over the years, and I have no doubt they will make sure you get home."',
        '"I just want my Mom." You squeak out.',
        '"Yes, I understand, Artemis. However, I\'ve learned in my time on this earth that it takes more than a mother, or a friend, to get through life. It takes a herd \u2013 others who have your back and whom you can rely on to be beside you, rain or shine."',
    ], 'horse.png')


def pre_final_game_text():
    show_paragraphs_over_image([
        "You approach the farmhouse, a cold wind now pulling at your hair. You reach to knock on the door.",
    ], 'house.png')
    draw_wrapped_text("Press SPACE to begin the final game.", 520)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})


def ending():
    w, h = screen.get_size()
    path = os.path.join(IMAGE_DIR, 'house.png')
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.smoothscale(bg, (w, h))
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(bg, (0, 0))
    screen.blit(overlay, (0, 0))
    msg = story_font.render("Thanks for playing the interactive story!", True, WHITE)
    screen.blit(msg, (w // 2 - msg.get_width() // 2, h // 2 - 30))
    quit_msg = small_font.render("Press ESC to quit.", True, (200, 200, 200))
    screen.blit(quit_msg, (w // 2 - quit_msg.get_width() // 2, h // 2 + 20))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


# ─── Game 1: Maze Game ───────────────────────────────────────────────────────

def run_maze_game():

    GRID_SIZE = 7
    # Dynamically calculate cell size to maximize maze area (with some margin)
    max_maze_width = STORY_WIDTH - 40
    max_maze_height = STORY_HEIGHT - 40
    CELL_SIZE = min(max_maze_width // GRID_SIZE, max_maze_height // GRID_SIZE)
    MAZE_W, MAZE_H = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
    OX = (STORY_WIDTH - MAZE_W) // 2
    OY = (STORY_HEIGHT - MAZE_H) // 2

    # Load maze asset images
    ASSET_DIR = os.path.join(IMAGE_DIR, 'mazeassets')
    clear_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, 'clear.png')).convert_alpha(),
        (CELL_SIZE, CELL_SIZE))
    start_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, 'start.png')).convert_alpha(),
        (CELL_SIZE, CELL_SIZE))
    finish_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, 'finish.png')).convert_alpha(),
        (CELL_SIZE, CELL_SIZE))
    tent_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, 'tentob_.png')).convert_alpha(),
        (CELL_SIZE * 2, CELL_SIZE * 2))
    tree_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, 'treeob_.png')).convert_alpha(),
        (CELL_SIZE * 2, CELL_SIZE * 2))
    artemiswalking_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, 'artemiswalking.png')).convert_alpha(),
        (CELL_SIZE - 8, CELL_SIZE - 8)) # Player sprite for blue dot

    obstacle_names = ['bushob_.png', 'flowersob_.png', 'puddleob.png',
                      'trunkob_.png', 'trunkob2.png', 'twigsob.png']
    obstacle_imgs = []
    for name in obstacle_names:
        img = pygame.transform.smoothscale(
            pygame.image.load(os.path.join(ASSET_DIR, name)).convert_alpha(),
            (CELL_SIZE, CELL_SIZE))
        obstacle_imgs.append(img)

    # Maze layout: 0=path, 1=wall, 2=start, 3=end
    # Top-right 2x2 reserved for tent, tree placed as 2x2 block too
    MAZE = [
        [2, 0, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 3],
    ]

    # Tent occupies top-right 2x2: cells (5,0),(6,0),(5,1),(6,1)
    TENT_CELLS = {(5, 0), (6, 0), (5, 1), (6, 1)}
    TENT_ORIGIN = (5, 0)

    # Find a 2x2 wall block for the tree (not overlapping tent)
    TREE_CELLS = set()
    TREE_ORIGIN = None
    for ty in range(GRID_SIZE - 1):
        for tx in range(GRID_SIZE - 1):
            cells = {(tx, ty), (tx+1, ty), (tx, ty+1), (tx+1, ty+1)}
            if cells & TENT_CELLS:
                continue
            if all(MAZE[cy][cx] == 1 for cx, cy in cells):
                TREE_ORIGIN = (tx, ty)
                TREE_CELLS = cells
                break
        if TREE_ORIGIN:
            break

    # Assign random obstacle images + rotations to remaining wall cells
    wall_img_map = {}
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if MAZE[y][x] == 1 and (x, y) not in TENT_CELLS and (x, y) not in TREE_CELLS:
                img = random.choice(obstacle_imgs)
                rot = random.choice([0, 90, 180, 270])
                wall_img_map[(x, y)] = pygame.transform.rotate(img, rot)

    def find_start():
        for y, row in enumerate(MAZE):
            for x, cell in enumerate(row):
                if cell == 2:
                    return x, y
        return 0, 0

    def draw_maze(player_pos):
        # Draw path / start / end cells
        for y, row in enumerate(MAZE):
            for x, cell in enumerate(row):
                rx = OX + x * CELL_SIZE
                ry = OY + y * CELL_SIZE
                if cell == 2:
                    screen.blit(start_img, (rx, ry))
                elif cell == 3:
                    screen.blit(finish_img, (rx, ry))
                elif cell == 0:
                    screen.blit(clear_img, (rx, ry))

        # Draw wall cells (obstacles)
        for (x, y), img in wall_img_map.items():
            screen.blit(img, (OX + x * CELL_SIZE, OY + y * CELL_SIZE))

        # Draw tent (2x2)
        tx, ty = TENT_ORIGIN
        screen.blit(tent_img, (OX + tx * CELL_SIZE, OY + ty * CELL_SIZE))

        # Draw tree (2x2)
        if TREE_ORIGIN:
            tx2, ty2 = TREE_ORIGIN
            screen.blit(tree_img, (OX + tx2 * CELL_SIZE, OY + ty2 * CELL_SIZE))

        # Draw player (artemiswalking.png, centered in cell)
        px, py = player_pos
        px_pix = OX + px * CELL_SIZE + (CELL_SIZE - artemiswalking_img.get_width()) // 2
        py_pix = OY + py * CELL_SIZE + (CELL_SIZE - artemiswalking_img.get_height()) // 2
        screen.blit(artemiswalking_img, (px_pix, py_pix))

    player_x, player_y = find_start()
    won = False
    running = True
    while running:
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
        pygame.display.flip()
        clock.tick(30)
        if won:
            fade_to_white()
            running = False


# ─── Game 2: Pair Matching Game ──────────────────────────────────────────────

def run_pair_matching_game():
    ROWS, COLS = 4, 4
    CARD_SIZE = 100
    GAP = 10
    BOARD_W = COLS * (CARD_SIZE + GAP) + GAP
    BOARD_H = ROWS * (CARD_SIZE + GAP) + GAP
    OX = (STORY_WIDTH - BOARD_W) // 2
    OY = (STORY_HEIGHT - BOARD_H) // 2

    # Load card images
    PAIR_DIR = os.path.join(IMAGE_DIR, 'pairassets')
    backcard_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(PAIR_DIR, 'backcard_.png')).convert_alpha(),
        (CARD_SIZE, CARD_SIZE))
    correct_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(PAIR_DIR, 'correct.png')).convert_alpha(),
        (CARD_SIZE, CARD_SIZE))
    incorrect_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(PAIR_DIR, 'incorrect.png')).convert_alpha(),
        (CARD_SIZE, CARD_SIZE))

    face_names = ['twig1.png', 'twig2.png', 'rock.png', 'flower1.png',
                  'flower2.png', 'leaf1.png', 'leaf2.png', 'butterfly.png']
    face_imgs = {}
    for i, name in enumerate(face_names):
        img = pygame.transform.smoothscale(
            pygame.image.load(os.path.join(PAIR_DIR, name)).convert_alpha(),
            (CARD_SIZE, CARD_SIZE))
        face_imgs[i] = img

    # Each value 0-7 appears twice → 8 pairs for 16 cards
    values = list(range(8)) * 2
    random.shuffle(values)

    # States: 0=face-down, 1=face-up, 2=matched, 3=incorrect (briefly shown)
    card_states = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    card_values = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(ROWS * COLS):
        card_values[i // COLS][i % COLS] = values[i]

    def draw_board():
        for y in range(ROWS):
            for x in range(COLS):
                rx = OX + GAP + x * (CARD_SIZE + GAP)
                ry = OY + GAP + y * (CARD_SIZE + GAP)
                state = card_states[y][x]
                if state == 2:
                    screen.blit(correct_img, (rx, ry))
                    screen.blit(face_imgs[card_values[y][x]], (rx, ry))
                elif state == 1:
                    screen.blit(face_imgs[card_values[y][x]], (rx, ry))
                elif state == 3:
                    screen.blit(incorrect_img, (rx, ry))
                else:
                    screen.blit(backcard_img, (rx, ry))

    def get_card_at_pos(pos):
        mx, my = pos
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(OX + GAP + x * (CARD_SIZE + GAP), OY + GAP + y * (CARD_SIZE + GAP), CARD_SIZE, CARD_SIZE)
                if rect.collidepoint(mx, my):
                    return x, y
        return None, None

    first = None
    second = None
    matched_pairs = 0
    running = True
    waiting = False
    wait_time = 0
    incorrect_shown = False
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
                        incorrect_shown = False
        if waiting:
            elapsed = pygame.time.get_ticks() - wait_time
            x1, y1 = first
            x2, y2 = second
            if elapsed > 800:
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
            elif elapsed > 400 and not incorrect_shown:
                if card_values[y1][x1] != card_values[y2][x2]:
                    card_states[y1][x1] = 3
                    card_states[y2][x2] = 3
                    incorrect_shown = True
        screen.fill(WHITE)
        draw_board()
        if matched_pairs == (ROWS * COLS) // 2:
            pygame.display.flip()
            fade_to_white()
            running = False
            continue
        pygame.display.flip()
        clock.tick(30)


# ─── Game 3: Clicker Bar Game ────────────────────────────────────────────────

def run_clicker_bar_game():
    W, H = STORY_WIDTH, STORY_HEIGHT

    # Load clicker images
    CLICKER_DIR = os.path.join(IMAGE_DIR, 'clickerassets')
    bar_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(CLICKER_DIR, 'bar.png')).convert_alpha(), (W, H))
    green_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(CLICKER_DIR, 'green.png')).convert_alpha(), (W, H))
    FINGER_SIZE = 60
    finger_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(CLICKER_DIR, 'finger.png')).convert_alpha(),
        (FINGER_SIZE, FINGER_SIZE))

    # Fox background (not blurred)
    fox_bg = pygame.image.load(os.path.join(IMAGE_DIR, 'fox.png')).convert()
    fox_bg = pygame.transform.smoothscale(fox_bg, (W, H))

    BAR_LEFT = 0.08
    BAR_RIGHT = 0.92
    BAR_CENTER_Y = H // 2
    GREEN_ZONE_START = 0.35
    GREEN_ZONE_END = 0.65

    pointer_pos = 0.5
    velocity = 0.0
    CLICK_POWER = 0.04
    FRICTION = 0.008

    def pointer_to_screen_x(p):
        return int((BAR_LEFT + p * (BAR_RIGHT - BAR_LEFT)) * W)

    def draw_bar(pointer):
        screen.blit(bar_img, (0, 0))
        screen.blit(green_img, (0, 0))
        px = pointer_to_screen_x(pointer) - FINGER_SIZE // 2
        py = BAR_CENTER_Y - FINGER_SIZE // 2
        screen.blit(finger_img, (px, py))

    def in_green_zone(pointer):
        return GREEN_ZONE_START <= pointer <= GREEN_ZONE_END

    game_over = False
    win = False
    time_in_zone = 0
    required_time = 5
    restart_pressed = False
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_over and event.key == pygame.K_SPACE:
                    velocity += CLICK_POWER
                if game_over and not win and event.key == pygame.K_r:
                    restart_pressed = True
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                velocity += CLICK_POWER

        if restart_pressed:
            pointer_pos = 0.5
            velocity = 0.0
            game_over = False
            win = False
            time_in_zone = 0
            restart_pressed = False
            continue

        if not game_over:
            if velocity > 0:
                velocity -= FRICTION
                if velocity < 0:
                    velocity = 0
            elif velocity < 0:
                velocity += FRICTION
                if velocity > 0:
                    velocity = 0

            pointer_pos -= 0.25 * dt
            pointer_pos += velocity
            pointer_pos = max(0.0, min(1.0, pointer_pos))

            if in_green_zone(pointer_pos):
                time_in_zone += dt
                if time_in_zone >= required_time:
                    win = True
                    game_over = True
            else:
                time_in_zone = max(0, time_in_zone - dt * 0.5)

        screen.blit(fox_bg, (0, 0))
        draw_bar(pointer_pos)
        remaining = max(0, int(required_time - time_in_zone))
        if game_over:
            if win:
                pygame.display.flip()
                fade_to_white()
                running = False
                continue
            else:
                msg = font.render("Game Over! Press R to retry.", True, RED)
                screen.blit(msg, (W // 2 - msg.get_width() // 2, BAR_CENTER_Y - 120))
        else:
            info = font.render(f"Stay in green: {remaining}s", True, WHITE)
            screen.blit(info, (W // 2 - info.get_width() // 2, BAR_CENTER_Y - 120))
        pygame.display.flip()


# ─── Game 4: Runner Game ─────────────────────────────────────────────────────

def run_runner_game():
    W, H = STORY_WIDTH, STORY_HEIGHT

    # Load runner assets
    RUNNER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'yohassets', 'runnerassets')
    RUNNER_ASSETS = os.path.join(RUNNER_DIR, 'betterassets')

    bg_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(RUNNER_DIR, 'background_.png')).convert(), (W, H))
    ground_img_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'ground_.png')).convert_alpha()
    canopy_img_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'canopy.png')).convert_alpha()

    GROUND_HEIGHT = 120
    CANOPY_HEIGHT = 280

    ground_img = pygame.transform.smoothscale(ground_img_raw, (W, GROUND_HEIGHT))
    canopy_img = pygame.transform.smoothscale(canopy_img_raw, (W, CANOPY_HEIGHT))

    GROUND_Y = H - GROUND_HEIGHT - 80  # player stands on top of ground strip

    # Helper to scale preserving aspect ratio
    def scale_to_height(img, h):
        iw, ih = img.get_size()
        w2 = int(iw * h / ih)
        return pygame.transform.smoothscale(img, (w2, h))

    PLAYER_HEIGHT = 150
    PLAYER_X = 100
    JUMP_VEL = -18
    GRAVITY = 1
    SLIDE_TIME = 30

    # Player sprites — scale to height, preserving aspect ratio
    run1_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'run1.png')).convert_alpha()
    run2_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'run2.png')).convert_alpha()
    jump_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'jump.png')).convert_alpha()
    slide_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'slide.png')).convert_alpha()

    run1_img = scale_to_height(run1_raw, PLAYER_HEIGHT)
    run2_img = scale_to_height(run2_raw, PLAYER_HEIGHT)
    jump_img = scale_to_height(jump_raw, PLAYER_HEIGHT)
    PLAYER_WIDTH = run1_img.get_width()

    SLIDE_HEIGHT = 100
    slide_img = scale_to_height(slide_raw, SLIDE_HEIGHT)
    SLIDE_WIDTH = slide_img.get_width()

    # Obstacle images — scale log to appropriate size
    log_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'log.png')).convert_alpha()
    log_img = scale_to_height(log_raw, 90)
    LOG_W = log_img.get_width()
    LOG_H = 90

    # Vine and branch — spawn from original canopy-bottom line, independent of canopy visual size
    OBS_SPAWN_Y = 200  # where obstacles hang from (original canopy bottom)
    OBS_HIGH_H = GROUND_Y + 20 - OBS_SPAWN_Y  # down to just below player head
    vine_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'vine.png')).convert_alpha()
    branch_raw = pygame.image.load(os.path.join(RUNNER_ASSETS, 'branch.png')).convert_alpha()
    vine_img = scale_to_height(vine_raw, OBS_HIGH_H)
    branch_img = scale_to_height(branch_raw, OBS_HIGH_H)

    OBSTACLE_SPEED = 8
    SPAWN_INTERVAL = 60

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
            self.anim_frame = 0
            self.anim_counter = 0

        def update(self):
            if self.jumping:
                self.y += self.vel_y
                self.vel_y += GRAVITY
                if self.y >= GROUND_Y:
                    self.y = GROUND_Y
                    self.jumping = False
                    self.vel_y = 0
            # Slide while S is held
            keys = pygame.key.get_pressed()
            if not self.jumping:
                self.sliding = keys[pygame.K_s]
            else:
                self.sliding = False
            # Cycle run animation
            self.anim_counter += 1
            if self.anim_counter >= 8:
                self.anim_counter = 0
                self.anim_frame = 1 - self.anim_frame

        def jump(self):
            if not self.jumping and not self.sliding:
                self.jumping = True
                self.vel_y = JUMP_VEL

        def slide(self):
            pass  # sliding now handled via key state in update()

        def rect(self):
            inset_x = 35
            inset_y = 15
            if self.sliding:
                return pygame.Rect(self.x + inset_x, self.y + (self.height - SLIDE_HEIGHT) + inset_y,
                                   self.width - inset_x * 2, SLIDE_HEIGHT - inset_y * 2)
            else:
                return pygame.Rect(self.x + inset_x, self.y + inset_y,
                                   self.width - inset_x * 2, self.height - inset_y * 2)

        def draw(self, surface):
            if self.jumping:
                surface.blit(jump_img, (self.x, self.y))
            elif self.sliding:
                surface.blit(slide_img, (self.x, self.y + (self.height - SLIDE_HEIGHT)))
            else:
                img = run1_img if self.anim_frame == 0 else run2_img
                surface.blit(img, (self.x, self.y))

    class Obstacle:
        def __init__(self, kind):
            self.kind = kind  # 'low' = log (jump over), 'high' = vine/branch (duck under)
            self.x = W
            if kind == 'low':
                self.img = log_img
                self.width = LOG_W
                self.height = LOG_H
                self.y = GROUND_Y + PLAYER_HEIGHT - LOG_H
            else:
                self.subkind = random.choice(['vine', 'branch'])
                self.img = vine_img if self.subkind == 'vine' else branch_img
                self.width = self.img.get_width()
                self.height = self.img.get_height()
                # Position so top aligns with obstacle spawn line
                self.y = OBS_SPAWN_Y
            self.passed = False

        def update(self):
            self.x -= OBSTACLE_SPEED

        def rect(self):
            if self.kind == 'high':
                box_w = self.width // 5
                danger_h = 40
                if self.subkind == 'branch':
                    # Bottom-left corner of the image
                    box_x = self.x
                    box_y = self.y + self.height - danger_h
                else:
                    # Vine: center-bottom of the image
                    box_x = self.x + (self.width - box_w) // 2
                    box_y = self.y + self.height - danger_h
                return pygame.Rect(box_x, box_y, box_w, danger_h)
            else:
                # Log: centered on the image
                inset_x = self.width // 6
                inset_y = self.height // 3
                return pygame.Rect(self.x + inset_x, self.y + inset_y,
                                   self.width - inset_x * 2, self.height - inset_y * 2)

        def draw(self, surface):
            surface.blit(self.img, (self.x, self.y))

    # --- Instruction screen ---
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        screen.blit(bg_img, (0, 0))
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        lines = ["W  -  Jump", "S  -  Slide", "", "Press SPACE to start"]
        for i, line in enumerate(lines):
            txt = font.render(line, True, (255, 255, 255))
            screen.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 - 60 + i * 40))
        pygame.display.flip()

    player = Player()
    obstacles = []
    frame_count = 0
    score = 0
    game_over = False
    win = False
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_w:
                        player.jump()
                else:
                    if event.key == pygame.K_r:
                        player = Player()
                        obstacles = []
                        frame_count = 0
                        score = 0
                        game_over = False
                        win = False

        if not game_over:
            player.update()
            if frame_count % SPAWN_INTERVAL == 0:
                # Only spawn if last obstacle is far enough away
                can_spawn = True
                if obstacles:
                    last = obstacles[-1]
                    if last.x > W - 500:
                        can_spawn = False
                if can_spawn:
                    kind = random.choice(['low', 'high'])
                    obstacles.append(Obstacle(kind))
            for obs in obstacles:
                obs.update()
            obstacles = [obs for obs in obstacles if obs.x + obs.width > 0]
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

        # Draw background
        screen.blit(bg_img, (0, 0))
        # Draw ground strip
        screen.blit(ground_img, (0, H - GROUND_HEIGHT))
        # Draw player and obstacles
        player.draw(screen)
        for obs in obstacles:
            obs.draw(screen)
        # Draw canopy AFTER obstacles so vines/branches disappear behind it
        screen.blit(canopy_img, (0, 0))
        # Center the score display as a single block, using Dandelion font
        dandelion_label = pygame.font.Font(dandelion_path, 64)
        dandelion_number = pygame.font.Font(dandelion_path, 56)
        label_surf = dandelion_label.render("Your Score Is", True, WHITE)
        number_surf = dandelion_number.render(str(score), True, WHITE)
        block_height = label_surf.get_height() + 10 + number_surf.get_height()
        block_y = CANOPY_HEIGHT // 2 - block_height // 2
        # Center both label and number horizontally
        label_x = W // 2 - label_surf.get_width() // 2
        number_x = W // 2 - number_surf.get_width() // 2
        screen.blit(label_surf, (label_x, block_y))
        screen.blit(number_surf, (number_x, block_y + label_surf.get_height() + 10))
        if game_over:
            if win:
                pygame.display.flip()
                fade_to_white()
                running = False
                continue
            else:
                msg = font.render("Game Over!", True, RED)
                screen.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 - 40))
                restart_msg = font.render("Press R to Restart", True, WHITE)
                screen.blit(restart_msg, (W // 2 - restart_msg.get_width() // 2, H // 2 + 10))
        pygame.display.flip()


# ─── Game 5: Knock Sequence Game ─────────────────────────────────────────────

def run_knock_sequence_game():
    W, H = STORY_WIDTH, STORY_HEIGHT
    BTN_SIZE = 60
    BTN_GAP = 80
    BTN_OX = (W - (4 * BTN_GAP - (BTN_GAP - BTN_SIZE))) // 2
    BTN_OY = H // 2 - BTN_SIZE // 2
    YELLOW_LIGHT = (255, 245, 157)
    YELLOW_DARK = (180, 140, 20)
    YELLOW_ACTIVE = (230, 200, 80)

    MAX_LENGTH = 7
    KNOCK_KEYS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
    KNOCK_LABELS = ['A', 'S', 'D', 'F']

    # Load knock assets
    KNOCK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'yohassets', 'knockassets')
    door_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(KNOCK_DIR, 'door.png')).convert(), (W, H))
    FIST_W, FIST_H = 350, 350
    FIST_X, FIST_Y = 30, H - FIST_H
    knock1_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(KNOCK_DIR, 'knock1.png')).convert_alpha(), (FIST_W, FIST_H))
    knock2_img = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(KNOCK_DIR, 'knock2.png')).convert_alpha(), (FIST_W, FIST_H))
    # Load door-opening animation frames
    open_frames = []
    frames_dir = os.path.join(KNOCK_DIR, 'open_frames')
    for i in range(11):
        frame = pygame.transform.smoothscale(
            pygame.image.load(os.path.join(frames_dir, f'frame_{i:02d}.png')).convert_alpha(), (W, H))
        open_frames.append(frame)

    # Load knock sounds
    SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sounds', 'knocking sounds')
    knock_sounds = [
        pygame.mixer.Sound(os.path.join(SOUNDS_DIR, f'knock{i}.mp3')) for i in range(1, 5)
    ]

    def draw_bg(knocking=False):
        screen.blit(door_img, (0, 0))
        screen.blit(knock1_img if knocking else knock2_img, (FIST_X, FIST_Y))

    def draw_buttons():
        lasiren_label_font = pygame.font.Font(lasiren_path, 32)
        for i in range(4):
            pygame.draw.rect(screen, YELLOW_LIGHT, (BTN_OX + i * BTN_GAP, BTN_OY, BTN_SIZE, BTN_SIZE))
            label = lasiren_label_font.render(KNOCK_LABELS[i], True, YELLOW_DARK)
            screen.blit(label, (BTN_OX + i * BTN_GAP + BTN_SIZE // 2 - label.get_width() // 2, BTN_OY + BTN_SIZE // 2 - label.get_height() // 2))

    def play_sequence(seq):
        for idx in seq:
            knock_sounds[idx].play()
            draw_bg(knocking=True)
            draw_buttons()
            pygame.draw.rect(screen, YELLOW_ACTIVE, (BTN_OX + idx * BTN_GAP, BTN_OY, BTN_SIZE, BTN_SIZE))
            lasiren_label_font = pygame.font.Font(lasiren_path, 32)
            label = lasiren_label_font.render(KNOCK_LABELS[idx], True, YELLOW_DARK)
            screen.blit(label, (BTN_OX + idx * BTN_GAP + BTN_SIZE // 2 - label.get_width() // 2, BTN_OY + BTN_SIZE // 2 - label.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(400)
            draw_bg(knocking=False)
            draw_buttons()
            pygame.display.flip()
            pygame.time.wait(200)

    # Build the full 7-knock sequence up front; reveal one more each round
    full_sequence = [random.randint(0, 3) for _ in range(MAX_LENGTH)]
    current_length = 1
    sequence = full_sequence[:current_length]
    user_input = []
    showing = True
    win = False
    lose = False
    running = True
    while running:
        draw_bg(knocking=False)
        draw_buttons()
        progress_text = small_font.render(f"Progress: {current_length}/{MAX_LENGTH}", True, WHITE)
        if showing:
            info = small_font.render("Listen to the knocks...", True, WHITE)
            screen.blit(info, (W // 2 - info.get_width() // 2, 80))
            screen.blit(progress_text, (W // 2 - progress_text.get_width() // 2, 120))
            pygame.display.flip()
            pygame.time.wait(1000)
            play_sequence(sequence)
            pygame.event.clear()
            showing = False
            continue
        if win:
            msg = big_font.render("You Gained Entry!", True, GREEN)
            screen.blit(msg, (W // 2 - msg.get_width() // 2, 60))
            screen.blit(progress_text, (W // 2 - progress_text.get_width() // 2, 120))
        elif lose:
            msg = big_font.render("Wrong! Press R to retry.", True, RED)
            screen.blit(msg, (W // 2 - msg.get_width() // 2, 60))
            screen.blit(progress_text, (W // 2 - progress_text.get_width() // 2, 120))
        else:
            info = small_font.render("Repeat the sequence!", True, WHITE)
            screen.blit(info, (W // 2 - info.get_width() // 2, 80))
            screen.blit(progress_text, (W // 2 - progress_text.get_width() // 2, 120))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not (win or showing):
                if lose and event.key == pygame.K_r:
                    full_sequence = [random.randint(0, 3) for _ in range(MAX_LENGTH)]
                    current_length = 1
                    sequence = full_sequence[:current_length]
                    user_input = []
                    showing = True
                    lose = False
                    pygame.event.clear()
                    continue
                if not lose and event.key in KNOCK_KEYS:
                    user_input.append(KNOCK_KEYS.index(event.key))
                    idx = KNOCK_KEYS.index(event.key)
                    knock_sounds[idx].play()
                    draw_bg(knocking=True)
                    draw_buttons()
                    pygame.draw.rect(screen, YELLOW_ACTIVE, (BTN_OX + idx * BTN_GAP, BTN_OY, BTN_SIZE, BTN_SIZE))
                    lasiren_label_font = pygame.font.Font(lasiren_path, 32)
                    label = lasiren_label_font.render(KNOCK_LABELS[idx], True, YELLOW_DARK)
                    screen.blit(label, (BTN_OX + idx * BTN_GAP + BTN_SIZE // 2 - label.get_width() // 2, BTN_OY + BTN_SIZE // 2 - label.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(200)
                    if user_input[-1] != sequence[len(user_input) - 1]:
                        lose = True
                    elif len(user_input) == len(sequence):
                        if current_length >= MAX_LENGTH:
                            win = True
                        else:
                            # Grow by one knock
                            current_length += 1
                            sequence = full_sequence[:current_length]
                            user_input = []
                            showing = True
        if win:
            # Play door-opening animation
            for frame in open_frames:
                screen.blit(frame, (0, 0))
                pygame.display.flip()
                pygame.time.wait(100)
            # Fade to white after door opens
            fade_to_white()
            running = False


# ─── Main story/game sequence ────────────────────────────────────────────────

def main():
    intro()

    # Story 1: The Warbler → Maze Game
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'ES_Early Morning Rain - Sunfish Grove.mp3'))
    pygame.mixer.music.play(-1)
    story_segment_1()
    run_maze_game()
    pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)

    # Story 2: The Beaver → Pair Matching Game
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'ES_Birdsong by the River - Center of Attention.mp3'))
    pygame.mixer.music.play(-1)
    story_segment_2()
    run_pair_matching_game()
    post_game_2_text()


    # Story 3: The Fox → Clicker Bar Game
    story_segment_3()
    run_clicker_bar_game()
    pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)

    # Show Mole title card after clicker game, before mole story text
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'ES_Escalation - Jon Bjork.mp3'))
    pygame.mixer.music.play(-1)
    show_mole_title_card()
    story_segment_4()
    run_runner_game()
    pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)

    # Story 5: The Horse → Knock Sequence Game
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'ES_Near Dawn - S.A. Karl.mp3'))
    pygame.mixer.music.play(-1)
    story_segment_5()
    pre_final_game_text()
    pygame.mixer.music.set_volume(0.15)
    run_knock_sequence_game()
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.fadeout(1000)

    # Ending
    ending()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', choices=['maze', 'pairs', 'clicker', 'runner', 'knock'],
                        help='Jump straight to a single game for testing')
    args = parser.parse_args()
    if args.test:
        {'maze': run_maze_game,
         'pairs': run_pair_matching_game,
         'clicker': run_clicker_bar_game,
         'runner': run_runner_game,
         'knock': run_knock_sequence_game}[args.test]()
        pygame.quit()
    else:
        main()
