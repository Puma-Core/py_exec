from typing import Callable


replace_prefix: Callable[[str, str], str] = lambda text, prefix: (
    text[len(prefix):]
    if text.startswith(prefix) else text
)

replace_prefix_list: Callable[[list[str], str], list[str]] = lambda lst, prefix: [
    replace_prefix(item, prefix) for item in lst
]