import time

import cv2
import mediapipe as mp
import numpy as np

from fastapi import APIRouter
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter(prefix="/ws", tags=["Websockets"])
connections = {}

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False, 
    model_complexity=0, 
    smooth_landmarks=False, 
    enable_segmentation=False
)
mp_draw = mp.solutions.drawing_utils

NEW_WIDTH = 128
NEW_HEIGHT = 128
DESIRED_FPS = 120


def process_image(frame, session_data: dict):
    if 'jump_started' not in session_data:
        session_data.update({'jump_started': False, 'repetitions_count': 0, 'p_time': 0})
    
    jump_started, repetitions_count, p_time \
        = session_data['jump_started'], session_data['repetitions_count'], session_data['p_time']

    frame_resized = cv2.resize(
        frame, 
        (NEW_WIDTH, NEW_HEIGHT), 
        interpolation=cv2.INTER_NEAREST
    )

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

        mp_draw.draw_landmarks(
            img_rgb, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS
        )
        for _, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = img_rgb.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img_rgb, (int(cx), int(cy)), 5, (255, 0, 0), cv2.FILLED)

    current_time = time.time()
    fps = 1 / (current_time - p_time)
    p_time = current_time

    cv2.putText(img_rgb, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    session_data.update({
        'jump_started': jump_started, 
        'repetitions_count': repetitions_count, 
        'p_time': p_time
    })

    return img_rgb, fps, repetitions_count


@router.websocket("")
async def workout_connection(websocket: WebSocket):
    global connections
    
    await websocket.accept()
    connections[websocket] = {"video_frames": []}
    
    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            connections[websocket]["video_frames"].append(img)
            r_img, _, repetitions_count = process_image(img, connections[websocket])

            await websocket.send_bytes(r_img.tobytes())
            await websocket.send_text(str(repetitions_count))

    except WebSocketDisconnect:
        del connections[websocket]
        print("WebSocket connection closed")
        await websocket.close()


# @router.get("/download_video")
# async def download_video():
#     async def video_generator():
#         for frame in video_frames:
#             ret, jpeg = cv2.imencode('.jpg', frame)
#             if not ret:
#                 continue
#             yield jpeg.tobytes()

#     return StreamingResponse(video_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

