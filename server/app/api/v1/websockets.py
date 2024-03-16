import time

import cv2
import mediapipe as mp
import numpy as np

from fastapi import APIRouter
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter(prefix="/ws", tags=["Websockets"])
pcs = set()
pcs_ws = set()
video_frames = []

mpPose = mp.solutions.pose
pose = mpPose.Pose(static_image_mode=False, model_complexity=0, smooth_landmarks=False, enable_segmentation=False)
mpDraw = mp.solutions.drawing_utils

jump_started = False
repetitions_count = 0
pTime = 0

new_width = 128
new_height = 128

desired_fps = 120


def process_image(frame):
    global jump_started, repetitions_count, pTime

    frame_resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        point_30_y = results.pose_landmarks.landmark[30].y
        point_29_y = results.pose_landmarks.landmark[29].y
        point_25_y = results.pose_landmarks.landmark[25].y
        point_26_y = results.pose_landmarks.landmark[26].y
        point_15_y = results.pose_landmarks.landmark[15].y
        point_16_y = results.pose_landmarks.landmark[16].y
        point_13_y = results.pose_landmarks.landmark[13].y
        point_14_y = results.pose_landmarks.landmark[14].y

        if (
                (point_30_y < point_25_y or point_29_y < point_26_y) and
                (point_15_y < point_13_y and point_16_y < point_14_y) and
                not jump_started
        ):
            jump_started = True
            repetitions_count += 1

        elif point_30_y >= point_25_y and point_29_y >= point_26_y:
            jump_started = False

        mpDraw.draw_landmarks(img_rgb, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img_rgb.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img_rgb, (int(cx), int(cy)), 5, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img_rgb, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return img_rgb, fps, repetitions_count


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            video_frames.append(img)  # Это было добавлено
            track_img, fps, repetitions_count = process_image(img)
            # print(repetitions_count)

            # Сохраняем одно изображение
            # cv2.imwrite('saved_image.jpg', img)

            # Отправляем изображение обратно на клиент
            _, img_encoded = cv2.imencode('.jpg', track_img)
            # await websocket.send_bytes(img_encoded.tobytes())  # если хотим видеть точки, включить
            await websocket.send_text(str(repetitions_count))

    except WebSocketDisconnect:
        pcs_ws.remove(websocket)
        pcs.remove(websocket)
        print("WebSocket connection closed")
        await websocket.close()


@router.get("/download_video")
async def download_video():
    async def video_generator():
        for frame in video_frames:
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield jpeg.tobytes()

    return StreamingResponse(video_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

