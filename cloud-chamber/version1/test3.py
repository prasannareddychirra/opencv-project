import cv2
import numpy as np

def detect_vapor_like_shapes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    vapor_detected = False

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Adjust the area threshold based on your needs
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)  # Draw vapor contours in green
            vapor_detected = True
    return vapor_detected

def detect_straight_lines(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw lines in blue

def process_frame(frame):
    # First, detect vapor-like shapes
    vapor_detected = detect_vapor_like_shapes(frame)

    # If vapor is detected, then detect straight lines
    if vapor_detected:
        detect_straight_lines(frame)

    cv2.imshow('Particle Detection', frame)

# Video processing loop
cap = cv2.VideoCapture('CloudChamber.mp4')

while True:
    ret, frame = cap.read()

    if not ret:
        break

    process_frame(frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
