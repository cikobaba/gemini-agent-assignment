# gemini-agent-assignment
Software engineering assignment implementing a modular AI agent in Python with Gemini API, conversational memory, tool integration, and ReAct architecture.
# Adaptive Personal Assistant Agent using Gemini API

## Overview
This project implements a modular AI personal assistant in Python using the Google Gemini API.
The system follows SOLID principles and applies software design patterns such as Strategy, Factory/Registry, and Observer.

## Features
- CLI-based natural language interaction
- Session-based conversational memory
- Dynamic tool execution
- ReAct loop (Reason → Act → Observe)
- Robust error handling

## Implemented Components
- Agent
- MemoryManager
- ToolRegistry
- BaseTool interface

## Tools
- CalculatorTool
- TimeTool
- TranslationTool
- FileReaderTool

## Installation
```bash
pip install -r requirements.txt
