import sys
from tkinter import *
from tkinter import messagebox

from pynput.keyboard import GlobalHotKeys
from pynput.mouse import Listener as MouseListener, Controller as MouseController

from bot import Bot
from config import config


class Gui:
    def __init__(self):
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.geometry('420x400')
        self.window.resizable(False, False)

        self.row = 0

        self.create_rate_entry()
        self.row += 1
        self.create_delay_before_reload_entry()
        self.row += 1
        self.create_delay_after_reload_entry()
        self.row += 1
        self.create_freeze_position_entry()
        self.row += 1
        self.create_discard_position_entry()
        self.row += 1
        self.create_load_position_entry()
        self.row += 1
        self.create_hotkey_entry()
        self.row += 1
        self.create_change_discard_hotkey_entry()
        self.row += 1
        self.create_change_load_hotkey_entry()
        self.row += 1
        self.create_save_button()
        self.row += 1
        self.create_status_label()


        self.bot = None
        self.hotkey_listener = GlobalHotKeys({
            config.stop_hotkey: self.on_stop_hotkey,
            config.change_freeze_position_hotkey: self.on_change_freeze_position_hotkey,
            config.change_discard_position_hotkey: self.on_change_discard_position_hotkey,
            config.change_load_position_hotkey: self.on_change_load_position_hotkey
        })
        self.mouse_listener = MouseListener(on_move=self.on_mouse_move)
        self.mouse_controller = MouseController()

    def create_rate_entry(self):
        Label(self.window, text="Ставка").grid(row=self.row, column=0)
        self.rate_entry = Entry(self.window, width=20)
        self.rate_entry.insert(0, config.rate)
        self.rate_entry.grid(row=self.row, column=1)

    def create_delay_before_reload_entry(self):
        Label(self.window, text="Ожидание после ставки (сек)").grid(row=self.row, column=0)
        self.delay_before_reload = Entry(self.window, width=20)
        self.delay_before_reload.insert(0, str(config.delay_before_reload))
        self.delay_before_reload.grid(row=self.row, column=1)

    def create_delay_after_reload_entry(self):
        Label(self.window, text="Ожидание после перезагрузки (сек)").grid(row=self.row, column=0)
        self.delay_after_reload = Entry(self.window, width=20)
        self.delay_after_reload.insert(0, str(config.delay_after_reload))
        self.delay_after_reload.grid(row=self.row, column=1)

    def create_freeze_position_entry(self):
        Label(self.window, text="Freeze координаты").grid(row=self.row, column=0)
        self.freeze_position = Entry(self.window, width=20)
        self.freeze_position.insert(0, f"{config.discard_position[0]},{config.discard_position[1]}")
        self.freeze_position.grid(row=self.row, column=1)

    def create_discard_position_entry(self):
        Label(self.window, text="Discard координаты").grid(row=self.row, column=0)
        self.discard_position = Entry(self.window, width=20)
        self.discard_position.insert(0, f"{config.discard_position[0]},{config.discard_position[1]}")
        self.discard_position.grid(row=self.row, column=1)

    def create_load_position_entry(self):
        Label(self.window, text="Load координаты").grid(row=self.row, column=0)
        self.load_position = Entry(self.window, width=20)
        self.load_position.insert(0, f"{config.load_position[0]},{config.load_position[1]}")
        self.load_position.grid(row=self.row, column=1)
        
    def create_hotkey_entry(self):
        Label(self.window, text="Клавиша старт-стоп").grid(row=self.row, column=0)
        self.hotkey_text = Entry(self.window, width=20)
        self.hotkey_text.insert(0, config.stop_hotkey)
        self.hotkey_text.grid(row=self.row, column=1)

    def create_change_discard_hotkey_entry(self):
        Label(self.window, text="Клавиша сменить discard").grid(row=self.row, column=0)
        self.change_discard_hotkey_entry = Entry(self.window, width=20)
        self.change_discard_hotkey_entry.insert(0, config.change_discard_position_hotkey)
        self.change_discard_hotkey_entry.grid(row=self.row, column=1)

    def create_change_load_hotkey_entry(self):
        Label(self.window, text="Клавиша сменить load").grid(row=self.row, column=0)
        self.change_load_hotkey_entry = Entry(self.window, width=20)
        self.change_load_hotkey_entry.insert(0, config.change_load_position_hotkey)
        self.change_load_hotkey_entry.grid(row=self.row, column=1)
        
    def create_status_label(self):
        self.status_label = Label(self.window, text="Выключен")
        self.status_label.grid(row=self.row, column=0)
        
    def create_save_button(self):
        self.save_button = Button(self.window, text="Сохранить", command=self.update_config)
        self.save_button.grid(row=self.row, column=0)

    def run(self):
        self.hotkey_listener.start()
        self.mouse_listener.start()
        self.window.mainloop()

    def update_config(self):
        try:
            config.rate = self.rate_entry.get()
            config.delay_before_reload = float(self.delay_before_reload.get())
            config.delay_after_reload = float(self.delay_after_reload.get())
            config.freeze_position = tuple(map(int, self.freeze_position.get().split(",")))
            config.discard_position = tuple(map(int, self.discard_position.get().split(",")))
            config.load_position = tuple(map(int, self.load_position.get().split(",")))
            config.stop_hotkey = self.hotkey_text.get()
            config.change_discard_position_hotkey = self.change_discard_hotkey_entry.get()
            config.change_load_position_hotkey = self.change_load_hotkey_entry.get()
            config.save_json()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неподходящие данные. {e}")

    def on_stop_hotkey(self):
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

    def on_change_freeze_position_hotkey(self):
        print("on_change_freeze_position_hotkey")
        pos = self.mouse_controller.position
        self.freeze_position.delete(0, "end")
        self.freeze_position.insert(0, f"{pos[0]},{pos[1]}")
        self.update_config()

    def on_change_discard_position_hotkey(self):
        print("on_change_discard_position_hotkey")
        pos = self.mouse_controller.position
        self.discard_position.delete(0, "end")
        self.discard_position.insert(0, f"{pos[0]},{pos[1]}")
        self.update_config()

    def on_change_load_position_hotkey(self):
        print("on_change_load_position_hotkey")
        pos = self.mouse_controller.position
        self.load_position.delete(0, "end")
        self.load_position.insert(0, f"{pos[0]},{pos[1]}")
        self.update_config()

    def on_mouse_move(self, x, y):
        self.window.title(f"1xBOT v0.2 x:{x} y:{y}")

    def on_close(self):
        print("close")
        sys.exit()


if __name__ == '__main__':
    Gui().run()
