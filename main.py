from pathlib import Path
from collections import deque

import cv2
import numpy as np
import torch

# ==========================
# 설정
# ==========================

BASE_DIR = Path(__file__).resolve().parent

RESULT_DIR = BASE_DIR / "Result"
OUTPUT_DIR = BASE_DIR / "output"

RESULT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_NAME = "yolov5s"

PERSON_CLASS_ID = 0
CONF_THRES = 0.3

EMPTY_BUFFER_FRAMES = 5

# ==========================
# 유틸
# ==========================

def fmt_mmss(sec):
    sec = max(0, int(round(sec)))
    return f"{sec // 60:02d}:{sec % 60:02d}"


# ==========================
# YOLO 모델
# ==========================

def load_model():
    model = torch.hub.load(
        "ultralytics/yolov5",
        MODEL_NAME,
        pretrained=True,
        trust_repo=True
    )

    model.conf = CONF_THRES
    model.classes = [PERSON_CLASS_ID]

    return model


# ==========================
# 비디오 처리
# ==========================

def process_video(video_path, model):

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    output_video = RESULT_DIR / f"{video_path.stem}_result.mp4"

    writer = cv2.VideoWriter(
        str(output_video),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (320, 180)
    )

    history = deque(maxlen=max(1, int(round(fps))))

    in_presence = False
    pending_start = None
    last_detected_frame = 0

    frame_idx = 0

    events = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)

        det = (
            results.xyxy[0].cpu().numpy()
            if len(results.xyxy) > 0
            else np.empty((0, 6))
        )

        person_present = False

        for x1, y1, x2, y2, conf, cls_id in det:

            if int(cls_id) != PERSON_CLASS_ID:
                continue

            if float(conf) < CONF_THRES:
                continue

            person_present = True

            x1, y1, x2, y2 = map(
                int,
                [x1, y1, x2, y2]
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Person {conf:.2f}",
                (x1, max(0, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        history.append(
            1 if person_present else 0
        )

        stable_present = (
            sum(history) > len(history) // 2
        )

        t = frame_idx / fps

        if stable_present:

            last_detected_frame = frame_idx

            if not in_presence:

                if pending_start is None:
                    pending_start = t

                elif (t - pending_start) >= 1.0:

                    events.append(
                        ("ENTER", pending_start + 1.0)
                    )

                    in_presence = True

        else:

            pending_start = None

            if (
                in_presence
                and
                (frame_idx - last_detected_frame)
                >= EMPTY_BUFFER_FRAMES
            ):
                events.append(
                    ("EXIT", t)
                )

                in_presence = False

        status_text = (
            "PERSON DETECTED"
            if stable_present
            else "NO PERSON"
        )

        cv2.putText(
            frame,
            status_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        out = cv2.resize(
            frame,
            (320, 180),
            interpolation=cv2.INTER_AREA
        )

        writer.write(out)

        frame_idx += 1

    if in_presence:
        events.append(
            ("EXIT", frame_idx / fps)
        )

    cap.release()
    writer.release()

    return events, output_video


# ==========================
# 메인
# ==========================

def main():

    video_name = input(
        "Video file name (example: videos/sample.mp4): "
    )

    video_path = BASE_DIR / video_name

    if not video_path.exists():
        print("Video not found")
        return

    print("\nLoading YOLO...")
    model = load_model()

    print("\nProcessing...")
    events, output_video = process_video(
        video_path,
        model
    )

    result_lines = []

    enter_time = None

    for event, sec in events:

        if event == "ENTER":
            enter_time = sec

        elif event == "EXIT" and enter_time is not None:

            duration = sec - enter_time

            result_lines.append(
                f"Enter    : {fmt_mmss(enter_time)}"
            )

            result_lines.append(
                f"Exit     : {fmt_mmss(sec)}"
            )

            result_lines.append(
                f"Duration : {duration:.1f} sec"
            )

            result_lines.append("")

    output_txt = OUTPUT_DIR / "result.txt"

    output_txt.write_text(
        "\n".join(result_lines),
        encoding="utf-8"
    )

    print("\nDone!")
    print("Video Result :", output_video)
    print("Text Result  :", output_txt)


if __name__ == "__main__":
    main()