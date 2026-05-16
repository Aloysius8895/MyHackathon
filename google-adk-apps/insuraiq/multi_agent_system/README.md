# InsuraIQ Multi Agent System

ADK based multi agent system containing Orchestrator agent, Information Collector Agent (via custom built adapter for A2A to ADK communication), Doctor Agent, Policy Agent.

## Prerequisites

- Python 3.13 or higher
- Install the needed packages from insuraiq/requirements.txt
- Access to a LLM and an API Key
- Running A2A and MCP server url

## Running the Sample

1.  Navigate to the directory containing the files:

    ```bash
    cd path/to/your/multi_agent_system
    ```

2.  Create an environment file with your API key or VertexAI details as specified in the ADK documentation inside insuraiq folder.

** Note: ** Update the A2A and MCP server url in agent.py

3.  Run the adk web ui:
    ```bash
    adk web
    ```

## Deploy

Use the following command to deploy to agent engine

```bash
adk deploy agent_engine insuraiq --staging_bucket YOUR_STAGING_GCS_BUCKET_URI
```
