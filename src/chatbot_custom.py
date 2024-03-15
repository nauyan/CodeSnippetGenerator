import requests
import json


class CustomLLM:

    def __init__(self):
        self.url = "http://localhost:11434/api/chat"

    def generate_response(self, user_message: str, prev_messages=None) -> str:
        system_prompt = """
You are an AI programming assistant. Follow the user's requirements carefully and to the letter. First, think step-by-step and describe your plan for what to build in pseudocode, written out in great detail. Then, output the code in a single code block. Minimize any other prose.

If the user asks any question that is not related to python or related to code generation then just reply with "I am sorry I am just a coding assistant that can response to coding realted queries"
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_message
            },
        ]

        if prev_messages:
            messages = prev_messages + messages

        data = {"model": "llama2", "messages": messages, "stream": False}

        response = requests.post(self.url,
                                 json=data).json()["message"]["content"]
        return response

    def test_snippet(self, code):
        try:
            exec(code)
            return True
        except Exception as e:
            print(e)
            return False
