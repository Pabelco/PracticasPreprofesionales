import * as React from 'react';
import { StyleSheet, Button, Image, View} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { LinearGradient } from 'expo-linear-gradient';
import Constants from 'expo-constants';
import * as Permissions from 'expo-permissions';
import { SplashScreen } from 'expo';

SplashScreen.preventAutoHide();
setTimeout(SplashScreen.hide, 3000);

export default class PicturePicker extends React.Component {
  state = {
    image: null,
  };

  render() {
    let { image } = this.state;

    return (
      <View style={styles.viewContainer}>
        <LinearGradient
          colors={['rgba(23,113,178,1)', 'transparent']}
          style={styles.gradientContainer}
        />
        <View>
          <Image source={require('./assets/bacteria.png')} style={styles.iconContainer}/>
        </View>
        <View style={styles.buttonContainer}>
          <Button
            title="Pick an image from camera roll"
            onPress={this._pickImage}
            color="black"
          />
        </View>
        <View style={styles.buttonContainer}>
          <Button
            title="Take a picture"
            onPress={this._takePicture}
            color="black"
          />
        </View>
        {image &&
          <Image source={{ uri: image }} style={styles.imgContainer} 
        />}
      </View>
    );
  }

  componentDidMount() {
    this.getPermissionAsync();
    console.log('Permits granted');
  }

  getPermissionAsync = async () => {
    if (Constants.platform.ios) {
      const { statusCamera } = await Permissions.askAsync(Permissions.CAMERA);
      const { statusCameraRoll } = await Permissions.askAsync(Permissions.CAMERA_ROLL);
      if (statusCameraRoll || statusCamera !== 'granted') {
        alert('Sorry, we need the camera and camera roll permissions');
      }
    }
  }

  _pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: false,
      allowsMultipleSelection: false,
      quality: 1
    });

    console.log(result);

    if (!result.cancelled) {
      this.setState({ image: result.uri });
    }
  };

  _takePicture = async () => {
    let result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: false,
      quality: 1
    });

    console.log(result);

    if (!result.cancelled) {
      this.setState({ image: result.uri });
    }
  };
}

const styles = StyleSheet.create({
  gradientContainer: {
      position: 'absolute',
      left: 0,
      right: 0,
      top: 0,
      height: 443,
  },
  viewContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonContainer: {
    backgroundColor: 'white',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 'bold',
    color: 'rgb(0,0,0)',
    borderRadius: 3,
    marginTop:10,
    marginBottom: 5,
  },
  imgContainer: { 
    width: 250,
    height: 250,
    marginTop: 25,
  },
  iconContainer: { 
    width: 100,
    height: 100,
    position: "relative",
    marginBottom: 25,
  },
});


// import React from 'react';
// import { StyleSheet, Text, View } from 'react-native';

// export default function App() {
//   return (
//     <View style={styles.container}>
//       <Text>Open up App.js to start working on your app!</Text>
//     </View>
//   );
// }


