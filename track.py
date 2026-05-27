import cv2
import mediapipe as mp
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Load chromium window
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://en.wikipedia.org/wiki/History")
time.sleep(2)


BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


# Create landmarker
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

frame_index = 0


def temporal_smoothing():
    """"
    Smooth the output data to the range of -1, 1 for all axes.
    """
    pass





previous_y = 999999
y = 999999


# Main event loop.
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    result = landmarker.detect_for_video(mp_image, frame_index)

    h, w, _ = frame.shape



    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            # Middle finger tip = landmark 12
            lm = hand[12]

            # Get the x and y coords.
            x = int(lm.x * w)
            y = int(lm.y * h)

            # Clip the coords to zero if negative (model can predict offscreen)
            x = max(0, x)
            y = max(0, y)

            # Normalize coords to the range 0, 1
            x_norm = x / w
            y_norm = y / h

            print("Middle finger:", x_norm, y_norm)

            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

    cv2.imshow("hand", frame)



    frame_index += 1
    
    if previous_y < y:
        driver.execute_script("window.scrollBy(0, 150, { behavior: 'smooth'});")
    previous_y = y
    time.sleep(.03)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
