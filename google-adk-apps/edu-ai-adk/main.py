import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from uuid import uuid4
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from agents.orchestrator_agent.agent import root_agent
from google.genai import types

load_dotenv()

# === CONFIG ===
APP_NAME = "orchestrator_agent"
AGENT_DIR = os.path.join(os.path.dirname(__file__), "agents/")
SESSION_DB_URL = "sqlite:///./sessions.db"

# === SERVICES ===
session_service = DatabaseSessionService(db_url=SESSION_DB_URL)
runner = Runner(agent=root_agent, 
                app_name=APP_NAME, 
                session_service=session_service)

# === FASTAPI ===
app = FastAPI()

# === SETUP CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ROUTES ===
@app.post("/run")
async def run_agent(payload: dict):
    user_id = payload["user_id"]
    session_id = payload["session_id"]
    message = payload["new_message"]
    print("Payload: ", payload)

    content = types.Content(
        role=message["role"],
        parts=[types.Part(**part) for part in message["parts"]]
    )

    response = None
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response = event.content.parts[0].text

    print(f"Response: {response}")
    return {
        "response": response
    }

@app.post("/initiate-session/{user_id}")
async def create_session(user_id: str):
    print(f"Creating session for user {user_id}")
    session_id = str(uuid4())
    stateful_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state={"user_name": user_id}
    )
    print(f"Session created: {stateful_session}")
    return {
        "id": stateful_session.id,
        "user_id": stateful_session.user_id,
        "state": stateful_session.state,
    }
    
@app.get("/apps/{app_name}/users/{user_id}/sessions/{session_id}/state")
async def get_user_state(app_name: str, user_id: str, session_id: str):
    try:
        state = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
        return state
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User state not found: {str(e)}")
    

@app.get("/hello", include_in_schema=True)
async def root():
  return {"Hello": "World"}

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080, 
        reload=False
    )