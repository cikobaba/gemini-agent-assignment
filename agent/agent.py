import json
from dataclasses import dataclass, field
from typing import Any, Dict, List

from agent.gemini_client import GeminiClient
from agent.memory import MemoryManager
from agent.observer import AgentObserver
from agent.registry import ToolRegistry

MAX_AGENT_STEPS = 5


@dataclass
class Agent:
    llm_client: GeminiClient
    memory: MemoryManager
    tool_registry: ToolRegistry
    observers: List[AgentObserver] = field(default_factory=list)

    def notify(self, event_type: str, payload: Dict[str, Any]) -> None:
        for observer in self.observers:
            observer.on_event(event_type, payload)

    def _build_system_prompt(self, user_input: str) -> str:
        tool_schemas = json.dumps(self.tool_registry.get_tool_declarations(), indent=2)
        conversation_history = self.memory.get_history_as_text()

        return f"""
You are a modular CLI personal assistant built with a ReAct architecture.

Your responsibilities:
1. Answer directly if no tool is needed.
2. If a tool is needed, return ONLY valid JSON in this format:
{{
  "action": "tool",
  "tool_name": "name_of_tool",
  "arguments": {{...}}
}}
3. If you want to answer the user directly, return ONLY valid JSON in this format:
{{
  "action": "final",
  "response": "your natural language response"
}}
4. Never output explanations outside JSON.
5. Use conversation history when useful.

Available tools:
{tool_schemas}

Conversation history:
{conversation_history}

Current user input:
{user_input}
""".strip()

    def _build_followup_prompt(self, original_user_input: str, tool_name: str, tool_output: Dict[str, Any]) -> str:
        conversation_history = self.memory.get_history_as_text()
        return f"""
You are continuing the ReAct loop.

Original user input:
{original_user_input}

The tool '{tool_name}' returned this JSON result:
{json.dumps(tool_output, indent=2)}

Conversation history:
{conversation_history}

Now decide the next step.
Return ONLY valid JSON.
If the tool result is enough, return:
{{
  "action": "final",
  "response": "your answer"
}}
If another tool is needed, return:
{{
  "action": "tool",
  "tool_name": "name_of_tool",
  "arguments": {{...}}
}}
""".strip()

    @staticmethod
    def _safe_parse_json(text: str) -> Dict[str, Any]:
        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.replace("json", "", 1).strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(f"LLM did not return valid JSON. Raw output: {text}") from exc

    def process(self, user_input: str) -> str:
        self.memory.add_user_message(user_input)
        self.notify("user_message", {"message": user_input})

        prompt = self._build_system_prompt(user_input)

        for step in range(1, MAX_AGENT_STEPS + 1):
            self.notify("agent_step", {"step": step})

            try:
                llm_response = self.llm_client.generate(prompt)
                raw_text = getattr(llm_response, "text", None)
                if not raw_text:
                    raise ValueError("Gemini returned an empty response.")

                decision = self._safe_parse_json(raw_text)
            except Exception as exc:
                fallback = f"I encountered an LLM error: {exc}"
                self.memory.add_assistant_message(fallback)
                self.notify("llm_error", {"error": str(exc)})
                return fallback

            action = decision.get("action")

            if action == "final":
                response = decision.get("response", "I could not generate a response.")
                self.memory.add_assistant_message(response)
                self.notify("assistant_response", {"response": response})
                return response

            if action == "tool":
                tool_name = decision.get("tool_name")
                arguments = decision.get("arguments", {})

                try:
                    if not tool_name:
                        raise ValueError("Tool name is missing in LLM response.")
                    if not isinstance(arguments, dict):
                        raise ValueError("Tool arguments must be a JSON object.")

                    self.notify("tool_call", {"tool_name": tool_name, "arguments": arguments})
                    tool_output = self.tool_registry.execute_tool(tool_name, arguments)
                    self.memory.add_tool_message(tool_name, json.dumps(tool_output))
                    self.notify("tool_result", {"tool_name": tool_name, "result": tool_output})

                    prompt = self._build_followup_prompt(user_input, tool_name, tool_output)
                    continue

                except Exception as exc:
                    error_result = {
                        "error": str(exc),
                        "tool_name": tool_name,
                        "arguments": arguments,
                    }
                    self.memory.add_tool_message(tool_name or "unknown", json.dumps(error_result))
                    self.notify("tool_error", error_result)

                    prompt = self._build_followup_prompt(user_input, tool_name or "unknown", error_result)
                    continue

            unknown_action_message = "The model returned an unknown action."
            self.memory.add_assistant_message(unknown_action_message)
            self.notify("protocol_error", {"decision": decision})
            return unknown_action_message

        fallback = "I could not complete the request within the maximum number of reasoning steps."
        self.memory.add_assistant_message(fallback)
        self.notify("max_steps_reached", {"max_steps": MAX_AGENT_STEPS})
        return fallback