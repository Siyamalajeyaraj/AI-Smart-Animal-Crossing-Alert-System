🧠 AI Smart Animal Crossing Alert System

Real-time AI-powered system that detects animals crossing the road and alerts drivers to prevent accidents.

This project uses YOLOv8, OpenCV, Streamlit, and audio alerts to create an intelligent safety system suitable for highways, rural roads, and wildlife crossing zones.

🚀 Features

✔ Real-time animal detection (cow, dog, cat, elephant, horse, sheep, etc.)
✔ Instant audio alerts when an animal is detected
✔ Webcam support + video upload support
✔ Adjustable confidence threshold
✔ Detection logs with timestamps
✔ Clean and interactive Streamlit dashboard
✔ YOLOv8 model integration
✔ Works with MP4, AVI, MOV videos

🛠️ Technologies Used

Python 3

Streamlit

OpenCV

Ultralytics YOLOv8

Pygame (audio alerts)

Threading (non-blocking sound)

📷 How It Works

The system takes video input (webcam or uploaded video).

YOLOv8 processes each frame and detects animals.

If an animal is detected:

A bounding box appears on the screen

A warning message is displayed

A beep/alert sound plays

A detection log updates in real time.

🖥️ How to Run the Project
1️⃣ Clone the repository
git clone : (https://github.com/Siyamalajeyaraj/AI-Smart-Animal-Crossing-Alert-System.git)
cd AI-Smart-Animal-Crossing-Alert-System

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the Streamlit app
streamlit run app.py

4️⃣ Choose your input

Upload a video

Or use your webcam

🎯 Use Cases

Smart road safety systems

Highway animal crossing detection

Real-time wildlife protection

AI-assisted transportation monitoring

Farmer/livestock monitoring systems

📁 Project Structure
📦 AI Smart Animal Crossing Alert System
 ├── app.py                # Main Streamlit application
 ├── sound_test.py         # Sound testing script
 ├── alert.mp3             # Beep/alert sound
 ├── SmartAnimalCrossingSample.mp4  # Sample video
 ├── requirements.txt      # Dependencies
 ├── README.md             # Project documentation
 ├── LICENSE               # MIT license
 └── .gitignore            # Ignored files

📜 License

This project is licensed under the MIT License — feel free to use and modify it.

👩‍💻 Author

Siyamalajeyaraj Renu
AI & Machine Learning Enthusiast

