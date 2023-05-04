import pygame
import os
import random
#initialize font module
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1300, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AmongUs Shooter")

BROWN = (154, 58, 42)
PINK = (252, 76, 134)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(0,HEIGHT/2 - 5 , WIDTH, 10)
#custom sounds
FART_SOUND = [ pygame.mixer.Sound('Assets/fart-01.mp3') , pygame.mixer.Sound('Assets/fart-02.mp3'), 
               pygame.mixer.Sound('Assets/fart-03.mp3'), pygame.mixer.Sound('Assets/fart-04.mp3'), 
               pygame.mixer.Sound('Assets/fart-05.mp3'), pygame.mixer.Sound('Assets/fart-squeak-01.mp3') ]
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Gun1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun2.mp3')

#custom fonts 
HEALTH_FONT = pygame.font.Font('Assets/AmongUsFilled-Regular.ttf', 70)
WINNER_FONT = pygame.font.Font('Assets/AmongUsFilled-Regular.ttf', 70)

FPS = 60
VEL = 10
BULLET_VEL = 15
MAX_BULLETS = 100
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 52, 64

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
#event for when dead amongus are hit
OB_HIT = pygame.USEREVENT + 3


#loading yellow ship
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
#loading red spaceship
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
#loading obstacle
DEAD_AMONGUS_IMAGE = pygame.image.load(
    os.path.join('Assets', 'deadmogus.png'))
DEAD_AMONGUS = pygame.transform.scale(
    DEAD_AMONGUS_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
#loading obstacle 2
DEAD_AMONGUS_IMAGE2 = pygame.image.load(
    os.path.join('Assets', 'deadmogus2.png'))
DEAD_AMONGUS2 = pygame.transform.scale(
    DEAD_AMONGUS_IMAGE2, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))



#background img
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, ob1, ob2):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, BROWN)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, YELLOW)
    #Bottom health text 
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, HEIGHT - red_health_text.get_height() - 10))
    #Top health text 
    WIN.blit(yellow_health_text, (10, 10))
    #obstacle
    WIN.blit(DEAD_AMONGUS2,(ob2.x, ob2.y))
    WIN.blit(DEAD_AMONGUS,(ob1.x, ob1.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, BROWN, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

#player 1 controller
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_z] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_c] and yellow.x + VEL < WIDTH - SPACESHIP_WIDTH:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL > 15:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_x] and yellow.y + VEL + yellow.height < HEIGHT/2:  # DOWN
        yellow.y += VEL

#player 2 controller
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_j] and red.x - VEL > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_l] and red.x + VEL < WIDTH - SPACESHIP_WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_i] and red.y - VEL > HEIGHT/2:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_k] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red, ob1, ob2):
    for bullet in yellow_bullets:
        bullet.y += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            #Bounces bullets off dead amongus
        elif ob1.colliderect(bullet) or ob2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(OB_HIT))
            yellow_bullets.remove(bullet)
            bullet.y -= (2 * BULLET_VEL)
            red_bullets.append(bullet)
            
        elif bullet.y > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            #Bounces bullets off dead amongus
        elif ob1.colliderect(bullet) or ob2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(OB_HIT))
            red_bullets.remove(bullet)
            bullet.y += (2 * BULLET_VEL)
            yellow_bullets.append(bullet)
            
        elif bullet.y < 0:
            red_bullets.remove(bullet)

  
   


#winner text    
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)

#game run
def main():
    ob1 = pygame.Rect(300, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    ob2 = pygame.Rect(900, 500, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(100, 500, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 15
    yellow_health = 15

    clock = pygame.time.Clock()
    run = True
    while run:
        #Changing window color to pink
        WIN.fill(PINK)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.width//2 - 2, 10, 20)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_p and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.width//2 - 2, 10, 20)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == OB_HIT:
               random.choice(FART_SOUND).play()
               

        winner_text = ""
        if red_health <= 0:
            winner_text = "Top Wins!"

        if yellow_health <= 0:
            winner_text = "Bottom Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red, ob1, ob2)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, ob1, ob2)

    main()


if __name__ == "__main__":
    main()