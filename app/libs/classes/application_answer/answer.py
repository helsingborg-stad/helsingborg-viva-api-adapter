class ApplicationAnswer:
    def __init__(self, tags=None, value=None):
        if not all(isinstance(tag, str) for tag in tags):
            raise TypeError(f'expected all items in {tags} to be strings')

        if not isinstance(value, (str, int)):
            raise TypeError(f'expected {value} to be string or integer')

        self.tags = tags
        self.value = value

    def has_all_tags(self, tags):
        return all((tag in self.tags) for tag in tags)

    def has_tag(self, tag):
        if tag in self.tags:
            return True
        return False

    def get_tag_starting_with(self, value: str = None):
        tag = next(
            (tag for tag in self.tags if tag.startswith(value)), None)
        return tag
