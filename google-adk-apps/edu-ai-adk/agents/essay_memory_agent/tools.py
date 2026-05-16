from google.adk.tools.tool_context import ToolContext

def save_essay_feedback(feedback: dict, tool_context: ToolContext) -> dict:
    all_essays = tool_context.state.get("essay_history", [])
    all_essays.append(feedback)
    tool_context.state["essay_history"] = all_essays
    return {"status": "success", "message": "Essay feedback saved."}

def get_all_essays(tool_context: ToolContext) -> dict:
    essays = tool_context.state.get("essay_history", [])
    return {"essays": essays, "count": len(essays)}
