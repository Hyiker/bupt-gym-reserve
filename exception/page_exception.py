__all__ = (
    'PageFormatException',
)


class PageFormatException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg
