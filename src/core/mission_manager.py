import logging
import cv2

class MissionManager:
    STATE_IDLE = "IDLE"
    STATE_RUNNING = "RUNNING"
    STATE_COMPLETED = "COMPLETED"
    STATE_ABORTED = "ABORTED"

    def __init__(self):
        self.state = self.STATE_IDLE
        self.logger = logging.getLogger(__name__)
        self.logger.info("MissionManager initialized. State: IDLE")

    def check_start_signal(self):
        """
        Checks for the start signal.
        For simulation, we check if 's' key is pressed.
        In a real mission, this might check a GPIO pin or network message.
        """
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            self.start_mission()
            return True
        return False

    def start_mission(self):
        if self.state == self.STATE_IDLE:
            self.state = self.STATE_RUNNING
            self.logger.info("Start signal received. Mission STARTED.")
        else:
            self.logger.warning(f"Cannot start mission from state {self.state}")

    def abort_mission(self):
        if self.state == self.STATE_RUNNING:
            self.state = self.STATE_ABORTED
            self.logger.warning("Mission ABORTED by user.")
        else:
            self.logger.info("Mission stopped.")

    def is_running(self):
        return self.state == self.STATE_RUNNING

    def is_idle(self):
        return self.state == self.STATE_IDLE
