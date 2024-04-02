import pygame
import random
import math
from superwires import games

games.init(1280,748,80)

class Pers(games.Sprite):
    keys = pygame.key.get_pressed()
    is_jump = False
    is_walk = False
    is_idle = True
    jump_count = 10
    pers_image = games.load_image("pers3.png", transparent="False")
    used_fireballs = []
    idle_pers_images = (
        "idle_pers1.png",
        "idle_pers2.png",
        "idle_pers3.png"
    )
    walk_pers_images = (
        "walking_pers1.png",
        "walking_pers2.png",
        "walking_pers3.png"
    )
    def __init__(self):
            super().__init__(image=Pers.pers_image,
                             angle=0,
                             x=640,
                             y=570,
                             is_collideable=False)
    def update(self):
        walk_pers_anim = games.Animation(Pers.walk_pers_images, 0, self.x, self.y, n_repeats=1, repeat_interval=1)
        idle_pers_anim = games.Animation(Pers.idle_pers_images, 0, self.x, self.y, n_repeats=1, repeat_interval=1)
        if games.keyboard.is_pressed(games.K_d):
            if self.x <= 1250:
                self.x += 5
                Pers.is_walk = True
                Pers.is_idle = False
        elif games.keyboard.is_pressed(games.K_a):
            if self.x >= 30:
                self.x-= 5
                Pers.is_walk = True
                Pers.is_idle = False
        else:
            Pers.is_walk = False
            Pers.is_idle = True
        if not Pers.is_jump:
            if games.keyboard.is_pressed(games.K_SPACE):
                Pers.is_jump = True
        else:
            if Pers.jump_count >= -10:
                if Pers.jump_count > 0:
                    self.y -= (Pers.jump_count ** 2)/2
                else:
                    self.y += (Pers.jump_count ** 2)/2
                Pers.jump_count -= 1
            else:
                Pers.is_jump = False
                Pers.jump_count = 10
        if Pers.is_idle:
            games.screen.add(idle_pers_anim)
        if Pers.is_walk:
            games.screen.add(walk_pers_anim)
        if 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    fireball = Attack(Attack.fireball_image, 0, self.x, self.y)
                    games.screen.add(fireball)
                    Pers.used_fireballs.append(fireball)
                if event.type == pygame.QUIT:
                    exit()






class Attack(games.Sprite):
    fireball_image = games.load_image("pngwing.com.png")
    def update(self):
        self.x += 10
        self.check_collide()
    def check_collide(self):
        for Enemies in self.overlapping_sprites:
            Enemies.collide()
class Enemy_attack(games.Sprite):
    fireball_image = games.load_image("pngwing.com.png")
    def update(self):
        self.x -= 10
class Enemies(games.Sprite):
    enemy_image = games.load_image("enemy.png")
    def __init__(self):
            super().__init__(image=Enemies.enemy_image,
                             angle=0,
                             x=1300,
                             y=570)
    def update(self):
        self.x -= 1
        if random.randint(1,500) == 1:
            fireball = Enemy_attack(Enemy_attack.fireball_image, 0, self.x, self.y)
            games.screen.add(fireball)
            Pers.used_fireballs.append(fireball)
        if self.x < 0:
            self.destroy()
        if self.x == Attack.x:
            self.destroy()
    def get_x(self):
        return self.x
    def collide(self):
        self.destroy()
        self.__init__()

while True:
    bg_image = games.load_image("bg.png")
    games.screen.background = bg_image

    pers = Pers()
    games.screen.add(pers)

    enemy = Enemies()
    games.screen.add(enemy)

    games.screen.mainloop()
