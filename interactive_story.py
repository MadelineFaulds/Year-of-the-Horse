
import pygame
import sys

# pygame
pygame.init()

# window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Story with Games")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fonts
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 64)


def wrap_text(text, max_width, text_font):
    # wrap
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


def draw_wrapped_text(text, y, text_font=font, x=50, max_width=700, line_gap=40):
    # draw
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
    # wait
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in valid_keys:
                return


def intro():
    # intro
    screen.fill(WHITE)
    draw_wrapped_text("Welcome to the Interactive Story!\nPress SPACE to continue.", 200)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})


def show_title_card(title):
    # title
    screen.fill(WHITE)
    rendered = title_font.render(title, True, BLACK)
    screen.blit(
        rendered,
        (WIDTH // 2 - rendered.get_width() // 2, HEIGHT // 2 - rendered.get_height() // 2),
    )
    prompt = font.render("Press SPACE to continue.", True, BLACK)
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 90))
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})


def story_segment_1():
    opening_text = (
        "You feel the hot sun on your face, warm and inviting. You stretch a tentative limb out "
        "of your sleeping bag, prying your eyelids open. It smells like rain. Mom isn’t in the "
        "tent, how strange.. Looking around, it seems as if her things aren’t thrown around the "
        "groundsheet like they were last night. You call out, confident she is just beyond the thin "
        "sheet of nylon. When no response comes, you unzip the flap and take a peak outside. Her old "
        "white car is gone, its left pieces of rust behind, and deep tire marks in the mud. Mom is "
        "gone, but perhaps she’ll come back. You can wait."
    )

    dialogue_text = (
        "As you sit cross legged at the foot of a large elm tree, a warbler lands just above your "
        "head. You feel as if he’s looking at you, playfully tilting his head. You are beyond "
        "surprised when the warbler begins to sing, and you begin to understand him…\n\n"
        "Warbler: “What are you waiting for?” he asks, he sounds eager and excited. "
        "“It’s a beautiful day, no use in sitting around.”\n\n"
        "You: “I’m waiting for Mom” you reply, looking longingly back towards your tent, and the "
        "empty spot where her car was last night.\n\n"
        "Warbler: “I’ve waited before. But I find I’m quite impatient. Have you tried going to search "
        "for her? Maybe she’s waiting for you!” he offers.\n\n"
        "You: “I haven’t. I’m not sure I’d be able to find my way back…”\n\n"
        "Warbler: “Sometimes we spend our whole lives waiting, and only when we reach the end do we "
        "realize our mistake – life is out there-“ he points his wings out generally towards the woods "
        "“you’ll only find it if you take the risk. You know what they say, the early bird gets the worm.”"
    )

    screen.fill(WHITE)
    draw_wrapped_text(opening_text, 60)
    draw_wrapped_text("Press SPACE to continue.", 540)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

    show_title_card("The Warbler")

    screen.fill(WHITE)
    draw_wrapped_text(dialogue_text, 40, line_gap=34)
    draw_wrapped_text("Press SPACE to continue.", 550)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

    # New reflection/decision text before game 1
    reflection_text = (
        "You think over the Warbler’s advice carefully. He’s right, sometimes action needs to be taken. "
        "But on the other hand, Mom always told you not to wander off…\n"
        "How often does a bird speak? Doesn’t the significance of this magical moment mean the advice given to you by the Warbler should be heeded?\n"
        "You stand, wobbly in your yellow rainboots. You look at the woods that surround you, considering which direction would be most fruitful. "
        "You remember the river was towards the rising sun, so you begin to put one foot after the other."
    )
    screen.fill(WHITE)
    draw_wrapped_text(reflection_text, 60)
    draw_wrapped_text("Press SPACE to begin the game.", 540)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})



