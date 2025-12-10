from ultralytics import YOLO
import os

class Detector:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'Model file not found at {model_path}')
        self.model = YOLO(model_path)
        self.names = self.model.names

    def detect(self, frame, conf_thresh=0.25):
        """
        Run inference on the frame using ByteTrack.
        Returns a list of detections: {'box': [x1, y1, x2, y2], 'conf': float, 'label': str, 'id': int}
        """
        # Run tracking
        results = self.model.track(frame, conf=conf_thresh, tracker="bytetrack.yaml", persist=True, verbose=False)
        
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Confidence and Class
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = self.model.names[cls]
                
                # Track ID (if available)
                track_id = int(box.id[0]) if box.id is not None else None
                
                detections.append({
                    'box': [x1, y1, x2, y2],
                    'conf': conf,
                    'label': label,
                    'id': track_id
                })
                
        return detections
