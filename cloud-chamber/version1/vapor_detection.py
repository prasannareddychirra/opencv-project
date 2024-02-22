import cv2
import numpy as np

# Load the video
video_path = 'CloudChamber.mp4'
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# CLAHE (Contrast Limited Adaptive Histogram Equalization)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

# Loop through each frame in the video
while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE for contrast enhancement
    enhanced_gray = clahe.apply(gray_frame)

    # Adaptive Thresholding
    thresh_frame = cv2.adaptiveThreshold(enhanced_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 11, 2)

    # Optional: Morphological operations to clean up
    kernel = np.ones((5, 5), np.uint8)
    cleaned_frame = cv2.morphologyEx(thresh_frame, cv2.MORPH_OPEN, kernel)

    # Convert the cleaned frame back to BGR
    cleaned_frame_bgr = cv2.cvtColor(cleaned_frame, cv2.COLOR_GRAY2BGR)

    # Concatenate original and processed frames side by side
    combined_frame = np.hstack((frame, cleaned_frame_bgr))

    # Display combined frame
    cv2.imshow('Original + Enhanced Detection', combined_frame)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release and destroy
cap.release()
cv2.destroyAllWindows()
