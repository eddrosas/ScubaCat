import cv2
import mediapipe as mp
import imageio
import time


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

gif = imageio.mimread(r"path\assets\scuba-cat.gif")
gif_index = 0
gif_visible = False 


cap = cv2.VideoCapture(0)

def dedo_arriba(lm, punta, base):
    return lm[punta].y < lm[base].y

def mano_abierta(lm):
    return (
        dedo_arriba(lm, 8, 6) and
        dedo_arriba(lm, 12, 10) and
        dedo_arriba(lm, 16, 14) and
        dedo_arriba(lm, 20, 18)
    )

def mano_cerrada(lm):
    return not (
        dedo_arriba(lm, 8, 6) or
        dedo_arriba(lm, 12, 10) or
        dedo_arriba(lm, 16, 14) or
        dedo_arriba(lm, 20, 18)
    )

# Variables de tiempo 
historial_x = []
ultimo_tiempo = time.time()
gif_activo = False
gif_inicio = 0
DURACION_GIF = 1


def mano_agitada(x_actual, umbral=0.03, max_frames=5):
    historial_x.append(x_actual)

    if len(historial_x) > max_frames:
        historial_x.pop(0)

    if len(historial_x) < max_frames:
        return False

    desplazamiento = max(historial_x) - min(historial_x)
    return desplazamiento > umbral

# Loop principal
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    tiempo_actual = time.time()

    if not gif_activo:
        resultado = hands.process(frame_rgb)

        mano_izq_abierta_agitada = False
        mano_der_cerrada = False

        if resultado.multi_hand_landmarks and resultado.multi_handedness:
            for idx, hand_landmarks in enumerate(resultado.multi_hand_landmarks):

                lm = hand_landmarks.landmark
                mano = resultado.multi_handedness[idx].classification[0].label

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                x_centro = lm[9].x

                if mano == "Left":
                    if mano_abierta(lm) and mano_agitada(x_centro):
                        mano_izq_abierta_agitada = True

                if mano == "Right":
                    if mano_cerrada(lm):
                        mano_der_cerrada = True

        if mano_izq_abierta_agitada and mano_der_cerrada:
            gif_activo = True
            gif_inicio = tiempo_actual

    # Mostrar GIF
    if gif_activo:
        gif_frame = gif[gif_index % len(gif)]
        gif_index += 1

        gif_frame = cv2.cvtColor(gif_frame, cv2.COLOR_RGB2BGR)
        gif_frame = cv2.resize(gif_frame, (300, 300))

        cv2.imshow("GIF", gif_frame)

        if tiempo_actual - gif_inicio >= DURACION_GIF:
            gif_activo = False
            cv2.destroyWindow("GIF")

    cv2.imshow("Camara", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
