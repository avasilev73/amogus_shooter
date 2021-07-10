from pygame import *
from random import randint
from time import time as timer #!импортируем функцию для засекания времени, чтобы интерпретатор не искал эту функцию в pygame модуле time, даём ей другое название сами
#!подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
 
font2 = font.SysFont("Arial", 36)
 
#фоновая музыка
mixer.init()
mixer.music.load('амогдрип.ogg')
mixer.music.play()
fire_sound = mixer.Sound('d8a048f-8891-4b.ogg')
#нам нужны такие картинки:
img_back = "дежаву.png" #фон игры
img_bullet = "пулиотбабули.png" #пуля
img_hero = "амогусгус.png" #герой
img_enemy = "амогус.png" #враг
img_ast = "казах.png" #астероид
 
score = 0 #сбито кораблей
goal = 20 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 10 #проиграли, если пропустили столько кораблей
life = 3  #очки жизни
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#класс главного игрока
class Player(GameSprite): 
  #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
   #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
#класс спрайта-врага 
class Enemy(GameSprite):
  #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Ast(GameSprite):
  #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            
 
#класс спрайта-пули 
class Bullet(GameSprite):
  #движение врага
    def update(self):
        self.rect.y += self.speed
        #исчезает, если дойдёт до края экрана
        if self.rect.y < 0:
            self.kill()
  
#создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
#создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
#создание группы спрайтов-астероидов ()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Ast(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
 
bullets = sprite.Group()
 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
 
rel_time = False #флаг, отвечающий за перезарядку
 
num_fire = 0  #переменная для подсчёта выстрелов         
 
while run:
   #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
        #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE: # если клавиша пробел нажата 
                    #проверяем, сколько выстрелов сделано и не происходит ли перезарядка
                    if num_fire < 5 and rel_time == False: #
                        num_fire = num_fire + 1 #
                        fire_sound.play() #
                        ship.fire() #
                        
                    if num_fire  >= 5 and rel_time == False : #если игрок сделал 5 выстрелов
                        last_time = timer() #засекаем время, когда это произошло
                        rel_time = True #ставим флаг перезарядки
              
   #сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        #обновляем фон
        window.blit(background,(0,0)) #
    
        #производим движения спрайтов
        ship.update() # отслеживаем движение корабля
        monsters.update() # тарелок
        asteroids.update() #мастероидов
        bullets.update() # пуль
    
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset() # отбрадем на экране всех персонажей
        monsters.draw(window) #
        asteroids.draw(window) #
        bullets.draw(window) #
 
        #перезарядка
        if rel_time == True: # если истинно
            now_time = timer() #считываем время
        
            if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font2.render('Wait, reload...', 1, (150, 0, 0)) # выводим на экран уведомление о перезарядке
                window.blit(reload, (260, 460)) # рисуем на экране
            else:
                num_fire = 0   #обнуляем счётчик пуль
                rel_time = False #сбрасываем флаг перезарядки
 
        #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True) #
        for c in collides: #
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1 # увеличиваем счетчик
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) # возобнавляем тарелку с рандомными свойствами
            monsters.add(monster) # добавляем в группу
  
        #если спрайт коснулся врага, уменьшает жизнь
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False): #
            sprite.spritecollide(ship, monsters, True) # или врага
            sprite.spritecollide(ship, asteroids, True) # или астероид
            life = life -1 # уменишить переменнную жизней
 
        #проигрыш
        if life == 0 or lost >= max_lost: # если пропустил или кончились жизни
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200)) # вывести на экране надпись
    
    
        #проверка выигрыша: сколько очков набрали?
        if score >= goal: # если сбил бальше или равно счетчику
            finish = True # установить флаг TRUE
            window.blit(win, (200, 200)) # написовать на экране надпись о победе
 
        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255)) #
        window.blit(text, (10, 20)) # написовать на экране
    
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255)) #
        window.blit(text_lose, (10, 50)) # написовать на экране
 
        #задаём разный цвет в зависимости от количества жизней
        if life == 3: # если жизнь равна 3 зеленая
            life_color = (0, 150, 0)
        if life == 2: # если жизнь равна 2 желтая
            life_color = (150, 150, 0)
        if life == 1: # если жизнь равна 1 красная
            life_color = (150, 0, 0)
    
        text_life = font1.render(str(life), 1, life_color) # создать тестовый объект 
        window.blit(text_life, (650, 10)) # написовать на экране
    
        display.update() # сбновлять все спрайты на экране
 
   #бонус: автоматический перезапуск игры
    else: # иначе
        finish = False # если игра закончилать и finish == true
        score = 0 # все обнулить
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill() # убрать с эерана
        for m in monsters:
            m.kill() # убрать с эерана
        for a in asteroids:
            a.kill()    # убрать с эерана
        
        time.delay(3000) # установить задержку в 3 секунды
        for i in range(1, 6): # заполнить группу врагами
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3): # заполнить группу метеорами
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)   
    
    time.delay(50) # задержка итериций цыкла в 50 мс для ретро эффекта
