from pico2d import *
import game_framework
import math


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)


class Mouse:
    def __init__(self):
        self.x, self.y = 0, 90
        self.image = load_image('hand_arrow.png')

    def draw(self):
        # hide_cursor()
        self.image.draw(self.x + 20, self.y - 25)


class Explosive:
    def __init__(self):
        self.x, self.y = 800, 300
        self.speed_x, self.speed_y = 0, 0
        self.explode = False
        self.image = load_image('ball21x21.png')

    def update(self):

        self.y += self.speed_y
        self.x += self.speed_x

        if self.y > 60:
            self.speed_y -= 0.01
        else:
            self.explode = True

    def launch(self, x, y, dir_x, dir_y):

        self.x, self.y = x, y
        if dir_x > x:
            self.speed_x += math.log(dir_x - x, 50)
        else:
            self.speed_x -= math.log(x - dir_x, 50)
        if dir_y > y:
            self.speed_y += math.log(dir_y - y, 50)
        else:
            self.speed_y -= math.log(y - dir_y, 50)

    def draw(self):
        self.image.draw(self.x, self.y)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.speed_x, self.speed_y = 0, 0
        self.jump = False
        self.left = False
        self.right = False
        self.dir = True  # 오른쪽
        self.airborne = False
        self.image = load_image('animation_sheet.png')

    def update(self):
        self.frame = (self.frame + 1) % 128

        self.y += self.speed_y
        self.x += self.speed_x

        if self.jump and self.y <= 90:
            self.y = 90
            self.speed_y = 1
            self.airborne = True
            self.jump = False
            # self.speed_x -= 0.1

        if self.right:
            if self.speed_x < 0.5:
                self.speed_x += 0.1
            self.dir = True

        if self.left:
            if self.speed_x > -0.5:
                self.speed_x -= 0.1
            self.dir = False

        if self.airborne:
            if self.y > 90:
                self.speed_y -= 0.01
            else:
                if self.y < 90:
                    self.y = 90
                    self.speed_y = 0
                    self.airborne = False
        else:
            if self.speed_x < -1 or self.speed_x > 1:
                self.speed_x = self.speed_x / 2
            elif self.speed_x > 0.01:
                self.speed_x -= 0.01
            elif self.speed_x < -0.01:
                self.speed_x += 0.01
            else:
                self.speed_x = 0

        if self.x > 1600:
            self.x = 0
            # self.speed_x = 0
        elif self.x < 0:
            self.x = 1600
            # self.speed_x = 0

    def draw(self):

        if self.dir:
            if self.speed_x > 0:
                self.image.clip_draw((self.frame // 32) * 100, 100, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw((self.frame // 32) * 100, 300, 100, 100, self.x, self.y)
        else:
            if self.speed_x < 0:
                self.image.clip_draw((self.frame // 32) * 100, 0, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw((self.frame // 32) * 100, 200, 100, 100, self.x, self.y)

    def ramp(self):
        # self.speed_y = self.speed_x / 2 + self.speed_y
        self.speed_x, self.speed_y = self.speed_y, self.speed_x

    def explosion(self, explode_x, explode_y):

        # if (explode_x - self.x) ** 2 + (explode_y - self.y) ** 2 < 90000:
        #     self.airborne = True
        #
        #     if self.x > explode_x:
        #         self.speed_x += 3
        #     else:
        #         self.speed_x -= 3
        #
        #     if self.y > explode_y:
        #         self.speed_y += 3
        #     else:
        #         self.speed_y -= 3
        #
        #     self.speed_x -= (self.x - explode_x) / 100
        #     self.speed_y -= (self.y - explode_y) / 100

        self.airborne = True

        if explode_x > self.x:
            self.speed_x -= math.log(explode_x - self.x, 50)
        else:
            self.speed_x += math.log(self.x - explode_x, 50)
        if explode_y > self.y:
            self.speed_y -= math.log(explode_y - self.y, 50)
        else:
            self.speed_y += math.log(self.y - explode_y, 50)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouse.x, mouse.y = event.x, 600 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                boy.explosion(event.x, 600 - event.y)
            elif event.button == SDL_BUTTON_RIGHT:
                explosives.append(Explosive())
                explosives[-1].launch(boy.x, boy.y, event.x, 600 - event.y)
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.quit()
                case pico2d.SDLK_SPACE:
                    boy.jump = True
                case pico2d.SDLK_a:
                    boy.left = True
                case pico2d.SDLK_d:
                    boy.right = True
                case pico2d.SDLK_q:
                    boy.x, boy.y = 400, 90
                    boy.speed_x, boy.speed_y = 0, 0
                case pico2d.SDLK_e:
                    boy.ramp()
        elif event.type == SDL_KEYUP:
            match event.key:
                case pico2d.SDLK_a:
                    boy.left = False
                case pico2d.SDLK_d:
                    boy.right = False


boy = None
explosives = None
grass = None
running = None
mouse = None


def enter():
    global boy, explosives, mouse, grass, running
    boy = Boy()
    explosives = [Explosive()]
    mouse = Mouse()
    grass = Grass()
    running = True


def exit():
    global boy, explosives, mouse, grass
    del boy
    del explosives
    del mouse
    del grass


def update():
    boy.update()
    for explosive in explosives:
        explosive.update()
        if explosive.explode:
            boy.explosion(explosive.x, explosive.y)
            explosives.remove(explosive)


def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    grass.draw()
    mouse.draw()
    boy.draw()
    for explosive in explosives:
        explosive.draw()


def pause():
    pass


def resume():
    pass
