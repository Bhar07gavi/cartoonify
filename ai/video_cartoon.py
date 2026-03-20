import cv2
import numpy as np
from cartoonify import cartoonify_image


def cartoonify_video(input_path, output_path, style="anime"):

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise ValueError("Could not open video")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24

    print("\nVideo Info")
    print("Frames:", total_frames)
    print("Resolution:", orig_width, "x", orig_height)
    print("FPS:", fps)

    # Resize for performance
    max_width = 720

    if orig_width > max_width:
        scale = max_width / orig_width
    else:
        scale = 1.0

    width = int(orig_width * scale)
    height = int(orig_height * scale)

    print("Processing resolution:", width, "x", height)

    # Use stable codec
    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        raise ValueError("Could not create output video")

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        try:

            frame = cv2.resize(frame, (width, height))

            success, encoded = cv2.imencode(".jpg", frame)

            if not success:
                continue

            cartoon_bytes = cartoonify_image(encoded.tobytes(), style)

            cartoon_frame = cv2.imdecode(
                np.frombuffer(cartoon_bytes, np.uint8),
                cv2.IMREAD_COLOR
            )

            if cartoon_frame is None:
                continue

            cartoon_frame = cv2.resize(cartoon_frame, (width, height))

            out.write(cartoon_frame)

        except Exception as e:
            print("Frame error:", e)
            continue

        if frame_count % 60 == 0:
            progress = int((frame_count / total_frames) * 100)
            print(f"Progress: {progress}% ({frame_count}/{total_frames})")

    cap.release()
    out.release()

    print("Video processing complete")