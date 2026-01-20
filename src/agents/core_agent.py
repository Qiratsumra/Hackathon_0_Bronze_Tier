"""Core agent implementation with Gemini integration and rate limit handling"""

import asyncio
import logging
import re
from typing import Any, Optional
from datetime import datetime, timedelta

import google.genai as genai # pyright: ignore[reportMissingImports]
from google.api_core import exceptions

from ..config import get_settings
from ..watchers import FileSystemWatcher, GmailWatcher, WhatsAppWatcher
from .context_manager import ContextManager
from .skills_manager import SkillsManager

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter to prevent exceeding API quotas"""
    
    def __init__(self, max_requests_per_minute: int = 10, max_requests_per_day: int = 1000):
        self.max_per_minute = max_requests_per_minute
        self.max_per_day = max_requests_per_day
        self.minute_requests = []
        self.day_requests = []
    
    async def acquire(self):
        """Wait if necessary to respect rate limits"""
        now = datetime.now()
        
        # Clean old requests
        one_minute_ago = now - timedelta(minutes=1)
        one_day_ago = now - timedelta(days=1)
        
        self.minute_requests = [req for req in self.minute_requests if req > one_minute_ago]
        self.day_requests = [req for req in self.day_requests if req > one_day_ago]
        
        # Check minute limit
        if len(self.minute_requests) >= self.max_per_minute:
            wait_time = (self.minute_requests[0] - one_minute_ago).total_seconds() + 1
            logger.warning(f"Rate limit: waiting {wait_time:.1f}s for per-minute quota")
            await asyncio.sleep(wait_time)
            return await self.acquire()
        
        # Check day limit
        if len(self.day_requests) >= self.max_per_day:
            wait_time = (self.day_requests[0] - one_day_ago).total_seconds() + 1
            logger.warning(f"Daily rate limit reached. Waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
            return await self.acquire()
        
        # Record this request
        self.minute_requests.append(now)
        self.day_requests.append(now)


class CoreAgent:
    """Main agent orchestrator with Gemini AI"""

    def __init__(self):
        self.settings = get_settings()
        self.client = genai.Client(api_key=self.settings.gemini_api_key)
        self.context_manager = ContextManager()
        self.skills_manager = SkillsManager()

        # Initialize rate limiter (adjust limits based on your tier)
        self.rate_limiter = RateLimiter(
            max_requests_per_minute=5,   # Conservative for free tier
            max_requests_per_day=100     # Adjust based on your quota
        )

        # Initialize watchers
        self.gmail_watcher = GmailWatcher()
        self.whatsapp_watcher = WhatsAppWatcher()
        self.fs_watcher = FileSystemWatcher()

        self.is_running = False
        self.conversation_history: list[dict[str, str]] = []

    async def _call_gemini_with_retry(
        self,
        prompt: str,
        max_retries: int = 3,
        base_delay: float = 20.0
    ) -> Optional[str]:
        """Call Gemini API with exponential backoff retry logic"""
        
        for attempt in range(max_retries):
            try:
                # Wait for rate limiter
                await self.rate_limiter.acquire()
                
                # Make the API call
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                return response.text
                
            except exceptions.ResourceExhausted as e:
                error_msg = str(e)
                
                # Extract retry delay from error if available
                match = re.search(r'retry in ([\d.]+)s', error_msg)
                if match:
                    suggested_delay = float(match.group(1))
                    delay = max(suggested_delay, base_delay * (2 ** attempt))
                else:
                    delay = base_delay * (2 ** attempt)
                
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Rate limit exceeded (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        "Quota exceeded after all retries. "
                        "Please check your API quota at https://ai.dev/rate-limit"
                    )
                    raise
            
            except Exception as e:
                logger.error(f"Unexpected error calling Gemini: {e}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay:.1f}s...")
                    await asyncio.sleep(delay)
                else:
                    raise
        
        return None

    async def initialize(self) -> bool:
        """Initialize the agent with retry logic"""
        logger.info(f"Initializing {self.settings.agent_name}...")
        try:
            # Verify API connectivity with retry
            response_text = await self._call_gemini_with_retry(
                "Acknowledge your startup with a brief message."
            )
            
            if response_text:
                logger.info(f"Gemini API connected: {response_text}")
                return True
            else:
                logger.error("Failed to get response from Gemini API")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            return False

    async def think(self, task: str) -> str:
        """Use Gemini for reasoning about a task"""
        logger.info(f"Agent thinking about: {task}")

        self.conversation_history.append({"role": "user", "content": task})

        try:
            system_prompt = f"""You are {self.settings.agent_name}, a {self.settings.agent_role}.
You work autonomously to handle personal and business tasks.
Be concise, actionable, and proactive.
Available skills: {', '.join(self.skills_manager.list_available_skills())}"""

            # Format conversation for Gemini
            conversation_text = "\n".join(
                [f"{msg['role']}: {msg['content']}" for msg in self.conversation_history]
            )

            full_prompt = f"{system_prompt}\n\nConversation:\n{conversation_text}"
            
            # Use retry-enabled API call
            assistant_message = await self._call_gemini_with_retry(full_prompt)
            
            if not assistant_message:
                assistant_message = "Unable to process due to API limits. Please try again later."
            
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            return assistant_message
            
        except Exception as e:
            logger.error(f"Error during reasoning: {e}")
            error_message = f"Error: {e}"
            self.conversation_history.append(
                {"role": "assistant", "content": error_message}
            )
            return error_message

    async def ralph_wiggum_loop(self, task: str, max_retries: int | None = None) -> None:
        """Ralph Wiggum Stop Hook: Keep agent working until task is complete"""
        max_retries = max_retries or self.settings.ralph_wiggum_retries
        attempt = 0

        logger.info(f"Starting Ralph Wiggum loop for task: {task}")

        while attempt < max_retries:
            attempt += 1
            logger.info(f"Ralph Wiggum attempt {attempt}/{max_retries}")

            try:
                # Think about the task
                thought = await self.think(task)

                # Log the decision
                self.context_manager.log_decision(task, thought)

                # Check if task is complete
                if "complete" in thought.lower() or "done" in thought.lower():
                    logger.info(f"Task completed: {task}")
                    break

                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in Ralph Wiggum loop: {e}")
                # Continue to next attempt instead of crashing
                await asyncio.sleep(5)

        if attempt >= max_retries:
            logger.warning(f"Task did not complete within {max_retries} attempts: {task}")

    async def process_event(self, event: dict[str, Any]) -> None:
        """Process an incoming event from watchers"""
        event_type = event.get("type")
        event_data = event.get("data", {})

        logger.info(f"Processing event: {event_type}")

        task_description = f"Handle {event_type} event: {event_data}"
        await self.ralph_wiggum_loop(task_description, max_retries=3)

    async def run(self) -> None:
        """Main agent loop"""
        if not await self.initialize():
            logger.error("Agent initialization failed")
            return

        self.is_running = True
        logger.info(f"{self.settings.agent_name} started")

        # Start watchers
        watcher_tasks = [
            asyncio.create_task(self.gmail_watcher.watch()),
            asyncio.create_task(self.whatsapp_watcher.watch()),
            asyncio.create_task(self.fs_watcher.watch()),
        ]

        try:
            # Keep agent running
            while self.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Agent interrupted by user")
        finally:
            self.stop()
            for task in watcher_tasks:
                task.cancel()

    def stop(self) -> None:
        """Stop the agent"""
        self.is_running = False
        self.gmail_watcher.stop()
        self.whatsapp_watcher.stop()
        self.fs_watcher.stop()
        logger.info(f"{self.settings.agent_name} stopped")