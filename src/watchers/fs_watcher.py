"""Filesystem event watcher"""

import asyncio
import logging
from pathlib import Path
from typing import Any

from ..config import get_settings

logger = logging.getLogger(__name__)


class FileSystemWatcher:
    """Monitors filesystem for file changes"""

    def __init__(self):
        self.settings = get_settings()
        self.watch_dirs = [
            Path(d.strip()) for d in self.settings.watch_directories.split(",")
        ]
        self.monitor_interval = self.settings.file_monitor_interval
        self.is_running = False
        self.file_cache: dict[str, float] = {}

    async def scan_directories(self) -> list[Path]:
        """Scan watched directories for new files"""
        new_files = []
        for watch_dir in self.watch_dirs:
            if not watch_dir.exists():
                logger.warning(f"Watch directory does not exist: {watch_dir}")
                continue

            for file_path in watch_dir.rglob("*"):
                if file_path.is_file():
                    try:
                        mtime = file_path.stat().st_mtime
                        if (
                            str(file_path) not in self.file_cache
                            or self.file_cache[str(file_path)] != mtime
                        ):
                            self.file_cache[str(file_path)] = mtime
                            new_files.append(file_path)
                    except OSError as e:
                        logger.error(f"Error accessing file {file_path}: {e}")

        return new_files

    async def process_file(self, file_path: Path) -> None:
        """Process a single file event"""
        logger.info(f"Processing file: {file_path}")
        # TODO: Route file event to agent for processing

    async def watch(self) -> None:
        """Start watching filesystem"""
        self.is_running = True
        logger.info(
            f"Filesystem watcher started (monitoring: {self.settings.watch_directories})"
        )

        while self.is_running:
            try:
                new_files = await self.scan_directories()
                for file_path in new_files:
                    await self.process_file(file_path)

                await asyncio.sleep(self.monitor_interval)

            except Exception as e:
                logger.error(f"Error in filesystem watcher: {e}")
                await asyncio.sleep(self.monitor_interval)

    def stop(self) -> None:
        """Stop watching filesystem"""
        self.is_running = False
        logger.info("Filesystem watcher stopped")
