import pygame
import random


pygame.font.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
BACK = pygame.image.load('assets/back.jpg')
BACKGROUND = pygame.transform.scale(BACK, (WIDTH, HEIGHT))

# Title
pygame.display.set_caption("It's raining stones")

# Icon
ICON = pygame.image.load('assets/icon.png')
pygame.display.set_icon(ICON)

# FPS
clock = pygame.time.Clock()
FPS = 60


class Player:
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.left = False
        self.right = False
        self.walk_count = 0
        self.walk_left_img = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
        self.walk_right_img = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
        self.still_char_img = pygame.image.load('assets/standing.png')
        self.mask = pygame.mask.from_surface(self.still_char_img)


    def draw(self):
        if self.walk_count > 26:
            self.walk_count = 0

        if self.left:
            WINDOW.blit(self.walk_left_img[self.walk_count//3], (self.x, self.y))  
            self.walk_count += 1

        elif self.right:
            WINDOW.blit(self.walk_right_img[self.walk_count//3], (self.x, self.y))
            self.walk_count += 1

        else:
            WINDOW.blit(self.still_char_img, (self.x, self.y))
            self.walk_count = 0 


class Stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.choice_list = [pygame.image.load('assets/stone.png'), pygame.image.load('assets/stone2.png')]
        self.img = random.choice(self.choice_list)
        self.mask = pygame.mask.from_surface(self.img)


    def draw(self):
        WINDOW.blit(self.img, (self.x, self.y))


    def move(self, vel):
        self.y += vel


def increase_speed(score, vel):
    if score > 20:
        vel = 4 
    elif score > 50:
        vel = 5 
    elif score > 100:
        vel = 7
    elif score > 150:
        vel = 9
    elif score > 200:
        vel = 11
    return vel


def check_collision(player, stone):
    offset_x = stone.x - player.x
    offset_y = stone.y - player.y
    return player.mask.overlap(stone.mask, (offset_x, offset_y))


def redraw_window(player, stones, blood_img, font, score, lost, lost_font):
    WINDOW.blit(BACKGROUND, (0, 0))

    for stone in stones:
        stone.draw()

    player.draw()

    score_font = font.render(f'Score: {score}', 1, (255, 255, 255))
    WINDOW.blit(score_font, (10, 10))

    if lost:
        WINDOW.blit(blood_img, (player.x + 19, player.y + 12))
        over_font = lost_font.render('Game Over!', 1, (0, 0, 0))
        WINDOW.blit(over_font, (WIDTH//2 - over_font.get_width()//2, HEIGHT//2 - over_font.get_height()//2))
        score_font = font.render(f'Score: {score}', 1, (0, 0, 0))
        WINDOW.blit(score_font, (WIDTH//2 - score_font.get_width()//2, HEIGHT//2 - score_font.get_height()//2 + 50))
    pygame.display.update()


def main():
    player_vel = 5
    player = Player(350, 520)
    blood_img = pygame.image.load('assets/blood.png')

    stone_list = []
    num_of_stones = 9
    stone_vel = 3

    score = 0
    lost = False
    lost_wait = 0
    font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 70)

    pygame.mixer.music.load('assets/music.mp3')
    pygame.mixer.music.play(-1)

    global over_sound
    over_sound = pygame.mixer.Sound('assets/over.wav')

    running = True
    while running:
        clock.tick(FPS) 
        redraw_window(player, stone_list, blood_img, font, score, lost, lost_font)

        if lost:
            lost_wait += 1 
            if lost_wait > FPS * 2:
                 running = False 
            else:
                continue

        for stone in stone_list:
            if check_collision(player, stone):
                    lost = True
                    over_sound.play()
                    break  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x + player_vel >= 0:
            player.left = True
            player.x -= player_vel
            player.right = False

        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x <= WIDTH + 10 - player.still_char_img.get_width():
            player.left = False
            player.right = True
            player.x += player_vel

        else:
            player.left = False
            player.right = False
            player.walk_count = 0

        if len(stone_list) == 0:
            num_of_stones += 1
            for i in range(num_of_stones):
                stone = Stone(random.randint(0, 750), random.randint(-1000, -300))
                stone_list.append(stone)

        for stone in stone_list:
            stone.move(stone_vel)
            if stone.y >= HEIGHT:
                score += 1 
                stone_list.remove(stone)

        stone_vel = increase_speed(score, stone_vel)


def start_screen():
    running = True
    font = pygame.font.SysFont('comicsans', 70)

    while running:
        WINDOW.blit(BACKGROUND, (0,0))
        start_font = font.render("Press the mouse to begin...", 1, (0 ,0 ,0))
        WINDOW.blit(start_font, (WIDTH//2 - start_font.get_width()//2, 265))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
                over_sound.stop()
                pygame.mixer.music.fadeout(2500)
                
        pygame.display.update()

start_screen()