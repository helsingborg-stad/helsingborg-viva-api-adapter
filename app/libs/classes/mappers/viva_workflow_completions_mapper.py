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

    def is_due_date_expired(self):
        due_date = self.get_due_date()
        if not due_date:
            return False

        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        today_time = int(round(datetime.datetime.strptime(
            today_date, "%Y-%m-%d").timestamp() * 1000))

        return (today_time > due_date) is True

    def get_received_date(self):
        received_date = self.viva_workflow['application']['completionreceiveddate']
        if not received_date:
            return None

        return int(round(datetime.datetime.strptime(received_date, "%Y-%m-%d").timestamp() * 1000))

    def is_attachment_pending(self):
        attachments_uploaded = self.viva_workflow['application']['completionsuploaded']
        if not attachments_uploaded:
            return False

        return True

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
