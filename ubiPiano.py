import cv2
import mediapipe as mp
import playsound as ps


def play_key(key):
    # path = f'./sounds/{key}.mp3'
    # ps.playsound(path)
    print(f'Key: {key}')


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

boundary_x = 0.90
boundary_a = 0.33
boundary_b = 0.66

left_hand_notes = {'thumb': 'F', 'index': 'E', 'middle': 'D', 'ring': 'C'}
right_hand_notes = {'thumb': 'G', 'index': 'A', 'middle': 'B', 'ring': 'C'}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, c = frame.shape
    boundary_y = int(boundary_x * h)
    boundary_a_x = int(boundary_a * w)
    boundary_b_x = int(boundary_b * w)
    cv2.line(frame, (boundary_a_x, boundary_y), (boundary_a_x, h), (255, 0, 0), 2)
    cv2.line(frame, (boundary_b_x, boundary_y), (boundary_b_x, h), (0, 255, 0), 2)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            if id == 0:
                fingers = left_hand_notes
            else:
                fingers = right_hand_notes

            for finger, note in fingers.items():
                if lm.y > boundary_x:
                    if lm.x < boundary_a:
                        play_key("A")
                    if boundary_a < lm.x < boundary_b:
                        play_key("B")
                    if lm.x > boundary_b:
                        play_key("C")
                    play_key("Touching Piano")

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
