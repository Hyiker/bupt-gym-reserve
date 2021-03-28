__all__ = (
    'RegexException',
)


class RegexException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg
