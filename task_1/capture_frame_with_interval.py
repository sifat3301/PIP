import os

import cv2


# initial load parts.
path = "TextBasedExplainerVideo.mp4"
cap = cv2.VideoCapture(path)
if not cap.isOpened():
    raise IOError("Couldn't open webcam or video")

save_directory = "stored_frames"
frame_count = 0
interval = 10
flag = "second"
if flag == "minutes":
    interval = 60 * interval
else:
    interval = interval

fps = cap.get(cv2.CAP_PROP_FPS)
print("fps:", fps)

frame_interval = int(fps * interval)
print(f"Capturing every {interval} seconds -> every {frame_interval} frames")

while True:
    ret, frame = cap.read()
    os.makedirs(save_directory, exist_ok=True)
    if not ret:
        break
    cv2.imshow('frame', frame)

    if frame_count % frame_interval == 0:
        cv2.imwrite(os.path.join(save_directory, str(frame_count) + ".jpg"), frame)
    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
