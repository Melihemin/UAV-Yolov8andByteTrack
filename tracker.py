import numpy as np

def _is_fixedwing_label(label: str) -> bool:
    if label is None:
        return False
    s = label.lower()
    return 'fixed' in s or 'fixedwing' in s or 'fixed-wing' in s

class Tracker:
    def __init__(self, locked_square_size):
        self.locked_square_size = locked_square_size
        self.score = 0
        self.locked_time = 0.0
        self.status = "UNLOCKED"

    def process_detections(self, detections, frame_shape, dt):
        h, w = frame_shape[:2]
        cx, cy = w // 2, h // 2
        half = self.locked_square_size // 2
        
        fixedwing_candidates = []
        
        for det in detections:
            if not _is_fixedwing_label(det['label']):
                continue
                
            x1, y1, x2, y2 = map(int, det['box'])
            obj_cx = (x1 + x2) // 2
            obj_cy = (y1 + y2) // 2
            
            dist = np.sqrt((obj_cx - cx)**2 + (obj_cy - cy)**2)
            
            fixedwing_candidates.append({
                'box': (x1, y1, x2, y2),
                'center': (obj_cx, obj_cy),
                'label': det['label'],
                'conf': det['conf'],
                'dist': dist
            })
            
        nearest_obj = None
        if fixedwing_candidates:
            # Sort by distance (ascending) to find the nearest to center
            nearest_obj = min(fixedwing_candidates, key=lambda x: x['dist'])
            
            # Check if inside locked square
            obj_cx, obj_cy = nearest_obj['center']
            is_locked = (cx - half <= obj_cx <= cx + half and cy - half <= obj_cy <= cy + half)
            
            if is_locked:
                self.status = "LOCKED"
                self.locked_time += dt
                if self.locked_time >= 5.0:
                    self.score += 1
                    self.locked_time = 0.0 # Reset timer after scoring
            else:
                self.status = "UNLOCKED"
                self.locked_time = 0.0
                
            # Calculate direction vector
            dx = obj_cx - cx
            dy = obj_cy - cy
            
            nearest_obj['status'] = self.status
            nearest_obj['locked_time'] = self.locked_time
            nearest_obj['score'] = self.score
            nearest_obj['direction'] = (dx, dy)
            
            # Print Telemetry to Console (Single Line)
            status_icon = "🟢" if self.status == "LOCKED" else "🔴"
            print(f"{status_icon} [{self.status}] ID: {nearest_obj.get('id', 'N/A')} | Score: {self.score} | Lock: {self.locked_time:.1f}s | Dist: {nearest_obj['dist']:.0f}px | Dir: ({dx}, {dy})")
            
        else:
            self.status = "UNLOCKED"
            self.locked_time = 0.0
            print(f"🔴 [UNLOCKED] Searching...")
            
        return nearest_obj
