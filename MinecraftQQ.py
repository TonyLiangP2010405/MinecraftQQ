import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def open_close_group_bot(data, timer):
    if data is not None:
        data_group_id = data.get('group_id', None)
        data_messages = data.get('message', None)
        if data_group_id is not None and data_messages is not None:
            for message in data_messages:
                if message['type'] == 'text':
                    if data_group_id == '856708153':
                        if message['data']['text'] == 'open':
                            if timer == 0:
                                send_group_message('bot', '当前bot的状态为open')
                            return 'open'
                        elif message['data']['text'] == 'close':
                            if timer == 0:
                                send_group_message('bot', '当前bot的状态为close')
                            return 'close'
    return None


def check_qq_json():
    with open('data.json', 'r') as f:
        if f.read().strip():
            # Move the file pointer back to the start of the file
            f.seek(0)
            data = json.load(f)
            return data
        else:
            print('File is empty.')
            return None  # or return {}, depending on how you want to handle an empty file.


import json
import os


def check_qq_json2(file_path='data.json'):
    # Check if the file exists and is not empty
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f'File {file_path} is empty or does not exist.')
        return None  # or return {}, depending on how you want to handle this case

    # If the file exists and is not empty, attempt to parse it as JSON
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        print(f'JSON decode error in file {file_path}: {e}')
        return None  # or handle the error as needed
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return None  # or handle the error as needed


def get_Mincraft_message2():
    url = 'http://main.wycraft.cn:45502/up/world/world/'
    max_retries = 3
    backoff_factor = 0.5

    # Create a session object
    session = requests.Session()

    # Set up retry logic with backoff factor
    retries = Retry(total=max_retries,
                    backoff_factor=backoff_factor,
                    status_forcelist=[500, 502, 503, 504])

    # Mount it for HTTP requests
    session.mount('http://', HTTPAdapter(max_retries=retries))

    # Attempt to make the request and process the response
    try:
        response = session.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        result_json = response.json()
        update_information = result_json.get('updates', [])  # default to empty list if 'updates' is not in response
        if update_information:
            for information_list in update_information:
                if information_list['type'] == 'chat':
                    playerName = information_list['playerName']
                    message = information_list['message']
                    message_list = [playerName, message]
                    return message_list
        return None
    except requests.exceptions.HTTPError as errh:
        print(f'HTTP Error: {errh}')
    except requests.exceptions.ConnectionError as errc:
        print(f'Error Connecting: {errc}')
    except requests.exceptions.Timeout as errt:
        print(f'Timeout Error: {errt}')
    except requests.exceptions.RequestException as err:
        print(f'Oops: Something Else: {err}')
    except ValueError as e:
        print(f"JSON decoding failed: {e}")

    return None  # Return None if no message is found or in case of an error


def send_group_message(player, message):
    print(message)
    url = 'http://127.0.0.1:3000/send_group_msg'
    data = {
        'group_id': '856708153',
        'message': [
            {
                "type": "text",
                "data": {
                    "text": "[world]" + "[" + player + "]" + ":" + message
                }
            }
        ]
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Success:", response.text)
    else:
        print("Error:", response.text)


def get_Mincraft_message():
    url = 'http://main.wycraft.cn:45502/up/world/world/'
    response = requests.get(url)
    result_json = response.json()
    update_information = result_json['updates']
    print(update_information)
    if len(update_information) != 0:
        for information_list in update_information:
            if information_list['type'] == 'chat':
                playerName = information_list['playerName']
                message = information_list['message']
                message_list = []
                message_list.append(playerName)
                message_list.append(message)
                return message_list
    else:
        return None


bot_state = 'close'
bot_state_timer = 0
tem_message = None
while True:
    json_data = check_qq_json2()
    if json_data is not None:
        tem_state = open_close_group_bot(json_data, bot_state_timer)
        if bot_state == 'close' and tem_state == 'open':
            bot_state_timer = 0
        if bot_state == 'open' and tem_state == 'close':
            bot_state_timer = 0
        else:
            bot_state_timer = 1
        if tem_state is not None:
            bot_state = tem_state
        message_list = get_Mincraft_message2()
        if message_list is not None and message_list[1] != tem_message and bot_state == 'open':
            tem_message = message_list[1]
            send_group_message(message_list[0], message_list[1])
