# Policy Finder MCP Server

This MCP server exposes a tool to find top 2 policies based on search query. It uses ChromaDB as vector database and finds the top 2 policies. 

This MCP server uses streamable-http transport.

## Prerequisites

*   Python 3.13 or higher
*   [UV](https://github.com/astral-sh/uv)
*   Access to a Embedding Model and an API Key

## Running the Sample

1.  Navigate to the directory containing the files:
    ```bash
    cd path/to/your/mcp
    ```

2.  Create an environment file with your API key or VertexAI details as specified in the ADK documentation.

3.  Run the mcp server:
    ```bash
    uv run main.py
    ```

## Deploy

Build the image using the given Dockerfile with .env file and deploy.