import pygame, random, os
from pygame import mixer
pygame.font.init()
pygame.init()

# BACKGROUND
WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lizard Run")
BG = (pygame.image.load(os.path.join('assets', 'desert2.png')))
# IMAGES
LIZARD_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'lizard7.png')))
ENEMY_1 = pygame.image.load(os.path.join('assets', 'cactus.png'))
ENEMY_2 = pygame.transform.flip(pygame.image.load(os.path.join('assets', 'scorpion.png')), 180, 0)
ENEMY_3 = (pygame.image.load(os.path.join('assets', 'eagle.png')))
# BACKGROUND SOUND
mixer.music.load(os.path.join('assets', 'monkey.wav'))
mixer.music.play(-1)

GRAVITY = .5

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJumping = False
        self.img = LIZARD_IMG
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.y += vel

class Enemy():
    ENEMY_MAP = {
                "cactus": (ENEMY_1),
                "scorpion": (ENEMY_2),
                "eagle": (ENEMY_3),
                }
    def __init__(self, x, y, enemy):
        self.x = x
        self.img = self.ENEMY_MAP[enemy]
        self.y = y + self.img.get_height()
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.x += vel

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y)))

def main():
    running = True
    pygame.mixer.music.unpause()
    surface_y = 400
    y_vel = 0
    jump_vel = -12
    down_vel = 8
    player = Player(200, surface_y)
    enemies = []
    enemy_vel = -9
    # CLOCK AND TIMER
    clock = pygame.time.Clock()
    FPS = 60
    timer = 0
    score = 0
    score_timer = 0
    score_font = pygame.font.Font("score.ttf", 40)
    # SCROLLING BACKGROUND VARIABLES
    bg_x = 0
    bg_change = -5

    # REDRAW WINDOW
    def redraw_window():
        # SCROLLING BACKGROUND
        WIN.blit(BG, (bg_x % BG.get_width() - BG.get_width(),0))
        if bg_x % BG.get_width() <= WIDTH:
            WIN.blit(BG, (bg_x % BG.get_width(), 0))
        # SCORE LABEL
        score_label = score_font.render(f"Score: {score}", 1, (255,255,255))
        WIN.blit(score_label, (WIDTH - score_label.get_width(), 10))
        # PLAYER AND ENEMIES
        player.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        pygame.display.update()

    # GAME OVER
    def game_over():
        GO_font = pygame.font.Font("score.ttf", 70)
        run = True
        timer = 0
        pygame.mixer.music.pause()
        while run:
            clock.tick(FPS)
            WIN.blit(BG, (0,0))
            GO_label = GO_font.render("GAME OVER", 1, (255,255,255))
            WIN.blit(GO_label, (WIDTH/2 - GO_label.get_width()/2, HEIGHT/2 - GO_label.get_height()/2 - 20))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            timer += 1

            if timer >= 120: # 2 second delay
                main_menu()

    # INFINITE LOOP
    while running:
        clock.tick(FPS)
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # MOVE BACKGROUND
        bg_x += bg_change

        # GRAVITY
        if player.y < surface_y:
            new_y = player.y
            y_vel += GRAVITY
            new_y += y_vel
            player.y = new_y

        # MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player.y >= surface_y:
            y_vel = jump_vel
            player.move(y_vel)
        if keys[pygame.K_DOWN] and player.y < surface_y:
            y_vel = down_vel
            player.move(y_vel)

        # SPAWNS AND MOVES ENEMIES
        timer += 1
        if timer >= random.randint(40, 300):
            timer = 0
            enemy = Enemy(WIDTH, surface_y, random.choice(['scorpion', 'eagle']))
            enemies.append(enemy)
        for enemy in enemies:
            enemy.move(enemy_vel)
            if enemy.x <= (0 - enemy.img.get_width()):
                enemies.remove(enemy)
            if collide(player, enemy):
                game_over()

        # SCORE
        score_timer += 1
        if score_timer == 10:
            score_timer = 0
            score += 1

        # INCREASE DIFFICULTY
        if score % 100 == 0 and score != 0:
            enemy_vel -= 0.2
            bg_change -= 0.2

        # REDRAW WINDOW
        redraw_window()

def main_menu():
    menu_font = pygame.font.Font("score.ttf", 45)
    run = True

    while run:
        menu_label = menu_font.render("Press SPACE to play!", 1, (255,255,255))
        WIN.blit(BG, (0,0))
        WIN.blit(menu_label, (WIDTH/2 - menu_label.get_width()/2, HEIGHT/2 - menu_label.get_height()/2 - 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

main_menu()
