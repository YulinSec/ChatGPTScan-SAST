import yaml
import uuid


class Config:
    __instance: object = None
    __config: dict = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @classmethod
    def load_config(cls) -> None:
        if cls.__config is None:
            cls.__config = yaml.safe_load(open("config.yaml"))
            cls.__config["web"]["SECRET_KEY"] = str(uuid.uuid4())

    @property
    def config(self):
        self.load_config()
        return self.__config
