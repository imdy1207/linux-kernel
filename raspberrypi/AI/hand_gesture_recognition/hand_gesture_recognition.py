import cv2
import mediapipe as mp
import time
import RPi.GPIO as GPIO
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def led_off(i):
    if i == 5:
        for led_pin in led_pins:
            GPIO.PWM(led_pin, 1).stop()
    else :
        GPIO.PWM(led_pins[i], 1).stop()

# led : pin 번호, duration : 지속시간, pwm_frequency : 주기
def led_dimming_many(nums, duration, pwm_frequency=100):
    pwms = [GPIO.PWM(led_pins[num], pwm_frequency) for num in nums]

    try:
        for pwm in pwms:
            pwm.start(0)

        for _ in range(int(duration * pwm_frequency)):
            # 밝아지는 과정
            for duty_cycle in range(0, 101, 5):
                for pwm in pwms:
                    pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(1 / (pwm_frequency * 2))

            # 어두워지는 과정
            for duty_cycle in range(100, -1, -5):
                for pwm in pwms:
                    pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(1 / (pwm_frequency * 2))
    finally:
        for pwm in pwms:
            pwm.stop()

# 손가락 개수 세기 함수
def count_fingers(hand_landmarks):
    finger_tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    count = 0
    for finger_tip in finger_tips:
        if hand_landmarks.landmark[finger_tip].y < hand_landmarks.landmark[finger_tip-1].y:
            count += 1
    return count

GPIO.setmode(GPIO.BCM)
led_pins = [24, 23, 22, 27]
for led_pin in led_pins:
    GPIO.setup(led_pin, GPIO.OUT)

hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

num = 0

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 손가락 끝이 PIP보다 위에 있고 엄지손가락 끝이 IP보다 오른쪽에 있는 경우
            if (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y) and (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x):
                print("Okay!")

            # 손가락 개수가 4개인 경우
            elif count_fingers(hand_landmarks) == 4 and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
                print("palm detection!")
                if num == 4 :
                    continue
                led_dimming_many([0, 1, 2, 3], 0.1)
                num = 4
                time.sleep(0.5)

            # 손가락 개수가 3개인 경우
            elif count_fingers(hand_landmarks) == 3 and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y:
                print("3")
                if num == 3 :
                    continue
                led_dimming_many([0, 1, 2], 0.1)
                num = 3
                time.sleep(0.5)

            # 손가락 개수가 2개인 경우
            elif count_fingers(hand_landmarks) == 2 and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y:
                led_off(5)
                print("2")
                if num == 2 :
                    continue
                led_dimming_many([0, 1], 0.1)
                num = 2
                time.sleep(0.5)

            # 손가락 개수가 1개인 경우
            elif count_fingers(hand_landmarks) == 1 and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y :
                #led_off(5)
                print("1")
                if num == 1 :
                    continue
                led_dimming_many([0], 0.1)
                num = 1
                time.sleep(0.5)

            # 손가락 개수 출력
            finger_count = count_fingers(hand_landmarks)
            if finger_count > 0:
                print("count of finger is " + str(finger_count))

        #cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()