import requests
from pandasai.llm.base import LLM
from pandasai.prompts.base import BasePrompt
from pandasai.helpers.memory import Memory

class CustomMistralLLM(LLM):
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url
        self.api_token = api_token

    @property
    def type(self) -> str:
        return "custom_mistral"

    def call(self, instruction: BasePrompt, context: Memory = None) -> str:
        headers = {
            "accept": "application/json; charset=utf-8",
            "Process-Mode": "sync",
            "Authorization": f"Basic {self.api_token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = {
            "prompts": [{"role": "user", "content": instruction.to_string()}],
            "doSample": True,
            "maxTokens": 1200,
            "numBeams": 1,
            "repPenalty": 1.2,
            "temperature": 0,
            "topK": 50,
            "topP": 0.6
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        print(data['payload']['data']['text'])
        print("############")
        return data['payload']['data']['text']
