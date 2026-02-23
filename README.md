# 🏋️ PoseTrack — Real-Time Pose Estimation & Rep Counter

> Real-time human pose estimation using **MediaPipe** & **OpenCV** that detects 33 body keypoints, calculates joint angles, and counts exercise reps — built for fitness apps and sports analytics.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📸 Demo

> Webcam opens → skeleton overlays on your body → joint angles display in real-time → reps get counted automatically.

---

## ✨ Features

- 🦴 **33 Body Keypoint Detection** — full body skeleton tracking in real-time
- 📐 **Joint Angle Calculation** — elbow and knee angles rendered on-screen
- 🔢 **Bicep Curl Rep Counter** — automatic up/down stage detection
- 📸 **Screenshot Capture** — press `S` to save any frame
- ⚡ **FPS Overlay** — monitor performance live
- 🎥 **Video File Support** — works on webcam or any `.mp4` file

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| MediaPipe | Pose landmark detection |
| OpenCV | Video capture & rendering |
| NumPy | Angle calculations |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Anaconda (recommended) or virtualenv

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/posetrack.git
cd posetrack

# 2. Create and activate environment
conda create -n posetrack python=3.10
conda activate posetrack

# 3. Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python pose_estimation.py
```

To use a **video file** instead of webcam, edit the last line in `pose_estimation.py`:
```python
run_pose_estimation(source="your_video.mp4")
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `Q` | Quit the app |
| `S` | Save screenshot |

---

## 🧠 How the Rep Counter Works

The bicep curl counter tracks the **right elbow angle** using 3 landmarks:

```
Shoulder → Elbow → Wrist
```

| Condition | Stage |
|-----------|-------|
| Angle > 160° | `down` |
| Angle < 40° (after down) | `up` → count +1 |

You can extend this for:
- 🦵 **Squats** → track knee angle (hip → knee → ankle)
- 💪 **Push-ups** → track shoulder & elbow together
- 🏃 **Running form** → track hip & knee symmetry

---

## 📁 Project Structure

```
posetrack/
├── pose_estimation.py   ← main script
├── requirements.txt     ← dependencies
└── README.md
```

---

## ⚠️ Troubleshooting

**Mac Apple Silicon (M1/M2/M3) — `mediapipe has no attribute 'solutions'`:**
```bash
pip uninstall mediapipe -y
pip install mediapipe==0.10.14
# or if that fails:
pip install mediapipe-silicon
```

**Webcam not opening:**
- Make sure no other app is using the camera
- Try changing `source=0` to `source=1` in the script

---

## 🔮 Future Improvements

- [ ] Squat & push-up counters
- [ ] Form correction feedback (good/bad angle alerts)
- [ ] Multi-person tracking
- [ ] Save workout session as CSV/JSON
- [ ] Streamlit web app deployment

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Author

**Saikumar**  
Computer Vision Enthusiast  
[![GitHub]([https://img.shields.io/badge/GitHub-yourusername-black?style=flat-square&logo=github)(https://github.com/SaiiiKumarrr05))
