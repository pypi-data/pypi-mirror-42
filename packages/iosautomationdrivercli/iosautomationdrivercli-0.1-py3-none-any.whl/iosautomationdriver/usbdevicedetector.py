import threading
import time
from .utils import *
from events import Events


class USBDeviceDetector:
    def __init__(self):
        self.events = Events()
        self.detected_device_ids = []
        self.is_running = False
        self.thread = None

    def start(self):
        if self.is_running:
            return
        self.thread = threading.Thread(target=USBDeviceDetector.run, args=[self])
        self.thread.start()
        self.is_running = True

    def close(self):
        if not self.thread:
            return
        self.is_running = False
        self.thread = None

    def run(self):
        while self.is_running:
            raw_ids = run_command("idevice_id -l")
            ids = []
            for id in raw_ids:
                ids.append(str(id, 'utf-8').strip())
            removed_devices = list(set(self.detected_device_ids) - set(ids))
            added_devices = list(set(ids) - set(self.detected_device_ids))
            self.detected_device_ids = ids
            self.events.on_change(ids, removed_devices, added_devices)
            time.sleep(5)
