from app.libs.classes.mappers.ekb_user_to_api_user_mapper import EkbUserToApiUserMapper
from app.libs.data_domain.api_user import (
    ApiCalculation,
    ApiCase,
    ApiCompletion,
    ApiCompletionItem,
    ApiDecision,
    ApiDecisionCause,
    ApiExpense,
    ApiIncome,
    ApiJournalNote,
    ApiNorm,
    ApiPayment,
    ApiPerson,
    ApiUser,
    DateSpan,
)
from app.libs.data_domain.ekb_case import EkbCase, TimeSpan
from app.libs.data_domain.ekb_user import EkbUser


def test_viva_user_to_api_user_mapper():
    input: EkbUser = EkbUser(
        first_name="Karl",
        last_name="Svensson",
        personal_number="198912079999",
        cases=[
            EkbCase(
                id="R99999", time_span=TimeSpan(start="2023-02-01", end="2023-02-28")
            )
        ],
        persons=[],
    )
    expected: ApiUser = ApiUser(
        id="R99999",
        cases=[
            ApiCase(
                calculations=[
                    ApiCalculation(
                        description="calculation description",
                        incomes=[
                            ApiIncome(amount=100, description="income description")
                        ],
                        expenses=[
                            ApiExpense(amount=101, description="expense description")
                        ],
                        norms=[ApiNorm(amount=102, description="norm description")],
                        note="calculation note",
                    )
                ],
                completion=ApiCompletion(
                    description="completion description",
                    dueDate="2023-01-01",
                    isAttachmentPending=False,
                    isCompleted=False,
                    isDueDateExpired=True,
                    isRandomCheck=False,
                    items=[
                        ApiCompletionItem(
                            description="completion item description", received=True
                        )
                    ],
                    receivedDate="2023-01-01",
                    uploadedDocuments=["document1.pdf", "document2.jpg"],
                ),
                decisions=[
                    ApiDecision(
                        description="decision description",
                        amount=103,
                        cause=ApiDecisionCause(
                            partner="partner cause", self="self cause"
                        ),
                    )
                ],
                journalNotes=[
                    ApiJournalNote(
                        label="journal note label",
                        message="journal note message",
                    )
                ],
                payments=[
                    ApiPayment(
                        amount=104,
                        description="payment description",
                        giveDate="2023-01-02",
                        method="payment method",
                    )
                ],
                period=DateSpan(startDate="2023-02-01", endDate="2023-02-28"),
                recievedISOTime="",
            )
        ],
        firstName="Karl",
        lastName="Svensson",
        personalNumber="198912079999",
        relatedPersons=[
            ApiPerson(
                firstName="Emma",
                lastName="Svensson",
                personalNumber="200212227777",
                type="partner",
            ),
            ApiPerson(
                firstName="Eren",
                lastName="Svensson",
                personalNumber="200802016969",
                type="child",
            ),
        ],
    )

    mapper = EkbUserToApiUserMapper(input)
    result = mapper.get_api_user()

    assert result == expected
