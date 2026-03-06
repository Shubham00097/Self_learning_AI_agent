import time
import signal
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger("agent.daemon")

class WorkspaceHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory or '.git' in event.src_path:
            return
        logger.info(f"File event: {event.event_type} at {event.src_path}")

class DaemonWatcher:
    def __init__(self, watch_dir: str, poll_interval: int = 5):
        self.watch_dir = watch_dir
        self.poll_interval = poll_interval
        self.observer = None
        self.running = False
        self.crash_count = 0

    def start(self):
        self.running = True
        
        # Register signal handlers for graceful shutdown (only in main thread)
        try:
            signal.signal(signal.SIGINT, self.shutdown)
            signal.signal(signal.SIGTERM, self.shutdown)
        except ValueError:
            # Might happen if not run in main thread during tests
            pass
        
        while self.running and self.crash_count < 3:
            try:
                self.observer = Observer()
                event_handler = WorkspaceHandler()
                self.observer.schedule(event_handler, self.watch_dir, recursive=True)
                self.observer.start()
                logger.info(f"Started daemon watching {self.watch_dir} (polling: {self.poll_interval}s)")
                
                while self.running:
                    time.sleep(self.poll_interval)
                    
            except Exception as e:
                self.crash_count += 1
                logger.error(f"Daemon crashed: {e}. Restart {self.crash_count}/3")
                if self.observer:
                    self.observer.stop()
                    self.observer.join()
                
                if self.crash_count < 3:
                    backoff = (2 ** self.crash_count) * 5
                    logger.info(f"Sleeping {backoff}s before restart...")
                    time.sleep(backoff)
                else:
                    logger.critical("Maximum crash limit reached. Exiting.")
                    self.running = False
        
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()

    def shutdown(self, signum=None, frame=None):
        logger.info(f"Shutdown signal received ({signum}). Stopping daemon...")
        self.running = False
        if self.observer:
            self.observer.stop()
