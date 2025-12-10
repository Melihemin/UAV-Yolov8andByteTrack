import os

# BASE_DIR is one level up from config/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths Config
MODEL_PATH = os.path.join(BASE_DIR, 'data/models/best_model.pt')
VIDEO_SOURCE = os.path.join(BASE_DIR, 'data/videos/input_cam_video.mp4')
CSV_LOG_PATH = os.path.join(BASE_DIR, 'logs')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

LOCKED_SQUARE_SIZE = 300
CONF_THRESH = 0.15

# Preprocessing Configuration
FRAME_SIZE = None       # Resize target (None = Original size)
ENABLE_NORMALIZE = False # Normalize to 0-1
ENABLE_SHARPEN = False   # Apply sharpening
ENABLE_DENOISE = False   # Optional low-light denoise

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
