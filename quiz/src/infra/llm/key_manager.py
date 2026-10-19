import asyncio
import time
import uuid
from os import getenv

from domain.entities.api_key import ApiKey
from infra.environment import load_project_environment

load_project_environment()

ApiKeyState = ApiKey

class ApiKeyLease:
    def __init__(
        self,
        manager: "KeyManager",
        state: ApiKey,
        token: str,
    ):
        self.manager = manager
        self.state = state
        self.token = token

    @property
    def value(self) -> str:
        return self.state.value

    async def release(self) -> None:
        await self.manager.release(self.state, self.token)


class KeyManager:
    total_keys = 58

    def __init__(self, cooldown_seconds: float = 2.0):
        self.cooldown_seconds = cooldown_seconds
        self.switched = False
        self.current_key = 0
        self._cursor = 0
        self._lock = asyncio.Lock()

        values = [
            getenv(f"EITA_{index}")
            for index in range(1, self.total_keys + 1)
        ]
        self.keys = [value for value in values if value]
        self._states = [
            ApiKey(
                key_id=f"key-{index}",
                value=value,
            )
            for index, value in enumerate(self.keys)
        ]

    async def try_acquire(self) -> ApiKeyLease | None:
        """Tenta obter uma chave sem aguardar uma chave ocupada."""
        if not self._states:
            return None

        async with self._lock:
            now = time.monotonic()
            total_keys = len(self._states)

            for offset in range(total_keys):
                index = (self._cursor + offset) % total_keys
                state = self._states[index]

                if not state.is_available(now):
                    continue

                token = str(uuid.uuid4())
                if not state.acquire(now, token, self.cooldown_seconds):
                    continue
                self._cursor = (index + 1) % total_keys

                return ApiKeyLease(self, state, token)

            return None

    async def release(self, state: ApiKey, token: str) -> None:
        async with self._lock:
            state.release(token)

    def get_key(self):
        """Mantém compatibilidade com o cliente síncrono de geração."""
        return self.keys[self.current_key]

    def next_key(self):
        """Avança a chave usada pelo cliente síncrono de geração."""
        if self.current_key == len(self.keys) - 1:
            self.current_key = 0
            self.switched = True
        else:
            self.current_key += 1