def story_segment_2():
    # Title card
    show_title_card("The Beaver")

    # Dialogue
    dialogue = (
        "You can hear the faint sound of rushing water, but before you can lay eyes on the river, you notice a very large tree in the verge of falling over. "
        "Gnaw marks have eaten away the trunk into a point at one end, how curious…\n\n"
        '“Admiring my work?” you hear a voice ask. A head, peeking out from behind the trunk, stares at you proudly.\n\n'
        '“Oh! Yes, it’s… lovely.” You return, looking at the beaver. His teeth are very large, and as result, he has a lisp.\n\n'
        '“I’ve been gnawing away at this big oak tree for a week now. I’ve been laughed at and ridiculed by my woodland peers, but I know that reaching one’s goals isn’t easy.” '
        'He stands now, admiring his own work with his hands on his… hips?\n\n'
        '“that’s a nice thought…” You nod politely, looking towards the sound of the river, hinting to the beaver that you’d like to be moving along.\n\n'
        '“Trust me, you will face large obstacles in life, and they will feel insurmountable, but a breakthrough is always possible.” He looks at his handy – or toothy - work and turns back to look at you. '
        '“The next time you walk through this clearing, this will be but a stump.”'
    )
    screen.fill(WHITE)
    draw_wrapped_text(dialogue, 40, line_gap=34)
    draw_wrapped_text("Press SPACE to continue.", 550)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

    # Reflection/decision text before game 2
    reflection = (
        "Finally, you find the river. It’s wider than you remember, and it looks very cold this morning. "
        "You stand, with your toes a mere meter away from the rushing water. You recall the beaver’s advice and decide this is one of those moments where a breakthrough must be made.\n"
        "You look to your left, and then your right, as if crossing a road. At this moment, you’re wishing the beaver had built his damn right here. "
        "But in the distance, you notice a curved tree stretching over the water, like its reaching for the bank on the other side.\n"
        "You’ve climbed trees before. They were smaller, and more approachable, and not suspended over a river… but still, all it would take was a hop, skip, and a jump!"
    )
    screen.fill(WHITE)
    draw_wrapped_text(reflection, 60)
    draw_wrapped_text("Press SPACE to begin the game.", 540)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

def post_game_2_text():
    post_text = (
        "You make it to the base of the tree, digging your heels into the dirt. You reach out and latch onto a branch and begin your ascent.\n"
        "Finally, you are at the edge of the curving tree, you take a deep, brave breath, and launch yourself towards the riverbank. You made it!"
    )
    screen.fill(WHITE)
    draw_wrapped_text(post_text, 80)
    draw_wrapped_text("Press SPACE to continue.", 520)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})


def ending():
    screen.fill(WHITE)
    draw_wrapped_text("Thanks for playing the interactive story!\nPress ESC to quit.", 250)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


# Game launching helper 
import subprocess
def run_game(filename):
    # run
    subprocess.run(["python3", filename])

# Fox segment 
def story_segment_3():
    show_title_card("The Fox")
    dialogue = (
        "As you stand up, finding your footing once more, you realize you’re tired, hungry, and sore. "
        "It’s been a long day of walking, and you just want to sit down… As you let your eyelids close gently, and allow your head to lull to the side, you hear a rustle in the nearby leaves.\n\n"
        '“You are doing very well.” A voice says. You startle awake, the fatigue leaving your body almost immediately.\n\n'
        '“You’ve been following me?” You ask tentatively towards the bush.\n\n'
        '“Not following, we just happened to be moving in the same direction.” It replies, finally emerging from the bush. A fox! How special, Mom always told you that a fox sighting symbolized adaptability and intelligence.\n\n'
        '“Okay, what do I do know?” You ask, believing Mom that this fox must be wise.\n\n'
        '“You keep going. Stagnancy is the antithesis of growth. If you want to become better and reach your desired outcome, you must continue to move forward.”\n\n'
        'You stand up, searching the woods for some clear path. There is none. You turn back to the fox, he nods his head, “forge your own path.”'
    )
    screen.fill(WHITE)
    draw_wrapped_text(dialogue, 40, line_gap=34)
    draw_wrapped_text("Press SPACE to begin the game.", 550)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

# Mole segment 
def story_segment_4():
    show_title_card("The Mole")
    dialogue = (
        "Now covered in thorns and leaves, you are feeling exhausted. You can see a break in the tree line, but you can’t find the will to keep moving your feet. Your boots feel so heavy, your hands feel so cold. As you continue to glance longingly to the break in the tree line, a mole pops out of the ground at your feet.\n\n"
        '“Oh, pardon me! Sometimes I have no idea where I’ll breach the surface!” It says, patting your boot apologetically where it had careened into you.\n\n'
        '“No problem.” You say, the exasperation coming through in your voice.\n\n'
        '“What’s wrong?” It asks, turning back towards you. Evidently, it couldn’t see you, but you surmised it must have been able to smell you.\n\n'
        '“Oh.. well. I guess I just can’t find the strength to keep going. Every time it feels like my journey should be ending,  a new challenge appears.” You reply, crouching down to get closer to the mole.\n\n'
        '“Ahh. I know this dilemma well! Sometimes, I get away from myself and I dig far too deep into the soil. When I realize my mistake, I’m so far underground and so tired, that finding the surface seems impossible, I dig, and I dig, and I dig, and it feels like I’ll never reach the surface. The important part… I keep digging!” He exclaims, nose twitching. “Perseverance is about what you do in those moments where you can’t see the light at the end of the tunnel. Do you stop, letting the cold soil surround you, or do you keep digging until your find the warm sun?”\n\n'
        'The mole waves goodbye, and burrows back into the ground. You stand up and begin to march towards that break in the treeline.'
    )
    screen.fill(WHITE)
    draw_wrapped_text(dialogue, 40, line_gap=34)
    draw_wrapped_text("Press SPACE to begin the game.", 550)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

