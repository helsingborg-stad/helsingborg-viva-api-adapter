from typing import List
from app.libs.classes.mappers.viva_workflow_completions_mapper import VivaWorkflowCompletionsMapper
from app.libs.classes.viva_data_domain import VivaPersonCaseWorkflow
from app.libs.classes.viva_data_domain import Workflow
from app.libs.data_domain.ekb_case import EkbCase
from app.libs.data_domain.ekb_case import TimeSpan


class VivaWorkflowsToEkbCasesMapper:
    def __init__(self, workflows: VivaPersonCaseWorkflow) -> None:
        self._workflows = workflows.vivadata.vivacaseworkflows

    def get_ekb_cases(self) -> List[EkbCase]:
        return [self._create_ekb_case(w) for w in self._workflows]

    def _create_ekb_case(self, w: Workflow) -> EkbCase:
        return EkbCase(id=w.workflowid,
                       description='EkbCase',
                       received_date=w.application.receiveddate if w.application else None,
                       locked_date=w.application.islocked if w.application else None,
                       time_span=TimeSpan(
                           start=w.application.periodstartdate if w.application else None,
                           end=w.application.periodenddate if w.application else None))
