from app.libs.classes.viva_data_domain import VivaPersonCaseWorkflow
from app.libs.classes.viva_data_domain import VivaCaseWorkflows
from app.libs.classes.viva_data_domain import Workflow
from app.libs.classes.viva_data_domain import Application
from app.libs.classes.mappers.viva_workflows_to_ekb_cases_mapper import VivaWorkflowsToEkbCasesMapper


def test_happy_path():
    viva_person_case_workflow = VivaPersonCaseWorkflow(
        vivadata=VivaCaseWorkflows(status=1, vivacaseworkflows=[
            Workflow(workflowid='23abfsasdxc', application=Application(
                receiveddate='2020-01-13',
                periodstartdate='2020-01-01',
                periodenddate='2020-01-31',
                islocked='2020-01-20',
            )),
        ]))

    mapper = VivaWorkflowsToEkbCasesMapper(workflows=viva_person_case_workflow)
    ekb_cases = mapper.get_ekb_cases()

    assert len(ekb_cases) == 1
    assert ekb_cases[0].id == '23abfsasdxc'
    assert ekb_cases[0].received_date == '2020-01-13'
    assert ekb_cases[0].locked_date == '2020-01-20'
    assert ekb_cases[0].time_span.start == '2020-01-01'
    assert ekb_cases[0].time_span.end == '2020-01-31'
