"""Context and memory management for the agent"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..config import get_vault_path

logger = logging.getLogger(__name__)


class ContextManager:
    """Manages agent context, memory, and Obsidian vault integration"""

    def __init__(self):
        self.vault_path = get_vault_path()
        self.memory_path = self.vault_path / "Memory"
        self.brain_path = self.vault_path / "Brain"
        self._ensure_vault_structure()

    def _ensure_vault_structure(self) -> None:
        """Ensure Obsidian vault directories exist"""
        (self.vault_path / "Brain").mkdir(parents=True, exist_ok=True)
        (self.vault_path / "Memory").mkdir(parents=True, exist_ok=True)
        (self.vault_path / "Skills").mkdir(parents=True, exist_ok=True)
        (self.vault_path / "Workflows").mkdir(parents=True, exist_ok=True)
        logger.info(f"Vault structure ready at {self.vault_path}")

    def load_context(self, context_name: str) -> dict[str, Any]:
        """Load context from Memory directory"""
        context_file = self.memory_path / f"{context_name}.md"
        if not context_file.exists():
            logger.warning(f"Context file not found: {context_file}")
            return {}

        try:
            with open(context_file, "r", encoding="utf-8") as f:
                content = f.read()
            return {"name": context_name, "content": content}
        except Exception as e:
            logger.error(f"Failed to load context: {e}")
            return {}

    def save_context(self, context_name: str, data: dict[str, Any]) -> bool:
        """Save context to Memory directory"""
        try:
            context_file = self.memory_path / f"{context_name}.md"
            with open(context_file, "w", encoding="utf-8") as f:
                f.write(f"# {context_name}\n\n")
                f.write(f"Updated: {datetime.now().isoformat()}\n\n")
                f.write(json.dumps(data, indent=2))

            logger.info(f"Context saved: {context_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to save context: {e}")
            return False

    def log_decision(self, decision: str, reasoning: str) -> bool:
        """Log agent decision to Brain directory"""
        try:
            timestamp = datetime.now().isoformat()
            log_file = self.brain_path / f"decision_{timestamp.replace(':', '-')}.md"

            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"# Agent Decision\n\n")
                f.write(f"**Time**: {timestamp}\n\n")
                f.write(f"**Decision**: {decision}\n\n")
                f.write(f"**Reasoning**:\n{reasoning}\n")

            logger.info(f"Decision logged: {decision}")
            return True
        except Exception as e:
            logger.error(f"Failed to log decision: {e}")
            return False

    def get_recent_decisions(self, limit: int = 5) -> list[dict[str, str]]:
        """Get recent agent decisions from Brain directory"""
        decisions = []
        try:
            for log_file in sorted(
                self.brain_path.glob("decision_*.md"), reverse=True
            )[:limit]:
                with open(log_file, "r", encoding="utf-8") as f:
                    decisions.append({"file": log_file.name, "content": f.read()})
        except Exception as e:
            logger.error(f"Failed to retrieve decisions: {e}")

        return decisions
