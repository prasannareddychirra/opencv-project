import cv2

def detect_cameras(max_to_check=5):
    # List to store indexes of the available cameras
    available_cameras = []

    for i in range(max_to_check):
        cap = cv2.VideoCapture(i)  # CAP_DSHOW to speed up the process on Windows
        if cap is None or not cap.isOpened():
            # If the capture is not opened, the camera index is not available
            print(f'Camera index {i} is not available.')
            cap.release()
        else:
            # If the capture is opened, the camera index is available
            print(f'Camera index {i} is available.')
            available_cameras.append(i)
            cap.release()

    return available_cameras

# Detect all connected cameras
detected_cameras = detect_cameras()
print(f'Detected cameras: {detected_cameras}')
