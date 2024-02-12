import cv2
import numpy as np

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
    cv2.imshow('White and Grey Areas Tracking', frame)

    return white_grey_areas_count

# Open a video capture object
cap = cv2.VideoCapture('./videos/cloudchamber_20220325_Po_edit_noAudio.mp4')
frame_rate = 30  # Adjust this based on the video's fps and how slow you want to process frames
frame_count = 0


while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % frame_rate == 0:
        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Enhance contrasts, assuming fumes are lighter or darker than surroundings
            # This is a simple way to potentially make fumes more visible
        # enhanced_frame = cv2.equalizeHist(gray_frame)

        process_frame(frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
