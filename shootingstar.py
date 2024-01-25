import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

NUM_STAR = 200
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 3

BULLET_WIDTH = 2
BULLET_HEIGHT = 8
BULLET_COLOR = 11
BULLET_SPEED = 10

ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
ENEMY_SPEED = 1.5

ENEMY2_WIDTH = 8
ENEMY2_HEIGHT = 17
ENEMY2_SPEED = 2

ENEMY3_WIDTH = 19
ENEMY3_HEIGHT = 8
ENEMY3_SPEED = 0.5
enemies = []
bullets = []


def update_list(list):
    for elem in list:
        elem.update()


def draw_list(list):
    for elem in list:
        elem.draw()


def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.is_alive:
            list.pop(i)
        else:
            i += 1


class Background:
    def __init__(self):
        self.stars = []
        for i in range(NUM_STAR):
            self.stars.append(
                (
                    pyxel.rndi(0, pyxel.width - 1),
                    pyxel.rndi(0, pyxel.height - 1),
                    pyxel.rndf(1, 2.5),
                )
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.stars[i] = (x, y, speed)

    def draw(self):
        for x, y, speed in self.stars:
            pyxel.pset(x, y, pyxel.rndi(1,13))


class Player:
    def __init__(self):
        self.x = pyxel.width / 2
        self.y = pyxel.height - 20
        self.w = PLAYER_WIDTH  
        self.h = PLAYER_HEIGHT  
    def update(self):
        self.x = max(0, min(pyxel.mouse_x - self.w // 2, pyxel.width - self.w))
        self.y = max(0, min(pyxel.mouse_y - self.h // 2, pyxel.height - self.h))


    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.is_alive = True
        bullets.append(self)

    def update(self):
        self.y -= BULLET_SPEED
        if self.y + self.h - 1 < 0:
            self.is_alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.timer_offset = pyxel.rndi(0, 59)
        self.is_alive = True
        enemies.append(self)

    def update(self):
        if (pyxel.frame_count + self.timer_offset) % 60 < 30:
            self.x += ENEMY_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY_SPEED
            self.dir = -1
        self.y += ENEMY_SPEED
        if self.y > pyxel.height - 1:
            self.is_alive = False

    def draw(self):
        pyxel.rect(self.x,self.y,self.w,self.h,pyxel.rndi(1,15))


class Enemy2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY2_WIDTH
        self.h = ENEMY2_HEIGHT
        self.dir = 1
        self.timer_offset = pyxel.rndi(0, 59)
        self.is_alive = True
        enemies.append(self)

    def update(self):
        if (pyxel.frame_count + self.timer_offset) % 60 < 30:
            self.x += ENEMY2_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY2_SPEED
            self.dir = -1
        self.y += ENEMY2_SPEED
        if self.y > pyxel.height - 1:
            self.is_alive = False

    def draw(self):
        pyxel.rect(self.x,self.y,self.w,self.h,pyxel.rndi(2,14))

class Enemy3:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY3_WIDTH
        self.h = ENEMY3_HEIGHT
        self.dir = 1
        self.timer_offset = pyxel.rndi(0, 59)
        self.is_alive = True
        enemies.append(self)

    def update(self):
        if (pyxel.frame_count + self.timer_offset) % 60 < 30:
            self.x += ENEMY3_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY3_SPEED
            self.dir = -1
        self.y += ENEMY3_SPEED
        if self.y > pyxel.height - 1:
            self.is_alive = False

    def draw(self):
         pyxel.rect(self.x, self.y, self.w, self.h, pyxel.rndi(1,15))




class App:
    def __init__(self):
        pyxel.init(120, 160, title="Pyxel Shooter")
        pyxel.image(0).set(
            0,
            0,
            [
                "00c00c00",
                "0c7007c0",
                "0c7007c0",
                "c703b07c",
                "77033077",
                "785cc587",
                "85c77c58",
                "0c0880c0",
            ],
        )
       

        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)
        self.scene = SCENE_TITLE
        self.score = 0
        self.background = Background()
        self.player = Player()  
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            bullets.append(Bullet(self.player.x + self.player.w // 2 - BULLET_WIDTH // 2, self.player.y))
        if pyxel.frame_count % 6 == 0:
            Enemy(pyxel.rndi(0, pyxel.width - ENEMY_WIDTH), 0)
        if pyxel.frame_count % 15 == 0:
            Enemy2(pyxel.rndi(0, pyxel.width - ENEMY2_WIDTH), 0)
        if pyxel.frame_count % 15 == 0:
            Enemy3(pyxel.rndi(0, pyxel.width - ENEMY3_WIDTH), 0)
       

        for enemy in enemies:
            for bullet in bullets:
                if (
                    enemy.x + enemy.w > bullet.x
                    and bullet.x + bullet.w > enemy.x
                    and enemy.y + enemy.h > bullet.y
                    and bullet.y + bullet.h > enemy.y
                ):
                    enemy.is_alive = False
                    bullet.is_alive = False
                    pyxel.play(3, 1)
                    self.score += 10

        for enemy in enemies:
            if (
                self.player.x + self.player.w > enemy.x
                and enemy.x + enemy.w > self.player.x
                and self.player.y + self.player.h > enemy.y
                and enemy.y + enemy.h > self.player.y
            ):
                enemy.is_alive = False
                pyxel.play(3, 1)
                self.scene = SCENE_GAMEOVER
                pyxel.playm(0, loop=True)

        update_list(bullets)
        update_list(enemies)
        cleanup_list(enemies)
        cleanup_list(bullets)

        self.player.update()

    def update_gameover_scene(self):
        update_list(bullets)
        update_list(enemies)
        cleanup_list(enemies)
        cleanup_list(bullets)

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0
            enemies.clear()
            bullets.clear()
            pyxel.playm(1, loop=True)

    def draw(self):
        pyxel.cls(0)
        self.background.draw()
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    def draw_title_scene(self):
        pyxel.text(35, 66, "shoooothing star", pyxel.frame_count % 16)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
    def draw_gameover_scene(self):
        draw_list(bullets)
        draw_list(enemies)
        pyxel.text(43, 66, "GAME OVER", 8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)


App()
