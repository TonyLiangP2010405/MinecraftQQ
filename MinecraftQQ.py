import json
import os

import nonebot
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import datetime
import nonebot
from flask import Flask, request, jsonify


def open_close_group_bot(data):
    if data is not None:
        data_group_id = data.get('group_id', None)
        data_messages = data.get('message', None)
        if data_group_id is not None and data_messages is not None:
            for message in data_messages:
                if message['type'] == 'text':
                    if data_group_id == '856708153':
                        if message['data']['text'] == 'open':
                            return 'open'
                        elif message['data']['text'] == 'close':
                            return 'close'
    return None


def check_qq_json():
    file_path = 'data.json'
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Read the JSON data from the file
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    else:
        return None


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
    url = 'http://127.0.0.1:3000/send_group_msg'
    data = {
        'group_id': '856708153',
        'message': [
            {
                "type": "text",
                "data": {
                    "text": player + "在我的世界说:" + message
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
tem_message = None
while True:
    json_data = check_qq_json()
    tem_state = open_close_group_bot(json_data)
    if tem_state is not None:
        bot_state = tem_state
    message_list = get_Mincraft_message2()
    if message_list is not None and message_list[1] != tem_message and bot_state == 'open':
        tem_message = message_list[1]
        send_group_message(message_list[0], message_list[1])
