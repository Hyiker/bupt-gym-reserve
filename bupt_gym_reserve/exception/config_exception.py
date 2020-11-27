__all__ = (
    'ConfigException',
)


class ConfigException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg
