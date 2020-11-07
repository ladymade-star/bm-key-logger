
import pyglet
import ctypes
import datetime
import json
import copy
from collections import deque


# constants
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 640
SCREEN_TITLE = "BMKeyLogger 20201107"


def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000))


def load_center_image(path):
    image = pyglet.image.load(path)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        pyglet.clock.schedule_interval(self.update, 1/1000)

    def setup(self):
        self.load_config()

        # sprite
        self.bg_sprite = pyglet.sprite.Sprite(
            load_center_image("images/bg_ac.png"), x=360, y=360)
        self.note_white_image = load_center_image("images/note_w.png")
        self.note_black_image = load_center_image("images/note_b.png")
        self.note_scr_image = load_center_image("images/note_scr.png")
        self.note_sprites = [deque() for i in range(18)]

        self.key_pressed = [False for i in range(18)]
        self.key_pressed_button = [-1 for i in range(18)]
        self.key_pressed_count = [0 for i in range(18)]

        # time
        self.init_time = datetime.datetime.now()
        self.tmp_time = 0
        self.tmp_kps = 0

        # label
        self.key_pressed_count_label = []
        for i in range(18):
            if (i <= 8 and i % 2 == 0) or (9 <= i and i % 2 != 0):
                label_y = 10
            else:
                label_y = 35
            label = pyglet.text.Label("0", font_name=self.my_config["font_name"], font_size=12, x=(
                30, 30, 79, 111, 143, 175, 207, 239, 271, 449, 481, 513, 545, 577, 609, 641, 688, 688)[i], y=label_y, anchor_x="center")
            self.key_pressed_count_label.append(label)

        self.current_time_label = pyglet.text.Label(
            "", font_name=self.my_config["font_name"], font_size=10, x=360, y=100, anchor_x="center")
        self.elapsed_time_label = pyglet.text.Label(
            "", font_name=self.my_config["font_name"], font_size=10, x=360, y=70, anchor_x="center")
        self.kps_label = pyglet.text.Label(
            "KPS:0", font_name=self.my_config["font_name"], font_size=32, x=360, y=140, anchor_x="center")
        # joypad
        self.joysticks = pyglet.input.get_joysticks()
        for joystick in self.joysticks:
            joystick.open()

    def load_config(self):
        with open("config.json", "r") as f:
            self.my_config = json.load(f)

    def on_draw(self):
        self.clear()
        self.bg_sprite.draw()

        for i in range(18):
            # note
            for sprite in self.note_sprites[i]:
                sprite.draw()

            # label
            self.key_pressed_count_label[i].draw()
        self.current_time_label.draw()
        self.elapsed_time_label.draw()
        self.kps_label.draw()

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.ESCAPE:
            self.on_close()

    def on_key_release(self, key, modifiers):
        pass

    def update(self, delta_time):
        # time
        dt_now = datetime.datetime.now()
        self.current_time_label.text = str(
            dt_now.strftime("%Y/%m/%d %H:%M:%S"))
        self.elapsed_time_label.text = str((dt_now - self.init_time))


        self.tmp_time += delta_time
        if self.tmp_time > 1:
            self.kps_label.text = "KPS:" + str(self.tmp_kps)
            self.tmp_time = self.tmp_kps = 0

        # joypad
        for j, joystick in enumerate(self.joysticks):
            for i in range(18):  # 鍵盤のindex
                for button in self.my_config["joypad"][j][i]:
                    if type(button) is int:
                        if not self.key_pressed[i]:
                            if joystick.buttons[button - 1]:
                                self.key_pressed[i] = True
                                self.key_pressed_button[i] = button - 1
                                self.make_note(i)

                        elif not joystick.buttons[button - 1] and self.key_pressed_button[i] == button - 1:
                            self.key_pressed[i] = False
                    elif button == "-x":
                        if not self.key_pressed[i]:
                            if joystick.x <= -self.my_config["threshold"]:
                                self.key_pressed[i] = True
                                self.key_pressed_button[i] = "-x"
                                self.make_note(i)
                        elif joystick.x > -self.my_config["threshold"] and self.key_pressed_button[i] == "-x":
                            self.key_pressed[i] = False
                    elif button == "+x":
                        if not self.key_pressed[i]:
                            if joystick.x >= self.my_config["threshold"]:
                                self.key_pressed[i] = True
                                self.key_pressed_button[i] = "+x"
                                self.make_note(i)
                        elif joystick.x < self.my_config["threshold"] and self.key_pressed_button[i] == "+x":
                            self.key_pressed[i] = False
                    elif button == "-y":
                        if not self.key_pressed[i]:
                            if joystick.y <= -self.my_config["threshold"]:
                                self.key_pressed[i] = True
                                self.key_pressed_button[i] = "-y"
                                self.make_note(i)
                        elif joystick.y > -self.my_config["threshold"] and self.key_pressed_button[i] == "-y":
                            self.key_pressed[i] = False
                    elif button == "+y":
                        if not self.key_pressed[i]:
                            if joystick.y >= self.my_config["threshold"]:
                                self.key_pressed[i] = True
                                self.key_pressed_button[i] = "+y"
                                self.make_note(i)
                        elif joystick.y < self.my_config["threshold"] and self.key_pressed_button[i] == "+y":
                            self.key_pressed[i] = False

        # keyboard
        for i in range(18):  # 鍵盤のindex
            for key in self.my_config["keyboard"][i]:
                if not self.key_pressed[i]:
                    if getkey(int(key, 16)):
                        self.key_pressed[i] = True
                        self.key_pressed_button[i] = key
                        self.make_note(i)

                elif not getkey(int(key, 16)) and self.key_pressed_button[i] == key:
                    self.key_pressed[i] = False

        # note
        for i in range(18):
            for sprite in copy.copy(self.note_sprites[i]):
                x, y = sprite.position
                sprite.update(x, y-self.my_config["speed"]*delta_time)
                if y <= -20:
                    self.note_sprites[i].popleft()

    def make_note(self, i):
        self.key_pressed_count[i] += 1
        self.tmp_kps += 1
        self.key_pressed_count_label[i].text = str(self.key_pressed_count[i])
        # make notes
        if i <= 1 or 16 <= i:
            image = self.note_scr_image
        elif (i <= 8 and i % 2 == 0) or (9 <= i and i % 2 != 0):
            image = self.note_white_image
        else:
            image = self.note_black_image

        self.note_sprites[i].append(pyglet.sprite.Sprite(
            image, x=(30, 30, 79, 111, 143, 175, 207, 239, 271, 449, 481, 513, 545, 577, 609, 641, 688, 688)[i], y=SCREEN_HEIGHT+15))

    def on_close(self):
        self.close()


def main():
    window = Window()
    window.setup()
    pyglet.app.run()


if __name__ == "__main__":
    main()
