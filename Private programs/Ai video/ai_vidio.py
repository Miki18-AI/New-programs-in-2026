import cv2
import mediapipe as mp
import math

# Инициализируем модули
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

def get_dist(p1, p2):
    return math.hypot(p1[1] - p2[1], p1[2] - p2[2])

cap = cv2.VideoCapture(0)

# Пути к файлам
video_cat_path = r'C:\codiki\codoko\Private programs\gato.gif' 
video_cat_cap = cv2.VideoCapture(video_cat_path)

video_smile_path = r'C:\codiki\codoko\Private programs\smile.gif' 
video_smile_cap = cv2.VideoCapture(video_smile_path)

# --- ТЕ САМЫЕ ПРЕДОХРАНИТЕЛИ ---
is_cat_open = False
is_smile_open = False

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    open_hands_count = 0
    pointing_hands_count = 0 

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            if len(lm_list) != 0:
                wrist = lm_list[0]
                
                index_open = get_dist(lm_list[8], wrist) > get_dist(lm_list[6], wrist)
                middle_open = get_dist(lm_list[12], wrist) > get_dist(lm_list[10], wrist)
                ring_open = get_dist(lm_list[16], wrist) > get_dist(lm_list[14], wrist)
                pinky_open = get_dist(lm_list[20], wrist) > get_dist(lm_list[18], wrist)

                if index_open and middle_open and ring_open and pinky_open:
                    open_hands_count += 1
                elif index_open and not middle_open and not ring_open and not pinky_open:
                    pointing_hands_count += 1

    # --- ИСПРАВЛЕННАЯ ЛОГИКА УПРАВЛЕНИЯ ОКНАМИ ---
    
    if open_hands_count == 2:
        cv2.putText(img, "2 HANDS = CAT!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        v_success, v_img = video_cat_cap.read()
        if v_success:
            cv2.imshow("Cat Video", cv2.resize(v_img, (640, 480)))
            is_cat_open = True # Запоминаем, что открыли
        else:
            video_cat_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
        # Если был открыт смайл - закрываем его 1 раз
        if is_smile_open:
            cv2.destroyWindow("Smile Video")
            is_smile_open = False

    elif pointing_hands_count == 2:
        cv2.putText(img, "POINTING = SMILE!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        s_success, s_img = video_smile_cap.read()
        if s_success:
            cv2.imshow("Smile Video", cv2.resize(s_img, (640, 480)))
            is_smile_open = True # Запоминаем, что открыли
        else:
            video_smile_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
        # Если был открыт кот - закрываем его 1 раз
        if is_cat_open:
            cv2.destroyWindow("Cat Video")
            is_cat_open = False

    else:
        # Если жестов нет, проверяем открыты ли окна, и удаляем строго 1 раз!
        if is_cat_open:
            cv2.destroyWindow("Cat Video")
            is_cat_open = False
        if is_smile_open:
            cv2.destroyWindow("Smile Video")
            is_smile_open = False

    cv2.imshow("Scubacat Tracker", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_cat_cap.release()
video_smile_cap.release()
cv2.destroyAllWindows()