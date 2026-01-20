"""Bronze Tier: Personal AI Employee - Entry Point"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.core_agent import CoreAgent
from src.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point"""
    settings = get_settings()

    print(f"""
    ╔═══════════════════════════════════════════════════╗
    ║   {settings.agent_name:^47} ║
    ║   {settings.agent_role:^47} ║
    ║   Bronze Tier - Autonomous AI Employee           ║
    ╚═══════════════════════════════════════════════════╝
    """)

    logger.info(f"Starting {settings.agent_name}...")
    logger.info(f"Vault location: {settings.vault_path}")

    # Initialize and run agent
    agent = CoreAgent()
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
