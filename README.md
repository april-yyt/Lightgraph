# Lightgraph


LightGraph is a lightweight framework for serving LangGraph runnables via FastAPI. It provides an easy way to create endpoints for streaming intermediate steps and final responses from LangGraph agents.


## Installation

```bash
pip install lightgraph
```

## Usage

```python
from lightgraph import create_lightgraph
from your_langgraph_module import your_runnable

lightgraph = create_lightgraph(your_runnable, allowed_hosts=["localhost", "127.0.0.1"])
app = lightgraph.create_app()
