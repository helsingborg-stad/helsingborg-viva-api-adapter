def trim_last_character(string: str = None) -> str:
    if not isinstance(string, str):
        raise TypeError(f'expected {string} to be of type string')

    return string[:-1]
