from typing import Optional, Union, List


class ApplicationAnswer:
    def __init__(self, tags: List[str], value: Union[str, int, float]):
        if not all(isinstance(tag, str) for tag in tags):
            raise TypeError(f'expected all items in {tags} to be strings')

        if not isinstance(value, (str, int, float)):
            raise TypeError(f'expected {value} to be string, integer or float')

        self.tags = tags
        self.value = value

    def has_all_tags(self, tags: List[str]) -> bool:
        return all((tag in self.tags) for tag in tags)

    def has_tag(self, tag: str) -> bool:
        if tag in self.tags:
            return True
        return False

    def get_tag_starting_with(self, value: str = None) -> Optional[str]:
        tag = next(
            (tag for tag in self.tags if tag.startswith(value)), None)
        return tag
