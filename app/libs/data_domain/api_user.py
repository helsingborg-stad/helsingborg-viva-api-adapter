from dataclasses import dataclass
from typing import List


@dataclass
class DateSpan:
    startDate: str
    endDate: str


@dataclass
class ApiCompletionItem:
    description: str
    received: bool


@dataclass
class ApiCompletion:
    items: List[ApiCompletionItem]
    description: str
    receivedDate: str
    dueDate: str
    uploadedDocuments: List[str]
    isCompleted: bool
    isRandomCheck: bool
    isAttachmentPending: bool
    isDueDateExpired: bool


@dataclass
class ApiIncome:
    description: str
    amount: float


@dataclass
class ApiExpense:
    description: str
    amount: float


@dataclass
class ApiNorm:
    description: str
    amount: float


@dataclass
class ApiCalculation:
    description: str
    incomes: List[ApiIncome]
    expenses: List[ApiExpense]
    norms: List[ApiNorm]
    note: str


@dataclass
class ApiDecisionCause:
    self: str
    partner: str


@dataclass
class ApiDecision:
    cause: ApiDecisionCause
    description: str
    amount: float


@dataclass
class ApiPayment:
    method: str
    giveDate: str
    description: str
    amount: float


@dataclass
class ApiJournalNote:
    label: str
    message: str


@dataclass
class ApiPerson:
    firstName: str
    lastName: str
    personalNumber: str
    type: str


@dataclass
class ApiCase:
    period: DateSpan
    recievedISOTime: str
    completion: ApiCompletion
    calculations: List[ApiCalculation]
    decisions: List[ApiDecision]
    payments: List[ApiPayment]
    journalNotes: List[ApiJournalNote]


@dataclass
class ApiUser:
    id: str
    personalNumber: str
    firstName: str
    lastName: str
    cases: List[ApiCase]
    relatedPersons: List[ApiPerson]
