"""Watcher modules for event detection"""

from .fs_watcher import FileSystemWatcher
from .gmail_watcher import GmailWatcher
from .whatsapp_watcher import WhatsAppWatcher

__all__ = ["FileSystemWatcher", "GmailWatcher", "WhatsAppWatcher"]
