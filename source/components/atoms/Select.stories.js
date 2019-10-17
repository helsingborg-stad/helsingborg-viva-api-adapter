import React from 'react';
import { View } from 'react-native';
import { storiesOf } from '@storybook/react-native';
import StoryWrapper from '../molecules/StoryWrapper';
import Select from './Select';
import styled, { css } from 'styled-components/native';

storiesOf('Select', module)
    .add('default', () => (
        <StoryWrapper>           
            <Select
                onValueChange={developer => {
                    if (developer !== 'nikolas' && developer !== '') {
                        alert('SORRY THIS IS NOT TRUE PLEASE SELECT ANOTHER DEVELOPER');
                    }
                }}
                placeholder={'Select the best developer'}
                items={[
                    { label: 'Nikolas', value: 'nikolas' },
                    { label: 'Ehsan', value: 'Ehsan' },
                    { label: 'Jonatan', value: 'jonatan' },
                ]} 
            />
        </StoryWrapper>
));

