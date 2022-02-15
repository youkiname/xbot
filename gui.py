import sys
from tkinter import *
from tkinter import messagebox

from pynput.keyboard import GlobalHotKeys
from pynput.mouse import Listener as MouseListener

from bot import Bot
from config import config


class Gui:
    def __init__(self):
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.geometry('400x400')
        self.window.resizable(False, False)

        Label(self.window, text="Ставка").grid(row=0, column=0)
        self.rate_entry = Entry(self.window, width=20)
        self.rate_entry.insert(0, config.rate)
        self.rate_entry.grid(row=0, column=1)

        Label(self.window, text="Ожидание (сек)").grid(row=1, column=0)
        self.delay_entry = Entry(self.window, width=20)
        self.delay_entry.insert(0, str(config.delay_before_reload))
        self.delay_entry.grid(row=1, column=1)

        Label(self.window, text="Discard координаты").grid(row=2, column=0)
        self.discard_position = Entry(self.window, width=20)
        self.discard_position.insert(0, f"{config.discard_position[0]},{config.discard_position[1]}")
        self.discard_position.grid(row=2, column=1)

        Label(self.window, text="load координаты").grid(row=3, column=0)
        self.load_position = Entry(self.window, width=20)
        self.load_position.insert(0, f"{config.load_position[0]},{config.load_position[1]}")
        self.load_position.grid(row=3, column=1)

        Label(self.window, text="Клавиша").grid(row=4, column=0)
        self.hotkey_text = Entry(self.window, width=20)
        self.hotkey_text.insert(0, config.stop_hotkey)
        self.hotkey_text.grid(row=4, column=1)

        self.status_label = Label(self.window, text="Выключен")
        self.status_label.grid(row=5, column=0)

        self.save_button = Button(self.window, text="Сохранить", command=self.update_config)
        self.save_button.grid(row=6, column=0)

        self.bot = None
        self.hotkey_listener = GlobalHotKeys({config.stop_hotkey: self.on_hot_key})
        self.mouse_listener = MouseListener(on_move=self.on_mouse_move)

    def run(self):
        self.hotkey_listener.start()
        self.mouse_listener.start()
        self.window.mainloop()

    def update_config(self):
        try:
            config.rate = self.rate_entry.get()
            config.delay_before_reload = float(self.delay_entry.get())
            config.discard_position = tuple(map(int, self.discard_position.get().split(",")))
            config.load_position = tuple(map(int, self.load_position.get().split(",")))
            config.stop_hotkey = self.hotkey_text.get()
            config.save_json()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неподходящие данные. {e}")

    def on_hot_key(self):
        print('hotkey pressed')
        if self.bot is None:
            self.bot = Bot()
            self.bot.stopped = False
            self.bot.start()
            self.status_label.config(text="Включён")
            print("Bot started")
        else:
            self.bot.stop()
            self.bot.join()
            self.bot = None
            self.status_label.config(text="Выключен")
            print("Bot stopped")

    def on_mouse_move(self, x, y):
        self.window.title(f"1xBOT v0.1 x:{x} y:{y}")

    def on_close(self):
        print("close")
        sys.exit()


if __name__ == '__main__':
    Gui().run()
