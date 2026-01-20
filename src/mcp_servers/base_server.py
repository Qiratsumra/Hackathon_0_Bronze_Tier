"""Base MCP server implementation"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from ..config import get_settings

logger = logging.getLogger(__name__)


class MCPServer(ABC):
    """Abstract base class for MCP servers"""

    def __init__(self, name: str):
        self.settings = get_settings()
        self.name = name
        self.is_running = False
        logger.info(f"MCP Server initialized: {name}")

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize MCP server"""
        pass

    @abstractmethod
    async def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Handle incoming MCP request"""
        pass

    async def start(self) -> None:
        """Start the MCP server"""
        self.is_running = True
        if await self.initialize():
            logger.info(f"{self.name} MCP server started")
        else:
            logger.error(f"Failed to initialize {self.name}")

    def stop(self) -> None:
        """Stop the MCP server"""
        self.is_running = False
        logger.info(f"{self.name} MCP server stopped")
