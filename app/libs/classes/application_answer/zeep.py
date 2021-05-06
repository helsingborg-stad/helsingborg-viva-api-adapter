from . import ApplicationAnswerCollection

from ...strings import strip_last_character
from ...datetime_helper import milliseconds_to_date_string


class ZeepApplication(dict):
    EMPTY_POST = {
        'TYPE': None,
        'FREQUENCY': 12,
        'DATE': None,
        'PERIOD': None,
        'APPLIESTO': 'applicant',
        'DESCRIPTION': None
    }

    POST_GROUPS = (
        'EXPENSES',
        'INCOMES',
        'OTHERAPPLICATIONS',
        'OCCUPATIONS',
        'ATTACHMENTS'
    )

    POST_TYPES = (
        'boende',
        'el',
        'reskostnad',
        'hemforsakring',
        'bredband',
        'akassa',
        'lakarvard',
        'medicin',
        'barnomsorg',
        'barnomsorgsskuld',
        'bostadslan',
        'hyresskuld',
        'fackskuld',
        'elskuld',
        'lon',
        'bil',
        'mobile',
        'annat',
        'annan',
        'other_attachments'
    )

    POST_TYPE_ATTRIBUTES = (
        'AMOUNT', 'DATE', 'DESCRIPTION', 'APPLIESTO', 'FREQUENCY'
    )

    def __init__(self, application_answer_collection: ApplicationAnswerCollection = None):
        super().__init__(self)
        self.application_answer_collection = application_answer_collection
        self._create()

    def _create(self):
        for post_group_name in ZeepApplication.POST_GROUPS:
            posts = self._get_posts(post_group_name=post_group_name)

            if posts:
                posts_key = strip_last_character(post_group_name)
                self[post_group_name] = {posts_key: posts}

    def _get_posts(self, post_group_name: str = None):
        posts = []

        for post_type in ZeepApplication.POST_TYPES:
            post_type_answers = self._get_post_type_answers(
                post_type, post_group_name)

            if not post_type_answers:
                continue

            post_type_collection = self._get_post_type_collection(
                post_type=post_type, post_answers=post_answers)

            for post_type_attributes in post_type_collection.values():
                post = self._get_post(post_type, post_type_attributes)
                post_key = strip_last_character(post_group_name)
                posts.append(post)

        return posts

    def _get_post(self, post_type: str, post_type_attributes: dict):
        post = {
            'TYPE': '',
            'FREQUENCY': 12,
            'DATE': '',
            'PERIOD': '',
            'APPLIESTO': 'applicant',
            'DESCRIPTION': ''
        }

        post['TYPE'] = post_type

        for attribute, value in post_type_attributes.items():
            if value == None:
                post[attribute] = ''

            else:
                if attribute == 'DESCRIPTION':
                    amount = post_type_attributes['AMOUNT']
                    post[attribute] = self._get_post_description(
                        description=value, amount=amount)

                if attribute == 'DATE':
                    post[attribute] = milliseconds_to_date_string(
                        milliseconds=value)

                if attribute == 'AMOUNT':
                    post[attribute] = int(value)

                if attribute == 'COAPPLICANT':
                    post['APPLIESTO'] = name

        return post

    def _get_post_type_collection(self, post_type: str, post_answers):
        post_type_collection = dict()

        for post_answer in post_answers:
            post_type_key = post_type
            answer_group_tag = post_answer.get_tag_starting_with(
                value='group:')

            if answer_group_tag:
                post_type_key = post_type_key + answer_group_tag

            if not post_type_key in post_type_collection:
                post_type_collection[post_type_key] = dict()

            for post_type_attribute in ZeepApplication.POST_TYPE_ATTRIBUTES:
                if post_answer.has_tag(post_type_attribute.lower()):

                    post_value = post_answer.value
                    if post_type_attribute == 'coapplicant':
                        post_value = post_type_attribute

                    post_type_collection[post_type_key][post_type_attribute] = post_value

        return post_type_collection

    def _get_post_type_answers(self, post_name: str, post_group_name: str):
        post_tags = [post_name.lower(), post_group_name.lower()]
        return self.application_answer_collection.filter_by_tags(tags=post_tags)

    def _get_post_description(self, description, amount):
        if isinstance(amount, int):
            return f'{description} {amount}'
        return description
