import cv2
import numpy as np

# def detect_cylindrical_shapes(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (7, 7), 0)
#     edges = cv2.Canny(blur, 50, 150)
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if area > 100:  # Area threshold to ignore small contours
#             try:
#                 ellipse = cv2.fitEllipse(contour)
#                 cv2.ellipse(frame, ellipse, (255, 0, 0), 2)  # Draw ellipse in blue
#             except:
#                 pass  # Skip contours where an ellipse cannot be fitted

def detect_straight_lines(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw lines in green

def detect_vapor_like_shapes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Area threshold to filter out small shapes
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)  # Draw contours in red

def process_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    white_areas_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            cv2.drawContours(frame, [contour], -1, (0, 255, 255), 2)  # Draw white area contours in yellow
            white_areas_count += 1

    # Additional detections
    detect_straight_lines(frame)
    detect_vapor_like_shapes(frame)
    # detect_cylindrical_shapes(frame)  # Detect and display cylindrical shapes

    cv2.imshow('Particle Detection', frame)

    return white_areas_count

# Video processing loop remains unchanged
cap = cv2.VideoCapture('CloudChamber.mp4')

while True:
    ret, frame = cap.read()

    if not ret:
        break

    count = process_frame(frame)
    print(f'White Areas Count: {count}')

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
