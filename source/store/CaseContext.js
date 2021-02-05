import React, { useContext, useReducer, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import AuthContext from './AuthContext';
import CaseReducer, { initialState as defaultInitialState } from './reducers/CaseReducer';
import {
  updateCase as update,
  createCase as create,
  deleteCase as remove,
  fetchCases as fetch,
} from './actions/CaseActions';

const CaseState = React.createContext();
const CaseDispatch = React.createContext();

/**
 * An array that defines the different types of cases there is in the application.
 * Note: Not sure if this is the right place to save these params, but will do for know.
 * */
export const caseTypes = [
  {
    name: 'Ekonomiskt Bistånd',
    formTypes: ['EKB-recurring'],
    icon: 'ICON_EKB',
    navigateTo: 'CaseSummary',
  },
];

function CaseProvider({ children, initialState = defaultInitialState }) {
  const [state, dispatch] = useReducer(CaseReducer, initialState);
  const { user } = useContext(AuthContext);
  async function createCase(form, callback = (response) => {}) {
    dispatch(await create(form, user, Object.values(state.cases), callback));
  }

  async function updateCase(caseId, data, status, currentPosition, form) {
    dispatch(await update(caseId, data, status, currentPosition, form));
  }

  function getCase(caseId) {
    return state?.cases[caseId];
  }

  /**
   * This functions retrives cases based on formIds
   * @param {array} formIds an array of form ids.
   * @returns {array}
   */
  function getCasesByFormIds(formIds) {
    const formCases = [];
    Object.values(state.cases).forEach((c) => {
      if (formIds.includes(c.formId)) {
        formCases.push(c);
      }
    });

    return formCases;
  }

  async function deleteCase(caseId) {
    dispatch(remove(caseId));
  }

  const fetchCases = useCallback(
    async function loadCases(callback = () => {}) {
      dispatch(await fetch(callback));
    },
    [dispatch]
  );

  useEffect(() => {
    if (user) {
      fetchCases();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  return (
    <CaseState.Provider value={{ cases: state.cases, getCase, getCasesByFormIds }}>
      <CaseDispatch.Provider value={{ createCase, updateCase, deleteCase }}>
        {children}
      </CaseDispatch.Provider>
    </CaseState.Provider>
  );
}

CaseProvider.propTypes = {
  children: PropTypes.node,
  initialState: PropTypes.shape({}),
};

CaseProvider.defaultProps = {
  initialState: defaultInitialState,
};

export { CaseProvider, CaseState, CaseDispatch };