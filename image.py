import cv2
import numpy as np

# Load the Haar cascade for eye detection
haarcascade_eye = './detect/haarcascade_eye.xml'
eye_cascade = cv2.CascadeClassifier(haarcascade_eye)

# Load the glasses filter with transparency
glasses_filter = cv2.imread('./detect/filter.png', cv2.IMREAD_UNCHANGED)

# Load the input image
image_path = './img.jpg'  # Change to your image path
frame = cv2.imread(image_path)

if frame is None:
    raise FileNotFoundError("Image not found. Check the path.")

# Convert image to grayscale for detection
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
eyes = eye_cascade.detectMultiScale(gray)

if len(eyes) >= 2:
    eye_x0, eye_y0, eye_w0, eye_h0 = eyes[0]
    eye_x1, eye_y1, eye_w1, eye_h1 = eyes[1]

    x = min(eye_x0, eye_x1)
    y = min(eye_y0, eye_y1)
    w = (eye_x1 + eye_w1) - eye_x0  
    h = max(eye_h0, eye_h1)

    if w > 0 and h > 0:
        glasses_resized = cv2.resize(glasses_filter, (max(1, w + 50), max(1, h + 55)))
    else:
        raise ValueError("Invalid dimensions for glasses overlay.")

    x_offset, y_offset = x - 20, y - 20
    h_glasses, w_glasses, _ = glasses_resized.shape

    for i in range(h_glasses):
        for j in range(w_glasses):
            if glasses_resized[i, j, 3] > 0:  # Alpha channel check
                frame[y_offset + i, x_offset + j] = glasses_resized[i, j, :3]

# Save or display the output image
cv2.imshow('Glasses Filter', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./output.jpg', frame)  # Save the output image