# Post-game 4 text 
def post_game_4_text():
    post_text = (
        "It’s a field of long, soft grass, a pasture. The field is painted with the soft warm glow of the setting sun, and you see a farmhouse in the distance. "
        "You walk through the grass, dancing your fingers through it as you breathe in the evening air. You close your eyes, seeing the light come through your eyelids magnificently."
    )
    screen.fill(WHITE)
    draw_wrapped_text(post_text, 80)
    draw_wrapped_text("Press SPACE to continue.", 520)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

# Horse segment
def horse_segment():
    show_title_card("The Horse")
    dialogue = (
        '“Well done, Artemis.” Your eyes open, you stop in your tracks. A big horse with long flowing blonde hair stands in front of you. She looks like she’s on fire, but it’s just the sunlight.\n\n'
        '“How did you know my name?” You ask, amazed that an animal so beautiful would ever concern herself with the likes of you.\n\n'
        '“Artemis, we’ve been waiting for you!” She laughs, her tail swishing gently.  “You’ve been very brave so far, and I admire how you take advice in stride. But now, you must confront the most difficult of challenges.” She adds.\n\n'
        'You lower your head with dread, you thought it was over.\n\n'
        '“You have to ask for help.” She says, playfully nudging you on your shoulder with her head. “In that house over there-“ she nods to the farmhouse, “there is a kind, old couple. They’ve taken very good care of me over the years, and I have no doubt they will make sure you get home.”\n\n'
        '“I just want my Mom.” You squeak out.\n\n'
        '“Yes, I understand, Artemis. However, I’ve learned in my time on this earth that it takes more than a mother, or a friend, to get through life. It takes a herd – others who have your back and whom you can rely on to be beside you, rain or shine.”'
    )
    screen.fill(WHITE)
    draw_wrapped_text(dialogue, 40, line_gap=34)
    draw_wrapped_text("Press SPACE to continue.", 550)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})
def story_segment_5():
    show_title_card("The Horse")
    dialogue = (
        '“Well done, Artemis.” Your eyes open, you stop in your tracks. A big horse with long flowing blonde hair stands in front of you. She looks like she’s on fire, but it’s just the sunlight.\n\n'
        '“How did you know my name?” You ask, amazed that an animal so beautiful would ever concern herself with the likes of you.\n\n'
        '“Artemis, we’ve been waiting for you!” She laughs, her tail swishing gently.  “You’ve been very brave so far, and I admire how you take advice in stride. But now, you must confront the most difficult of challenges.” She adds.\n\n'
        'You lower your head with dread, you thought it was over.\n\n'
        '“You have to ask for help.” She says, playfully nudging you on your shoulder with her head. “In that house over there-“ she nods to the farmhouse, “there is a kind, old couple. They’ve taken very good care of me over the years, and I have no doubt they will make sure you get home.”\n\n'
        '“I just want my Mom.” You squeak out.\n\n'
        '“Yes, I understand, Artemis. However, I’ve learned in my time on this earth that it takes more than a mother, or a friend, to get through life. It takes a herd – others who have your back and whom you can rely on to be beside you, rain or shine.”'
    )
    screen.fill(WHITE)
    draw_wrapped_text(dialogue, 40, line_gap=34)
    draw_wrapped_text("Press SPACE to continue.", 550)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

# Pre-final game text
def pre_final_game_text():
    pre_text = (
        "You approach the farmhouse, a cold wind now pulling at your hair. You reach to knock on the door. "
    )
    screen.fill(WHITE)
    draw_wrapped_text(pre_text, 180)
    draw_wrapped_text("Press SPACE to begin the final game.", 520)
    pygame.display.flip()
    wait_for_key({pygame.K_SPACE})

# Main story/game sequence 
def main():
    intro()

    # story 1
    story_segment_1()
    # maze
    run_game("maze_game.py")

    # beaver
    story_segment_2()
    # pair
    run_game("pair_matching_game.py")
    post_game_2_text()

    # fox
    story_segment_3()
    # clicker
    run_game("clicker_bar_game.py")

    # mole
    story_segment_4()
    post_game_4_text()
    # runner
    run_game("runner_game.py")

    # horse
    story_segment_5()
    pre_final_game_text()

    # knock
    run_game("knock_sequence_game.py")

    # end
    ending()


if __name__ == "__main__":
    main()
