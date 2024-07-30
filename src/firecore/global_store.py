class OnceStore:
    def __init__(self) -> None:
        self._store = {}

    def set(self, key: str, value):
        """
        Only set once
        """
        assert key not in self._store
        self._store[key] = value

    def get(self, key: str):
        return self._store[key]


GLOBAL_STORE = OnceStore()
