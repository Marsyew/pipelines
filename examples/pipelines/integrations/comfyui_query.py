from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
from schemas import OpenAIChatMessage
import requests
import os
import json

class Pipeline:
    class Valves(BaseModel):
        api_key: str

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "chat_pipeline"
        self.name = "Chat Pipeline"

        # Initialize rate limits
        self.valves = self.Valves(api_key=os.getenv("OPENAI_API_KEY", "123"))

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.valves.api_key}'
        }

        data = {
            'model': model_id,
            'messages': messages
        }

        try:
            response = requests.post('http://192.168.31.30:8816/v1/chat/completions', headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            result = response.json()
            return json.dumps(result, indent=4)  # Format the response as a pretty JSON string
        except requests.RequestException as e:
            return f"Error sending chat request: {str(e)}"
        except json.JSONDecodeError:
            return "Error decoding the response JSON"
