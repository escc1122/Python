class StopSignal:
    value = True

    @classmethod
    def set(cls, value: bool):
        cls.value = value

    @classmethod
    def is_set(cls) -> bool:
        return cls.value