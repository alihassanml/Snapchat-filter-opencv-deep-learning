import cv2
import numpy as np

haarcascade_eye = './detect/haarcascade_eye.xml'
eye_cascade = cv2.CascadeClassifier(haarcascade_eye)

glasses_filter = cv2.imread('./detect/filter.png', cv2.IMREAD_UNCHANGED)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
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
            continue  # Skip if invalid dimensions


        x_offset, y_offset = x - 20, y - 20
        h_glasses, w_glasses, _ = glasses_resized.shape

        for i in range(h_glasses):
            for j in range(w_glasses):
                if glasses_resized[i, j, 3] > 0:
                    frame[y_offset + i, x_offset + j] = glasses_resized[i, j, :3]

    cv2.imshow('Glasses Filter', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
