import { Question } from "app/types/FormTypes";
import { PartnerInfo, User } from "app/types/UserTypes";
import { Step } from "../../../../types/Form";
import { replaceMarkdownTextInSteps } from "../textReplacement";

const mockedUserData: User = {
  address: {
    city: "",
    postalCode: "",
    street: "",
  },
  civilStatus: "",
  email: "",
  firstName: "Kaj-Bertil",
  lastName: "Efternamnsson",
  mobilePhone: "",
};

const baseStep: Step = {
  title: "",
  colorSchema: "blue",
  description: "Description",
  group: "",
};

const baseQuestion: Question = {
  id: "question-1",
  label: "Label",
  type: "text",
};

const fakedPartnerInfo: PartnerInfo = {
  partnerName: "Anna-Stina",
  partnerLastname: "Partnersson",
  partnerPersonalid: "123456789",
};

const doTest = (
  placeholder: string,
  expected: string,
  partner: PartnerInfo | undefined = undefined
): void => {
  const res = replaceMarkdownTextInSteps(
    [
      {
        ...baseStep,
        title: placeholder,
        description: placeholder,
        questions: [
          { ...baseQuestion, label: placeholder },
          {
            ...baseQuestion,
            type: "summaryList",
            items: [
              {
                inputId: "amount",
                id: "unemploymentAllowance",
                category: "benefits",
                title: placeholder,
                type: "checkbox",
                inputSelectValue: "checkbox",
              },
            ],
          },
          {
            ...baseQuestion,
            type: "repeaterField",
            description: placeholder,
            heading: placeholder,
            text: placeholder,
            title: placeholder,
            inputs: [
              {
                id: "amount",
                label: placeholder,
                title: placeholder,
              },
            ],
          },
        ],
      },
    ],
    mockedUserData,
    {
      endDate: new Date("2021-01-01").getTime(),
      startDate: new Date("2020-12-01").getTime(),
    },
    partner
  );
  expect(res[0].title).toBe(expected);
  expect(res[0].description).toBe(expected);
  expect(res[0].questions?.[0].label).toBe(expected);

  expect(res[0]?.questions?.[1].items?.[0].title).toBe(expected);
  expect(res[0]?.questions?.[2].inputs?.[0].label).toBe(expected);
  expect(res[0]?.questions?.[2].inputs?.[0].title).toBe(expected);
  expect(res[0]?.questions?.[2].text).toBe(expected);
  expect(res[0]?.questions?.[2].heading).toBe(expected);
  expect(res[0]?.questions?.[2].title).toBe(expected);
};

describe("replaceMarkdownTextInSteps", () => {
  describe("#month", () => {
    it.each([
      ["#month", "januari"],
      ["#month-1", "december"],
      ["#month-2", "november"],
      ["#month+1", "februari"],
      ["#month+2", "mars"],
      ["#month, #month+1 & #month+2", "januari, februari & mars"],
    ])("Replaces %s with %s", doTest);
  });

  describe("#date", () => {
    it.each([
      ["#date-1", "1/2"],
      ["#date-2", "28/2"],
    ])("Replaces %s with %s", doTest);
  });

  describe("Miscellaneous date stuff", () => {
    it.each([
      ["#year", "2021"],
      ["#today", "1"],
    ])("Replaces %s with %s", doTest);
  });

  describe("User", () => {
    it.each([
      ["#firstName", "Kaj-Bertil"],
      ["#lastName", "Efternamnsson"],
    ])("Replaces %s with %s", doTest);
  });

  describe("Partner", () => {
    describe("Has a partner", () => {
      it.each([["#partnerName", "Anna-Stina"]])(
        "Replaces %s with %s",
        (placeholder, expected) =>
          doTest(placeholder, expected, fakedPartnerInfo)
      );
    });

    describe("Doesn't have a partner", () => {
      it.each([["#partnerName", ""]])("Replaces %s with %s", doTest);
    });
  });
});
