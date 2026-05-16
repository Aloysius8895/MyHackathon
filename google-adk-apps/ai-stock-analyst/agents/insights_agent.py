from vertexai.preview.generative_models import GenerativeModel

class InsightsAgent:
    def __init__(self):
        self.model = GenerativeModel("gemini-2.0-flash-001")

    def generate_advice(self, news: str, trends: dict) -> str:
        try:
            prompt = (
                "You're a senior financial analyst. Consider the following news and technical data, "
                "and provide a buy/hold/sell recommendation with confidence and reasoning.\n"
                f"NEWS SUMMARY:\n{news}\n\nTECHNICAL ANALYSIS:\n{trends}"
            )
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Analysis unavailable: {str(e)}"
