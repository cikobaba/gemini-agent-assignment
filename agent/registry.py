from typing import Any, Dict, List

from tools.base_tool import BaseTool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise KeyError(f"Unknown tool requested: {name}")
        return self._tools[name]

    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        tool = self.get_tool(name)
        return tool.execute(**arguments)

    def get_tool_declarations(self) -> List[Dict[str, Any]]:
        return [tool.get_declaration() for tool in self._tools.values()]