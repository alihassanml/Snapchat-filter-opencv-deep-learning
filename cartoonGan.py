import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2



model = tf.saved_model.load('model')
cartongen = model.signatures['serving_default']
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.expand_dims(frame, 0).astype(np.float32) / 127.5 - 1
    frame = cartongen(tf.constant(frame))['output_1']
    frame = ((frame.numpy().squeeze() + 1) * 127.5).astype(np.uint8)
    cv2.imshow('cartoonized', frame)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()