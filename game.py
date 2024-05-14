from superwires import games, color
import random
import pygame

games.init(1280,748,80)
games.pygame.display.set_caption("Forest Battle")
icon = games.pygame.image.load("pers.png")
games.pygame.display.set_icon(icon)

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
    bosses_alive = []
    value = 0
    fake_value = value
    is_jump = False
    hitpoints = 100
    spawn_time = 150
    jump_count = 30
    scene = 1
    def __init__(self):
        super().__init__(image=Pers.pers_image,
                         angle=0,
                         x=640,
                         y=570)
        self.spawn_time = 0
        self.attack_reload = 0
    def update(self):
        if Pers.fake_value % 10 == 0 and Pers.fake_value > 0:
            Enemies.attack_reload -= 5
            Enemies.speed += 0.5
            Pers.spawn_time -= 5
            Enemy_attack.speed += 1
            Pers.fake_value += 1
        if Pers.fake_value % 15 == 0 and Pers.fake_value > 0:
            boss = Boss()
            games.screen.add(boss)
            Pers.bosses_alive.append(boss)
            Pers.fake_value += 1
        if games.keyboard.is_pressed(games.K_d):
            if self.x <= 1250:
                self.x += 5
        elif games.keyboard.is_pressed(games.K_a):
            if self.x >= 30:
                self.x -= 5
        elif games.keyboard.is_pressed(games.K_s) and Pers.is_jump == False:
            if self.y <= 690:
                self.y += 5
        elif games.keyboard.is_pressed(games.K_w) and Pers.is_jump == False:
            if self.y >= 500:
                self.y -= 5
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
            self.spawn_time = Pers.spawn_time
            return new_enemy
class Enemies(games.Sprite):
    enemy_image = games.load_image("enemy.png")
    is_jump = False
    jump_count = 30
    jump_time = 0
    speed = 2
    attack_reload = 200
    def __init__(self):
        super().__init__(image=Enemies.enemy_image,
                         angle=0,
                         x=1300,
                         y=random.randint(500,690))
        self.attack_reload = 0
    def update(self):
        self.x -= Enemies.speed
        if Enemies.jump_time > 0:
            Enemies.jump_time -= 1
        if self.x < 0:
            self.destroy()
            Pers.hitpoints = 0
            end_message = games.Message(value="Конец игры",
                                        size=90,
                                        color=color.red,
                                        x=games.screen.width / 2,
                                        y=games.screen.height / 2,
                                        lifetime=5 * games.screen.fps,
                                        after_death=games.screen.quit)
            games.screen.add(end_message)
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
            self.attack_reload = Enemies.attack_reload
class Heal(games.Sprite):
    heal_image = games.load_image("heal.png")
    def update(self):
        self.collide()
    def collide(self):
        for pers in Pers.pers_alive:
            if pers in self.overlapping_sprites:
                if Pers.hitpoints <= 90:
                    Pers.hitpoints += 10
                else:
                    Pers.hitpoints = 100
                self.destroy()
class Boss(games.Sprite):
    hitpoints = 5
    boss_image = games.load_image("bos.png")
    def __init__(self):
        super().__init__(image=Boss.boss_image,
                         angle=0,
                         x=1300,
                         y=random.randint(500,690))
    def update(self):
        self.x -= 1
        if Boss.hitpoints == 0:
            self.destroy()
            Pers.bosses_alive.remove(self)
            Boss.hitpoints = 5
        if self.x < 0:
            end_message = games.Message(value="Конец игры",
                                        size=90,
                                        color=color.red,
                                        x=games.screen.width / 2,
                                        y=games.screen.height / 2,
                                        lifetime=5 * games.screen.fps,
                                        after_death=games.screen.quit)
            games.screen.add(end_message)
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
                Pers.enemies_alive.remove(enemies)
                Pers.value += 1
                Pers.fake_value = Pers.value
                if random.randint(1,5) == 1:
                    heal = Heal(image=Heal.heal_image, x=enemies.x, y=enemies.y, angle=0)
                    games.screen.add(heal)
        for bosses in Pers.bosses_alive:
            if bosses in self.overlapping_sprites:
                Boss.hitpoints -= 1
                self.destroy()
                Pers.value += 1
                Pers.fake_value = Pers.value
class Enemy_attack(games.Sprite):
    fireball_image = games.load_image("pngwing.com.png")
    speed = 10
    def update(self):
        self.x -= Enemy_attack.speed
        if self.x > 1280:
            self.destroy()
        self.collide()

    def collide(self):
        for pers in Pers.pers_alive:
            if pers in self.overlapping_sprites:
                self.destroy()
                Pers.hitpoints -= 10
def menu():
    bg_image = games.load_image("menu_bg.png")
    games.screen.background = bg_image
    games.screen.mainloop()
def game():
    bg_image = games.load_image("them.png")
    games.screen.background = bg_image
    pers = Pers()
    text = Hitpoints()
    score = Score()
    games.screen.add(score)
    games.screen.add(text)
    games.screen.add(pers)
    Pers.pers_alive.append(pers)
    games.screen.mainloop()
def start():
    if Pers.scene == 0:
        menu()
    if Pers.scene == 1:
        game()
start()
