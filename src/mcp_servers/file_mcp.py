"""MCP server for file operations"""

import logging
from pathlib import Path
from typing import Any

from .base_server import MCPServer

logger = logging.getLogger(__name__)


class FileMCPServer(MCPServer):
    """MCP server for file operations"""

    def __init__(self):
        super().__init__("FileMCP")

    async def initialize(self) -> bool:
        """Initialize file service"""
        logger.info("Initializing file service...")
        return True

    async def read_file(self, file_path: str) -> dict[str, Any]:
        """Read file content"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"status": "error", "error": f"File not found: {file_path}"}

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            return {"status": "success", "content": content}
        except Exception as e:
            logger.error(f"Failed to read file: {e}")
            return {"status": "error", "error": str(e)}

    async def write_file(self, file_path: str, content: str) -> dict[str, Any]:
        """Write to file"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"File written: {file_path}")
            return {"status": "success", "file_path": str(path)}
        except Exception as e:
            logger.error(f"Failed to write file: {e}")
            return {"status": "error", "error": str(e)}

    async def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Handle file MCP requests"""
        action = request.get("action")

        if action == "read":
            return await self.read_file(request.get("file_path"))

        if action == "write":
            return await self.write_file(
                request.get("file_path"), request.get("content")
            )

        return {"status": "error", "error": f"Unknown action: {action}"}
