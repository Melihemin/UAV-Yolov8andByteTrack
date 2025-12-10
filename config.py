import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models/best_model2.pt')
VIDEO_SOURCE = os.path.join(BASE_DIR, 'cam_sources/input_cam_video.mp4')
LOCKED_SQUARE_SIZE = 300
CONF_THRESH = 0.15
CSV_LOG_PATH = os.path.join(BASE_DIR, 'logs')

# Preprocessing Configuration
FRAME_SIZE = (640, 640)  # Resize target
ENABLE_NORMALIZE = True   # Normalize to 0-1
ENABLE_SHARPEN = True    # Apply sharpening
ENABLE_DENOISE = False   # Optional low-light denoise

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
LOG_DIR = os.path.join(BASE_DIR, 'logs')
