import csv
import time
import os
import threading
import queue
from config import settings as config

class CSVLogger:
    def __init__(self):
        self.log_dir = config.LOG_DIR
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(self.log_dir, f"mission_log_{timestamp}.csv")
        
        self.file = open(self.filename, 'w', newline='')
        self.writer = csv.writer(self.file)
        
        # Write Header
        self.header = [
            'Timestamp', 'FPS', 'Status', 'Score', 'LockTime', 
            'ObjLabel', 'ObjConf', 'ObjDist', 'ObjDirX', 'ObjDirY', 
            'BBox_X1', 'BBox_Y1', 'BBox_X2', 'BBox_Y2'
        ]
        self.writer.writerow(self.header)
        self.file.flush()
        
        # Async Queue
        self.queue = queue.Queue()
        self.stopped = False
        self.thread = threading.Thread(target=self._worker)
        self.thread.daemon = True
        self.thread.start()
        
    def log(self, data):
        """
        Adds data to the queue for logging.
        """
        self.queue.put(data)
        
    def _worker(self):
        while not self.stopped or not self.queue.empty():
            try:
                data = self.queue.get(timeout=0.1)
                row = []
                for col in self.header:
                    row.append(data.get(col, ''))
                
                self.writer.writerow(row)
                self.file.flush()
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Logging error: {e}")
        
    def close(self):
        self.stopped = True
        self.thread.join()
        if self.file:
            self.file.close()
