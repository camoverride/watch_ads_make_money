import cv2
import mediapipe as mp
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yaml



# Load the config file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load chromium window
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(config["website_address"])
time.sleep(2)

# Mediapipe settings and setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1)

landmarker = HandLandmarker.create_from_options(options)

# Start cv2 video capture.
cap = cv2.VideoCapture(0)

# Track frames for hand tracking.
frame_index = 0

# Track y idexes of hands for scrolling.
previous_y = 999999
y = 999999

# Track frames for penny dispensing.
drop_penny = 1


# Main event loop.
while True:
    # Read from the camera.
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frae to RGB.
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get mediapipe landmarks.
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect_for_video(mp_image, frame_index)

    # Get frame dimensions.
    h, w, _ = frame.shape

    # If a hand is tracked, continue
    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            # Middle finger tip = landmark 12
            lm = hand[12]

            # Get the x and y coords.
            x = int(lm.x * w)
            y = int(lm.y * h)

            # Clip the coords to zero if negative (model can predict offscreen).
            x = max(0, x)
            y = max(0, y)

            # Normalize coords to the range (0, 1).
            x_norm = x / w
            y_norm = y / h

            # Debug the landmarks.
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

    # Show the hand image.
    if config["debug_window"]:
        cv2.imshow("hand", frame)

    # Increment tracked frames.
    frame_index += 1

    # Track descending finger (y-coordinate decreases)
    if previous_y < y:
        # Execute the script, which scrolls the page down.
        driver.execute_script("window.scrollBy(0, 150, { behavior: 'smooth'});")

        # Increment, which will eventually signal a dropped penny.
        drop_penny += 1

    previous_y = y
    time.sleep(.03)

    # Drop the penny.
    if drop_penny % config["penny_drop_increment"] == 0:
        print("penny")

    # Quit opencv on key press
    if cv2.waitKey(1) == 27:
        break

# Clean up opencv.
cap.release()
cv2.destroyAllWindows()
