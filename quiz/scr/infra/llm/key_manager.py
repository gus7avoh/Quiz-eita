from os import getenv

from dotenv import load_dotenv

load_dotenv()


class GeminiKeyManager:

    def __init__(self):
        self.switched = False

        self.keys = [
            getenv("EITA_1"),
            getenv("EITA_2"),
            getenv("EITA_4"),
            getenv("EITA_5"),
            getenv("EITA_6"),
            getenv("EITA_7"),
            getenv("EITA_8"),
            getenv("EITA_9"),
            getenv("EITA_10"),
        ]

        self.keys = [key for key in self.keys if key]

        self.current_key = 0

    def get_key(self):
        return self.keys[self.current_key]

    def next_key(self):
        if self.current_key == len(self.keys) - 1:
            self.current_key = 0
            self.switched = True
        else:
            self.current_key += 1