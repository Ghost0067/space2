#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-7, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_ship = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'

lost = 0
score = 0
goal = 10
win_width = 700
win_height = 500

display.set_caption('Shooter')

window = display.set_mode((win_width, win_height))

background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player('rocket.png', 5, 420, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80,), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()


font.init()
font1 = font.Font(None, 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (180, 0, 0))
font2 = font.Font(None, 36)


score = 0
lost = 0
max_lost = 3


rel_time = False
finish = False
run = True

num_fire = 0


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key== K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
        
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:

                    last_time = timer()
                    rel_time = True


            if rel_time == True:
                now_time = timer()
                if now_time - last_time < 3:
                    reload = font2.render("Wait, reload...", 1,(150, 0, 0))
                    window.blit(reload, (260, 460))
                else:
                    num_fire = 0
                    rel_time = False

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))



        ship.reset()
        ship.update()
        
        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)


        collides = sprite.groupcollide(monsters, bullets, True, True)

        for i in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
  
            monsters.add(monster)

            if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))

            if score >= goal:
                finish = True
                window.blit(win, (200, 200))

            
        display.update()

    time.delay(50)
