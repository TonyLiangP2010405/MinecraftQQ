from openai import OpenAI


class AI:
    def __init__(self, message):
        self.message = message
        self.reply = None

    def send_ai_message(self):
        message = self.message
        client = OpenAI(api_key="sk-ed6792c6ad3448cdb8ae2373e57f8d2f", base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": message},
            ],
            stream=False
        )

        self.reply = response.choices[0].message.content
        print("AI说" + self.reply)

    def get_message(self):
        return self.reply
