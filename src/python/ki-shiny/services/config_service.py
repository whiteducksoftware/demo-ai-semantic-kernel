from decouple import config

MY_CONFIG_SETTING = config("MY_CONFIG_SETTING", default="default_value")


class ConfigService:
    def __init__(self):
        global MY_CONFIG_SETTING
        MY_CONFIG_SETTING = self.get_config("MY_CONFIG_SETTING", MY_CONFIG_SETTING)  # type: ignore

    def get_config(self, key: str, default: str) -> str:
        return config(key, default=default)  # type: ignore

    def set_config(self, key: str, value: str) -> None:
        config(key, value)

    def load_all(self) -> dict:
        return {
            "MY_CONFIG_SETTING": MY_CONFIG_SETTING,
        }
