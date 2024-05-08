from superwires import games, color
import random
import pygame

games.init(1280,748,80)
class Pers(games.Sprite):
    pers_image = games.load_image("pers.png")
    keys = pygame.key.get_pressed()
    enemies_alive = []
    pers_alive = []
    is_jump = False
    jump_count = 30
    scene = 0
    def __init__(self):
        super().__init__(image=Pers.pers_image,
                         angle=0,
                         x=640,
                         y=570)
        self.spawn_time = 0
        self.attack_reload = 0
        self.hitpoints = 100
        self.timer = games.Text(value=0, size=25, color=color.black,
                                top=5, right=games.screen.width - 10)
    def update(self):
        self.timer.value += 1
        self.timer.right = games.screen.width - 10
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
                if Pers.jump_count >= -30:
                    if Pers.jump_count > 0:
                        self.y -= (Pers.jump_count) / 2
                    else:
                        self.y += (Pers.jump_count*-1) / 2
                    Pers.jump_count -= 1
                else:
                    Pers.is_jump = False
                    Pers.jump_count = 30
        if self.attack_reload > 0:
            self.attack_reload -= 1
        if pygame.mouse.get_pressed()[0]:
            if self.attack_reload == 0:
                new_fireball = Attack(Attack.fireball_image, 0, self.x, self.y)
                games.screen.add(new_fireball)
                self.attack_reload = 50
        self.check_enemy()

    def check_enemy(self):
        if self.spawn_time > 0:
            self.spawn_time -= 1
        else:
            new_enemy = Enemies()
            games.screen.add(new_enemy)
            Pers.enemies_alive.append(new_enemy)
            self.spawn_time = 150
            return new_enemy
class Enemies(games.Sprite):
    enemy_image = games.load_image("enemy.png")
    is_jump = False
    jump_count = 30
    jump_time = 0
    def __init__(self):
        super().__init__(image=Enemies.enemy_image,
                         angle=0,
                         x=1300,
                         y=570)
        self.attack_reload = 0
    def update(self):
        if self.attack_reload > 0:
            self.attack_reload -= 1
        if self.attack_reload == 0:
            new_fireball = Enemy_attack(Attack.fireball_image, 0, self.x - 100, self.y)
            games.screen.add(new_fireball)
            self.attack_reload = 50
class Attack(games.Sprite):
    fireball_image = games.load_image("pngwing.com.png")
    def update(self):
        self.x += 10
        if self.x > 1280:
            self.destroy()
        self.collide()

    def collide(self):
        for enemies in Pers.enemies_alive:
            if enemies in self.overlapping_sprites:
                enemies.destroy()
class Enemy_attack(games.Sprite):
    fireball_image = games.load_image("pngwing.com.png")
    def update(self):
        self.x -= 10
        if self.x > 1280:
            self.destroy()
        self.collide()

    def collide(self):
        for pers in Pers.pers_alive:
            if pers in self.overlapping_sprites:
                pers.destroy()

def main():
    bg_image = games.load_image("bg.png")
    games.screen.background = bg_image
    pers = Pers()
    games.screen.add(pers)
    Pers.pers_alive.append(pers)
    games.screen.mainloop()

main()