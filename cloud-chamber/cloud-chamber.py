import cv2
import numpy as np

def process_frame(frame):
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for white color in HSV
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])

    # Create a mask to extract the white region
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a counter for white areas
    white_areas_count = 0

    # Loop over the contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # Set a threshold for the contour area to filter out small areas (adjust as needed)
        if area > 50:
            # Draw the contour on the original frame
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

            # Increment the white areas count
            white_areas_count += 1

    # Display the frame with contours
    cv2.imshow('White Areas Tracking', frame)

    return white_areas_count

# Open a video capture object (replace 'your_video_file.mp4' with the actual video file name)
cap = cv2.VideoCapture('CloudChamber.mp4')

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Call the function to process the frame and get the count of white areas
    count = process_frame(frame)

    # Print the count of white areas
    print(f'White Areas Count: {count}')

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
