import cv2
import numpy as np

class Visualizer:
    def __init__(self, locked_square_size):
        self.locked_square_size = locked_square_size
        self.color_locked = (0, 255, 0)
        self.color_unlocked = (0, 0, 255)
        self.color_obj = (255, 0, 0)
        self.color_line = (0, 255, 255)
        

    def draw_overlay(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        half = self.locked_square_size // 2
        
        # Draw locked square
        cv2.rectangle(frame, (cx - half, cy - half), (cx + half, cy + half), (255, 255, 255), 2)
        
        # Draw center point
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

    def draw_tracking(self, frame, nearest_obj, fps):
        # Draw FPS
        cv2.putText(frame, f'FPS: {fps:.1f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if nearest_obj is None:
            # Display Status and Score even if no object (using last known or default)
            # But here we only have access to nearest_obj if it exists. 
            # Ideally Tracker holds state, but for now we display what we have.
            return

        x1, y1, x2, y2 = nearest_obj['box']
        obj_cx, obj_cy = nearest_obj['center']
        label = nearest_obj['label']
        conf = nearest_obj['conf']
        status = nearest_obj['status']
        score = nearest_obj['score']
        locked_time = nearest_obj['locked_time']
        dist = nearest_obj['dist']
        dx, dy = nearest_obj['direction']
        
        # Draw bounding box and center
        cv2.rectangle(frame, (x1, y1), (x2, y2), self.color_obj, 2)
        cv2.circle(frame, (obj_cx, obj_cy), 4, self.color_obj, -1)
        cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_obj, 2)
        
        # Draw Status, Score, Timer
        status_color = (0, 255, 0) if status == "LOCKED" else (0, 0, 255)
        cv2.putText(frame, f'Status: {status}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        cv2.putText(frame, f'Score: {score}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        if status == "LOCKED":
            cv2.putText(frame, f'Lock Time: {locked_time:.1f}s', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
        # Draw Telemetry
        cv2.putText(frame, f'Dist: {dist:.1f}px', (10, frame.shape[0] - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, f'Dir: ({dx}, {dy})', (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Redirection line logic
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        
        if status == "UNLOCKED":
            # Draw redirection line
            cv2.line(frame, (cx, cy), (obj_cx, obj_cy), self.color_line, 2)

    def draw_idle_screen(self, frame):
        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        
        # Darken the background slightly
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Draw "WAITING FOR START SIGNAL" text
        text = "WAITING FOR START SIGNAL (Press 's')"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = (h + text_size[1]) // 2
        
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 255, 255), thickness)
