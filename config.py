import json


class Config:
    def __init__(self):
        self.delay_after_reload = 7
        self.delay_before_reload = 0.5
        self.default_delay = 0.2
        self.stop_hotkey = "<shift>"
        self.rate = "100"
        self.discard_position = (1424, 276)
        self.load_position = (1424, 276)
        self.freeze_position = (1424, 276)
        self.change_freeze_position_hotkey = "\\"
        self.change_discard_position_hotkey = "-"
        self.change_load_position_hotkey = "="

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
