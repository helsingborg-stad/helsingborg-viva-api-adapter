import datetime


class VivaWorkflowCompletionsMapper():

    def __init__(self, viva_workflow):
        self.viva_workflow = viva_workflow

    def is_random_check(self):
        description = self.viva_workflow['application']['completiondescription']
        return (description and 'stickprov' in description) is True

    def get_due_date(self):
        due_date = self.viva_workflow['application']['completionduedate']
        if not due_date:
            return None

        return int(round(datetime.datetime.strptime(due_date, "%Y-%m-%d").timestamp() * 1000))

    def get_completion_list(self):
        received = []
        if self.viva_workflow['application']['completionsreceived']:
            received = self.viva_workflow['application']['completionsreceived']['completionreceived']

        if not self.viva_workflow['application']['completions']:
            return []

        requested = self.viva_workflow['application']['completions']['completion']

        if not isinstance(requested, list):
            requested = [requested]

        completion_list = list(self._set_completion(text=text, received=received)
                               for text in requested)

        return completion_list

    def _set_completion(self, text, received):
        return {
            'description': text,
            'received': text in received,
        }
