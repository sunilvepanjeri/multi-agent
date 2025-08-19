from openai import OpenAI
from app import tool
from app.config import settings


class Agent:

    def __init__(self, data):
        self.instruction = [{"role": "system", "content": data['instruction']}]
        self.tools = data['tools']
        self.client = OpenAI()

    async def run(self, query: str, chat_history: list[dict] = []):


        if not chat_history:
            chat_history = [{
                "role": "user",
                "content": query
            }]

        response = self.client.responses.create(
            model = settings.MODEL,
            input = self.instruction + chat_history,
            tools = self.tools
        )

        for item in response.output:
            if item.type == "function_call":
                chat_history += response.output
                name = item.name
                function_call = getattr(tool, name)
                tool_results = await function_call(query)

                chat_history.append({
                               "type": "function_call_output",
                               "call_id": item.call_id,
                               "output": str(tool_results)
                               })

                return await self.run(query, chat_history)
        return response.output_text





