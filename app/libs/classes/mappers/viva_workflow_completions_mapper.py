from dataclasses import dataclass
import datetime

SKIP_COMPLETIONS_TYPE: str = 'stickprovskontroll'


def create_timestamp(date: str) -> int:
    return int(round(datetime.datetime.strptime(f'{date}+00:00:00.000', "%Y-%m-%d%z").timestamp() * 1000))


@dataclass
class VivaWorkflowCompletionsMapper():
    viva_workflow: dict

    @property
    def due_date(self):
        due_date = self.viva_workflow['application']['completionduedate']
        if not due_date:
            return None

        return create_timestamp(date=due_date)

    @property
    def is_random_check(self):
        description = self.viva_workflow['application']['completiondescription']
        return (description and SKIP_COMPLETIONS_TYPE in description) is True

    @property
    def is_due_date_expired(self):
        if not self.due_date:
            return False

        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        today_time = int(round(datetime.datetime.strptime(
            today_date, "%Y-%m-%d").timestamp() * 1000))

        return (today_time > self.due_date) is True

    @property
    def is_attachment_pending(self):
        attachments_uploaded = self.viva_workflow['application']['completionsuploaded']
        if not attachments_uploaded:
            return False

        return True

    @property
    def received_date(self):
        received_date = self.viva_workflow['application']['completionreceiveddate']
        if not received_date:
            return None

        return create_timestamp(date=received_date)

    @property
    def description(self):
        description = self.viva_workflow['application']['completiondescription'] or ''
        if not description or self.is_due_date_expired or SKIP_COMPLETIONS_TYPE in description:
            return None

        return description

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

    def get_completion_uploaded(self):
        if not self.viva_workflow['application']['completionsuploaded']:
            return []

        uploaded = self.viva_workflow['application']['completionsuploaded']['completionuploaded']

        if not isinstance(uploaded, list):
            uploaded = [uploaded]

        return uploaded

    def _set_completion(self, text, received):
        return {
            'description': text,
            'received': text in received,
        }
