from typing import Any, Dict

import requests

from tools.base_tool import BaseTool


class TranslationTool(BaseTool):
    @property
    def name(self) -> str:
        return "translation_tool"

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        text = kwargs.get("text", "")
        source_lang = kwargs.get("source_lang", "en")
        target_lang = kwargs.get("target_lang", "tr")

        if not text:
            raise ValueError("'text' argument is required.")

        try:
            response = requests.get(
                "https://api.mymemory.translated.net/get",
                params={"q": text, "langpair": f"{source_lang}|{target_lang}"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            translated = data.get("responseData", {}).get("translatedText")

            if not translated:
                raise ValueError("Translation API returned empty result.")

            return {
                "original": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "translated_text": translated,
            }
        except requests.RequestException as exc:
            raise RuntimeError(f"Translation service error: {exc}") from exc

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": "Translates text from one language to another.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to translate."
                    },
                    "source_lang": {
                        "type": "string",
                        "description": "Source language code like en, tr, de."
                    },
                    "target_lang": {
                        "type": "string",
                        "description": "Target language code like en, tr, de."
                    }
                },
                "required": ["text", "source_lang", "target_lang"]
            }
        }