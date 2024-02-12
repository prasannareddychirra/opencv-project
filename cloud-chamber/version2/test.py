import cv2
import numpy as np

def enhance_frame(frame):
    # Convert to HSV for brightness and contrast adjustment
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Adjust brightness and contrast (these values are examples; adjust as needed)
    v = cv2.convertScaleAbs(v, alpha=1.5, beta=50)

    enhanced_hsv = cv2.merge([h, s, v])
    enhanced_frame = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)

    # Apply a sharpening filter
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    enhanced_frame = cv2.filter2D(enhanced_frame, -1, kernel)

    return enhanced_frame

def process_frame(frame):
    # Apply Gaussian Blur to reduce noise
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    
    # Convert the blurred frame to the HSV color space
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # Updated lower and upper bounds for white and light grey
    lower_white_grey = np.array([0, 0, 180])  # Adjust this to capture light grey
    upper_white_grey = np.array([180, 60, 255])  # Adjust upper bound to be more inclusive of greys

    # Create masks to extract white and grey regions
    mask_white_grey = cv2.inRange(hsv, lower_white_grey, upper_white_grey)

    # Optional: Combine masks if you have multiple ranges

    # Find contours in the combined mask
    contours, _ = cv2.findContours(mask_white_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    white_grey_areas_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:  # Consider adjusting the threshold based on your needs
            # Draw the contour on the original frame
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            white_grey_areas_count += 1

    # Display the frame with contours
    # cv2.imshow('White and Grey Areas Tracking', frame)

    return white_grey_areas_count


cap = cv2.VideoCapture('./videos/cloudchamber_20220325_Po_edit_noAudio.mp4')

# Slow down the video by reducing the playback speed
frame_delay = 100  # milliseconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Enhance frame
    enhanced_frame = enhance_frame(frame)

    # Process the enhanced frame
    process_frame(enhanced_frame)

    cv2.imshow('Enhanced and Slowed Down Video', enhanced_frame)

    if cv2.waitKey(frame_delay) & 0xFF == ord('q'):  # Increase delay for slower playback
        break

cap.release()
cv2.destroyAllWindows()
