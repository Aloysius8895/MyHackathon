from google.adk.tools.tool_context import ToolContext
from datetime import datetime

def consolidate_progress(tool_context: ToolContext) -> dict:
    essays = tool_context.state.get("essay_history", [])
    exams = tool_context.state.get("practice_exams", [])  # se você quiser incluir simulados no futuro

    total_scores = [e["total_score"] for e in essays if "total_score" in e]
    avg_writing = round(sum(total_scores) / len(total_scores), 1) if total_scores else 0

    practice_areas = {}
    for exam in exams:
        area = exam["area"]
        score = exam["score"]
        if area in practice_areas:
            practice_areas[area].append(score)
        else:
            practice_areas[area] = [score]

    avg_by_area = {area: round(sum(scores)/len(scores), 1) for area, scores in practice_areas.items()}
    if essays:
        avg_by_area["Writing"] = avg_writing

    recommendations = []
    if avg_writing < 600:
        recommendations.append("📌 Improve writing by reviewing essay feedback.")
    if "Human Sciences" in avg_by_area and avg_by_area["Human Sciences"] < 600:
        recommendations.append("📚 Practice Human Sciences with thematic quizzes.")

    return {
        "essays": essays,
        "practice_exams": exams,
        "average_by_area": avg_by_area,
        "recommendations": recommendations
    }
