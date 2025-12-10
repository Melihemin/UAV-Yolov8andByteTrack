import cv2
import time
import logging
import config
from video_loader import VideoLoader
from preprocessor import apply_filter
from detector import Detector
from tracker import Tracker
from visualizer import Visualizer
from mission_manager import MissionManager
from csv_logger import CSVLogger

# Configure logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL), format=config.LOG_FORMAT)
logger = logging.getLogger("Main")

def main():
    logger.info(f"Loading model from {config.MODEL_PATH}...")
    try:
        detector = Detector(config.MODEL_PATH)
    except FileNotFoundError as e:
        logger.error(e)
        return

    logger.info(f"Opening video source {config.VIDEO_SOURCE}...")
    try:
        loader = VideoLoader(config.VIDEO_SOURCE)
    except RuntimeError as e:
        logger.error(e)
        return

    tracker = Tracker(config.LOCKED_SQUARE_SIZE)
    visualizer = Visualizer(config.LOCKED_SQUARE_SIZE)
    mission_manager = MissionManager()
    csv_logger = None
    
    logger.info("System initialized. Entering main loop.")
    prev_time = time.time()
    
    try:
        while True:
            try:
                ret, frame = loader.read_frame()
                if not ret:
                    logger.info("Video source ended.")
                    break
                    
                # 1. Preprocessing (Filtering)
                processed_frame = apply_filter(frame)
                
                # Check Mission State
                if mission_manager.is_idle():
                    visualizer.draw_idle_screen(processed_frame)
                    if mission_manager.check_start_signal():
                        # Reset timer/state if needed when starting
                        prev_time = time.time()
                        # Initialize CSV Logger on start
                        csv_logger = CSVLogger()
                        logger.info(f"CSV Logger started: {csv_logger.filename}")
                
                elif mission_manager.is_running():
                    current_time = time.time()
                    dt = current_time - prev_time
                    prev_time = current_time
                    fps = 1.0 / dt if dt > 0 else 0.0
                    
                    # 2. Detection
                    detections = detector.detect(processed_frame, conf_thresh=config.CONF_THRESH)
                    
                    # 3. Tracking (Nearest Object)
                    nearest_obj = tracker.process_detections(detections, processed_frame.shape, dt)
                    
                    # 4. Visualization
                    visualizer.draw_overlay(processed_frame)
                    visualizer.draw_tracking(processed_frame, nearest_obj, fps)
                    
                    # 5. CSV Logging
                    if csv_logger:
                        log_data = {
                            'Timestamp': time.strftime("%H:%M:%S"),
                            'FPS': f"{fps:.2f}",
                            'Status': tracker.status,
                            'Score': tracker.score,
                            'LockTime': f"{tracker.locked_time:.2f}"
                        }
                        
                        if nearest_obj:
                            log_data.update({
                                'ObjLabel': nearest_obj['label'],
                                'ObjConf': f"{nearest_obj['conf']:.2f}",
                                'ObjDist': f"{nearest_obj['dist']:.2f}",
                                'ObjDirX': f"{nearest_obj['direction'][0]}",
                                'ObjDirY': f"{nearest_obj['direction'][1]}",
                                'BBox_X1': nearest_obj['box'][0],
                                'BBox_Y1': nearest_obj['box'][1],
                                'BBox_X2': nearest_obj['box'][2],
                                'BBox_Y2': nearest_obj['box'][3]
                            })
                        
                        csv_logger.log(log_data)
                
                # Display
                cv2.imshow('UAV Tracking Pipeline', processed_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    mission_manager.abort_mission()
                    break
            
            except Exception as e:
                logger.error(f"Runtime Error in Main Loop: {e}")
                # Continue to next frame instead of crashing
                continue
                
    except KeyboardInterrupt:
        mission_manager.abort_mission()
    finally:
        loader.release()
        if csv_logger:
            csv_logger.close()
        cv2.destroyAllWindows()
        logger.info("System shutdown.")

if __name__ == '__main__':
    main()
