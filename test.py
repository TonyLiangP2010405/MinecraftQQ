import requests


def test_message():
    text = "test"
    url = "http://localhost:3000/send_group_msg"
    data = {
        "group_id": "1136693630",
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


test_message()
