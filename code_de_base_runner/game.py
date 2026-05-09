# game data

from argparse import Action
from random import randint
from pgzero.actor import Actor
import pgzrun
import pgzero.screen
screen : pgzero.screen.Screen
import os
os.environ["SDL_VIDEO_CENTERED"] = "1" 


WIDTH = 800
HEIGHT = 600

GROUND = 458
GRAVITY = 200

NUMBER_OF_BACKGROUND = 2
GAME_SPEED = 100
JUMP_SPEED = 200

running = True

# hero initialisation

hero = Actor("hero", anchor=('middle', 'bottom'))
hero.pos = (64, GROUND)
hero_speed = 0

game_over_screen = Actor("game_over", anchor = ('middle','middle'))
game_over_screen.pos = (400,300)
game_over_screen.speed = 0


# enemies initialisations

BOX_APPARTION = (2, 5)
next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])
boxes = []

# background inititalisation

backgrounds_bottom = []
backgrounds_top = []

for n in range(NUMBER_OF_BACKGROUND):
    bg_b = Actor("bg_1", anchor=('left', 'top'))
    bg_b.pos = n * WIDTH, 0
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("bg_2", anchor=('left', 'top'))
    bg_t.pos = n * WIDTH, 0
    backgrounds_top.append(bg_t)

    
def draw():
    screen.clear()

    for bg in backgrounds_bottom:
        bg.draw()

    for bg in backgrounds_top:
        bg.draw()

    for box in boxes:
        box.draw()

    hero.draw()

    


def update(dt):

    # enemies update
    # box
    global next_box_time

    next_box_time -= dt
    if next_box_time <= 0:
        box = Actor("box", anchor=('left', 'bottom'))
        box.pos = WIDTH, GROUND
        boxes.append(box)
        next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])

    for box in boxes:
        x, y = box.pos
        x -= GAME_SPEED * dt
        box.pos = x, y
        if box.colliderect(hero):
            exit()

    if boxes:
        if boxes[0].pos[0] <= - 32:
            boxes.pop(0)

    # hero update

    global hero_speed

    hero_speed -= GRAVITY * dt
    x, y = hero.pos
    y -= hero_speed * dt

    if y > GROUND:
        y = GROUND
        hero_speed = 0

    hero.pos = x, y

    # bg update

    for bg in backgrounds_bottom:
        x, y = bg.pos
        x -= GAME_SPEED * dt
        bg.pos = x, y

    if backgrounds_bottom[0].pos[0] <= - WIDTH:
        bg = backgrounds_bottom.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_bottom.append(bg)

    for bg in backgrounds_top:
        x, y = bg.pos
        x -= GAME_SPEED/3 * dt
        bg.pos = x, y

    if backgrounds_top[0].pos[0] <= - WIDTH:
        bg = backgrounds_top.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_top.append(bg)


def on_key_down(key):
    global hero_speed
    global pygame
    global dt

    # jump
    if key == keys.SPACE and hero.pos[1] == GROUND:

        if hero_speed <= 0:
            hero_speed = JUMP_SPEED

    if key == keys.RETURN :
        draw()
        #update(dt)#help? dt not defined

    if key == keys.ESCAPE :
        pgzrun.sys.exit()



def game_over(vies):

    if vies == 0 : #ou alors mettre cette condition dans update plutot qu'ici? 
        GAME_SPEED = 0
        screen.fill("white")
        screen.set_alpha(160)
        game_over.draw()


pgzrun.go()

