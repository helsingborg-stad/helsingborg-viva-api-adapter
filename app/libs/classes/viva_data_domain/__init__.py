from dataclasses import dataclass
from typing import Union, List, Optional


@dataclass
class VivaData:
    status: int


@dataclass
class CaseSsi:
    server: str
    path: str
    id: str


@dataclass
class Officer:
    name: str
    type: str
    typeenclair: str
    phone: str
    mail: str
    title: str


@dataclass
class Client:
    pnumber: str
    fname: str
    lname: str


@dataclass
class PhoneNumber:
    type: str
    number: str


@dataclass
class Person:
    pnumber: str
    fname: str
    lname: str
    type: str
    startdate: Union[str, None]
    enddate: Union[str, None]
    days: Union[str, None]


@dataclass
class VivaCase:
    casessi: CaseSsi
    idunique: str
    idenclair: str
    type: str
    typeenclair: str
    opendate: str
    classifiedassecret: str
    unit: str
    team: str
    officers: List[Officer]
    client: Client
    persons: Union[List[Person], None]
    phonenumbers: Union[List[PhoneNumber], None]


@dataclass
class Application:
    receiveddate: Union[str, None] = None
    periodstartdate: Union[str, None] = None
    periodenddate: Union[str, None] = None
    otherperiod: Union[str, None] = None
    requestingcompletion: Union[str, None] = None
    completiondate: Union[str, None] = None
    completionreceiveddate: Union[str, None] = None
    completionsreceived: Union[str, None] = None
    completions: Union[str, None] = None
    completiondescription: Union[str, None] = None
    completionduedate: Union[str, None] = None
    islockedwithoutcompletionreceived: Union[str, None] = None
    islocked: Union[str, None] = None


@ dataclass
class Calculation:
    pass


@ dataclass
class Decision:
    pass


@ dataclass
class Payment:
    pass


@ dataclass
class Journal:
    pass


@ dataclass
class Workflow:
    workflowid: str
    calculations: Optional[List[Calculation]] = None
    decisions: Optional[List[Decision]] = None
    payments: Optional[List[Payment]] = None
    journals: Optional[List[Journal]] = None
    application: Optional[Application] = None


@ dataclass
class VivaCaseWorkflows(VivaData):
    vivacaseworkflows: List[Workflow]


@ dataclass
class VivaCases(VivaData):
    vivacases: List[VivaCase]


@ dataclass
class VivaPersonCases:
    vivadata: VivaCases


@ dataclass
class VivaPersonCaseWorkflow:
    vivadata: VivaCaseWorkflows
