import colorama as cma


def to_string(cm, text: str) -> str:
    return f"{cm}{text}{cma.Style.RESET_ALL}"
