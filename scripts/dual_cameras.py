from flask import Flask, Response
import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Face Detection.
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

app = Flask(__name__)

# Initialize the cameras
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

# Define the codec and create VideoWriter objects for MP4 format
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'x264', 'H264'
out1 = cv2.VideoWriter('output1.mp4', fourcc, 20.0, (640, 480))
out2 = cv2.VideoWriter('output2.mp4', fourcc, 20.0, (640, 480))

# Check if the webcams are opened correctly
if not cap1.isOpened() or not cap2.isOpened():
    raise IOError("Cannot open webcams")

def gen_frames(camera):
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while True:
            ret, frame = camera.read()
            if not ret:
                break
            else:
                # Resize frame for faster processing
                frame = cv2.resize(frame, (640, 480))
                
                # Convert the frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # To improve performance, optionally mark the frame as not writeable to pass by reference.
                frame.flags.writeable = False
                results = face_detection.process(frame)

                # Draw the face detection annotations on the frame.
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                if results.detections:
                    for detection in results.detections:
                        mp_drawing.draw_detection(frame, detection)
                
                # Write the frame to the video file
                if camera == cap1:
                    out1.write(frame)
                else:
                    out2.write(frame)
                
                # Encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", frame)
                if not flag:
                    continue
                
                # Yield the output frame in the byte format
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                    bytearray(encodedImage) + b'\r\n')
                
                # Introduce a slight delay to reduce frame rate
                time.sleep(0.033)

@app.route('/camera1')
def video_feed1():
    return Response(gen_frames(cap1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera2')
def video_feed2():
    return Response(gen_frames(cap2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8200, debug=True, threaded=True, use_reloader=False)

# Release the cameras and video writers when the app is stopped
cap1.release()
cap2.release()
out1.release()
out2.release()
