# Cloud Chamber 


## Flask Webcam Face Detection

This Flask web application captures video from the webcam, performs face detection using the MediaPipe library, and streams the processed video to a web browser.

### Prerequisites

- Python3.9
- Flask
- OpenCV
- MediaPipe

Install the required dependencies:

```bash
pip install flask opencv-python mediapipe
```

#### Camera Detection Script

This Python script uses OpenCV to detect available cameras on the system.

#### Usage

- Detect the cameras using this script
```bash
python check_cameras_availability.py
```
#### Output
The script will print the availability status of each camera index and provide a list of detected cameras.

Example:
![Webcam Face Detection Indexes](/images/cameras.png) 
## Detect the faces

- Run the flask app 
```bash
python flask_app_for_camera.py
```
- Open your web browser and go to http://localhost:8200/ to view the live video feed with face detection.
- Press `Ctrl+C` in the terminal to stop the Flask app.

#### Notes


- The application captures video from the default camera (camera index 0).

- The face detection annotations are drawn on the video feed.

- The processed video is also saved to an MP4 file named output.mp4.

- Press Ctrl+C to stop the Flask app and release the camera.
