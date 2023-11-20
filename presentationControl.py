import cv2
import pyautogui
from pynput.keyboard import Key, Controller
import mediapipe as mp

keyboard = Controller()

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# Define a function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    print("Screenshot saved!")

# Define a function to count fingers
def count_fingers(hand_landmarks):
    if hand_landmarks:
        landmarks = hand_landmarks[0].landmark
        fingers = [1 if landmarks[lm_index].y < landmarks[lm_index - 2].y else 0 for lm_index in tipIds]
        total_fingers = fingers.count(0)  # Count closed fingers

        if total_fingers >= 3:  # Adjust the threshold as needed
            take_screenshot()

# Define a function to draw hand landmarks
def draw_hand_landmarks(image, hand_landmarks):
    if hand_landmarks:
        for landmarks in hand_landmarks:
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)

while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)

    # Detect the hands landmarks
    results = hands.process(image)
    hand_landmarks = results.multi_hand_landmarks

    # Draw hand landmarks
    draw_hand_landmarks(image, hand_landmarks)

    # Count fingers and take a screenshot if palm is closed
    count_fingers(hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Spacebar key
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
