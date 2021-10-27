import PropTypes from "prop-types";
import React, {
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import { Animated, Easing, RefreshControl } from "react-native";
import styled from "styled-components/native";
import { useFocusEffect } from "@react-navigation/native";
import { Modal } from "../../components/molecules/Modal";

import Wrapper from "../../components/molecules/Dialog/Wrapper";
import Heading from "../../components/atoms/Heading";
import Body from "../../components/molecules/Dialog/Body";
import BackgroundBlur from "../../components/molecules/Dialog/BackgroundBlur";
import Button from "../../components/atoms/Button";
import icons from "../../helpers/Icons";
import { Text } from "../../components/atoms";
import {
  Card,
  CaseCard,
  Header,
  ScreenWrapper,
} from "../../components/molecules";
import { getSwedishMonthNameByTimeStamp } from "../../helpers/DateHelpers";
import { CaseState, caseTypes } from "../../store/CaseContext";
import FormContext from "../../store/FormContext";
import { convertDataToArray, calculateSum } from "../../helpers/FormatVivaData";
import AuthContext from "../../store/AuthContext";
import { put } from "../../helpers/ApiRequest";
import { State as CaseContextState } from "../../types/CaseContext";
import wait from "../../helpers/Misc";
import { Case } from "../../types/Case";

const ButtonContainer = styled.View`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  margin-top: 25px;
  width: 100%;
`;

const PopupButton = styled(Button)`
  border: 0;
  margin-bottom: 12px;
`;

const Container = styled.ScrollView`
  flex: 1;
  padding-left: 16px;
  padding-right: 16px;
`;

const DialogContainer = styled(Body)`
  text-align: center;
  align-items: center;
  justify-content: center;
  padding: 32px;
`;

const StyledText = styled(Text)`
  margin-bottom: 8px;
`;

const ListHeading = styled(Text)`
  margin-left: 4px;
  margin-top: 24px;
  margin-bottom: 8px;
`;

const CardMessageBody = styled(Card.Body)`
  background-color: ${(props) => props.theme.colors.neutrals[5]};
`;

const colorSchema = "red";

/**
 * Returns a case card component depending on it's status
 * @param {obj} caseData
 * @param {obj} navigation
 * @param {obj} authContext
 * @param {object?} extra Extra properties
 * @param {function?} extra.dialogState
 */
const computeCaseCardComponent = (caseData, navigation, authContext, extra) => {
  const currentStep =
    caseData?.forms?.[caseData.currentFormId]?.currentPosition
      ?.currentMainStep || 0;
  const totalSteps = caseData.form?.stepStructure
    ? caseData.form.stepStructure.length
    : 0;
  const {
    details: {
      period = {},
      workflow: { decision = {}, payments = {}, application = {} } = {},
    } = {},
    persons = [],
  } = caseData;

  const applicationPeriodTimestamp =
    application?.periodenddate ?? period?.endDate;
  const applicationPeriodMonth = applicationPeriodTimestamp
    ? getSwedishMonthNameByTimeStamp(applicationPeriodTimestamp, true)
    : "";

  const decisions = decision?.decisions?.decision
    ? convertDataToArray(decision.decisions.decision)
    : [];

  const paymentsArray = decisions.filter(
    (decision) => decision.typecode === "01"
  );
  const partiallyApprovedDecisionsAndRejected = decisions.filter((decision) =>
    ["03", "02"].includes(decision.typecode)
  );

  const casePersonData = persons.find(
    (person) => person.personalNumber === authContext.user.personalNumber
  );

  const statusType = caseData?.status?.type || "";
  const isNotStarted = statusType.includes("notStarted");
  const isOngoing = statusType.includes("ongoing");
  const isCompletionRequired = statusType.includes("completionRequired");
  const isSigned = statusType.includes("signed");
  const isClosed = statusType.includes("closed");
  const isWaitingForSign = statusType.includes("active:signature:pending");
  const selfHasSigned = casePersonData?.hasSigned;
  const isCoApplicant = casePersonData?.role === "coApplicant";

  const currentForm = caseData?.forms[caseData.currentFormId];
  const selfNeedsToConfirm =
    isCoApplicant &&
    currentForm.encryption.publicKeys[authContext.user.personalNumber] === null;
  const isWaitingForCoApplicantSign =
    currentForm.encryption.publicKeys &&
    !Object.entries(currentForm.encryption.publicKeys).every(
      (item) => item[1] !== null
    );

  const shouldShowCTAButton = isCoApplicant
    ? (isWaitingForSign && !selfHasSigned) ||
      (isWaitingForCoApplicantSign && selfNeedsToConfirm)
    : isOngoing || isNotStarted || isCompletionRequired || isSigned;

  const buttonProps = {
    onClick: () => navigation.navigate("Form", { caseId: caseData.id }),
    text: "",
    colorSchema: null,
  };

  const cardProps = {
    subtitle: caseData.status.name,
    description: null,
    onClick: () => {
      navigation.navigate("UserEvents", {
        screen: caseData.caseType.navigateTo,
        params: {
          id: caseData.id,
          name: caseData.caseType.name,
        },
      });
    },
  };

  if (isOngoing) {
    buttonProps.text = "Fortsätt";
  }

  if (isNotStarted) {
    buttonProps.text = "Starta ansökan";

    if (isWaitingForCoApplicantSign) {
      cardProps.subtitle = "Väntar";
      cardProps.description = "Din medsökande måste bekräfta...";
      buttonProps.colorSchema = "red";
      buttonProps.onClick = () => {
        if (extra && extra.setDialogState) {
          extra.setDialogState({
            ...extra.dialogState,
            showCoSignModal: true,
            caseData,
          });
        }
      };

      cardProps.onClick = () => {};

      if (selfNeedsToConfirm) {
        cardProps.subtitle = "Öppen";
        cardProps.description = "Din partner väntar på din bekräftelse";
        buttonProps.colorSchema = "red";
        buttonProps.text = "Bekräftar att jag söker ihop med någon";

        buttonProps.onClick = () => {
          if (extra && extra.setDialogState) {
            extra.setDialogState({
              ...extra.dialogState,
              showConfirmationThanksModal: true,
              caseData,
            });
          }
        };
      }
    }
  }

  if (isCompletionRequired) {
    buttonProps.text = "Starta stickprov";
  }

  if (isSigned) {
    buttonProps.text = "Ladda upp filer och dokument";
  }

  if (isWaitingForSign && !selfHasSigned) {
    buttonProps.onClick = () =>
      navigation.navigate("Form", { caseId: caseData.id, isSignMode: true });
    buttonProps.text = "Granska och signera";
  }

  const giveDate = payments?.payment?.givedate
    ? `${
        payments.payment.givedate.split("-")[2]
      } ${getSwedishMonthNameByTimeStamp(payments.payment.givedate, true)}`
    : null;

  return (
    <CaseCard
      key={caseData.id}
      colorSchema={colorSchema}
      title={caseData.caseType.name}
      subtitle={cardProps.subtitle}
      month={applicationPeriodMonth}
      largeSubtitle={applicationPeriodMonth}
      description={cardProps.description}
      icon={icons[caseData.caseType.icon]}
      showButton={shouldShowCTAButton}
      buttonText={buttonProps.text}
      currentStep={currentStep}
      totalSteps={totalSteps}
      showPayments={isClosed}
      showProgress={isOngoing}
      payments={calculateSum(paymentsArray)}
      declined={calculateSum(partiallyApprovedDecisionsAndRejected)}
      givedate={giveDate}
      onCardClick={cardProps.onClick}
      onButtonClick={buttonProps.onClick}
      buttonColorScheme={buttonProps.colorSchema || colorSchema}
    />
  );
};

interface CoSignDialogState {
  showCoSignModal: boolean;
  showConfirmationThanksModal: boolean;
  hasShownConfirmationThanksModal: boolean;
  caseData: Case | null;
}

/**
 * Case overview screen
 * @param {obj} props
 */
function CaseOverview(props): JSX.Element {
  const { navigation } = props;
  const [caseItems, setCaseItems] = useState<Case[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [pendingCaseSign, setPendingCaseSign] = useState<Case | null>(null);
  const { cases, getCasesByFormIds, fetchCases } = useContext(
    CaseState
  ) as Required<CaseContextState>;
  const { getForm, getFormIdsByFormTypes } = useContext(FormContext);
  const fadeAnimation = useRef(new Animated.Value(0)).current;

  const [dialogState, setDialogState] = useState<CoSignDialogState>({
    showCoSignModal: false,
    showConfirmationThanksModal: false,
    hasShownConfirmationThanksModal: false,
    caseData: null,
  });

  const authContext = useContext(AuthContext);

  const getCasesByStatuses = (statuses: string[]) =>
    caseItems.filter((caseData) => {
      let matchesStatus = false;
      statuses.forEach((status) => {
        matchesStatus =
          matchesStatus || caseData?.status?.type?.includes(status);
      });
      return matchesStatus;
    });

  const activeCases = getCasesByStatuses(["notStarted", "active"]);
  const closedCases = getCasesByStatuses(["closed"]);

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchCases();
    wait(500).then(() => {
      setRefreshing(false);
    });
  }, [fetchCases]);

  useFocusEffect(
    useCallback(() => {
      // Sometimes new cases is not created in an instant.
      // Due to this we have to give the api some time before we try to fetch cases,
      // since we cannot react to changes as of now.
      const milliseconds = 4000;
      wait(milliseconds).then(() => {
        fetchCases();
      });
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])
  );

  useFocusEffect(
    useCallback(() => {
      Animated.timing(fadeAnimation, {
        toValue: 1,
        easing: Easing.ease,
        duration: 200,
        useNativeDriver: true,
      }).start();
    }, [fadeAnimation])
  );

  useEffect(() => {
    const updateItems = async () => {
      const updateCaseItemsPromises = caseTypes.map(async (caseType) => {
        const formIds = await getFormIdsByFormTypes(caseType.formTypes);
        const formCases = getCasesByFormIds(formIds);
        const updatedFormCaseObjects = formCases.map(async (caseData) => {
          const form = await getForm(caseData.currentFormId);
          return { ...caseData, caseType, form };
        });
        return Promise.all(updatedFormCaseObjects);
      });

      await Promise.all(updateCaseItemsPromises).then((updatedItems) => {
        const flattenedList = updatedItems.flat();
        flattenedList.sort((caseA, caseB) => caseB.updatedAt - caseA.updatedAt);
        setCaseItems(flattenedList);
        setIsLoading(false);
      });
    };

    updateItems();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cases]);

  useEffect(() => {
    if (pendingCaseSign && authContext.status === "signResolved") {
      (async () => {
        const currentForm =
          pendingCaseSign.forms[pendingCaseSign.currentFormId];

        const updateCaseRequestBody = {
          currentFormId: pendingCaseSign.currentFormId,
          ...currentForm,
          signature: { success: true },
        };

        try {
          const updateCaseResponse = await put(
            `/cases/${pendingCaseSign.id}`,
            JSON.stringify(updateCaseRequestBody)
          );

          if (updateCaseResponse.status !== 200) {
            throw new Error(
              `${updateCaseResponse.status} ${updateCaseResponse?.data?.data?.message}`
            );
          }

          setPendingCaseSign(null);
          onRefresh();

          // Show last screen of form
          navigation.navigate("Form", {
            caseId: pendingCaseSign.id,
          });
        } catch (error) {
          console.log(`Could not update case with new signature: ${error}`);
        }
      })();
    }
  }, [
    pendingCaseSign,
    authContext.status,
    setPendingCaseSign,
    onRefresh,
    navigation,
  ]);

  useEffect(() => {
    const coApplicantItemsToSign = caseItems.filter((caseData) => {
      if (!caseData.persons) return false;

      const person = caseData.persons.find(
        (personEntry) =>
          personEntry.personalNumber === authContext.user.personalNumber
      );
      const isCoApplicant = person?.role === "coApplicant";

      if (!isCoApplicant) return false;

      const currentForm = caseData.forms[caseData.currentFormId];

      const isWaitingForCoApplicantSign =
        currentForm.encryption.publicKeys &&
        !Object.entries(currentForm.encryption.publicKeys).every(
          (item) => item[1] !== null
        );

      return isWaitingForCoApplicantSign;
    });

    if (coApplicantItemsToSign.length > 0) {
      if (dialogState.hasShownConfirmationThanksModal) return;
      setDialogState({
        ...dialogState,
        showConfirmationThanksModal: true,
        caseData: coApplicantItemsToSign[0],
        hasShownConfirmationThanksModal: true,
      });
    }
  }, [authContext.user?.personalNumber, caseItems, dialogState]);

  const activeCaseCards = activeCases.map((caseData) =>
    computeCaseCardComponent(caseData, navigation, authContext, {
      dialogState,
      setDialogState,
    })
  );

  const closedCaseCards = closedCases.map((caseData) =>
    computeCaseCardComponent(caseData, navigation, authContext)
  );

  const mainApplicantData = dialogState.caseData?.persons?.find(
    (person) => person.role === "applicant"
  );
  const coApplicantData = dialogState.caseData?.persons?.find(
    (person) => person.role === "coApplicant"
  );

  return (
    <ScreenWrapper {...props}>
      <Header title="Mina ärenden" />
      <Modal
        visible={dialogState.showCoSignModal}
        hide={() =>
          setDialogState({
            ...dialogState,
            showCoSignModal: false,
          })
        }
        transparent
        presentationStyle="overFullScreen"
        animationType="fade"
        statusBarTranslucent
      >
        <Wrapper>
          <DialogContainer>
            <Heading type="h4">Bekräftelse behövs</Heading>
            <Text align="center">
              För att starta ansökan måste {coApplicantData?.firstName} bekräfta
              att ni söker tillsammans. {coApplicantData?.firstName} bekräftar
              genom att logga in i appen Mitt Helsingborg.
            </Text>
            <ButtonContainer>
              <PopupButton
                onClick={() =>
                  setDialogState({
                    ...dialogState,
                    showCoSignModal: false,
                  })
                }
                block
                colorSchema="red"
              >
                <Text>Okej</Text>
              </PopupButton>
            </ButtonContainer>
          </DialogContainer>
          <BackgroundBlur
            blurType="light"
            blurAmount={15}
            reducedTransparencyFallbackColor="white"
          />
        </Wrapper>
      </Modal>
      <Modal
        visible={dialogState.showConfirmationThanksModal}
        hide={() =>
          setDialogState({
            ...dialogState,
            showConfirmationThanksModal: false,
          })
        }
        transparent
        presentationStyle="overFullScreen"
        animationType="fade"
        statusBarTranslucent
      >
        <Wrapper>
          <DialogContainer>
            <Heading type="h4">Tack, för din bekräftelse!</Heading>
            <StyledText align="center">
              Genom att logga in har du bekräftat att du och{" "}
              {mainApplicantData?.firstName} söker ekonomiskt bistånd
              tillsammans.
            </StyledText>
            <Text align="center">
              {mainApplicantData?.firstName} kan nu starta ansökan.
            </Text>
            <ButtonContainer>
              <PopupButton
                onClick={() =>
                  setDialogState({
                    ...dialogState,
                    showConfirmationThanksModal: false,
                  })
                }
                block
                colorSchema="red"
              >
                <Text>Okej</Text>
              </PopupButton>
            </ButtonContainer>
          </DialogContainer>
          <BackgroundBlur
            blurType="light"
            blurAmount={15}
            reducedTransparencyFallbackColor="white"
          />
        </Wrapper>
      </Modal>
      <Container
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        <ListHeading type="h5">Aktiva</ListHeading>
        {activeCases.length > 0 && (
          <Animated.View style={{ opacity: fadeAnimation }}>
            {activeCaseCards}
          </Animated.View>
        )}

        {!isLoading && activeCases.length === 0 && (
          <Animated.View style={{ opacity: fadeAnimation }}>
            <Card>
              <CardMessageBody>
                <Card.Text>Du har inga aktiva ärenden.</Card.Text>
              </CardMessageBody>
            </Card>
          </Animated.View>
        )}

        {closedCases.length > 0 && (
          <Animated.View style={{ opacity: fadeAnimation }}>
            <ListHeading type="h5">Avslutade</ListHeading>
            {closedCaseCards}
          </Animated.View>
        )}
      </Container>
    </ScreenWrapper>
  );
}

CaseOverview.propTypes = {
  navigation: PropTypes.any,
};

export default CaseOverview;