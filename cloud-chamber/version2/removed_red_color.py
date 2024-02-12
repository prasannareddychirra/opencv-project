import cv2
import numpy as np
import os

def process_frame(frame):
    # Remove red color from the frame
    frame_without_red = remove_red(frame)
    
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame_without_red, cv2.COLOR_BGR2GRAY)
    
    # Display the frame
    cv2.imshow('Processed Frame', gray_frame)

    return gray_frame

def remove_red(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Invert the mask to get areas without red
    mask_inverse = cv2.bitwise_not(mask)

    # Bitwise-AND mask and original image
    frame_without_red = cv2.bitwise_and(frame, frame, mask=mask_inverse)

    return frame_without_red

# Open a video capture object
cap = cv2.VideoCapture('./videos/cloudchamber_20220325_Po_edit_noAudio.mp4')

# Initialize variables for video saving
processed_frames = []
output_path = './processed_videos/processed_video.mp4'

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = process_frame(frame)
    processed_frames.append(processed_frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Combine processed frames into a single video
height, width = processed_frames[0].shape[:2]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, 30, (width, height), isColor=False)

for frame in processed_frames:
    out.write(frame)

out.release()
