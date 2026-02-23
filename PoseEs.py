import cv2
import mediapipe as mp
import numpy as np
import time

# ─────────────────────────────────────────
#  MediaPipe Setup
# ─────────────────────────────────────────
mp_pose     = mp.solutions.pose
mp_drawing  = mp.solutions.drawing_utils
mp_styles   = mp.solutions.drawing_styles

# ─────────────────────────────────────────
#  Angle Calculator (for reps counter)
# ─────────────────────────────────────────
def calculate_angle(a, b, c):
    """
    Calculate the angle at point B formed by A-B-C.
    a, b, c → [x, y] coordinates
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))

    if angle > 180:
        angle = 360 - angle

    return angle


# ─────────────────────────────────────────
#  Draw Overlay Info
# ─────────────────────────────────────────
def draw_info_box(frame, text_lines, x=10, y=10, color=(0, 255, 0)):
    """Draw a semi-transparent box with text."""
    padding = 8
    line_h  = 28
    box_w   = 280
    box_h   = len(text_lines) * line_h + padding * 2

    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + box_w, y + box_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    for i, line in enumerate(text_lines):
        cv2.putText(frame, line,
                    (x + padding, y + padding + (i + 1) * line_h - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)


def draw_angle_arc(frame, point, angle, color=(255, 255, 0)):
    """Draw the angle value near a joint."""
    px = int(point[0])
    py = int(point[1])
    cv2.putText(frame, f"{int(angle)}°",
                (px + 10, py - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


# ─────────────────────────────────────────
#  Main Application
# ─────────────────────────────────────────
def run_pose_estimation(source=0):
    """
    source: 0 for webcam, or a video file path string.
    """
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open source: {source}")
        return

    # ── Curl counter state ──
    curl_count   = 0
    curl_stage   = None      # "up" or "down"

    # ── FPS tracking ──
    prev_time = time.time()

    print("[INFO] Press  Q  to quit | Press  S  to save a screenshot")

    with mp_pose.Pose(
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
        model_complexity=1          # 0=Lite, 1=Full, 2=Heavy
    ) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[INFO] End of stream.")
                break

            # ── FPS calc ──
            curr_time = time.time()
            fps       = 1 / (curr_time - prev_time + 1e-9)
            prev_time = curr_time

            h, w, _ = frame.shape

            # ── Convert to RGB for MediaPipe ──
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            results = pose.process(rgb)
            rgb.flags.writeable = True

            # ── Draw skeleton ──
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style()
                )

                lm = results.pose_landmarks.landmark

                def get_coords(landmark):
                    return [landmark.x * w, landmark.y * h]

                # ── Right arm angles ──
                try:
                    r_shoulder = get_coords(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER])
                    r_elbow    = get_coords(lm[mp_pose.PoseLandmark.RIGHT_ELBOW])
                    r_wrist    = get_coords(lm[mp_pose.PoseLandmark.RIGHT_WRIST])
                    r_hip      = get_coords(lm[mp_pose.PoseLandmark.RIGHT_HIP])
                    r_knee     = get_coords(lm[mp_pose.PoseLandmark.RIGHT_KNEE])
                    r_ankle    = get_coords(lm[mp_pose.PoseLandmark.RIGHT_ANKLE])

                    elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
                    knee_angle  = calculate_angle(r_hip, r_knee, r_ankle)

                    draw_angle_arc(frame, r_elbow, elbow_angle, (255, 255, 0))
                    draw_angle_arc(frame, r_knee,  knee_angle,  (0, 255, 255))

                    # ── Bicep curl counter ──
                    if elbow_angle > 160:
                        curl_stage = "down"
                    if elbow_angle < 40 and curl_stage == "down":
                        curl_stage = "up"
                        curl_count += 1

                except Exception:
                    pass

            # ── Info overlay ──
            draw_info_box(frame, [
                f"FPS:        {fps:.1f}",
                f"Bicep Curls: {curl_count}",
                f"Stage:      {curl_stage or 'N/A'}",
            ])

            # ── Show ──
            cv2.imshow("Pose Estimation | Press Q to quit", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"screenshot_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                print(f"[INFO] Screenshot saved → {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Session ended. Total curls counted: {curl_count}")


# ─────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────
if __name__ == "__main__":
    # ── To use webcam ──
    run_pose_estimation(source=0)

    # ── To use a video file, comment above and uncomment below ──
    # run_pose_estimation(source="your_video.mp4")