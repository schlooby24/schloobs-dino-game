import pygame
import os

pygame.init()

# constants

WINDOW_HEIGHT, WINDOW_WIDTH = 600, 1100
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


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

    LOW_OBSTACLES = [
        pygame.image.load(os.path.join("assets/cactus", "LargeCactus1.png")),
        pygame.image.load(os.path.join("assets/cactus", "LargeCactus2.png")),
        pygame.image.load(os.path.join("assets/cactus", "LargeCactus3.png")),
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
    def __init__(self):
        self.run_img = Assets.RUNNING
        self.jump_img = Assets.JUMPING
        self.duck_img = Assets.DUCKING

        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False

        self.step_index = 0
        self.image = self.run_img[0]
        self.player_rect = self.image.get_rect()
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

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_run, self.dino_duck = False, False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN]:
            self.dino_jump, self.dino_run = False, False
            self.dino_duck = True
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_jump, self.dino_duck = False, False
            self.dino_run = True


    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.X_POS
        self.player_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        pass

    def duck(self):
        pass

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.player_rect.x, self.player_rect.y))



def main():
    run = True
    clock = pygame.time.Clock()
    player=Dinosaur()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((225,225,225))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)


        clock.tick(30)
        pygame.display.update()


main()
