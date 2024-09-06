from config.config_base import ConfigBase


class ConfigLight(ConfigBase):
    def __init__(self):
        super().__init__()

        print(" [ Using ConfigLight ]")
