import pygame
import os
import random
from random import randint
from sys import exit

pygame.init()
pygame.display.set_caption('Chrome Dino Ripoff by Schlooby ♥')
pygame.display.set_icon(pygame.image.load(os.path.join("assets/dino", "DinoRun1.png")))

# constants

WINDOW_HEIGHT, WINDOW_WIDTH = 600, 1100
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

failure_list = [
    'Ouch!',
    'Oof!',
    'Zoo wee mama!',
    'Aw, man!',
    'Aw, Beans!',
    'You got fucked, bro.',
    'Yikes!',
    'That sucked...',
    'No don\'t do that!',
    'Rest in R.I.P.;',
    'Press F to pay respects.'
]


class Assets:
    RUNNING = [
        pygame.image.load(os.path.join("assets/dino", "DinoRun1.png")),
        pygame.image.load(os.path.join("assets/dino", "DinoRun2.png"))
    ]

    JUMPING = [
        pygame.image.load(os.path.join("assets/dino", "DinoJump.png"))
    ]

    DUCKING = [
        pygame.image.load(os.path.join("assets/dino", "DinoDuck1.png")),
        pygame.image.load(os.path.join("assets/dino", "DinoDuck2.png"))
    ]

    START = [
        pygame.image.load(os.path.join("assets/dino", "DinoStart.png"))
    ]

    DEAD = [
        pygame.image.load(os.path.join("assets/dino", "DinoDead.png"))
    ]

    LOW_OBSTACLES_BIG = [
        pygame.image.load(os.path.join("assets/cactus", "LargeCactus1.png")),
        pygame.image.load(os.path.join("assets/cactus", "LargeCactus2.png")),
        pygame.image.load(os.path.join("assets/cactus", "LargeCactus3.png"))
    ]

    LOW_OBSTACLES_SMALL = [
        pygame.image.load(os.path.join("assets/cactus", "SmallCactus1.png")),
        pygame.image.load(os.path.join("assets/cactus", "SmallCactus2.png")),
        pygame.image.load(os.path.join("assets/cactus", "SmallCactus3.png"))
    ]

    HIGH_OBSTACLES = [
        pygame.image.load(os.path.join("assets/bird", "Bird1.png")),
        pygame.image.load(os.path.join("assets/bird", "Bird2.png"))
    ]

    CLOUD = [
        pygame.image.load(os.path.join("assets/other", "Cloud.png"))
    ]

    GAME_OVER = [
        pygame.image.load(os.path.join("assets/other", "GameOver.png"))
    ]

    RESET = [
        pygame.image.load(os.path.join("assets/other", "Reset.png"))
    ]

    BG = [
        pygame.image.load(os.path.join("assets/other", "Track.png"))
    ]


