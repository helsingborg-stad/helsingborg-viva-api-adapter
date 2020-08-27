/* eslint-disable react/destructuring-assignment */
import PropTypes from 'prop-types';
import React, { useState, useContext } from 'react';
import styled from 'styled-components/native';
import { WatsonAgent, Chat } from 'app/components/organisms';
import { ScreenWrapper } from 'app/components/molecules';
import { View } from 'react-native';
import { Text, Button } from 'app/components/atoms';
import { CaseDispatch } from 'app/store/CaseContext';
import FormList from 'app/components/organisms/FormList/FormList';

const ButtonContainer = styled.View`
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  bottom: 0;
`;

const HomeScreenButton = styled(Button)`
  align-content: center;
  padding: 10px;
  margin: 15px;
  max-width: 90%;
`;

const ChatScreenWrapper = styled(ScreenWrapper)`
  padding-top: 0px;
  padding-left: 0;
  padding-right: 0;
  padding-bottom: 0px;
`;

const HomeScreen = ({ navigation }) => {
  const [isInputVisible, setInputVisible] = useState(false);
<<<<<<< HEAD
  const [showChat] = useState(false);

  const { createCase, currentCase } = useContext(CaseContext);
  const { setCurrentForm, currentForm } = useContext(FormContext);

  /**
   * This side effect sets the currentForm when the currentCase is updated.
   */
  useEffect(() => {
    if (currentCase && currentCase.formId) {
      setCurrentForm(currentCase.formId);
    }
  }, [currentCase, setCurrentForm]);
=======
  const [showChat, setShowChat] = useState(false);
  const { createCase } = useContext(CaseDispatch);

  const recurringFormId = 'a3165a20-ca10-11ea-a07a-7f5f78324df2';
>>>>>>> develop

  const toggleInput = () => {
    setInputVisible(true);
    showChat(false);
  };

  return (
    <>
      <ChatScreenWrapper>
        {showChat && (
          <Chat
            ChatAgent={props => <WatsonAgent {...props} initialMessages="remote" />}
            inputComponents={{
              type: 'text',
              placeholder: 'Skriv något...',
              autoFocus: false,
              display: 'none',
            }}
            ChatUserInput={false}
            keyboardVerticalOffset={0}
            isInputVisible={isInputVisible}
          />
        )}

        <View style={{ padding: 20, marginTop: 40, height: '73%' }}>
          <FormList
            heading="Ansökningsformulär"
            onClickCallback={async formId => {
              createCase(
                formId,
                async newCase => {
                  navigation.navigate('Form', { caseData: newCase });
                },
                true
              );
            }}
          />
        </View>

        <ButtonContainer>
          {showChat ? (
            <HomeScreenButton color="purpleLight" onClick={() => toggleInput()} block>
              <Text>Ställ en fråga</Text>
            </HomeScreenButton>
          ) : null}
<<<<<<< HEAD
          <HomeScreenButton
            disabled={!currentForm.steps}
            color="purple"
            block
            onClick={() => {
              createCase(
                {},
                recurringFormId,
                async () => {
                  await setCurrentForm(recurringFormId);
                  navigation.navigate('Form');
                },
                true
              );
            }}
          >
            <Text>Starta ny Ekonomiskt Bistånd ansökan</Text>
          </HomeScreenButton>
          <HomeScreenButton
            disabled={!currentForm.steps}
            color="purple"
            block
            onClick={() => navigation.navigate('Form')}
          >
            <Text>Fortsätt senaste ansökan</Text>
          </HomeScreenButton>
        </ButtonContainer>
=======
          <Button
            color="purple"
            block
            style={styles.button}
            onClick={async () => {
              await createCase(recurringFormId, newCase => {
                navigation.navigate('Form', { caseData: newCase });
              });
            }}
          >
            <Text>Starta ny Ekonomiskt Bistånd ansökan</Text>
          </Button>
          {/* <Button
            color="purple"
            block
            style={styles.button}
            onClick={() => {
              navigation.navigate('Form', { caseData: { hello: 'world' } });
            }}
          >
            <Text>Fortsätt senaste ansökan</Text>
          </Button> */}
        </View>
>>>>>>> develop
      </ChatScreenWrapper>
    </>
  );
};

HomeScreen.propTypes = {
  navigation: PropTypes.object,
};

export default HomeScreen;
