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

        response = requests.post('http://192.168.31.29:8817/v1/chat/completions', headers=headers, data=json.dumps(data))

        return response.json()

class Pipeline:
    def __init__(self):
        self.name = "comfyui_query"
        self.chat_pipeline = ChatPipeline()

    async def on_startup(self):
        await self.chat_pipeline.on_startup()

    async def on_shutdown(self):
        await self.chat_pipeline.on_shutdown()

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        return self.chat_pipeline.pipe(user_message, model_id, messages, body)

if __name__ == "__main__":
    import asyncio
    pipeline = Pipeline()
    asyncio.run(pipeline.on_startup())
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '查一下在深圳拍摄的照片'}
    ]
    result = pipeline.pipe("查一下在深圳拍摄的照片", 'test_model', messages, {})
    print(result)
    asyncio.run(pipeline.on_shutdown())
