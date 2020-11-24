import { useReducer, useEffect } from 'react';
import formReducer from './formReducer';
import { Question, Step, StepperActions } from '../../../types/FormTypes';
import { User } from '../../../types/UserTypes';

export interface FormPosition {
  index: number;
  level: number;
  currentMainStep: number;
  currentMainStepIndex: number;
}
export interface FormReducerState {
  submitted: boolean;
  currentPosition: FormPosition;
  steps: Step[];
  allQuestions: Question[];
  user: User;
  connectivityMatrix: StepperActions[][];
  formAnswers: Record<string, any>;
  validations: Record<string, any>;
  numberOfMainSteps?: number;
}

function useForm(initialState: FormReducerState) {
  const [formState, dispatch] = useReducer(formReducer, initialState);

  useEffect(() => {
    dispatch({
      type: 'REPLACE_MARKDOWN_TEXT',
    });
    dispatch({
      type: 'COUNT_MAIN_STEPS',
    });
  }, [formState.connectivityMatrix]);

  useEffect(() => {
    dispatch({
      type: 'GET_ALL_QUESTIONS',
    });
  }, [formState.steps]);
  /**
   * Function for going forward in the form
   */
  const goToNextStep = () =>
    dispatch({
      type: 'GO_NEXT',
    });

  /**
   * Function for going back in the form
   */
  const goToPreviousStep = () =>
    dispatch({
      type: 'GO_BACK',
    });

  /**
   * Function for going back in the form
   */
  const goIntoStep = (targetStep: number | string) =>
    dispatch({
      type: 'GO_DOWN',
      payload: { targetStep },
    });

  /**
   * Function for going back in the form
   */
  const goOutToStep = (targetStep: number | string) =>
    dispatch({
      type: 'GO_UP',
      payload: { targetStep },
    });

  /** Goes back to the main form. 'Closes' the substep modal. */
  const goToMainForm = () => {
    dispatch({ type: 'GO_TO_MAIN_FORM' });
  };

  const isLastStep = () => false; // Need to think and fix this. //formState.steps.length === formState.counter;

  /**
   * Function for passing state and step values to the callback function that is passed down
   * to handle a form start action.
   * @param {func} callback callback function to be called on when a start action is triggerd
   */
  const startForm = (callback: () => void) => {
    dispatch({
      type: 'START_FORM',
      payload: { callback },
    });
  };

  /**
   * Function for handling a on submit action in the form.
   * @param {func} callback callback function to be called on form submit.
   */
  const handleSubmit = (callback: (formAnswers: Record<string, any>) => void) => {
    dispatch({
      type: 'SUBMIT_FORM',
      payload: { callback },
    });
  };

  const handleSkip = () =>
    /** TO BE IMPLEMENTED */
    null;

  /**
   * Function for passing state and step values to the callback function that is passed down
   * to handle a form close action.
   * @param {func} callback callback function to be called on when a close action is triggered
   */
  // const closeForm = (callback: (s: { state: FormReducerState }, isLastStep: boolean) => any) =>
  //   callback({ state: formState }, isLastStep());

  function closeForm() {}
  /**
   * Function for updating answer.
   */
  const handleInputChange = (answer: Record<string, any>, questionId: string) => {
    dispatch({ type: 'UPDATE_ANSWER', payload: answer });

    dispatch({ type: 'VALIDATE_ANSWER', payload: { answer, id: questionId } });
  };

  const formNavigation = {
    next: goToNextStep,
    back: goToPreviousStep,
    up: goOutToStep,
    down: goIntoStep,
    start: startForm,
    close: closeForm,
    goToMainForm,
    isLastStep,
  };

  return {
    formState,
    formNavigation,
    handleInputChange,
    handleSubmit,
  };
}

export default useForm;
