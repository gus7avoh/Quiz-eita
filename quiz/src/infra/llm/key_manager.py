from os import getenv
from dotenv import load_dotenv


load_dotenv()

class GeminiKeyManager:
    total_keys = 58
    def __init__(self):
        self.switched = False

        self.keys = [
            getenv(f"EITA_{i}")
            for i in range(1, GeminiKeyManager.total_keys + 1)
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