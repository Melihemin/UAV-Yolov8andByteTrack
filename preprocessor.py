import cv2
import numpy as np
import config

def apply_clahe(frame):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the frame.
    """
    # Convert to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    # Split channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    # Merge channels
    limg = cv2.merge((cl, a, b))
    
    # Convert back to BGR
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return final

def apply_sharpen(frame):
    """
    Apply a sharpening kernel to the frame.
    """
    # Standard sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(frame, -1, kernel)
    return sharpened

def apply_filter(frame):
    """
    Apply the configured filter to the frame.
    """
    method = config.PREPROCESS_METHOD
    
    if method == 'CLAHE':
        return apply_clahe(frame)
    elif method == 'SHARPEN':
        return apply_sharpen(frame)
    else:
        return frame
