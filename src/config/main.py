from src.config.abastract import AbstractConfig


class MainConfig(AbstractConfig):
    token = ""
    group_chat_id = 0

    def _assign(self, fjson):
        self.token = fjson["token"]
        self.group_chat_id = fjson["group_chat_id"]
