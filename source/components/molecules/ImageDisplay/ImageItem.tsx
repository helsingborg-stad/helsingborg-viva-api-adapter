/* eslint-disable no-nested-ternary */
import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components/native';
import ImageZoom from 'react-native-image-pan-zoom';
import { existsAssets, exists, readFile } from 'react-native-fs';
import {
  TouchableOpacity,
  Dimensions,
  Image as RNImage,
  GestureResponderEvent,
} from 'react-native';
import { Icon, Button, Text } from '../../atoms';
import { Modal, useModal } from '../Modal';
import { Image } from './ImageDisplay';

const DefaultItem = styled.TouchableOpacity`
  margin-bottom: 20px;
`;
const Flex = styled.View`
  flex-direction: column;
  align-items: center;
  padding: 0;
  padding-top: 10px;
  padding-right: 20px;
  margin: 0;
`;

const DeleteBackground = styled.View`
  position: absolute;
  top: 2px;
  right: 7px;
  padding: 4px;
  elevation: 3;
  background: #eeeeee;
  z-index: 1;
  border-radius: 20px;
`;
const ButtonWrapper = styled.View`
  padding: 5px;
  flex-direction: row;
  justify-content: center;
`;
const IconContainer = styled.View`
  margin: 2px
  elevation: 2;
  shadow-offset: 0px 2px;
  shadow-color: black;
  shadow-opacity: 0.4;
  shadow-radius: 5px;
  border: 1px solid transparent;
  elevation: 1;
`;
const ImageIcon = styled.Image`
  width: 126px;
  height: 178px;
`;

type FileStatus =
  | 'checkLocalFile'
  | 'localFileAvailable'
  | 'downloading'
  | 'downloadedFileAvailable';

interface Props {
  image: Image;
  onRemove: () => void;
}

const ImageItem: React.FC<Props> = ({ image, onRemove }) => {
  const [modalVisible, toggleModal] = useModal();
  const [fileStatus, setFileStatus] = useState<FileStatus>('checkLocalFile');
  const [downloadedFilePath, setDownloadedFilePath] = useState('');

  const downloadImage = async () => {
    console.log('download file, to be implemented...');
  };

  useEffect(() => {
    const checkStatus = async () => {
      if (fileStatus === 'checkLocalFile') {
        try {
          await readFile(image.path, 'base64');
          setFileStatus('localFileAvailable');
        } catch (fileNotFoundError) {
          setFileStatus('downloading');
          downloadImage();
        }
      }
    };

    checkStatus();
  }, [fileStatus, image.path]);

  const handleRemove = (event: GestureResponderEvent) => {
    event.stopPropagation();
    onRemove();
  };

  return (
    <>
      <DefaultItem onPress={toggleModal} activeOpacity={0.1}>
        <Flex>
          <DeleteBackground>
            <TouchableOpacity onPress={handleRemove} activeOpacity={0.1}>
              <Icon name="clear" color="#00213F" />
            </TouchableOpacity>
          </DeleteBackground>
          <IconContainer>
            {fileStatus === 'checkLocalFile' && <Text>Checking</Text>}
            {image && image?.path && fileStatus === 'localFileAvailable' && (
              <ImageIcon source={{ uri: image.path }} />
            )}
            {fileStatus === 'downloading' && <Text>Downloading</Text>}
            {image && image?.path && fileStatus === 'downloadedFileAvailable' && (
              <ImageIcon source={{ uri: downloadedFilePath }} />
            )}
          </IconContainer>
        </Flex>
      </DefaultItem>
      <Modal visible={modalVisible} hide={toggleModal}>
        {image && image?.path && fileStatus === 'localFileAvailable' && (
          <ImageZoom
            cropWidth={Dimensions.get('window').width}
            cropHeight={Dimensions.get('window').height * 0.89}
            imageWidth={image.width}
            imageHeight={image.height}
            panToMove
            enableCenterFocus={false}
            centerOn={{
              x: 0,
              y: 0,
              scale: Dimensions.get('window').width / image.width,
              duration: 10,
            }}
            minScale={Dimensions.get('window').width / image.width}
          >
            <RNImage
              style={{ width: image.width, height: image.height }}
              source={{ uri: image.path }}
            />
          </ImageZoom>
        )}
        {image && fileStatus === 'downloadedFileAvailable' && (
          <ImageZoom
            cropWidth={Dimensions.get('window').width}
            cropHeight={Dimensions.get('window').height * 0.89}
            imageWidth={image.width}
            imageHeight={image.height}
            panToMove
            enableCenterFocus={false}
            centerOn={{
              x: 0,
              y: 0,
              scale: Dimensions.get('window').width / image.width,
              duration: 10,
            }}
            minScale={Dimensions.get('window').width / image.width}
          >
            <RNImage
              style={{ width: image.width, height: image.height }}
              source={{ uri: downloadedFilePath }}
            />
          </ImageZoom>
        )}
        <ButtonWrapper>
          <Button colorSchema="red" onClick={toggleModal}>
            <Text>Stäng</Text>
          </Button>
        </ButtonWrapper>
      </Modal>
    </>
  );
};

ImageItem.propTypes = {
  image: PropTypes.object,
  onRemove: PropTypes.func,
};

export default ImageItem;
