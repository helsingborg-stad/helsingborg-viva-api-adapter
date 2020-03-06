import { CompletedTasks, NavItems } from 'app/assets/dashboard';
import forms from 'app/assets/mock/forms';
import { Heading, Text } from 'app/components/atoms';
import { GroupedList, Header, ListItem, ScreenWrapper } from 'app/components/molecules';
import StorageService, { COMPLETED_FORMS_KEY } from 'app/services/StorageService';
import AuthContext from 'app/store/AuthContext';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { NavigationEvents } from 'react-navigation';
import styled from 'styled-components/native';

const TaskScreenWrapper = styled(ScreenWrapper)`
  padding-left: 0;
  padding-right: 0;
  padding-top: 0;
  padding-bottom: 0;
  background-color: #f5f5f5;
`;

const Container = styled.ScrollView`
  padding-left: 16px;
  padding-right: 16px;
`;

const List = styled.View`
  margin-top: 24px;
`;

const ListHeading = styled(Heading)`
  margin-left: 4px;
  margin-bottom: 8px;
`;

class TaskScreen extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTasks: [],
    };
  }

  componentDidMount() {
    this.getTasks();
  }

  sortTasksByDate = list => list.sort((a, b) => new Date(b.created) - new Date(a.created));

  getTasks = async () => {
    try {
      const tasks = await StorageService.getData(COMPLETED_FORMS_KEY);
      this.setState({
        activeTasks: Array.isArray(tasks) && tasks.length ? this.sortTasksByDate(tasks) : [],
      });
    } catch (error) {
      console.log('Tasks not found: ', error);
    }
  };

  renderTaskItem = item => {
    const {
      navigation: { navigate },
    } = this.props;

    const form = forms.find(formData => formData.id === item.formId);
    if (!form) {
      return null;
    }

    return (
      <ListItem
        key={item.id}
        highlighted
        title="Ansökan"
        text={form.name}
        iconName={form.icon || null}
        imageSrc={form.imageIcon || null}
        onClick={() =>
          navigate('TaskDetails', {
            answers: item.data,
            form,
          })
        }
      />
    );
  };

  render() {
    const { user } = this.context;
    const { activeTasks } = this.state;

    return (
      <TaskScreenWrapper>
        <NavigationEvents onWillFocus={() => this.getTasks()} />

        <Header
          title="Mitt Helsingborg"
          message={user && user.givenName ? `Hej ${user.givenName}!` : 'Hej!'}
          themeColor="purple"
          navItems={NavItems}
        />
        <Container>
          <List>
            <ListHeading type="h3">Aktiva</ListHeading>
            {activeTasks.length > 0 ? (
              activeTasks.map(this.renderTaskItem)
            ) : (
              <Text style={{ marginLeft: 4 }}>Inga aktiva ärenden..</Text>
            )}
          </List>

          <List>
            <GroupedList heading="Avslutade" items={CompletedTasks} />
          </List>
        </Container>
      </TaskScreenWrapper>
    );
  }
}

TaskScreen.propTypes = {
  navigation: PropTypes.object,
};

TaskScreen.contextType = AuthContext;

export default TaskScreen;
