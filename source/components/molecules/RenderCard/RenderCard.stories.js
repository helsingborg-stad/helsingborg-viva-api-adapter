import React from 'react';
import { storiesOf } from '@storybook/react-native';
import { Text } from 'app/components/atoms';
import styled from 'styled-components/native';
import StoryWrapper from '../StoryWrapper';
import RenderCard from './RenderCard';

const FlexContainer = styled.ScrollView`
  background-color: #fff;
  padding: 16px;
`;

const Title = styled(Text)`
  font-size: 16px;
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 6px;
`;

const cardData = {
  colorSchema: 'blue',
  bodyColor: 'blue',
  components: [
    { type: 'image', image: 'ICON_EXPENSES' },
    { type: 'title', text: 'Card Title' },
    { type: 'subtitle', text: 'Subtitle' },
    { type: 'text', text: 'Some card text here' },
  ],
};

const cardData2 = {
  shadow: true,
  colorSchema: 'green',
  bodyColor: 'neutral',
  components: [
    { type: 'image', image: 'ICON_CONTACT_PERSON', circle: true },
    { type: 'title', text: 'Contact us' },
    { type: 'subtitle', text: 'Subtitle' },
    { type: 'text', text: 'Some card text here' },
    {
      type: 'button',
      text: 'Do it!',
      action: { type: 'email', email: 'test@test.com' },
      icon: 'email',
      iconPosition: 'left',
    },
  ],
};

const cardData3 = {
  shadow: true,
  outlined: true,
  bodyColor: 'red',
  colorSchema: 'red',
  components: [
    { type: 'title', text: 'Navigate somewhere' },
    { type: 'subtitle', text: 'Subtitle' },
    { type: 'text', text: 'Some card text here' },
    {
      type: 'button',
      text: 'Do it!',
      action: { type: 'navigate', email: 'test@test.com' },
      icon: 'arrow-forward',
    },
  ],
};

const cardData4 = {
  shadow: false,
  outlined: true,
  bodyColor: 'purple',
  colorSchema: 'purple',
  components: [
    { type: 'image', image: 'ICON_CONTACT_PERSON', circle: true },
    { type: 'subtitle', text: 'Subtitle' },
    { type: 'title', text: 'Purple theme' },
    { type: 'text', text: 'Some italic text here', italic: true },
  ],
};
storiesOf('Card Renderer', module).add('default', props => (
  <StoryWrapper {...props}>
    <FlexContainer>
      <Title>Some different card variants</Title>
      <RenderCard {...cardData} />
      <RenderCard {...cardData2} />
      <RenderCard {...cardData3} />
      <RenderCard {...cardData4} />
    </FlexContainer>
  </StoryWrapper>
));
