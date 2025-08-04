# Deepsearch

Deepsearch is an automated research manager that performs deep research on any provided topic. It plans web searches, executes them asynchronously, and generates a comprehensive markdown report using AI agents.

## Features

- **Automated Planning:** Uses an AI agent to plan relevant web searches for a given query.
- **Asynchronous Search:** Executes multiple searches in parallel for efficiency.
- **Summarization:** Summarizes search results using AI.
- **Report Generation:** Compiles findings into a markdown report.
- **Traceability:** Provides trace links for debugging and transparency.

## Project Structure

```
Deepsearch/
├── research_manager.py
├── agents.py
├── planner.py
├── writer.py
├── search.py
├── .env
```

## Getting Started

### Prerequisites

- Python 3.10+
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```

### Environment Variables

Create a `.env` file with your API keys and configuration.

### Usage

Import and run the `ResearchManager`:

```python
from research_manager import ResearchManager
import asyncio

async def main():
    manager = ResearchManager()
    async for update in manager.run("Your research topic here"):
        print(update)

asyncio.run(main())
```

## How it Works

1. **Planning:** The system uses an AI agent to break down your query into actionable web searches.
2. **Searching:** Each search is performed and summarized.
3. **Reporting:** All summaries are compiled into a readable markdown report.

## Customization

- Extend `planner_agent`, `writer_agent`, or `search_and_summarize` in their respective files to customize planning, writing, or search logic.


---

*For questions or contributions, please open an issue or pull request.*
