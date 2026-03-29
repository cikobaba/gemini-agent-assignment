from datetime import datetime
from typing import Any, Dict

from tools.base_tool import BaseTool


class TimeTool(BaseTool):
    @property
    def name(self) -> str:
        return "time_tool"

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        now = datetime.now()
        return {
            "local_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "weekday": now.strftime("%A")
        }

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": "Returns the current local date and time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }