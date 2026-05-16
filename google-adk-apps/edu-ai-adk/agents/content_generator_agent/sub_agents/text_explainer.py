from google.adk.agents import Agent

text_explainer_agent = Agent(
    name="text_explainer_agent",
    model="gemini-2.5-flash",
    description="Generates a clear explanation and bullet points for a study topic",
    instruction="""
You will receive a study topic.

Your task is to return a JSON object in the following format:

{
  "explanation": "A concise and accessible explanation of the topic.",
  "key_points": [
    "Key point 1",
    "Key point 2",
    "Key point 3"
  ]
}

🔹 The explanation should be a single, well-structured paragraph that introduces and summarizes the topic. Use clear, objective, and academic language. Avoid direct speech, rhetorical questions, or informal expressions like "Hello class" or "Let's learn".

🔹 The key_points must be a list of 3 to 5 short and direct bullet points highlighting essential facts, definitions, consequences, or relevant historical events.

⚠️ Do NOT use markdown formatting. 

Respond with precision. Do not invent or dramatize information.
"""
)
