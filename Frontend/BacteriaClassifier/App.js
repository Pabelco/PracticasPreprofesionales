import * as React from 'react';
import { StyleSheet, Button, Image, View, TouchableNativeFeedback} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { LinearGradient } from 'expo-linear-gradient';
// import Constants from 'expo-constants';
// import * as Permissions from 'expo-permissions';
import { SplashScreen } from 'expo';

SplashScreen.preventAutoHide();
setTimeout(SplashScreen.hide, 3000);

export default class PicturePicker extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      image: null
    };
  }

  render() {

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
        {this.state.image &&
          <Image source={{ uri: this.state.image.uri }} style={styles.imgContainer} 
          />
        }
        <View style={styles.buttonContainer}>
          <Button
            title="Classify bacteria"
            onPress={this.sendPicture}
            color="black"
          />
          </View>
      </View>
    );
  }

  componentDidMount() {
    // this.getPermissionAsync();
    this.getPermissionCameraRollAsync();
    this.getPermissionCameraAsync();
    console.log('Permits granted');
  }

  // getPermissionAsync = async () => {
  //   if (Constants.platform.ios) {
  //     const { statusCamera } = await Permissions.askAsync(Permissions.CAMERA);
  //     const { statusCameraRoll } = await Permissions.askAsync(Permissions.CAMERA_ROLL);
  //     if (statusCameraRoll || statusCamera !== 'granted') {
  //       alert('Sorry, we need the camera and camera roll permissions');
  //     }
  //   }
  // }

  getPermissionCameraRollAsync = async () => {
    let permissionResult = await ImagePicker.requestCameraRollPermissionsAsync();
    if (permissionResult.granted === false) {
      alert('Permission to access camera roll is required!');
    }
  }

  getPermissionCameraAsync = async () => {
    let permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    if (permissionResult.granted === false) {
      alert('Permission to access camera is required!');
    }
  }

  sendPicture = async () => {
    let h = new Headers();
    h.append('Accept','application/json');
    // let fd = new FormData();
    // fd.append('bacteria',img,"bacteria.jpg")
    // fetch('http://localhost:3000', { // Your POST endpoint
      fetch('https://postman-echo.com/post', {
        method: 'POST',
        headers: h,
          // Content-Type may need to be completely **omitted**
          // or you may need something
        body: this.state.image
      }).then(
        response => response.json() // if the response is a JSON object
      ).then(
        success => console.log(success) // Handle the success response object
      ).catch(
        error => console.log(error) // Handle the error response object
      );
    };


  _pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: false,
      allowsMultipleSelection: false,
      quality: 1
    });

    console.log(result);

    if (!result.cancelled) {
      this.setState({ image: result });
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
      this.setState({ image: result });
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
