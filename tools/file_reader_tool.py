import os
from typing import Any, Dict

from tools.base_tool import BaseTool


class FileReaderTool(BaseTool):
    @property
    def name(self) -> str:
        return "file_reader"

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        file_path = kwargs.get("file_path", "")
        if not file_path:
            raise ValueError("'file_path' argument is required.")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a file: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except UnicodeDecodeError as exc:
            raise ValueError("The file is not a UTF-8 text file.") from exc

        return {
            "file_path": file_path,
            "content_preview": content[:2000],
            "character_count": len(content)
        }

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": "Reads a local UTF-8 text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the local file."
                    }
                },
                "required": ["file_path"]
            }
        }