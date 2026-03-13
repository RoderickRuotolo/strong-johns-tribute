import pygame
import sys
import random

pygame.init()

WIDTH = 1100
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jooes Fortões")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# CORES
BAR_BG = (90,55,30)
FLOOR = (60,35,20)
WOOD = (110,70,40)

SKIN = (230,200,170)
BEARD = (60,40,20)

BOSS_SKIN = (70,40,30)

BLUE = (40,100,220)
GRAY = (170,170,170)

RED = (160,60,60)

# ---------------- PLAYER ----------------

# =====================================================
# SPRITES ULTRA DETALHADOS DOS JOOES FORTÕES
# =====================================================

MUSCLE_LIGHT = (240,210,180)
MUSCLE_SHADOW = (200,170,140)

OUTLINE = (0,0,0)

def outline_circle(surface,color,pos,radius):

    pygame.draw.circle(surface,OUTLINE,pos,radius+2)
    pygame.draw.circle(surface,color,pos,radius)

def outline_rect(surface,color,rect):

    pygame.draw.rect(surface,OUTLINE,rect.inflate(4,4))
    pygame.draw.rect(surface,color,rect)

# ---------------- CABEÇA ----------------

def draw_head(surface,x,y):

    outline_circle(surface,MUSCLE_LIGHT,(x,y),24)

    pygame.draw.circle(surface,(0,0,0),(x-7,y-6),3)
    pygame.draw.circle(surface,(0,0,0),(x+7,y-6),3)

    pygame.draw.circle(surface,BEARD,(x,y+8),16)

# ---------------- TRAPÉZIO ----------------

def draw_traps(surface,x,y):

    pygame.draw.polygon(surface,MUSCLE_SHADOW,[
        (x-35,y+5),
        (x,y-10),
        (x+35,y+5),
        (x+20,y+20),
        (x-20,y+20)
    ])

# ---------------- PEITORAL ----------------

def draw_chest(surface,x,y):

    outline_rect(surface,MUSCLE_LIGHT,pygame.Rect(x-32,y+10,64,55))

    pygame.draw.line(surface,MUSCLE_SHADOW,(x,y+10),(x,y+65),2)

    pygame.draw.arc(surface,MUSCLE_SHADOW,(x-32,y+20,64,40),0,3.14,2)

# ---------------- ABDOMEN ----------------

def draw_abs(surface,x,y):

    for i in range(3):

        pygame.draw.line(
            surface,
            MUSCLE_SHADOW,
            (x-18,y+25+i*12),
            (x+18,y+25+i*12),
            2
        )

# ---------------- OMBROS ----------------

def draw_shoulders(surface,x,y):

    outline_circle(surface,MUSCLE_LIGHT,(x-40,y+20),22)
    outline_circle(surface,MUSCLE_LIGHT,(x+40,y+20),22)

# ---------------- BÍCEPS ----------------

def draw_biceps(surface,x,y):

    outline_circle(surface,MUSCLE_LIGHT,(x-70,y+40),24)
    outline_circle(surface,MUSCLE_LIGHT,(x+70,y+40),24)

# ---------------- ANTEBRAÇOS ----------------

def draw_forearms(surface,x,y,attack):

    if attack:

        outline_rect(surface,MUSCLE_LIGHT,pygame.Rect(x+70,y+35,70,18))

    else:

        outline_rect(surface,MUSCLE_LIGHT,pygame.Rect(x+40,y+35,35,18))

    outline_rect(surface,MUSCLE_LIGHT,pygame.Rect(x-100,y+35,45,18))

# ---------------- MÃOS ----------------

def draw_hands(surface,x,y,attack):

    outline_circle(surface,MUSCLE_LIGHT,(x-110,y+44),12)

    if attack:

        outline_circle(surface,MUSCLE_LIGHT,(x+150,y+44),12)

    else:

        outline_circle(surface,MUSCLE_LIGHT,(x+80,y+44),12)

# ---------------- PERNAS ----------------

def draw_legs(surface,x,y):

    outline_rect(surface,(30,30,30),pygame.Rect(x-20,y+70,18,32))
    outline_rect(surface,(30,30,30),pygame.Rect(x+2,y+70,18,32))

# ---------------- PERSONAGEM SEM CAMISA ----------------

def draw_fortao_shirtless(surface,x,y,attack):

    cx = x+35

    draw_head(surface,cx,y-12)

    draw_traps(surface,cx,y)

    draw_shoulders(surface,cx,y)

    draw_chest(surface,cx,y)

    draw_abs(surface,cx,y)

    draw_biceps(surface,cx,y)

    draw_forearms(surface,cx,y,attack)

    draw_hands(surface,cx,y,attack)

    draw_legs(surface,cx,y)

# ---------------- PERSONAGEM COM REGATA ----------------

def draw_fortao_tank(surface,x,y,attack,color):

    cx = x+35

    draw_head(surface,cx,y-12)

    draw_traps(surface,cx,y)

    draw_shoulders(surface,cx,y)

    outline_rect(surface,color,pygame.Rect(cx-32,y+10,64,55))

    draw_biceps(surface,cx,y)

    draw_forearms(surface,cx,y,attack)

    draw_hands(surface,cx,y,attack)

    draw_legs(surface,cx,y)

# ---------------- FUNÇÃO FINAL ----------------

def draw_players(player1,player2):

    draw_fortao_shirtless(screen,player1.rect.x,player1.rect.y,player1.attack)

    draw_fortao_tank(screen,player2.rect.x,player2.rect.y,player2.attack,BLUE)

