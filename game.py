from superwires import games
import random
import pygame
games.init(1280,748,80)

class Pers(games.Sprite):
    pers_image = games.load_image("pers.png")
    keys = pygame.key.get_pressed()
    is_jump = False
    jump_count = 10
    def __init__(self):
        super().__init__(image=Pers.pers_image,
                         angle=0,
                         x=640,
                         y=570)
        self.spawn_time = 0
        self.attack_reload = 0
        self.hitpoints = 100
    def update(self):
        if games.keyboard.is_pressed(games.K_d):
            if self.x <= 1250:
                self.x += 5
        elif games.keyboard.is_pressed(games.K_a):
            if self.x >= 30:
                self.x -= 5
        if not Pers.is_jump:
            if games.keyboard.is_pressed(games.K_SPACE):
                Pers.is_jump = True
        else:
            if not Pers.is_jump:
                if games.keyboard.is_pressed(games.K_SPACE):
                    Pers.is_jump = True
            else:
                if Pers.jump_count >= -10:
                    if Pers.jump_count > 0:
                        self.y -= (Pers.jump_count ** 2) / 2
                    else:
                        self.y += (Pers.jump_count ** 2) / 2
                    Pers.jump_count -= 1
                else:
                    Pers.is_jump = False
                    Pers.jump_count = 10
        if self.attack_reload > 0:
            self.attack_reload -= 1
        if games.keyboard.is_pressed(games.K_f):
            if self.attack_reload == 0:
                new_fireball = Attack(Attack.fireball_image, 0, self.x+100, self.y)
                games.screen.add(new_fireball)
                self.attack_reload = 50
        self.check_enemy()
    def check_enemy(self):
        if self.spawn_time > 0:
            self.spawn_time -= 1
        else:
            new_enemy = Enemies()
            games.screen.add(new_enemy)
            self.spawn_time = 150
class Enemies(games.Sprite):
    enemy_image = games.load_image("enemy.png")
    is_jump = False
    jump_count = 10
    jump_time = 200
    def __init__(self):
        super().__init__(image=Enemies.enemy_image,
                         angle=0,
                         x=1300,
                         y=570)
    def update(self):
        self.x -= 5
        if Enemies.jump_time > 0:
            Enemies.jump_time -= 1

        if not Enemies.is_jump:
            if Enemies.jump_time == 0:
                Enemies.is_jump = True
        else:
            if Enemies.jump_count >= -10:
                if Enemies.jump_count > 0:
                    self.y -= (Enemies.jump_count ** 2) / 2
                else:
                    self.y += (Enemies.jump_count ** 2) / 2
                Enemies.jump_count -= 1
            else:
                Enemies.is_jump = False
                Enemies.jump_count = 10
                Enemies.jump_time = 100

class Attack(games.Sprite):
    fireball_image = games.load_image("pngwing.com.png")
    def update(self):
        self.x += 10
        if self.x < 0:
            self.destroy()
class Enemy_attack(games.Sprite):
    fireball_image = games.load_image("pngwing.com.png")
    def update(self):
        self.x -= 10


def main():
    bg_image = games.load_image("bg.png")
    games.screen.background = bg_image
    pers = Pers()
    games.screen.add(pers)


    games.screen.mainloop()


main()