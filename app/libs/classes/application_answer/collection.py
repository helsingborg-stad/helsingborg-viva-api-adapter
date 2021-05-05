from . import ApplicationAnswer

from ...strings import strip_last_character


class ApplicationAnswerCollection(list):
    def __init__(self, *args):
        if not all(isinstance(argument, ApplicationAnswer) for argument in args):
            raise TypeError(
                f'expected all arguments {args} to be of instance ApplicationAnswer')

        self.extend(args)

    def filter_by_tags(self, tags):
        list_copy = [*self]
        items_with_tags = list(filter(
            lambda item, tags=tags: item.has_all_tags(tags), list_copy))
        return items_with_tags

    def to_zeep_dict(self):
        zeep_dict = ZeepApplication(application_answer_list=self)
        return

        # post group
        for category_tag in self.valid_category_tag_list:
            zeep_dict_group_items = []

            # get posts
            for type_tag in self.valid_type_tag_list:
                # get post

                # get post answers
                category_and_type_tag_names = [
                    category_tag.name, type_tag.name]
                answers_with_category_and_type_tag_names = self.filter_by_tag_names(
                    tag_names=category_and_type_tag_names)

                if len(answers_with_category_and_type_tag_names) == 0:
                    continue

                # get post type values
                grouped_answer_values = dict()
                value_type_tag_names = ['amount', 'date',
                                        'description', 'coapplicant', 'applicant']

                for answer in answers_with_category_and_type_tag_names:
                    key = type_tag.name

                    group_tag_name = answer.get_tag_name_starting_with(
                        value='group:')
                    if not group_tag_name == None:
                        key = key + group_tag_name

                    grouped_answer_values[key] = dict()
                    for tag_name in value_type_tag_names:

                        if answer.has_tag_name(tag_name=tag_name):

                            tag_value = answer.value
                            if tag_name == 'coapplicant':
                                tag_value = tag_name

                            grouped_answer_values[key][tag_name] = tag_value
                #
                for values in grouped_answer_values.values():
                    zeep_dict_item = self._generate_zeep_dict_item_with_values(
                        type_name=type_tag.name, tag_value_dict=values)
                    zeep_dict_group_items.append(zeep_dict_item)

            if len(zeep_dict_group_items) > 0:
                zeep_dict = self._add_group_to_zeep_dict(
                    zeep_dict, group_name=category_tag.name, group_items=zeep_dict_group_items)

        return zeep_dict

    def _add_group_to_zeep_dict(self, zeep_dict, group_name, group_items):
        group_key = group_name.upper()
        group_item_key = strip_last_character(group_name).upper()

        zeep_dict[group_key] = {
            group_item_key: group_items
        }

        return zeep_dict

    def _generate_zeep_dict_item_with_values(self, type_name, tag_value_dict):
        item = {
            'TYPE': type_name,
            'FREQUENCY': 12,
            'DATE': '',
            'PERIOD': '',
            'APPLIESTO': 'applicant',
            'DESCRIPTION': ''
        }

        for tag, value in tag_value_dict.items():
            item_key = tag.upper()
            if value == None:
                item[item_key] = ''
            else:
                if tag == 'description':
                    amount = tag_value_dict['amount']
                    item[item_key] = self._get_zeep_dict_item_description(
                        description=value, amount=amount)

                if tag == 'date':
                    item[item_key] = self._get_zeep_dict_item_date(
                        milliseconds=tag_value_dict[tag])

                if tag == 'amount':
                    item[item_key] = int(value)

                if tag == 'coapplicant':
                    item['APPLIESTO'] = tag

        return item

    def _get_zeep_dict_item_description(self, description, amount):
        if isinstance(amount, int):
            return f'{description} {amount}'
        return description

    def _get_zeep_dict_item_date(self, milliseconds):
        return milliseconds_to_date_string(milliseconds)
