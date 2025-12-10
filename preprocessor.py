import cv2
import numpy as np
import config

def apply_filter(frame):
    """
    Apply configured filters to the frame.
    Order: Resize -> Denoise (Optional) -> Sharpen -> Normalize
    """
    if frame is None:
        return None
        
    # 1. Resize (640x640)
    if config.FRAME_SIZE:
        frame = cv2.resize(frame, config.FRAME_SIZE)
        
    # 2. Denoise (Optional - for low light)
    if config.ENABLE_DENOISE:
        # Fast Denoising for real-time applications
        # h=3 is a conservative strength to preserve details
        frame = cv2.fastNlMeansDenoisingColored(frame, None, 3, 3, 7, 21)
        
    # 3. Sharpening (Hafif/Light)
    if config.ENABLE_SHARPEN:
        # Light sharpening kernel
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        frame = cv2.filter2D(frame, -1, kernel)
        
    # 4. Normalize (frame / 255.0)
    # NOTE: This converts the image to float32. cv2.imshow handles 0-1 floats correctly.
    if config.ENABLE_NORMALIZE:
        frame = frame.astype(np.float32) / 255.0
        
    return frame
