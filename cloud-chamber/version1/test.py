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

    # Loop over the contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # Set a threshold for the contour area to filter out small areas (adjust as needed)
        if area > 50:
            # Draw the contour on the original frame
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    # Return the modified frame
    return frame

# Open a video capture object
cap = cv2.VideoCapture('CloudChamber.mp4')

# Get the video frame width and height
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create a VideoWriter object to save the video
out = cv2.VideoWriter('processed_output.mp4', cv2.VideoWriter_fourcc('M','J','P','G'), frame_rate, (frame_width, frame_height))

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Process the frame
    processed_frame = process_frame(frame)

    # Write the frame into the file 'processed_output.avi'
    out.write(processed_frame)

    # Display the frame with contours
    cv2.imshow('White Areas Tracking', processed_frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release everything when the job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
