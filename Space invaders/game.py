import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Space Shooter')

ICON = pygame.image.load('assets/icon.png')
pygame.display.set_icon(ICON)

BACK = pygame.image.load('assets/back.jpg')
BACKGROUND = pygame.transform.scale(BACK, (WIDTH, HEIGHT))

clock = pygame.time.Clock()


class Ship():
    def __init__(self, img, x, y):
        self.x = x
        self.y= y
        self.img = pygame.image.load(img)
        self.mask = pygame.mask.from_surface(self.img)


    def draw(self):
        WINDOW.blit(self.img, (self.x, self.y))


class Player(Ship):
    def __init__(self, img, x, y):
        super().__init__( img, x, y)
        self.max_health = 100
        self.health = 100

    def draw(self):
        super().draw()
        self.healthbar()

    def healthbar(self):
        pygame.draw.rect(WINDOW, (255,0,0), (self.x, self.y + self.img.get_height() + 5, self.img.get_width(), 10))
        pygame.draw.rect(WINDOW, (0,255,0), (self.x, self.y + self.img.get_height() + 5, self.img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)


    def move(self, vel):
        self.y += vel


class Bullet:
    def __init__(self, img, x, y):
        self.x = x 
        self.y = y
        self.img = pygame.image.load(img)
        self.mask = pygame.mask.from_surface(self.img)


    def draw(self):
        WINDOW.blit(self.img, (self.x, self.y))


    def move(self, vel):
        self.y -= vel


class Enemy_bullet(Bullet):
    def __init__(self, img, x, y, state='ready'):
        super().__init__(img, x, y)
        self.state = state


    def move(self, vel):
        self.y += vel


def collision(object_1, object_2):
    offset_x = object_2.x - object_1.x
    offset_y = object_2.y - object_1.y
    return object_1.mask.overlap(object_2.mask, (offset_x, offset_y))


def main():
    running = True
    FPS = 60
    bullet_sound = pygame.mixer.Sound('assets/bullet.wav')
    collision_sound = pygame.mixer.Sound('assets/collision.wav')

    player_img = 'assets/player.png' 
    player = Player(player_img, 350, 520)
    player_vel = 5

    enemy_list = []
    num_of_enemies = 5
    enemy_img = 'assets/enemy.png'
    enemy_vel = 1

    bullet_img = 'assets/bullet.png'
    bullet = Bullet(bullet_img, player.x + 16, player.y + 1)
    bullet_state = 'ready'
    bullet_vel = 4

    enemy_bullet_img = 'assets/bomb.png'
    enemy_bullet_vel = 3
 
    score = 0
    lives = 10
    lost = False
    lost_count = 1
 
    font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 70)


    def redraw_window():
        WINDOW.blit(BACKGROUND, (0, 0))

        score_label = font.render(f'Score: {score}', 1, (255, 255, 255))
        WINDOW.blit(score_label, (10, 10))

        lives_label = font.render(f'Lives: {lives}', 1, (255, 255, 255))
        WINDOW.blit(lives_label, (WIDTH - lives_label.get_width() -10 , 10))

        for enemy in enemy_list:
            enemy[1].draw()
            enemy[0].draw()

        bullet.draw()
        player.draw()

        if lost:
            lost_label = lost_font.render('Game Over!', 1, (255, 255, 255))
            WINDOW.blit(lost_label, (WIDTH//2 - lost_label.get_width()//2, HEIGHT//2 - lost_font.get_height()//2))
            WINDOW.blit(score_label, (WIDTH//2 - score_label.get_width()//2, HEIGHT//2 - score_label.get_height()//2 + 50))
    
        pygame.display.update()

    while running:
        clock.tick(FPS)
        redraw_window()
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                running = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - player_vel > 0:
            player.x -= player_vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player_vel <= WIDTH - player.img.get_width():
            player.x += player_vel
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y - player_vel >= 0:
            player.y -= player_vel
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player_vel + 20 <= HEIGHT - player.img.get_height():
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            if bullet_state == 'ready':
                bullet_state = 'fire'
                bullet_sound.play()

        if len(enemy_list) == 0:
            num_of_enemies += 1
            for i in range(num_of_enemies):
                enemy = Enemy(enemy_img, random.randint(0, 750), random.randint(-800, -300))
                enemy_bullet = Enemy_bullet(enemy_bullet_img, enemy.x + 15, enemy.y + 30)
                enemy_list.append((enemy, enemy_bullet))

        for enemy in enemy_list:
            enemy[0].move(enemy_vel)
            if enemy[0].y > 0:
                enemy[1].state = 'fire'
                enemy[1].move(enemy_bullet_vel)
            if enemy[1].y > HEIGHT + 500:
                enemy[1].state = 'ready' 
            if enemy[1].state == 'ready':
                enemy[1].x = enemy[0].x + 15
                enemy[1].y = enemy[0].y + 30

            if enemy[0].y > HEIGHT:
                lives -= 1
                enemy_list.remove(enemy)
            elif collision(enemy[0], bullet):
                enemy_list.remove(enemy)
                collision_sound.play()
                bullet_state = 'ready'
                score += 1
            elif collision(player, enemy[0]):
                player.health -= 10
                enemy_list.remove(enemy)
            elif collision(enemy[1], player):
                player.health -= 10
                enemy[1].y = HEIGHT

        if bullet_state == 'fire':
            bullet.move(bullet_vel)

        if bullet.y < 0:
            bullet_state = 'ready'

        if bullet_state == 'ready':
            bullet.x = player.x + 16 
            bullet.y = player.y + 1

        pygame.display.update()


def start_screen():
    running = True
    font = pygame.font.SysFont('comicsans', 70)

    while running:
        WINDOW.blit(BACKGROUND, (0, 0))
        start_font = font.render('Press the mouse to begin...', 1, (255, 255, 255))
        WINDOW.blit(start_font, (WIDTH//2 - start_font.get_width()//2, HEIGHT//2 - start_font.get_height()//2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()

        pygame.display.update()


start_screen()