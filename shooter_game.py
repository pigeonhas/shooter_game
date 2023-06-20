#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer
save = 0
score = 0
file = open('record.txt' , 'r')
record = int(file.read())
life = 5
timer = 100
speed = 1
num_fire = 0
rel_time = False

class Gamesprite(sprite.Sprite):
    def __init__(self , player_speed , player_x , player_y , player_image , weight , height):
        sprite.Sprite.__init__(self)
        self.weight = weight
        self.height = height
        self.image = transform.scale(image.load(player_image) , (self.weight , self.height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image , (self.rect.x , self.rect.y))

class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 1420:
            self.rect.x += self.speed
    def shoot(self):
        bullet = Bullet(-7 , self.rect.centerx , self.rect.top , 'bullet.png' , 5 , 20)
        bullets.add(bullet)

class Enemy(Gamesprite):
    def update(self):
        global life
        global timer
        if self.rect.y > 1000:
            death.play()
            self.rect.y = 0
            self.rect.x = randint(10 , 610)
            life -= 1
            
        else:
            self.rect.y += self.speed * speed



class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for e in range(5):
    monster = Enemy(randint(4 , 7) , randint(10 , 1420) , 0 , 'ufo.png' , 80 , 50)
    monsters.add(monster)
for e in range(3):
    asteroid = Enemy(randint(4 , 7) , randint(10 , 1420) , 0 , 'asteroid.png' , 80 , 50)
    asteroids.add(asteroid)

window = display.set_mode((1500 , 1000))
display.set_caption('Space shooter')

background = transform.scale(image.load('galaxy.jpg') , (1500 , 1000))
rocket = Player(15 , 710 , 900 , 'rocket.png' , 80 , 100)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
death = mixer.Sound('dead.ogg')
fire = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Bahnschrift' , 30 )
game = True
finish = False
reloading = 0
num_fire = 0
while game:

    
    for e in event.get():
        if e.type == QUIT:
            finish = True
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire.play()
                    rocket.shoot()

                if num_fire  >= 5 and rel_time == False :  # если игрок сделал 5 выстрелов
                    rel_time = True  # ставим флаг перезарядки
                
                
    if not finish:
        for monster in monsters:
            monster.speed *= 1.001
        if rel_time == True:
            if reloading < 60:
                reloading += 1
            else:
                reloading = 0
                num_fire = 0  # обнуляем счётчик пуль
                rel_time = False  # сбрасываем флаг перезарядки

        collides = sprite.groupcollide(monsters , bullets , True , True)
        for c in collides:
            monster = Enemy(randint(1 , 3) , randint(10 , 1420) , 0 , 'ufo.png' , 80 , 50)
            monsters.add(monster)
            score += 1
            if int(record) < score:
                record = score
        if sprite.spritecollide(rocket , monsters , False) or sprite.spritecollide(rocket , asteroids , False):
            sprite.spritecollide(rocket , monsters , True)
            sprite.spritecollide(rocket , asteroids , True)
            life -= 1
        if life <= 0:
            finish = True
            life = 0
        timer -= 1
        if timer <= 0:
            timer = 100
            speed += 0.1

        window.blit(background , (0 , 0))
        text_life = font1.render('Жизни: ' + str(life) , 1 , (255 , 255 , 255))
        text_score = font1.render('Счет: ' + str(score) , 1 , (255 , 255 , 255))
        text_record = font1.render('Рекорд: ' + str(record) , 1 , (255 , 255 , 255))
        text_lose = font1.render('You lose!' , 10 , (255 , 255 , 255))
        reload_text = font1.render('Wait, reload...', 1, (150, 0, 0))
        if reloading < 60 and rel_time == True:
            window.blit(reload_text , (260, 460))
        window.blit(text_life , (5 , 35))
        window.blit(text_score , (5 , 9 ))
        window.blit(text_record , (5 , 63))
        rocket.update()
        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        bullets.update()
        monsters.update()
        asteroids.update()

        

    else:
        window.blit(text_lose , (270 , 250))
        if save == 0:
            file = open('record.txt' , 'w')
            file.write(str(record))
            file.close()
            save = 1

    time.delay(50)
    display.update()
