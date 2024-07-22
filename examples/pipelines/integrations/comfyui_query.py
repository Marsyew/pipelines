from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests
import os
import json

class ChatPipeline:
    class Valves(BaseModel):
        api_key: str

    def __init__(self):
        self.name = "Chat Pipeline"
        self.valves = self.Valves(api_key=os.getenv("API_KEY", "123"))

    async def on_startup(self):
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        print(f"pipe:{__name__}")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.valves.api_key}'
        }

        data = {
            'model': model_id,
            'messages': messages
        }

        response = requests.post('http://localhost:8817/v1/chat/completions', headers=headers, data=json.dumps(data))

        return response.json()