# ---------------- ENEMY ----------------

class Enemy:

    def __init__(self):

        self.rect = pygame.Rect(random.randint(700,1000),420,60,70)
        self.speed = random.randint(1,3)
        self.attack_timer = 0

    def move(self,player):

        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def attack(self,player):

        if self.rect.colliderect(player.rect):

            if self.attack_timer == 0:
                player.damage(5)
                self.attack_timer = 40

        if self.attack_timer > 0:
            self.attack_timer -= 1

    def draw(self):

        x=self.rect.x
        y=self.rect.y

        pygame.draw.circle(screen,(210,180,150),(x+30,y-5),15)
        pygame.draw.rect(screen,RED,(x,y,60,65))

# ---------------- BOSS ----------------

class Boss:

    def __init__(self):

        self.rect = pygame.Rect(850,400,110,90)
        self.health = 200
        self.speed = 2
        self.attack_timer = 0

    def move(self,player):

        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def attack(self,player):

        if self.rect.colliderect(player.rect):

            if self.attack_timer == 0:
                player.damage(12)
                self.attack_timer = 50

        if self.attack_timer > 0:
            self.attack_timer -= 1

    def draw(self):

        x=self.rect.x
        y=self.rect.y

        pygame.draw.circle(screen,BOSS_SKIN,(x+55,y-10),22)

        pygame.draw.rect(screen,BLUE,(x+30,y-30,50,15))
        pygame.draw.rect(screen,GRAY,(x,y,110,60))
        pygame.draw.rect(screen,BLUE,(x,y+60,110,30))

        pygame.draw.circle(screen,GRAY,(x-10,y+30),20)
        pygame.draw.circle(screen,GRAY,(x+120,y+30),20)

# ---------------- BAR ----------------

def draw_bar():

    screen.fill(BAR_BG)

    pygame.draw.rect(screen,FLOOR,(0,480,1100,120))

    pygame.draw.rect(screen,WOOD,(400,360,300,120))
    pygame.draw.rect(screen,WOOD,(200,400,120,80))
    pygame.draw.rect(screen,WOOD,(750,410,120,70))

    for x in range(420,660,40):
        pygame.draw.rect(screen,(30,130,50),(x,340,10,20))

# ---------------- UI ----------------

def draw_health(player,x,y):

    pygame.draw.rect(screen,(255,0,0),(x,y,200,20))
    pygame.draw.rect(screen,(0,255,0),(x,y,max(player.health*2,0),20))

# ---------------- ATTACK ----------------

def player_attack(players,enemies,boss):

    for p in players:

        if p.attack:

            for e in enemies[:]:

                if p.attack_rect.colliderect(e.rect):
                    enemies.remove(e)

            if boss and p.attack_rect.colliderect(boss.rect):
                boss.health -= 8

# ---------------- GAME SETUP ----------------
class Player:

    def __init__(self,x,color):

        self.rect = pygame.Rect(x,420,70,70)
        self.color = color
        self.speed = 5
        self.health = 100

        self.attack = False
        self.attack_timer = 0
        self.attack_rect = pygame.Rect(0,0,0,0)

        self.damage_cooldown = 0

    def move(self,left,right):

        keys = pygame.key.get_pressed()

        if keys[left]:
            self.rect.x -= self.speed

        if keys[right]:
            self.rect.x += self.speed

    def start_attack(self):

        if self.attack_timer == 0:
            self.attack = True
            self.attack_timer = 12

    def update(self):

        if self.attack_timer > 0:
            self.attack_timer -= 1
            self.attack = True
        else:
            self.attack = False

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # HITBOX DO SOCO
        if self.attack:

            self.attack_rect = pygame.Rect(
                self.rect.x + 80,
                self.rect.y + 20,
                90,
                35
            )

        else:

            self.attack_rect = pygame.Rect(0,0,0,0)

    def damage(self,amount):

        if self.damage_cooldown == 0:
            self.health -= amount
            self.damage_cooldown = 30

    def draw(self):
        pass

player1 = Player(150,(250,250,250))
player2 = Player(260,(30,130,240))

players=[player1,player2]

enemies=[]
boss=None

spawn_timer=0

# ---------------- LOOP ----------------

running=True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running=False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                player1.start_attack()
                player2.start_attack()

    player1.move(pygame.K_a,pygame.K_d)
    player2.move(pygame.K_LEFT,pygame.K_RIGHT)

    for p in players:
        p.update()

    spawn_timer+=1

    if spawn_timer>120 and boss is None:
        enemies.append(Enemy())
        spawn_timer=0

    if len(enemies)>7 and boss is None:
        boss=Boss()

    draw_bar()

    draw_players(player1,player2)

    for e in enemies:
        e.move(player1)
        e.attack(player1)
        e.attack(player2)
        e.draw()

    if boss:

        boss.move(player1)
        boss.attack(player1)
        boss.attack(player2)
        boss.draw()

        boss_text=font.render(
            "Black of Sausage Mouth HP: "+str(boss.health),
            True,(255,255,255)
        )

        screen.blit(boss_text,(750,40))

    player_attack(players,enemies,boss)

    draw_health(player1,40,40)
    draw_health(player2,40,70)

    if player1.health<=0 and player2.health<=0:

        game_over=font.render(
            "OS JOOES FORTÕES FORAM DERROTADOS",
            True,(255,0,0)
        )

        screen.blit(game_over,(380,200))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()