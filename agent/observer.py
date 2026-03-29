import logging
from typing import Any, Dict, Protocol

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class AgentObserver(Protocol):
    def on_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        ...


class LoggingObserver:
    def on_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        logger.info("[%s] %s", event_type, payload)