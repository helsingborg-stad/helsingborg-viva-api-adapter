import { Question, SummaryItem } from '../types/FormTypes';

const evaluateSummaryList = (
  answers: Record<string, any>,
  items: SummaryItem[]
): boolean => {
  if (!Array.isArray(items)) {
    return false;
  }
  let isEmpty = true;
  items.forEach((item) => {
    if (!isEmpty) return;

    if (['text', 'number', 'date', 'checkbox'].includes(item.type)) {
      if (answers[item.id] && answers[item.id] !== '') isEmpty = false;
    }
    if (['arrayText', 'arrayNumber', 'arrayDate'].includes(item.type)) {
      if (answers[item.id] && Array.isArray(answers[item.id]) && answers[item.id].length > 0) {
        (answers[item.id] as string[]).forEach(a => { if (a && a !== '') isEmpty = false; })
      }
    }
  });
  return !isEmpty;
};

/** Evaluates an answer value to a boolean. False if the value is empty or false, otherwise true. */
export const evaluateAnswer = (
  questionId: string,
  answers: Record<string, any>,
  allQuestions: Question[]
): boolean => {
  const question = allQuestions.find((q) => q.id === questionId);
  if (!question) return false;

  switch (question.type) {
    case 'checkbox':
      if (answers[questionId]) return answers[questionId];
      return false;
    case 'text':
    case 'number':
    case 'date':
      return (answers[questionId] && answers[questionId] !== '');
    case 'editableList':
      return (
        answers[questionId] &&
        Object.keys(answers[questionId]).filter(
          (key) => answers[questionId][key] && answers[questionId][key] !== ''
        ).length > 0
      );
    case 'repeaterField':
      return (answers[questionId] && answers[questionId].length > 0);
    case 'summaryList':
      return evaluateSummaryList(answers, question.items || []);
    default:
      return false;
  }
};

type EvaluatedValue = boolean | '!' | '&&' | '||';

// evaluation functions
const evaluateNot = (array: EvaluatedValue[]) => {
  const arrCopy = [...array];
  const reversedIndex = arrCopy.reverse().findIndex(expr => expr === '!');
  if (reversedIndex === -1) return array;
  
  const index = arrCopy.length - reversedIndex - 1;
  arrCopy.reverse()[index+1] = !arrCopy[index+1];
  arrCopy.splice(index,1);
  return evaluateNot(arrCopy);
};
const evaluateAnd = (array: EvaluatedValue[]) => {
  const arrCopy = [...array];
  const index = arrCopy.findIndex(expr => expr === '&&');
  if (index === -1) return array;
  
  arrCopy[index-1] = (array[index-1] && array[index+1]) as EvaluatedValue;
  arrCopy.splice(index,2);
  return evaluateAnd(arrCopy);
}
const evaluateOr = (array: EvaluatedValue[]) => {
  const arrCopy = [...array];
  const index = arrCopy.findIndex(expr => expr === '||');
  if (index === -1) return array;
  
  arrCopy[index-1] = (array[index-1] || array[index+1]) as EvaluatedValue;
  arrCopy.splice(index,2);
  return evaluateOr(arrCopy);
}

const specialWords = ['!', '&&', '||'];
// regex matching the special words above
const regex = /(!|&&|\|\|)/gm;

/**
 * Evaluates an expression of the form "questionId1 && questionId2 || !questionId3".
 * Allowed boolean operators are !, &&, ||. Parenthesis are not supported.
 * Evaluates ! first, then && and lastly ||.
 * @param condition the conditional expression
 * @param answers all answers of the form
 * @param allQuestions array of the questions in the form
 */
export const parseConditionalExpression = (
  condition: string,  
  answers: Record<string, any>,
  allQuestions?: Question[]): boolean => {
    if (!Array.isArray(allQuestions)) return false;

    const conditionArray = condition.split(regex).map(string => string.trim()).filter(string => string !== '');
    //evaluate all question-ids: 
    const evaluatedArray: EvaluatedValue[] = conditionArray.map(expression => {
      if (!specialWords.includes(expression))
        return evaluateAnswer(expression, answers, allQuestions);
      else 
        return (expression as '!' | '&&' | '||');
    });
    const evaluated: boolean[] = evaluateOr(evaluateAnd(evaluateNot(evaluatedArray)));
    return evaluated[0];
  };