import json
import time
import uuid
import base64
import shutil
from tempfile import NamedTemporaryFile

import cv2
import mediapipe as mp
import numpy as np

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.core.utils import TempFileResponse


router = APIRouter(prefix="/ws", tags=["Websockets"])
connections = {}

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    smooth_landmarks=False,
    enable_segmentation=False,
)
mp_draw = mp.solutions.drawing_utils

NEW_WIDTH = 128
NEW_HEIGHT = 128
DESIRED_FPS = 30


def process_high_knees(frame, session_data: dict):
    if "jump_started" not in session_data:
        session_data.update(
            {"jump_started": False, "repetitions_count": 0, "p_time": 0}
        )

    jump_started, repetitions_count, p_time = (
        session_data["jump_started"],
        session_data["repetitions_count"],
        session_data["p_time"],
    )

    cv2.resize(frame, (NEW_WIDTH, NEW_HEIGHT), interpolation=cv2.INTER_NEAREST)

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
            (point_30_y < point_25_y or point_29_y < point_26_y)
            and (point_15_y < point_13_y and point_16_y < point_14_y)
            and not jump_started
        ):
            jump_started = True
            repetitions_count += 1

        elif point_30_y >= point_25_y and point_29_y >= point_26_y:
            jump_started = False

        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for _, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (int(cx), int(cy)), 5, (255, 0, 0), cv2.FILLED)

    current_time = time.time()
    fps = 1 / (current_time - p_time)
    p_time = current_time

    frame = cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2,
    )

    session_data.update(
        {
            "jump_started": jump_started,
            "repetitions_count": repetitions_count,
            "p_time": p_time,
        }
    )

    return frame, fps, repetitions_count


def process_jumping_jacks(frame, session_data: dict):
    if "jump_started" not in session_data:
        session_data.update(
            {"jump_started": False, "repetitions_count": 0, "p_time": 0}
        )

    jump_started, repetitions_count, p_time = (
        session_data["jump_started"],
        session_data["repetitions_count"],
        session_data["p_time"],
    )

    cv2.resize(frame, (NEW_WIDTH, NEW_HEIGHT), interpolation=cv2.INTER_NEAREST)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        left_shoulder_y = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.LEFT_SHOULDER
        ].y
        left_hand_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y
        right_shoulder_y = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.RIGHT_SHOULDER
        ].y
        right_hand_y = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.RIGHT_WRIST
        ].y
        left_ankle_y = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.LEFT_ANKLE
        ].y
        right_ankle_y = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.RIGHT_ANKLE
        ].y

        if (
            left_hand_y > left_shoulder_y
            and right_hand_y > right_shoulder_y
            and not jump_started
        ):
            if (
                left_hand_y > left_shoulder_y
                and right_hand_y > right_shoulder_y
                and left_ankle_y > right_ankle_y
                and not jump_started
            ):
                jump_started = True
                repetitions_count += 1
        elif (
            left_hand_y <= left_shoulder_y
            and right_hand_y <= right_shoulder_y
            and left_ankle_y <= right_ankle_y
        ):
            jump_started = False

        # This is no longer needed as we are sending the count only
        # mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # for idx, lm in enumerate(results.pose_landmarks.landmark):
        #     h, w, c = frame.shape
        #     cx, cy = int(lm.x * w), int(lm.y * h)
        #     cv2.circle(frame, (int(cx), int(cy)), 10, (255, 0, 0), cv2.FILLED)

    current_time = time.time()
    fps = 1 / (current_time - p_time)
    p_time = current_time

    # frame = cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    session_data.update(
        {
            "jump_started": jump_started,
            "repetitions_count": repetitions_count,
            "p_time": p_time,
        }
    )

    return frame, fps, repetitions_count


@router.websocket("")
async def workout_connection(websocket: WebSocket):
    global connections

    connection_id = str(uuid.uuid4())
    await websocket.accept()

    connections[connection_id] = {"websocket": websocket, "video_frames": []}
    print(f"New WebSocket connection: {connection_id}")

    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)

            if "type" not in data_json:
                continue

            if data_json["type"] == "reset":
                connections[connection_id]["repetitions_count"] = 0
                continue

            exercise_type = data_json["type"]
            video_b64 = data_json["data"]
            video_bytes = base64.b64decode(video_b64)
            connections[connection_id]["video_frames"].append(video_bytes)

            np_array = np.frombuffer(video_bytes, np.uint8)
            img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            connections[connection_id]["video_frames"].append(img)

            if exercise_type == "high_knees":
                _, _, repetitions_count = process_high_knees(
                    img, connections[connection_id]
                )
            elif exercise_type == "jumping_jacks":
                _, _, repetitions_count = process_jumping_jacks(
                    img, connections[connection_id]
                )
            else:
                _, _, repetitions_count = process_jumping_jacks(
                    img, connections[connection_id]
                )

            # This is no longer needed as we are sending the count only

            # _, buffer = cv2.imencode('.jpg', r_img)
            # b64_img = base64.b64encode(buffer.tobytes()).decode('utf-8')
            # await websocket.send_json({
            #     "type": "image",
            #     "data": b64_img,
            #     "connection_id": connection_id
            # })

            await websocket.send_json(
                {
                    "type": "count",
                    "data": repetitions_count,
                    "connection_id": connection_id,
                }
            )

    except WebSocketDisconnect:
        del connections[connection_id]
        print("WebSocket connection closed")
        try:
            await websocket.close()
        except:
            pass


@router.get("/download_video")
async def download_video(connection_id: str):
    connection = connections.get(connection_id)
    if not connection:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                {
                    "detail": "Connection not found",
                }
            ),
        )

    video_frames = connection["video_frames"]
    if not video_frames:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(
                {
                    "detail": "Video frames not found",
                }
            ),
        )

    path = generate_video(video_frames)
    if not path:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                {
                    "detail": "Failed to generate video",
                }
            ),
        )

    return TempFileResponse(
        path=path,
        filename=f"video_{connection_id}.mp4",
        media_type="video/mp4",
    )


def generate_video(frame_data) -> str:
    if not frame_data:
        return None

    temp_file = NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file_path = temp_file.name

    sample_frame = cv2.imdecode(
        np.frombuffer(frame_data[0], np.uint8), cv2.IMREAD_COLOR
    )
    height, width, _ = sample_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # For MP4 format
    video = cv2.VideoWriter(temp_file_path, fourcc, DESIRED_FPS, (width, height))

    for frame_bytes in frame_data:
        frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
        video.write(frame)

    video.release()

    return temp_file_path
