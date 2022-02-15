from threading import Thread
from time import sleep

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

from config import config


class UserInterrupt(Exception):
    pass


class Bot(Thread):
    def __init__(self):
        super().__init__()
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.stopped = False

    def switch_tab(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)

    def enter_rate(self):
        self.keyboard.type(config.rate)

    def reload_page(self):
        self.switch_tab()
        self.stoppable_sleep(config.delay_before_click_discard)
        self.mouse.position = config.discard_position
        self.mouse.click(Button.left, 1)
        self.stoppable_sleep(config.delay_after_click_discard)
        self.mouse.position = config.load_position
        self.mouse.click(Button.left, 1)
        self.stoppable_sleep(config.delay_after_click_load)
        self.switch_tab()

    def run(self):
        sleep(config.delay_before_bot_run)
        while not self.stopped:
            try:
                self.enter_rate()
                self.stoppable_sleep(config.delay_after_input_rate)
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
                self.stoppable_sleep(config.delay_before_reload)
                self.reload_page()
                self.stoppable_sleep(config.delay_after_reload)
            except UserInterrupt:
                break

    def stop(self):
        self.stopped = True

    def stoppable_sleep(self, sec):
        sleep(sec)
        if self.stopped:
            raise UserInterrupt()
