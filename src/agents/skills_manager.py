"""Skills management and execution"""

import json
import logging
from pathlib import Path
from typing import Any, Callable

from ..config import get_vault_path

logger = logging.getLogger(__name__)


class SkillsManager:
    """Manages and executes agent skills"""

    def __init__(self):
        self.vault_path = get_vault_path()
        self.skills_path = self.vault_path / "Skills"
        self.skills_path.mkdir(parents=True, exist_ok=True)
        self.registered_skills: dict[str, Callable[..., Any]] = {}
        self._load_skills_metadata()

    def _load_skills_metadata(self) -> None:
        """Load skills metadata from Obsidian vault"""
        logger.info("Loading skills metadata...")
        # TODO: Parse skill definitions from Skills directory

    def register_skill(self, skill_name: str, handler: Callable[..., Any]) -> None:
        """Register a skill handler"""
        self.registered_skills[skill_name] = handler
        logger.info(f"Skill registered: {skill_name}")

    async def execute_skill(self, skill_name: str, params: dict[str, Any]) -> dict[str, Any]:
        """Execute a registered skill"""
        if skill_name not in self.registered_skills:
            logger.error(f"Skill not found: {skill_name}")
            return {"status": "error", "error": f"Skill not found: {skill_name}"}

        try:
            handler = self.registered_skills[skill_name]
            result = await handler(**params) if asyncio.iscoroutinefunction(handler) else handler(**params)
            logger.info(f"Skill executed: {skill_name}")
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Skill execution failed: {e}")
            return {"status": "error", "error": str(e)}

    def get_skill_definition(self, skill_name: str) -> dict[str, Any]:
        """Get skill definition from Skills directory"""
        skill_file = self.skills_path / f"{skill_name}.md"
        if not skill_file.exists():
            return {}

        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()
            return {"name": skill_name, "definition": content}
        except Exception as e:
            logger.error(f"Failed to load skill definition: {e}")
            return {}

    def list_available_skills(self) -> list[str]:
        """List all available skills"""
        skills = [f.stem for f in self.skills_path.glob("*.md")]
        logger.info(f"Available skills: {len(skills)}")
        return skills


import asyncio