class Dinosaur:
    X_POS, Y_POS = 80, 310
    Y_POS_DUCK = 340
    JUMP_V = 8.69
    def __init__(self):
        self.run_img = Assets.RUNNING
        self.jump_img = Assets.JUMPING[0]
        self.duck_img = Assets.DUCKING

        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.step_index = 0
        self.img = self.run_img[0]
        self.player_rect = self.img.get_rect()
        self.jump_v = self.JUMP_V
        self.player_rect.x = self.X_POS
        self.player_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_w]) and not self.dino_jump:
            self.dino_run, self.dino_duck = False, False
            self.dino_jump = True
        elif (userInput[pygame.K_DOWN] or userInput[pygame.K_s]) and not self.dino_jump:
            self.dino_jump, self.dino_run = False, False
            self.dino_duck = True
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_jump, self.dino_duck = False, False
            self.dino_run = True


    def run(self):
        self.img = self.run_img[self.step_index // 5]
        self.player_rect = self.img.get_rect()
        self.player_rect.x = self.X_POS
        self.player_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.img = self.jump_img
        if self.dino_jump:
            self.player_rect.y -= self.jump_v * 4.20
            self.jump_v -= 0.8
        if self.jump_v < - self.JUMP_V:
            self.dino_jump = False
            self.jump_v = self.JUMP_V

    def duck(self):
        self.img = self.duck_img[self.step_index // 5]
        self.player_rect = self.img.get_rect()
        self.player_rect.x = self.X_POS
        self.player_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def draw(self, SCREEN=SCREEN):
        SCREEN.blit(self.img, (self.player_rect.x, self.player_rect.y))


class Obstacle:
    def __init__(self, img, type):
        self.img = img
        self.type = type
        self.rect = self.img[self.type].get_rect()
        self.rect.x = WINDOW_WIDTH

    def update(self):
        self.rect.x -= move_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN=SCREEN):
        SCREEN.blit(self.img[self.type], self.rect)


class smallCactus(Obstacle):
    def __init__(self, img):
        self.type = randint(0, 2)
        super().__init__(img, self.type)
        self.rect.y = 325


class bigCactus(Obstacle):
    def __init__(self, img):
        self.type = randint(0, 2)
        super().__init__(img, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, img):
        self.type = 0
        super().__init__(img, self.type)
        self.rect.y = 250
        self.index = 0
    def draw(self, SCREEN=SCREEN):
        if self.index == 9:
            self.index = 0
        SCREEN.blit(self.img[self.index // 5], self.rect)
        self.index += 1


class Cloud:
    def __init__(self):
        self.x_pos = WINDOW_WIDTH + randint(800, 1000)
        self.y_pos = randint(50, 100)
        self.img = Assets.CLOUD[0]
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def update(self):
        self.x_pos -= move_speed * .69
        if self.x_pos < -self.width:
            self.x_pos = WINDOW_WIDTH + randint(2500, 3000)
            self.y_pos = randint(50, 100)

    def draw(self, SCREEN=SCREEN):
        SCREEN.blit(self.img, (self.x_pos, self.y_pos))


def main():
    global move_speed, bg_x_pos, bg_y_pos, score, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    cloud2 = Cloud()
    obstacles = []
    move_speed = 14
    bg_x_pos = 0
    bg_y_pos = 380
    score = 0
    font = pygame.font.SysFont('comic sans ms', 24)
    deaths = 0

    def keepScore():
        global score, move_speed
        score += 1
        if score % 100 == 0:
            move_speed += 1

        text = font.render(f"Score: {score}", True, (10, 10, 10))
        textField = text.get_rect()
        textField.midright = (1050, 50)
        SCREEN.blit(text, textField)

    def bground():
        global bg_x_pos, bg_y_pos
        bg_img = Assets.BG[0]
        img_width = bg_img.get_width()
        SCREEN.blit(bg_img, (bg_x_pos, bg_y_pos))
        SCREEN.blit(bg_img, (img_width + bg_x_pos, bg_y_pos))
        if bg_x_pos <= -img_width:
            SCREEN.blit(bg_img, (img_width + bg_x_pos, bg_y_pos))
            bg_x_pos = 0
        bg_x_pos -= move_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        SCREEN.fill((245,245,245))
        userInput = pygame.key.get_pressed()

        player.draw()
        player.update(userInput)

        bground()

        cloud.draw()
        cloud.update()

        cloud2.draw()
        cloud2.update()

        if len(obstacles) == 0:
            if randint(0, 2) == 0:
                obstacles.append(smallCactus(Assets.LOW_OBSTACLES_SMALL))
            elif randint(0, 2) == 1:
                obstacles.append(bigCactus(Assets.LOW_OBSTACLES_BIG))
            elif randint(0, 2) == 2:
                obstacles.append(Bird(Assets.HIGH_OBSTACLES))

        for o in obstacles:
            o.draw()
            o.update()
            if player.player_rect.colliderect(o.rect):
                pygame.time.delay(2000)
                deaths += 1
                menu(deaths)

        keepScore()


        clock.tick(30)
        pygame.display.update()



def menu(deaths):
    global points
    run = True
    failureText = random.choice(failure_list)

    while run:
        SCREEN.fill((245,245,245))
        font = pygame.font.SysFont('comic sans ms', 30)

        if deaths == 0:
            text = font.render('Press the any key...', True, (10,10,10))
        elif deaths >= 1:
            text = font.render(f'{failureText} Try again?', True, (10, 10, 10))
            scoreText = font.render(f'Score: {score}', True, (10, 10, 10))
            scoreRect = scoreText.get_rect()
            scoreRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
            SCREEN.blit(scoreText, scoreRect)
        textRect = text.get_rect()
        textRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(Assets.RUNNING[0], (WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT // 2 - 140))
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()

menu(0)