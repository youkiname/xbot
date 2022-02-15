import json


class Config:
    def __init__(self):
        self.delay_before_bot_run = 1
        self.delay_after_input_rate = 0.2
        self.delay_before_reload = 3
        self.delay_after_reload = 7
        self.delay_before_click_discard = 0.5
        self.delay_after_click_discard = 0.5
        self.delay_after_click_load = 0.2
        self.stop_hotkey = "<ctrl>"
        self.rate = "100"
        self.discard_position = (1424, 276)
        self.load_position = (1424, 276)

    def save_json(self):
        json_string = json.dumps(self.__dict__, indent=4, sort_keys=True)
        with open('config.json', 'w') as f:
            f.write(json_string)

    @staticmethod
    def load_json():
        config = Config()
        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
                config.__dict__.update(data)
        except Exception as e:
            print(e)
        return config


config = Config.load_json()
