import math
from typing import Any, Dict

from tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        expression = kwargs.get("expression", "")
        if not expression:
            raise ValueError("'expression' argument is required.")

        allowed_names = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "sqrt": math.sqrt,
            "ceil": math.ceil,
            "floor": math.floor,
        }

        try:
            result = eval(expression, {"__builtins__": {}}, allowed_names)
        except Exception as exc:
            raise ValueError(f"Invalid mathematical expression: {exc}") from exc

        return {"expression": expression, "result": result}

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": "Evaluates a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate."
                    }
                },
                "required": ["expression"]
            }
        }