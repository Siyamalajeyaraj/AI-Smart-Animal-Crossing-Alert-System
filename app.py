import streamlit as st
import cv2
from ultralytics import YOLO
import pygame
import threading
import time
import tempfile
import os

# -------------------------------
# ⚙️ App Configuration
# -------------------------------
st.set_page_config(page_title="AI Animal Crossing Alert", layout="wide")

st.title("🐾 AI Smart Animal Crossing Alert System")
st.markdown("### Real-time Animal Detection to Prevent Road Accidents 🚗🐄")

# -------------------------------
# 🎯 Load YOLOv8 Model
# -------------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8m.pt")  # change to yolov8l.pt for higher accuracy

model = load_model()

# -------------------------------
# 🔊 Initialize Pygame Mixer
# -------------------------------
pygame.mixer.init()

def play_alert_sound():
    """Play alert sound in a separate thread."""
    def _play():
        try:
            if os.path.exists("alert.mp3"):
                pygame.mixer.music.load("alert.mp3")
                pygame.mixer.music.play()
            else:
                st.warning("⚠️ 'alert.mp3' not found in folder.")
        except Exception as e:
            st.error(f"Sound Error: {e}")
    threading.Thread(target=_play).start()

# -------------------------------
# 📋 Sidebar Options
# -------------------------------
st.sidebar.header("⚙️ Settings & Logs")

confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.25, 0.9, 0.5, 0.05)
option = st.radio("Choose Input Source:", ("Upload Video", "Use Webcam"))
log_placeholder = st.sidebar.empty()
detection_log = []

# -------------------------------
# 🎥 Load Video Source
# -------------------------------
cap = None
if option == "Upload Video":
    video_file = st.file_uploader("Upload a road video file", type=["mp4", "avi", "mov"])
    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        cap = cv2.VideoCapture(tfile.name)
elif option == "Use Webcam":
    cap = cv2.VideoCapture(0)

# Initialize session state for control buttons
if "detecting" not in st.session_state:
    st.session_state.detecting = False

# -------------------------------
# ▶️ Detection Section
# -------------------------------
if cap:
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("▶️ Start Detection"):
            st.session_state.detecting = True
        if st.button("⏹️ Stop Detection"):
            st.session_state.detecting = False

    stframe = col1.empty()
    alert_placeholder = st.empty()

    last_alert = None

    while st.session_state.detecting and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("Video ended or no camera input detected.")
            st.session_state.detecting = False
            break

        # Run YOLO detection
        results = model(frame)
        detections = results[0].boxes.data

        animal_detected = False
        detected_name = ""

        for box in detections:
            conf = float(box[4])
            if conf < confidence_threshold:
                continue
            cls = int(box[5])
            label = model.names[cls]
            if label in ["dog", "cat", "cow", "elephant", "horse", "sheep", "bear", "zebra", "giraffe","tiger"]:
                animal_detected = True
                detected_name = label
                x1, y1, x2, y2 = map(int, box[:4])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # 🚨 Alert Handling
        if animal_detected:
            alert_placeholder.markdown(
                "<h3 style='color:red;'>⚠️ Animal Detected Ahead! Slow Down!</h3>",
                unsafe_allow_html=True
            )
            if detected_name != last_alert:
                play_alert_sound()
                last_alert = detected_name

            # Add detection log
            timestamp = time.strftime("%H:%M:%S")
            detection_log.append(f"{timestamp} - {detected_name.title()} Detected")
            log_placeholder.write(detection_log[-5:])
        else:
            alert_placeholder.empty()
            last_alert = None

        # 🖼️ Show frame — updated to use the new parameter
        stframe.image(frame, channels="BGR", use_container_width=True)

        # small sleep so the UI remains responsive
        time.sleep(0.05)

    cap.release()
