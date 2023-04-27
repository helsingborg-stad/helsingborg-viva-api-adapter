from dataclasses import dataclass
from typing import Union, List, Optional


@dataclass
class VivaData:
    status: int


@dataclass
class Ssi:
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
    casessi: Ssi
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
    completions: Union[List[str], None] = None
    completiondescription: Union[str, None] = None
    completionduedate: Union[str, None] = None
    islockedwithoutcompletionreceived: Union[str, None] = None
    islocked: Union[str, None] = None


@dataclass
class CalculationPerson:
    daycare: Union[str, None] = None
    days: Union[str, None] = None
    home: Union[str, None] = None
    name: Union[str, None] = None
    norm: Union[str, None] = None
    pnumber: Union[str, None] = None


@dataclass
class CalculationCost:
    actual: Union[str, None] = None
    approved: Union[str, None] = None
    note: Union[str, None] = None
    type: Union[str, None] = None


@dataclass
class CalculationNormPart:
    actual: Union[str, None] = None
    note: Union[str, None] = None
    type: Union[str, None] = None


@dataclass
class Calculation:
    calculationsum: Union[str, None] = None
    calculationtype: Union[str, None] = None
    costsum: Union[str, None] = None
    createdby: Union[str, None] = None
    createddatetime: Union[str, None] = None
    incomes: Union[str, None] = None
    incomesum: Union[str, None] = None
    normgemsum: Union[str, None] = None
    normsubtotal: Union[str, None] = None
    normsum: Union[str, None] = None
    note: Union[str, None] = None
    periodenddate: Union[str, None] = None
    periodstartdate: Union[str, None] = None
    reductions: Union[str, None] = None
    reductionsum: Union[str, None] = None
    subject: Union[str, None] = None
    parentssi: Union[Ssi, None] = None
    ssi: Union[Ssi, None] = None
    norm: Union[List[CalculationNormPart], None] = None


@dataclass
class Decision:
    createdby: Union[str, None] = None
    createddatetime: Union[str, None] = None
    amount: Union[str, None] = None
    author: Union[str, None] = None
    cause: Union[str, None] = None
    causepartner: Union[str, None] = None
    causetext: Union[str, None] = None
    causetextpartner: Union[str, None] = None
    code: Union[str, None] = None
    codetext: Union[str, None] = None
    createdby: Union[str, None] = None
    createddatetime: Union[str, None] = None
    date: Union[str, None] = None
    explanation: Union[str, None] = None
    id: Union[str, None] = None
    purpose: Union[str, None] = None
    type: Union[str, None] = None
    typecode: Union[str, None] = None


@dataclass
class DecisionBase:
    createdby: Union[str, None] = None
    createddatetime: Union[str, None] = None
    parentssi: Union[Ssi, None] = None
    decisions: Union[List[Decision], None] = None
    periodenddate: Union[str, None] = None
    periodstartdate: Union[str, None] = None
    ssi: Union[Ssi, None] = None
    subject: Union[str, None] = None


@dataclass
class Payment:
    pass


@dataclass
class Journal:
    pass


@dataclass
class Workflow:
    workflowid: str
    application: Application
    calculations: Optional[List[Calculation]] = None
    decisions: Optional[List[DecisionBase]] = None
    payments: Optional[List[Payment]] = None
    journals: Optional[List[Journal]] = None


@dataclass
class VivaCaseWorkflows(VivaData):
    vivacaseworkflows: List[Workflow]


@dataclass
class VivaCases(VivaData):
    vivacases: List[VivaCase]


@dataclass
class VivaPersonCases:
    vivadata: VivaCases


@dataclass
class VivaPersonCaseWorkflow:
    vivadata: VivaCaseWorkflows
