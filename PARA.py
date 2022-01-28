import pygame
import random
from pygame.constants import *
pygame.init()

SCREEN_WIDTH = ((320 * 4) // 1.5)
SCREEN_HEIGHT = ((100 * 4 + 80 * 4) // 1.5)

screen = pygame.display.set_mode((int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))

Achtergrond_Boven = pygame.image.load("images/Achtergrond_boven.png").convert_alpha()
Achtergrond_Boven = pygame.transform.scale(Achtergrond_Boven, (Achtergrond_Boven.get_width() * 4, Achtergrond_Boven.get_height() * 4))
Achtergrond_Onder = pygame.image.load("images/Achtergrond_Onder.png").convert_alpha()
Achtergrond_Onder = pygame.transform.scale(Achtergrond_Onder, (Achtergrond_Onder.get_width() * 4, Achtergrond_Onder.get_height() * 4))

BG = (144, 201, 120)

font = pygame.font.Font(None, 25)
font_para = pygame.font.Font(None, 100)
health_count = 0
health_get = False
coin_count = 0
coin_get = False
start_screen = True
hack_show = False
hack_counter = 0
hacked_count = 0
get_hacked = False
game_start = False
game_pause = False
game = False
BG_scroll = 0
BG_scrollcount = 1
obstacle_count = 0
BG_count = 2
keyup = False
clock = pygame.time.Clock()

def draw_bg():
    for x in range(BG_scrollcount):
        screen.blit(Achtergrond_Onder, ((x * Achtergrond_Boven.get_width()) - BG_scroll, 0 + Achtergrond_Boven.get_height()))
        screen.blit(Achtergrond_Boven, ((x * Achtergrond_Boven.get_width()) - BG_scroll, 0))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 3
        self.gravity = 0.75
        self.animatie_tijd = 8
        self.counter = 0
        self.index = 0
        self.scale = 2
        self.jump = False
        self.slide = False
        self.coin = 0
        self.vel_j = 0
        self.delta_j = 0
        self.healthimg = pygame.image.load("images/health.png").convert_alpha()
        self.healthimg = pygame.transform.scale(self.healthimg, (100, 100))
        self.img0 = pygame.image.load("images/JW_0.png").convert_alpha()
        self.img1 = pygame.image.load("images/JW_1.png").convert_alpha()
        self.img2 = pygame.image.load("images/JW_2.png").convert_alpha()
        self.coin_img = pygame.image.load("images/Coin.png").convert_alpha()
        self.width = self.img0.get_width()
        self.height = self.img0.get_height()
        self.widthimg = self.width * self.scale
        self.heightimg = self.height * self.scale
        self.img0 = pygame.transform.scale(self.img0, (self.widthimg, self.heightimg))
        self.img1 = pygame.transform.scale(self.img1, (self.widthimg, self.heightimg))
        self.img3 = pygame.transform.rotate(self.img1, -270)
        self.img = [self.img1, pygame.transform.scale(self.img2, (self.widthimg, self.heightimg)), self.img0, self.img3]
        self.rect = self.img0.get_rect()
    def update(self):
        self.counter += 1
        if self.counter >= self.animatie_tijd:
            self.index += 1
            self.counter = 0
            if self.index >= 2:
                self.index = 0
        if self.jump == True and not self.slide:
            self.delta_j += self.gravity
            if self.delta_j == 15:
                self.delta_j = 0
                self.jump = False
        self.vel_j += self.delta_j
        if not self.slide:
            self.mask = pygame.mask.from_surface(self.img[self.index])
        if self.slide:
            self.mask = pygame.mask.from_surface(self.img[3])
    def draw(self):
        if not self.jump and not self.slide:
            screen.blit((self.img[self.index]), (100, Achtergrond_Boven.get_height() - self.heightimg + self.vel_j))
        if self.jump and not self.slide:
            screen.blit((self.img[2]), (100, Achtergrond_Boven.get_height() - self.heightimg + self.vel_j))
        if self.slide and not self.jump:
            screen.blit((self.img[3]), (100, Achtergrond_Boven.get_height() - self.heightimg + 54 + self.vel_j))
        for x in range(self.health):
            screen.blit(self.healthimg, (40 * x, 0))
        screen.blit(self.coin_img, (10, 75))
        self.text_img = font.render(f"x{self.coin}",True,(0,0,0))
        screen.blit(self.text_img, (60, 100))
        
class Coins(pygame.sprite.Sprite):
    def __init__(self, obstacle, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/Coin.png")
        self.obstacle_type = obstacle
        self.obstacle_height = height
        if self.obstacle_type == "Muur":
            self.height = self.obstacle_height - 50
        if self.obstacle_type == "Spike":
            self.height = Achtergrond_Onder.get_height() - 125
        self.pos_x = SCREEN_WIDTH
        self.pos_y = self.height
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
    def update(self):
        self.rect.x -= obstacle_scroll
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        pygame.sprite.Sprite.__init__(self)
        self.obstacle_type = obstacle_type
        if self.obstacle_type == "Muur":
            self.image = pygame.image.load("images/Muur.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50,100))
            self.height = Achtergrond_Onder.get_height() - self.image.get_height() * 2 + 20
        if self.obstacle_type == "Spike":
            self.image = pygame.image.load("images/Spike.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, int(Achtergrond_Boven.get_height() * 1.3)))
            self.height = Achtergrond_Boven.get_height() - Achtergrond_Onder.get_height()
        self.pos_x = int(SCREEN_WIDTH)
        self.pos_y = self.height
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x -= obstacle_scroll
class Button():
    def __init__(self, text, width, height, pos):
        self.pressed = False
        self.top_rect = pygame.Rect(pos, (width, height))
        self.bottom_rect = pygame.Rect(pos, (width, 6))
        self.text_surf = font.render(text, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.pressed == False:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
    def draw(self):
        pygame.draw.rect(screen, (0,0,0), self.top_rect)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

obstacle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
jefrey_weird = Player()
JA = Button("JA",100,25, (150,SCREEN_HEIGHT - 200))
NEE = Button("NEE",100,25, (600,SCREEN_HEIGHT - 200))
run = True
while run:
    clock.tick(60)
    if start_screen:
        screen.fill((0,0,0))
        start_text1 = font_para.render("PARA",True,(255,255,255))
        start_text2 = font.render("Druk op SPACE om de game te spelen",True,(255,255,255))
        screen.blit(start_text1,(SCREEN_WIDTH//2 - 100,100))
        screen.blit(start_text2, (270,300))
    if game_start:
        BG_count = 0
        BG_scroll = 0
        BG_scrollcount = 1
        hack_counter = 0
        obstacle_scroll = 0
        jefrey_weird.health = 3
        jefrey_weird.coin = 0
        game_start = False
        game = True
        coin_group.empty()
        obstacle_group.empty()
    if game:
        obstacle_count += 1
        if BG_count == Achtergrond_Boven.get_width() - 853:
            BG_count = 0 
            BG_scrollcount += 1
        if obstacle_count >= 200:
            random_number = random.randrange(1,3)
            if random_number == 1:
                obstacle = Obstacle("Spike")
                obstacle_group.add(obstacle)
                obstacle_count = 0
            if random_number == 2:
                obstacle = Obstacle("Muur")
                obstacle_group.add(obstacle)
                coin = Coins("Muur", obstacle.rect.y)
                coin_group.add(coin)
                obstacle_count = 0
        for obstacle in obstacle_group:
            if obstacle.obstacle_type == "Spike":
                offset = (int(jefrey_weird.rect.x - obstacle.rect.x + 100), int(jefrey_weird.rect.y - obstacle.rect.y))
            if obstacle.obstacle_type == "Muur":
                offset = (int(jefrey_weird.rect.x - obstacle.rect.x + 100), int(jefrey_weird.rect.y - obstacle.rect.y + 300))
            collision = jefrey_weird.mask.overlap(obstacle.mask, offset)
            if collision and health_get == False:
                if obstacle.obstacle_type == "Spike" and not jefrey_weird.slide:
                    jefrey_weird.health -= 1
                    health_get = True
                if obstacle.obstacle_type == "Muur" and not jefrey_weird.jump:
                    jefrey_weird.health -= 1
                    health_get = True
        for coin in obstacle_group:
            if coin.obstacle_type == "Muur":
                offset = (int(jefrey_weird.rect.x - coin.rect.x + 100), int(jefrey_weird.rect.y - coin.rect.y + 300))
            collision = jefrey_weird.mask.overlap(obstacle.mask, offset)
            if collision and coin_get == False:
                if obstacle.obstacle_type == "Muur" and jefrey_weird.jump:
                    jefrey_weird.coin += 1
                    coin_get = True
                if obstacle.obstacle_type == "Spike" and jefrey_weird.slide:
                    jefrey_weird.coin += 1
                    coin_get = True
        if not game_pause:
            health_count += 1
            if health_count == 60:
                health_get = False
                health_count = 0
        if coin_get == True and not game_pause:
            coin_count += 1
            if coin_count == 120:
                coin_get = False
                coin_count = 0
        draw_bg()
        if not game_pause:
            obstacle_group.update()
        obstacle_group.draw(screen)
        if not game_pause:
            coin_group.update()
        coin_group.draw(screen)
        if not game_pause:
            jefrey_weird.update()
        jefrey_weird.draw()
        if not game_pause:
            BG_count += 1
            BG_scroll += 1
            obstacle_scroll = 5
        if jefrey_weird.health == 0:
            game = False
            start_screen = True
        if not game_pause:
            hack_counter += 1
        if hack_counter >= 600 and hacked_count == 0:
            hack_show = True
            game_pause = True
            hack_counter = 0
        if hack_counter >= 600 and hacked_count == 1:
            hack_show = False
            game_pause = False
            game = False
            get_hacked = True
            hack_counter = 0
    if hack_show:
        rect = pygame.Rect((100,100),(650,300))
        pygame.draw.rect(screen, (255,255,255), rect)
        hack_text = font.render("Wilt u een gratis IPHONE 12, klik dan op JA?",True,(0,0,0))
        screen.blit(hack_text, (250, 150))
        JA.draw()
        NEE.draw()
        if NEE.pressed:
            hack_show = False
            game_pause = False
            hacked_count = 1
            NEE.pressed = False
        if JA.pressed:
            get_hacked = True
            JA.pressed = False
    if get_hacked:
        screen.fill((0,0,0))
        hacked_text0 = font.render("000111000000111101100100100011110011010101010",True,(255,255,255))
        hacked_text1 = font.render("001110010101010101110011100101010101011110000",True,(255,255,255))
        hacked_text2 = font.render("110010101010101010010111000111100000111110010",True,(255,255,255))
        hacked_text3 = font.render("000111000000111101100100100011110011010101010",True,(255,255,255))
        hacked_text4 = font.render("Your computer is hacked",True,(255,255,255))
        hacked_text5 = font.render("Please wait for further instructions",True,(255,255,255))
        screen.blit(hacked_text0, (0, 0))
        screen.blit(hacked_text1, (0, 25))
        screen.blit(hacked_text2, (0, 50))
        screen.blit(hacked_text3, (0, 75))
        screen.blit(hacked_text4, (0, 100))
        screen.blit(hacked_text5, (0, 125))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jefrey_weird.jump == False and jefrey_weird.slide == False and not game_pause and game:
                jefrey_weird.delta_j = -15
                jefrey_weird.jump = True
            if event.key == pygame.K_c and jefrey_weird.jump == False and not game_pause and game:
                jefrey_weird.slide = True
            if event.key == pygame.K_SPACE and start_screen:
                game_start = True
                start_screen = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                jefrey_weird.slide = False


    pygame.display.update()
pygame.quit()