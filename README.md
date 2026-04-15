# ERPNext Agent

An intelligent agent system that bridges natural language interfaces with ERPNext/Frappe operations through LLM-powered tool orchestration and memory management.

## Overview

The project demonstrates a modular approach to building conversational agents that can execute complex ERP operations. The agent parses user requests, selects appropriate tools, executes operations against ERPNext, and maintains conversation context across sessions.

## Tech Stack

### Core Frameworks
- **LangChain** - LLM integration, tool binding, and agentic workflows
- **Frappe Client** - Direct ERPNext API communication
- **Ollama** - Local LLM deployment and inference
- **Google Generative AI** - Alternative LLM backend (Gemini)
- **Langfuse** - Agentic monitoring and observability

### Language & Environment
- Python 3.12+
- Virtual environment with pip dependency management

## Architecture

### Modular Structure

```
agents/
├── erp_agent/           # Main agent orchestration
│   ├── erp_agent.py     # Agent entry point and loop
│   ├── runner.py        # Agent execution logic
│   ├── prompt.py        # Prompt engineering and formatting
│   └── memory.py        # Conversation history and context management
└── summary_agent/       # Conversation summarization
    └── summary_agent.py # Long-context compression

erp/
├── frappe_client.py     # ERPNext API wrapper
└── customer_service.py  # Domain-specific operations

tools/
├── register_tools.py    # Tool registration with LLM binding
└── erp_tools/
    ├── customer_tools.py    # Customer CRUD operations
    └── attendance_tool.py   # Attendance data retrieval

llms/
├── ollama_client.py     # Ollama integration
└── gemini_client.py     # Google Generative AI integration

schemas/
├── customer_schema.py   # Input validation schemas
└── attendance_schema.py # Data structure definitions
```

## Key Features

### 1. Tool-Augmented LLM
- Structured tool definitions with input validation
- Dynamic tool selection based on request semantics
- Fallback mechanisms for tool failures

### 2. Memory Management
- Persistent chat history storage (JSON format)
- Conversation summarization for extended sessions
- Context retrieval for informed decision-making
- Automatic history trimming to maintain token efficiency

### 3. Multi-Backend LLM Support
- Local LLM execution via Ollama (Qwen 3.5:4b model)
- Cloud-based LLM via Google Generative AI
- Configurable through environment variables
- Model parameters: 16k context window, temperature 0

### 4. Observability Integration
- Langfuse callback handlers for request tracing
- Structured logging of agent execution flows
- Performance metrics collection

## Core Implementation Details

### Agent Workflow
1. User inputs natural language request
2. Agent retrieves recent conversation context
3. LLM processes request with available tools
4. Tool execution against ERPNext database
5. Result processing and response generation
6. Memory update and history persistence

### Tool Execution Pattern
```
Request → Tool Selection → Schema Validation → Execution → Result Processing
```

### Error Handling
- JSON deserialization with graceful fallback
- Missing module detection and early exit
- Tool invocation error wrapping
- Connection timeout resilience

## Running the Agent

```bash
# Activate environment
source .venv/bin/activate

# Execute agent
python -m agents.erp_agent.erp_agent
```

### Requirements
- ERPNext instance running at `http://127.0.0.1:8000`
- Valid authentication credentials configured
- Ollama service running on configured host/port
- Environment variables set (.env file)

## Learning Outcomes

- **LLM Integration**: Practical experience with LangChain tool binding and agentic workflows
- **Software Architecture**: Modular design patterns with separation of concerns
- **Error Resilience**: Defensive programming with graceful degradation
- **Memory Systems**: Persistent storage with context compression strategies
- **API Integration**: Frappe REST client implementation and error handling
- **Observability**: Integration with monitoring systems for production diagnostics
- **Configuration Management**: Environment-driven multi-backend support

## Configuration

### Environment Variables (.env)
```
OLLAMA_URL=http://localhost:11434
GEMINI_API_KEY=your_api_key
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_BASE_URL=http://localhost:3000
```

### Storage Locations
- Chat history: `storage/chat_history.json`
- Conversation summary: `storage/summary.txt`

## Dependencies

Key packages and their purposes:
- `langchain>=1.2.15` - Agentic framework and orchestration
- `langchain-community>=0.4.1` - Extended integrations
- `langchain-google-genai>=4.2.1` - Gemini API support
- `langchain-ollama>=1.1.0` - Local LLM support
- `langfuse>=4.2.0` - Observability and monitoring
- `frappeclient` - ERPNext API communication

## Current Capabilities

- Customer creation with validation
- Attendance record retrieval
- Multi-turn conversation with context awareness
- Automatic conversation summarization
- Structured error reporting

## Future Enhancement Opportunities

- Additional ERP operations (invoice, stock, payroll)
- Fine-tuned local models for domain-specific reasoning
- Real-time conversation metrics in Langfuse
- Batch operation support
- Caching layer for frequently accessed records
