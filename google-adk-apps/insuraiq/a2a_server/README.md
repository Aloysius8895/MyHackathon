# ADK Agent in A2A server

This uses the Agent Development Kit (ADK) to create an "Insurance Information Collector" that is hosted as an A2A server.

This agent guides a user through a health insurance questionnaire. It first presents a form to the user. After the user submits their information, the agent analyzes the data and generates a risk assessment report that is free of any PII data.

## Prerequisites

*   Python 3.13 or higher
*   [UV](https://github.com/astral-sh/uv)
*   Access to a LLM and an API Key

## Running the Sample

1.  Navigate to the directory containing the files:
    ```bash
    cd path/to/your/a2a_agent_system
    ```

2.  Create an environment file with your API key or VertexAI details as specified in the ADK documentation.

3.  Create the required `my_dict.json` file in the same directory. This file defines the form the agent will send to the user. Here is an example:
    ```json
    {
      "type": "object",
      "properties": {
        "full_name": { "type": "string", "description": "Full Name" },
        "age": { "type": "number", "description": "Age" },
        "smoker": { "type": "boolean", "description": "Are you a current or former smoker?" },
        "preexisting_conditions": { "type": "string", "description": "Please list any pre-existing medical conditions." }
      },
      "required": ["full_name", "age", "smoker"]
    }
    ```

** Note: ** Please update the A2A server url in main.py

4.  Run the agent server:
    ```bash
    uv run main.py
    ```

## Deploy

Build the image using the given Dockerfile with .env file and deploy.