# UAV Tracking & Redirection System

## Overview
This project is a real-time computer vision system designed for Unmanned Aerial Vehicles (UAVs). It detects fixed-wing aircraft using a YOLOv8 model, tracks the nearest target using ByteTrack, and provides redirection telemetry to keep the target within a locked zone.

## Features
-   **Real-time Detection**: Uses YOLOv8 with ByteTrack for robust object tracking.
-   **Target Locking**: Automatically locks onto the nearest object to the center of the frame.
-   **Telemetry Logging**: Records flight data (Timestamp, FPS, Status, Score, Position, Direction) to CSV files in real-time.
-   **Visual Feedback**: Displays a HUD with bounding boxes, status indicators, and FPS.
-   **Mission Management**: State machine implementation (IDLE -> RUNNING -> ABORTED/COMPLETED).
-   **Preprocessing**: Configurable image filters (Sharpening, CLAHE) to improve detection in various conditions.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Melihemin/UAVComputerVisionModel.git
    cd UAVComputerVisionModel
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Configuration**:
    Edit `config.py` to set your model path, video source, and parameters:
    ```python
    MODEL_PATH = 'models/best_model.pt'
    VIDEO_SOURCE = 'cam_sources/input_cam_video.mp4' # or 0 for webcam
    CONF_THRESH = 0.15
    ```

2.  **Run the System**:
    ```bash
    python main.py
    ```

3.  **Controls**:
    -   Press **'s'** to START the mission (when in IDLE state).
    -   Press **'q'** to ABORT/QUIT.

## Project Structure

-   `main.py`: Entry point, orchestrates the pipeline.
-   `detector.py`: Handles YOLO model inference and ByteTrack integration.
-   `tracker.py`: Logic for selecting the target and calculating redirection vectors.
-   `visualizer.py`: Draws the HUD, bounding boxes, and overlays.
-   `video_loader.py`: Handles video capture (file or webcam).
-   `csv_logger.py`: Async logging of telemetry data.
-   `mission_manager.py`: Manages system states.
-   `preprocessor.py`: Applies image enhancement filters.
-   `config.py`: Central configuration file.

## Logs
Mission logs are saved in the `logs/` directory with timestamped filenames (e.g., `mission_log_20251208_191227.csv`).
<img width="910" height="594" alt="image" src="https://github.com/user-attachments/assets/f1080d0a-def2-4738-b486-df4746c402ae" />

##TODO

- Filtering
- New Model Training
- İncrease Data Size & Augmention
- Validation
