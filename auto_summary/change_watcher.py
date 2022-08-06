'''This script watches some directory for changes and if any, runs summarizer'''
import sys
import logging
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

from auto_summary import generate_summary


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class AutosummaryEventHandler(FileSystemEventHandler):
    def __init__(
        self, path: str, wikilinks: bool = True, logger: Optional[logging.Logger] = None
    ):
        super().__init__()
        self.path = Path(path).resolve()
        self.wikilinks = wikilinks
        self.logger = logger or logging.root

    def on_any_event(self, event):
        super().on_any_event(event)
        src_path = Path(event.src_path).resolve()
        if (not event.event_type == 'modified') and (src_path.suffix == '.md'):
            generate_summary.main(self.path, wikilinks=self.wikilinks)
            self.logger.info('Summary is updated')


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = AutosummaryEventHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.schedule(LoggingEventHandler(), path, recursive=True)
    observer.start()
    observer.join()


if __name__ == '__main__':
    main()
