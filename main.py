import tensorflow as tf
import cv2
import numpy as np
import os

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="model/model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Initialize webcam
cap = cv2.VideoCapture(0)
os.makedirs('upload', exist_ok=True)

def cartGan(image):
    """Applies the GAN model to cartoonize an image."""
    frame = cv2.resize(image, (512, 512))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.expand_dims(frame, 0).astype(np.float32) / 127.5 - 1

    interpreter.set_tensor(input_details[0]['index'], frame)
    interpreter.invoke()
    out = interpreter.get_tensor(output_details[0]['index'])

    out = ((out.squeeze() + 1) * 127.5).astype(np.uint8)
    
    cv2.imshow('Cartoonized', out)
    cv2.imshow('Original Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow('Live Feed', frame)

    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):  # Capture and process frame on 'q' press
        frame_path = 'upload/frame.jpg'
        cv2.imwrite(frame_path, frame)
        
        try:
            os.remove(frame_path)
        except FileNotFoundError:
            pass
        
        cartGan(frame)

    elif key == 27:  # Exit on 'Esc' press
        break

cap.release()
cv2.destroyAllWindows()
