import pygame
import random
import sys
import os

pygame.init()
screen = pygame.display.set_mode((1350, 760), pygame.NOFRAME)
SIZE = WIDTH, HEIGHT = screen.get_size()
FPS = 50
FPS_WINDOW = 8
X, Y = screen.get_size()
tile_width = tile_height = 45


def load_image(file, colorkey=None):
    fullname = os.path.join('data', file)
    if not os.path.isfile(fullname):
        print(file)
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = 'data/' + filename
    if not os.path.isfile(filename):
        print('file')
        sys.exit()
    with open(filename, 'r', encoding='utf-8') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class StoryLine(pygame.sprite.Sprite):
    def __init__(self):
        super(StoryLine, self).__init__(all_sprites, story_sprites)
        self.image = pygame.transform.scale(load_image('wizzard.png'), (50, 100))
        self.rect = self.image.get_rect().move(12 * tile_width, 10 * tile_height + 30)
        self.dialog_list = ['Добро пожаловать в подземелье!', 'Первым делом возьми оружие из сундука',
                            'Хорошо. Теперь можно отправляться в путь...',
                            'Для этого подойди к красному или синему фонтану',
                            'В красном фонтане тебя ждет Монстр', 'В синем фонтане тебя ждет испытание',
                            'Чтобы покинуть подземелье подойди к двери', 'Желаю удачи!']
        self.number = 0
        self.gun = False
        self.fountain = False
        self.mask = pygame.mask.from_surface(self.image)
        self.player = False

    def update(self):
        try:
            if not player.gun is None:
                self.number += 1
                font = pygame.font.Font(None, 50)
                text = font.render(self.dialog_list[self.number], True, (255, 255, 255))
                screen.blit(text, (self.rect.x - text.get_size()[0] // 2, self.rect.y - 13))
                pygame.display.flip()
            elif player.gun is None and self.gun:
                font = pygame.font.Font(None, 50)
                text = font.render(self.dialog_list[self.number], True, (255, 255, 255))
                screen.blit(text, (self.rect.x - text.get_size()[0] // 2, self.rect.y - 13))
                pygame.display.flip()
            elif player.gun is None and not self.gun:
                font = pygame.font.Font(None, 50)
                text = font.render(self.dialog_list[self.number], True, (255, 255, 255))
                screen.blit(text, (self.rect.x - text.get_size()[0] // 2, self.rect.y - 13))
                pygame.display.flip()
                self.number += 1
            if self.number == 1:
                self.gun = True
            if self.number == 6:
                self.fountain = True
        except IndexError:
            pass

    def anim_player(self):
        if self.number < len(self.dialog_list):
            if self.player:
                font = pygame.font.Font(None, 50)
                text = font.render('E', True, (255, 255, 255))
                screen.blit(text, (self.rect.x + 15, self.rect.y - 13))
                pygame.display.flip()


class Flour(pygame.sprite.Sprite):
    def __init__(self, typer, x, y):
        if typer in '!#|%\\':
            super().__init__(wall_sprites, all_sprites)
        else:
            super().__init__(tile_sprites, all_sprites)
        self.type = typer
        self.image = pygame.transform.scale(load_image(tiles[typer]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)


class Decor(pygame.sprite.Sprite):
    def __init__(self, typer, x, y):
        if typer in 'L':
            super(Decor, self).__init__(all_sprites, column_sprites)
        elif typer in 'H':
            super(Decor, self).__init__(all_sprites, column_up_sprites)
        else:
            super(Decor, self).__init__(all_sprites, decor_sprites)
        self.type = typer
        self.image = pygame.transform.scale(load_image(decor[typer]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)


class Door(pygame.sprite.Sprite):
    def __init__(self, typer, x, y):
        super(Door, self).__init__(all_sprites, door_sprites)
        self.image = pygame.transform.scale(load_image(decor[typer]), (100, 100))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.player = False
        self.x = None
        self.y = None

    def anim_player(self):
        if self.player:
            font = pygame.font.Font(None, 50)
            text = font.render('P', True, (255, 255, 255))
            screen.blit(text, (self.x, self.y))
            pygame.display.flip()


class RedFountain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(RedFountain, self).__init__(all_sprites, red_fountain)
        self.list_image = ['wall_fountain_mid_red_anim_f0.png', 'wall_fountain_mid_red_anim_f1.png',
                           'wall_fountain_mid_red_anim_f2.png']
        self.number = 0
        self.image = pygame.transform.scale(load_image(self.list_image[self.number % 3]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)

        self.player = False
        self.x = None
        self.y = None

    def update(self):
        self.number += 0.2
        self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))

    def anim_player(self):
        if self.player:
            font = pygame.font.Font(None, 50)
            text = font.render('E', True, (255, 255, 255))
            screen.blit(text, (self.x, self.y))
            pygame.display.flip()


class RedFountainFloor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(RedFountainFloor, self).__init__(all_sprites, red_fountain_floor, tile_sprites)
        self.list_image = ['wall_fountain_basin_red_anim_f0.png', 'wall_fountain_basin_red_anim_f1.png',
                           'wall_fountain_basin_red_anim_f2.png']
        self.number = 0
        self.image = pygame.transform.scale(load_image(self.list_image[self.number % 3]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.number += 0.2
        self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))


class BlueFountain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BlueFountain, self).__init__(all_sprites, blue_fountain)
        self.list_image = ['wall_fountain_mid_blue_anim_f0.png', 'wall_fountain_mid_blue_anim_f1.png',
                           'wall_fountain_mid_blue_anim_f2.png']
        self.number = 0
        self.image = pygame.transform.scale(load_image(self.list_image[self.number % 3]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.player = False
        self.x = None
        self.y = None

    def update(self):
        self.number += 0.2
        self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))

    def anim_player(self):
        if self.player:
            font = pygame.font.Font(None, 50)
            text = font.render("E", True, (255, 255, 255))
            screen.blit(text, (self.x, self.y))
            pygame.display.flip()


class BlueFountainFloor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BlueFountainFloor, self).__init__(all_sprites, blue_fountain_floor, tile_sprites)
        self.list_image = ['wall_fountain_basin_blue_anim_f0.png', 'wall_fountain_basin_blue_anim_f1.png',
                           'wall_fountain_basin_blue_anim_f2.png']
        self.number = 0
        self.image = pygame.transform.scale(load_image(self.list_image[self.number % 3]), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.number += 0.2
        self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))


class BoxKnife(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BoxKnife, self).__init__(all_sprites, chest_sprites)
        self.image = pygame.transform.scale(load_image('chest_empty_open_anim_f0.png'), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.player = False
        self.x = None
        self.y = None
        self.list_image = ['chest_empty_open_anim_f0.png', 'chest_empty_open_anim_f1.png',
                           'chest_empty_open_anim_f2.png']
        self.number = 0
        self.open = False

    def update(self):
        if story.gun:
            if self.player:
                if not self.open:
                    font = pygame.font.Font(None, 50)
                    text = font.render('E', True, (255, 255, 255))
                    screen.blit(text, (self.x, self.y))
                    pygame.display.flip()

    def anim(self):
        self.number += 0.2
        if not self.open:
            self.image = pygame.transform.scale(load_image(self.list_image[int(self.number) % 3]), (50, 50))


class Knife(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Knife, self).__init__(all_sprites, gun_sprtites)
        self.image = pygame.transform.scale(load_image('weapon_duel.png'), (30, 65))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.number = 0
        self.damage = 2

    def attack(self):
        running = True
        while running:
            for event in boss_sprites:
                if player.rect.x + player.rect.w + 32 >= event.rect.x:
                    event.hp -= self.damage
            running = False

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Sheeps(pygame.sprite.Sprite):       # Sheeps типо шипы ^_^
    def __init__(self, x, y):
        super(Sheeps, self).__init__(all_sprites, tile_sprites, spikes_sprites)
        self.image = pygame.transform.scale(load_image('floor_spikes_f0.png'), (50, 50))
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.frames = ['floor_spikes_f0.png', 'floor_spikes_f1.png', 'floor_spikes_f2.png', 'floor_spikes_f3.png']
        self.frame = 'floor_spikes_f0.png'
        self.number = 0
        self.time = 0.5
        self.skipe = 0

    def update(self):
        if int(self.time) % 100 == 0:
            self.number += 0.1
            self.image = pygame.transform.scale(load_image(self.frames[int(self.number) % len(self.frames)]), (50, 50))
            if int(self.number) % len(self.frames) == 0 and int(self.number) != 0:
                self.time += 0.2
                self.image = pygame.transform.scale(load_image('floor_spikes_f0.png'), (50, 50))
        else:
            self.skipe = int(self.number)
            self.time += 0.5

    def player(self):
        if pygame.sprite.collide_mask(self, player):
            if int(self.number) % len(self.frames) == 0 and int(self.number) != self.skipe:
                if not player.damage:
                    player.hp -= 1
                    player.damage = True #


class HealfPoints(pygame.sprite.Sprite):
    def __init__(self, x, y, typer):
        super(HealfPoints, self).__init__(all_sprites, hp_sprites)
        if typer == 1:
            self.image = pygame.transform.scale(load_image('ui_heart_full.png'), (30, 30))
        elif typer == 2:
            self.image = pygame.transform.scale(load_image('ui_heart_half.png'), (30, 30))
        elif typer == 3:
            self.image = pygame.transform.scale(load_image('ui_heart_empty.png'), (30, 30))
        self.rect = self.image.get_rect().move(x, y)


class FireBall(pygame.sprite.Sprite):
    fire = load_image('FB001.png', -1)

    def __init__(self, x, y):
        super(FireBall, self).__init__(all_sprites, fireball_sprites)
        self.image = pygame.transform.scale(FireBall.fire, (60, 60))
        self.rect = self.image.get_rect().move(x, y)
        self.frames = ['FB001.png', 'FB002.png', 'FB003.png', 'FB004.png']
        self.frame = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x):
        self.frame += 0.5
        if int(self.frame) % 5 == 0:
            self.image = pygame.transform.scale(load_image(self.frames[int(self.frame) % len(self.frames)],
                                                           -1), (60, 60))
        self.rect.x += x
        running = True
        while running:
            for event in wall_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.kill()
                    break
            for event in player_sprites:
                if pygame.sprite.collide_mask(self, event):
                    event.hp -= 2.5
                    self.kill()
                    break
            running = False


class Player(pygame.sprite.Sprite):
    player = 'lizard_idle_f0.png'
    left_player = 'lizard_idle_f0.png'

    def __init__(self, x=None, y=None):
        super(Player, self).__init__(player_sprites)
        self.image = pygame.transform.scale(load_image(Player.player), (50, 100))
        if x is None and y is None:
            self.rect = self.image.get_rect().move(10 * tile_width, 11 * tile_height + 30)
        else:
            self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.frames = ['lizard_run_f0.png', 'lizard_run_f1.png', 'lizard_run_f2.png',
                       'lizard_run_f3.png', 'lizard_run_f0.png']
        self.frame = 0
        self.hp = 5
        self.gun = None
        self.damage = False
        self.time = 0
        self.see = 'r'

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        running = True
        while running:
            for fkn in story_sprites:
                fkn.player = False
            for event in boss_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.hp -= 0.5
                    self.rect.x -= x
                    self.rect.y -= y
            for event in wall_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    running = False
            for fkn in story_sprites:
                if pygame.sprite.collide_mask(self, fkn):
                    self.rect.x -= x
                    self.rect.y -= y
                    running = False
                    fkn.player = True
            for event in door_sprites:
                event.player = False
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    running = False
                    event.player = True
                    event.x = self.rect.x + 15
                    event.y = self.rect.y - 13
            for event in red_fountain:
                event.player = False
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    running = False
                    for fkn in story_sprites:
                        if fkn.fountain or time_level:
                            if not self.gun is None:
                                event.player = True
                                event.x = self.rect.x + 15
                                event.y = self.rect.y - 13
            for event in blue_fountain:
                event.player = False
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    running = False
                    for fkn in story_sprites:
                        if fkn.fountain or boss_level:
                            if not self.gun is None:
                                event.player = True
                                event.x = self.rect.x + 15
                                event.y = self.rect.y - 13
            for event in spikes_sprites:
                if pygame.sprite.collide_mask(self, event):
                    if event.frame == 'floor_spikes_f2.png' or event.frame == 'floor_spikes_f3.png':
                        player.hp -= 1
            for event in chest_sprites:
                event.player = False
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    running = False
                    if not event.open:
                        event.player = True
                        event.x = self.rect.x + 15
                        event.y = self.rect.y - 13
            for event in decor_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    running = False
            for event in wall_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.rect.x -= x
                    self.rect.y -= y
                    running = False
            for event in spikes_sprites:
                if pygame.sprite.collide_mask(self, event):
                    if event.frame == 'floor_spikes_f2.png' or event.frame == 'floor_spikes_f3.png':
                        player.hp -= 1
            running = False

    def anim(self, type):
        self.see = type
        if type == 'r':
            self.frame += 0.2
            self.image = pygame.transform.scale(load_image(self.frames[int(self.frame) % len(self.frames)]), (50, 100))
        elif type == 'l':
            self.frame += 0.2
            player.image = pygame.transform.flip(pygame.transform.scale(
                load_image(self.frames[int(self.frame) % len(self.frames)]), (50, 100)),
                True, False)

    def move_level(self, x, y):
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height - 30


class Boss(pygame.sprite.Sprite):
    boss = 'big_demon_idle_anim_f0.png'

    def __init__(self, x, y):
        super(Boss, self).__init__(all_sprites, boss_sprites)
        self.see = 'l'
        self.image = pygame.transform.flip(
            pygame.transform.scale(load_image(Boss.boss), (115, 150)),
            True, False)
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height + 30)
        self.figth = True
        self.hp = 62
        self.speed = 15
        self.mask = pygame.mask.from_surface(self.image)
        self.see = 'l'
        self.frame = 0
        self.frames = ['big_demon_idle_anim_f0.png', 'big_demon_idle_anim_f1.png', 'big_demon_idle_anim_f2.png',
                       'big_demon_idle_anim_f3.png']
        self.attack_num = 0

    def update(self):
        y = self.rect.y
        if player.rect.y < self.rect.y:
            self.rect.y -= self.speed
        elif player.rect.y > self.rect.y:
            self.rect.y += self.speed
        running = True
        while running:
            for event in wall_sprites:
                if pygame.sprite.collide_mask(self, event):
                    self.rect.y = y
            running = False

    def attack(self):
        self.attack_num += 0.2
        if int(self.attack_num) % 20 == 0 and int(self.attack_num) != 0:
            FireBall(self.rect.x - 20, self.rect.y + 20)
            self.attack_num += 1

    def anim(self):
        self.frame += 0.2
        self.image = pygame.transform.flip(pygame.transform.scale(
            load_image(self.frames[int(self.frame) % len(self.frames)]), (115, 150)),
            True, False)


def generate_level(level):
    for i in range(len(level)):
        for j in range(len(level[0])):
            if level[i][j] == 'A':
                BlueFountainFloor(j, i)
            elif level[i][j] == 'E':
                BlueFountain(j, i)
            elif level[i][j] == 'W':
                RedFountain(j, i)
            elif level[i][j] in list(tiles):
                Flour(level[i][j], j, i)
            elif level[i][j] == 'D':
                Door(level[i][j], j, i)
            elif level[i][j] == 'V':
                BoxKnife(j, i)
            elif level[i][j] == 'Q':
                RedFountainFloor(j, i)
            elif level[i][j] == ';':
                Sheeps(j, i)
            elif level[i][j] in list(decor):
                Decor(level[i][j], j, i)


def terminate():
    pygame.quit()
    sys.exit()


def start_window():
    global intro_rect, x_t, string_rendered

    text = ['LIZARD IN DUNGEON', '', 'Нажмите ПРОБЕЛ, чтобы начать игру']
    score_fon = 0
    font1 = pygame.font.Font('fonts/press-start-2p-regular.ttf', 60)
    font2 = pygame.font.Font('fonts/press-start-2p-regular.ttf', 35)
    while True:
        text_coord = 50
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_SPACE:
                    main()
        screen.blit(pygame.transform.scale(load_image(f'start{score_fon % 3}.png'),
                                           (X, Y)), (0, 0))
        for elem in text:
            if 'DUNGEON' in elem:
                string_rendered = font1.render(elem, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord = 170
                intro_rect.top = text_coord
            elif 'ПРОБЕЛ' in elem:
                string_rendered = font2.render(elem, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord += 50
                intro_rect.top = text_coord
            intro_rect.x = X // 2 - x_t // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        score_fon += 1
        pygame.display.flip()
        clock.tick(FPS_WINDOW)


def main():
    global run, time, fire, level_1, level_3, level_2, player, boss, time_level, boss_level, story, gun
    while run:
        num = player.hp
        if float(num) <= 0.0:
            run = False
            ending()
        x, y = 40, 0
        for k in range(5):
            if num >= 1:
                num -= 1
                HealfPoints(x, y, 1)
            elif num >= 0.5:
                num -= 0.5
                HealfPoints(x, y, 2)
            else:
                HealfPoints(x, y, 3)
            x += 30
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                ending()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                ending()
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.image = pygame.transform.scale(
                    load_image(Player.player) if player.see == 'r' else pygame.transform.flip(
                        load_image(Player.left_player), True, False), (50, 100))
                if player.gun:
                    image = gun.image
                    number = 0
                    for i in range(30):
                        number += 0.2
                        if int(number) % 20 == 0:
                            if player.see == 'r':
                                gun.image = pygame.transform.rotate(gun.image, -10)
                            elif player.see == 'l':
                                gun.update(player.rect.x - 20 - 10 * i, player.rect.y + 5)
                                gun.image = pygame.transform.rotate(gun.image, 10)
                        screen.fill('red')
                        tile_sprites.draw(screen), wall_sprites.draw(screen), decor_sprites.draw(screen)
                        door_sprites.draw(screen), chest_sprites.draw(screen), blue_fountain.draw(screen)
                        red_fountain.draw(screen), column_sprites.draw(screen), gun_sprtites.draw(screen)
                        player_sprites.draw(screen), column_up_sprites.draw(screen), story_sprites.draw(screen)
                        hp_sprites.draw(screen), boss_sprites.draw(screen)
                        if level_2:
                            boss.update()
                            boss.anim()
                            boss.attack()
                            for j in fireball_sprites:
                                j.update(-5)
                        fireball_sprites.draw(screen)
                        if i == 28:
                            gun.attack()
                        pygame.display.flip()
                        for j in blue_fountain:
                            j.update()
                        for j in red_fountain:
                            j.update()
                        clock.tick(FPS)
                    gun.image = image
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    dic['right'] = True
                if event.key == pygame.K_a:
                    dic['left'] = True
                if event.key == pygame.K_w:
                    dic['top'] = True
                if event.key == pygame.K_s:
                    dic['down'] = True
                if event.key == pygame.K_p:
                    for door in door_sprites:
                        if door.player:
                            ending()
                if event.key == pygame.K_e:
                    for story in story_sprites:
                        for ch in chest_sprites:
                            if not (story.gun and not (boss_level or time_level) and not ch.open and ch.player):
                                continue
                            if player.see == 'r':
                                player_image = pygame.transform.scale(load_image(Player.player), (50, 100))
                            else:
                                player_image = pygame.transform.flip(
                                    pygame.transform.scale(load_image(Player.left_player), (50, 100)), True, False)
                            for k in range(10):
                                ch.anim()
                            ch.open = True
                            gun = Knife(ch.rect.x // tile_width + 0.2, ch.rect.y // tile_height - 1.5)
                            player.gun = gun
                            for k in range(70):
                                gun_sprtites.draw(screen), chest_sprites.draw(screen)
                                for j in blue_fountain:
                                    j.update()
                                for j in red_fountain:
                                    j.update()
                                red_fountain.draw(screen), blue_fountain.draw(screen)
                                clock.tick(FPS)
                                pygame.display.flip()
                        if not boss_level and not time_level:
                            if story.player and story.number < 7:
                                if player.see == 'r':
                                    player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                                else:
                                    player.image = pygame.transform.flip(
                                        pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                                        True, False)
                                if story.number == 6:
                                    start = True
                                screen.fill('black')
                                tile_sprites.draw(screen), wall_sprites.draw(screen), gun_sprtites.draw(screen)
                                player_sprites.draw(screen), decor_sprites.draw(screen), chest_sprites.draw(screen)
                                blue_fountain.draw(screen), story_sprites.draw(screen), hp_sprites.draw(screen)
                                door_sprites.draw(screen), column_sprites.draw(screen), red_fountain.draw(screen)
                                column_up_sprites.draw(screen)
                                story.update()
                                for i in range(70):
                                    for j in blue_fountain:
                                        j.update()
                                    for j in red_fountain:
                                        j.update()
                                    red_fountain.draw(screen)
                                    blue_fountain.draw(screen)
                                    clock.tick(FPS)
                                    pygame.display.flip()
                        if (story.fountain or time_level or boss_level) and not boss_level:
                            for i in red_fountain:
                                if i.player:
                                    for ii in all_sprites:
                                        ii.kill()
                                    del story
                                    generate_level(load_level('level_2.txt'))
                                    player.move_level(x=9, y=7)
                                    player.see = 'r'
                                    boss = Boss(x=26, y=6)
                                    gun = Knife(player.rect.x + 20, player.rect.y + 5)
                                    player.gun = gun
                                    level_1 = False
                                    level_2 = True
                                    level_3 = False
                        elif (story.fountain or time_level or boss_level) and not time_level:
                            for i in blue_fountain:
                                if i.player:
                                    for j in all_sprites:
                                        if j not in list(player_sprites):
                                            j.kill()
                                    del story
                                    generate_level(load_level('level_3.txt'))
                                    player.rect.move(9 * tile_width, 7 * tile_height + 30)
                                    player.see = 'r'
                                    gun = Knife(player.rect.x + 20, player.rect.y + 5)
                                    player.gun = gun
                                    level_1 = False
                                    level_2 = False
                                    level_3 = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    dic['right'] = False
                    player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                    player.frame = 0
                if event.key == pygame.K_a:
                    dic['left'] = False
                    player.image = pygame.transform.flip(
                        pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                        True, False)
                    player.frame = 0
                if event.key == pygame.K_w:
                    dic['top'] = False
                    if player.see == 'r':
                        player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                    else:
                        player.image = pygame.transform.flip(
                            pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                            True, False)
                    player.frame = 0
                if event.key == pygame.K_s:
                    dic['down'] = False
                    if player.see == 'r':
                        player.image = pygame.transform.scale(load_image(Player.player), (50, 100))
                    else:
                        player.image = pygame.transform.flip(
                            pygame.transform.scale(load_image(Player.left_player), (50, 100)),
                            True, False)
                    player.frame = 0
        if dic['right']:
            player.update(10, 0)
            player.anim('r')
        if dic['left']:
            player.update(-10, 0)
            player.anim('l')
        if dic['top']:
            player.anim(player.see)
            player.update(0, -10)
        if dic['down']:
            player.update(0, 10)
            player.anim(player.see)
        if level_2:
            boss.update()
            boss.anim()
            boss.attack()
            for event in fireball_sprites:
                event.update(-5)
        if level_3:
            fire += 0.2
            if int(fire) % 5 == 0 and int(fire) != 0:
                FireBall(28 * tile_width, random.randint(1, 15) * tile_height + 30)
                fire += 0.2
                time += 1
            for i in fireball_sprites:
                i.update(-5)
        screen.fill('black')
        tile_sprites.draw(screen), wall_sprites.draw(screen), decor_sprites.draw(screen)
        door_sprites.draw(screen), column_sprites.draw(screen), fireball_sprites.draw(screen)
        chest_sprites.draw(screen), blue_fountain.draw(screen), red_fountain.draw(screen)
        if level_2:
            boss_sprites.draw(screen)
            if boss.figth:
                num = player.hp
                if float(num) == 0.0:
                    run = False
                    terminate()
                x, y = 40, 0
                hp_list = [1 if num - 1 >= 0 else 2 if num - 0.5 >= 0 else 3 for _ in range(5)]
                hp_sprites.add(HealfPoints(x + 30 * i, y, hp_type) for i, hp_type in enumerate(hp_list))

                for k in range(200):
                    if k % 5 == 0 and k != 0:
                        boss.anim()
                    tile_sprites.draw(screen), wall_sprites.draw(screen)
                    if not player.gun is None:
                        if player.see == 'r':
                            gun.update(player.rect.x + 20, player.rect.y + 5)
                        elif player.see == 'l':
                            gun.update(player.rect.x, player.rect.y + 5)
                    gun_sprtites.draw(screen), player_sprites.draw(screen)
                    boss_sprites.draw(screen), hp_sprites.draw(screen)
                    pygame.display.flip()
                    boss.figth = False
        if not player.gun is None:
            if player.see == 'r':
                gun.update(player.rect.x + 20, player.rect.y + 5)
            elif player.see == 'l':
                gun.update(player.rect.x, player.rect.y + 5)
            gun_sprtites.draw(screen)
        player_sprites.draw(screen), column_up_sprites.draw(screen), story_sprites.draw(screen), hp_sprites.draw(screen)
        player.time += 1
        if player.time % 100 == 0:
            player.damage = False
        for i in blue_fountain:
            i.update()
            i.anim_player()
        for i in red_fountain:
            i.update()
            i.anim_player()
        for i in blue_fountain_floor:
            i.update()
        for i in red_fountain_floor:
            i.update()
        for i in chest_sprites:
            i.update()
        for i in spikes_sprites:
            i.update()
        num = player.hp
        for story in story_sprites:
            story.anim_player()
        for event in spikes_sprites:
            event.player()
        for event in door_sprites:
            event.anim_player()
        pygame.display.flip()
        if level_2:
            if boss.hp <= 60.0:
                for i in all_sprites:
                    i.kill()
                level_2, level_3, level_1 = False, False, True
                generate_level(load_level('level.txt'))
                generate_level(load_level('decor_level.txt'))
                story = StoryLine()
                player.move_level(9, 11)
                boss_level = True
                player.gun = Knife(1, 1)
                gun = player.gun
                if player.see == 'r':
                    gun.update(player.rect.x + 20, player.rect.y + 5)
                elif player.see == 'l':
                    gun.update(player.rect.x, player.rect.y + 5)
        if level_3:
            if time == 40:
                for i in all_sprites:
                    i.kill()
                level_2, level_3, level_1 = False, False, True
                generate_level(load_level('level.txt'))
                generate_level(load_level('decor_level.txt'))
                story = StoryLine()
                player.move_level(10, 11)
                time_level = True
                player.gun = Knife(1, 1)
                gun = player.gun
                if player.see == 'r':
                    gun.update(player.rect.x + 20, player.rect.y + 5)
                elif player.see == 'l':
                    gun.update(player.rect.x, player.rect.y + 5)
        if time_level and boss_level:
            if level_1:
                for i in all_sprites:
                    i.kill()
                level_2, level_3, level_1 = False, False, True
                generate_level(load_level('level.txt'))
                generate_level(load_level('decor_level.txt'))
                story = StoryLine()
                player.move_level(10, 11)
                time_level = True
                player.gun = Knife(1, 1)
                gun = player.gun
                if player.see == 'r':
                    gun.update(player.rect.x + 20, player.rect.y + 5)
                elif player.see == 'l':
                    gun.update(player.rect.x, player.rect.y + 5)
                level_1 = False
        clock.tick(FPS)


def ending():
    global intro_rect, string_rendered

    intro_text = ['GAME OVER', '',
                  f'У вас {player.hp * 1.5} очков',
                  'Для завершения нажмите ПРОБЕЛ']

    font1 = pygame.font.Font('fonts/press-start-2p-regular.ttf', 60)
    font2 = pygame.font.Font('fonts/press-start-2p-regular.ttf', 40)
    switching_fon = 0
    while True:
        text_coord = 50
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    terminate()
        screen.blit(pygame.transform.scale(load_image(f'start{switching_fon % 3}.png'), (X, Y)), (0, 0))
        for line in intro_text:
            if 'GAME OVER' == line:
                string_rendered = font1.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord = 50
                intro_rect.top = text_coord
                intro_rect.x = X // 2 - x_t // 2
                text_coord += intro_rect.height
            elif 'У вас' in line:
                string_rendered = font2.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord += 70
                intro_rect.top = text_coord
                intro_rect.x = X // 2 - x_t // 2
                text_coord += intro_rect.height
            elif 'ПРОБЕЛ' in line:
                string_rendered = font2.render(line, True, pygame.Color('white'))
                x_t, y_t = string_rendered.get_size()
                intro_rect = string_rendered.get_rect()
                text_coord += 100
                intro_rect.top = text_coord
                intro_rect.x = X // 2 - x_t // 2
                text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        switching_fon += 1
        pygame.display.flip()
        clock.tick(FPS_WINDOW)


tiles = {'$': 'floor_1.png', '@': 'floor_8.png', '^': 'floor_2.png', '*': 'floor_7.png',
         '(': 'floor_4.png', '№': 'floor_3.png', ')': 'floor_5.png', '+': 'floor_6.png',
         '>': 'floor_ladder.png', '<': 'hole.png', '#': 'wall_hole_1.png', '!': 'wall_mid.png',
         '%': 'wall_banner_green.png', '|': 'wall_side_front_left.png', '\\': 'wall_side_front_right.png',
         'Q': 'wall_fountain_basin_red_anim_f2.png', 'A': 'wall_fountain_basin_blue_anim_f2.png',
         '&': 'wall_banner_yellow.png', ';': 'floor_spikes_anim_f0.png'}

decor = {'H': 'column_top.png', 'M': 'column_mid.png', 'L': 'coulmn_base.png', 'S': 'wall_side_mid_left.png',
         'P': 'wall_side_mid_right.png', 'T': 'wall_left.png', 'C': 'wall_mid.png', 'R': 'wall_corner_right.png',
         'O': 'wall_corner_left.png', '_': 'wall_top_mid.png', 'I': 'wall_inner_corner_l_top_left.png',
         'U': 'wall_inner_corner_l_top_rigth.png', 'J': 'wall_corner_top_left.png', 'G': 'wall_corner_top_right.png',
         'W': 'wall_fountain_mid_red_anim_f2.png', 'E': 'wall_fountain_mid_blue_anim_f2.png',
         'D': 'doors_leaf_closed.png', 'B': 'crate.png', 'V': 'chest_empty_open_anim_f0.png',
         'N': 'wall_right.png'}

run = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()
door_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
decor_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
column_sprites = pygame.sprite.Group()
blue_fountain = pygame.sprite.Group()
red_fountain = pygame.sprite.Group()
blue_fountain_floor = pygame.sprite.Group()
red_fountain_floor = pygame.sprite.Group()
chest_sprites = pygame.sprite.Group()
gun_sprtites = pygame.sprite.Group()
story_sprites = pygame.sprite.Group()
spikes_sprites = pygame.sprite.Group()
hp_sprites = pygame.sprite.Group()
column_up_sprites = pygame.sprite.Group()
boss_sprites = pygame.sprite.Group()
fireball_sprites = pygame.sprite.Group()
player = Player()
story = StoryLine()
boss_level = False
time_level = False
fire = 0
time = 0
dic = {'right': False, 'left': False, 'top': False, 'down': False}
generate_level(load_level('level.txt'))
generate_level(load_level('decor_level.txt'))
flag_gun = True
level_1 = True
level_2 = False
level_3 = False

start_window()
pygame.quit()
