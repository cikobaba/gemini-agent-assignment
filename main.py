from agent.agent import Agent
from agent.gemini_client import GeminiClient
from agent.memory import MemoryManager
from agent.observer import LoggingObserver
from agent.registry import ToolRegistry
from tools.calculator_tool import CalculatorTool
from tools.file_reader_tool import FileReaderTool
from tools.time_tool import TimeTool
from tools.translation_tool import TranslationTool


def build_agent() -> Agent:
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(TimeTool())
    registry.register(TranslationTool())
    registry.register(FileReaderTool())

    memory = MemoryManager()
    llm_client = GeminiClient()
    observers = [LoggingObserver()]

    return Agent(
        llm_client=llm_client,
        memory=memory,
        tool_registry=registry,
        observers=observers,
    )


def main() -> None:
    print("Personal Assistant Agent (Gemini CLI)")
    print("Type 'exit' to quit, 'clear' to reset memory.\n")

    try:
        agent = build_agent()
    except Exception as exc:
        print(f"Startup error: {exc}")
        return

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            agent.memory.clear()
            print("Memory cleared.\n")
            continue

        response = agent.process(user_input)
        print(f"Assistant: {response}\n")


if __name__ == "__main__":
    main()