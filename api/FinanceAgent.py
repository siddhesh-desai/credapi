import os
import json
from dotenv import load_dotenv

# import google.generativeai as genai
from google import genai

# import api.constants as constants
import constants as constants
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch


class FinanceAgent:
    """Personalised Finance Agent"""

    def __init__(self):
        """Initialise karega"""

        load_dotenv()

        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        self.google_search_tool = Tool(google_search=GoogleSearch())

    def generate_llm_response(self, user_prompt):
        """LLM Response dega"""

        result = self.client.models.generate_content(
            model=constants.FINANCE_AGENT_MODEL,
            contents=user_prompt,
            config=GenerateContentConfig(
                system_instruction=constants.FINANCE_AGENT_SYSTEM_PROMPT,
                tools=[self.google_search_tool],
                response_modalities=["TEXT"],
            ),
        )

        ans = ""

        for each in response.candidates[0].content.parts:
            ans += each.text

        return ans


if __name__ == "__main__":
    finance_agent = FinanceAgent()
    response = finance_agent.generate_llm_response("What is the stock price of Apple?")
    print(response)
