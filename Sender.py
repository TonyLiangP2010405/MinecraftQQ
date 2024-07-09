import requests


class Sender:
    def __init__(self, group_qq, content):
        self.group_qq = group_qq
        self.content = content

    def send_message(self):
        text = self.content
        url = "http://localhost:3000/send_group_msg"
        data = {
            "group_id": self.group_qq,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": text
                    }
                }
            ]
        }
        response = requests.post(url, json=data)
        print(response)
