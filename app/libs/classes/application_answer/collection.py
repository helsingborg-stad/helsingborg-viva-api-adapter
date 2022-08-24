from app.libs.classes.application_answer.answer import ApplicationAnswer


class ApplicationAnswerCollection(list):
    def __init__(self, *args: ApplicationAnswer):
        if not all(isinstance(argument, ApplicationAnswer) for argument in args):
            raise TypeError(
                f'expected all arguments {args} to be of instance ApplicationAnswer')

        self.extend(args)

    def filter_by_tags(self, tags: list):
        list_copy = [*self]
        items_with_tags = list(filter(
            lambda item, tags=tags: item.has_all_tags(tags), list_copy))
        return items_with_tags
