from superwires import games, color
import random
import pygame

games.init(1280,748,80)
games.pygame.display.set_caption("Forest Battle")
icon = games.pygame.image.load("pers.png")
games.pygame.display.set_icon(icon)
pygame.mixer.music.load("them.wav")
pygame.mixer.music.play(2)

class Score(games.Text):
    def __init__(self):
        super().__init__(value=0, color=color.white, size=50, x=600, y=50)
    def update(self):
        self.value = Pers.value
class Hitpoints(games.Text):
    def __init__(self):
        super().__init__(value=Pers.hitpoints, color=color.red, size=50, x=50, y=50)
    def update(self):
        self.value = Pers.hitpoints
class Pers(games.Sprite):
    pers_image = games.load_image("pers.png")
    keys = pygame.key.get_pressed()
    enemies_alive = []
    pers_alive = []
    value = 0
    is_jump = False
    hitpoints = 100
    jump_count = 30
    scene = 0
    def __init__(self):
        super().__init__(image=Pers.pers_image,
                         angle=0,
                         x=640,
                         y=570)
        self.spawn_time = 0
        self.attack_reload = 0
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
                    pygame.mixer.music.load("jump1.wav")
                    pygame.mixer.music.play(1)
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
                    games.music.load("jump2.wav")
                    games.music.play(1)
        if self.attack_reload > 0:
            self.attack_reload -= 1
        if pygame.mouse.get_pressed()[0]:
            if self.attack_reload == 0:
                new_fireball = Attack(Attack.fireball_image, 0, self.x+100, self.y)
                games.screen.add(new_fireball)
                pygame.mixer.music.load("attack.wav")
                pygame.mixer.music.play(1)
                self.attack_reload = 50
        self.check_enemy()
        if Pers.hitpoints == 0:
            self.destroy()
            end_message = games.Message(value="Конец игры",
                                        size=90,
                                        color=color.red,
                                        x=games.screen.width / 2,
                                        y=games.screen.height / 2,
                                        lifetime=5 * games.screen.fps,
                                        after_death=games.screen.quit)
            games.screen.add(end_message)

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
        self.x -= 2
        if Enemies.jump_time > 0:
            Enemies.jump_time -= 1

        if not Enemies.is_jump:
            if Enemies.jump_time == 0 and random.randint(1,200) == 1:
                Enemies.is_jump = True
        else:
            if Enemies.jump_count >= -30:
                if Enemies.jump_count > 0:
                    self.y -= (Enemies.jump_count) / 2
                else:
                    self.y += (Enemies.jump_count*-1) / 2
                Enemies.jump_count -= 1
            else:
                Enemies.is_jump = False
                Enemies.jump_count = 30
                Enemies.jump_time = 300
        if self.attack_reload > 0:
            self.attack_reload -= 1
        if self.attack_reload == 0:
            new_fireball = Enemy_attack(Attack.fireball_image, 0, self.x-100, self.y)
            games.screen.add(new_fireball)
            pygame.mixer.music.load("attack.wav")
            pygame.mixer.music.play(1)
            self.attack_reload = 200

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
                self.destroy()
                Pers.value += 1
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
                self.destroy()
                Pers.hitpoints -= 10
def main():
    bg_image = games.load_image("bg.png")
    games.screen.background = bg_image
    pers = Pers()
    text = Hitpoints()
    score = Score()
    games.screen.add(score)
    games.screen.add(text)
    games.screen.add(pers)
    Pers.pers_alive.append(pers)
    games.screen.mainloop()
main()