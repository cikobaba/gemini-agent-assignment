from dataclasses import dataclass
from typing import List


@dataclass
class MemoryTurn:
    role: str
    content: str


class MemoryManager:
    def __init__(self) -> None:
        self._history: List[MemoryTurn] = []

    def add_user_message(self, message: str) -> None:
        self._history.append(MemoryTurn(role="user", content=message))

    def add_assistant_message(self, message: str) -> None:
        self._history.append(MemoryTurn(role="assistant", content=message))

    def add_tool_message(self, tool_name: str, message: str) -> None:
        self._history.append(MemoryTurn(role="tool", content=f"{tool_name}: {message}"))

    def get_history_as_text(self) -> str:
        if not self._history:
            return "No previous conversation."

        return "\n".join(
            f"{turn.role.upper()}: {turn.content}"
            for turn in self._history
        )

    def clear(self) -> None:
        self._history.clear()