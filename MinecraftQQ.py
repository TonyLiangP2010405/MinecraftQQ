import base64
from io import BytesIO
from urllib.parse import quote
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import json
import os
from PIL import Image
import shutil
import random


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


def check_and_save_image(data):
    if_message = False
    message = data.get('message', None)
    if len(message) == 2:
        if message[0]['type'] == 'text':
            if message[0]['data']['text'][:4] == 'meme':
                if_message = True
        if message[1]['type'] == 'image' and if_message:
            image_path = message[1]['data']['path']
            destination_path = 'original.jpg'
            shutil.copyfile(image_path, destination_path)
            return image_path
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


def send_group_message_image(meme_original_path):
    image_path = None
    file_url = None
    absolute_path = None
    image_directory = 'C:/Users/Tony/PycharmProjects/MincrafMap/'
    image_name_without_extension = 'result'
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    for ext in image_extensions:
        image_path = image_directory + image_name_without_extension + ext
        if os.path.isfile(image_path):
            # File found, get the absolute path
            absolute_path = os.path.abspath(image_path)
            file_url = 'file://' + image_path
            print(file_url)
            print(absolute_path)
            break
    if os.path.isfile(image_path):
        url = 'http://127.0.0.1:3000/send_group_msg'
        data = {
            'group_id': '856708153',
            'message': [
                {
                    "type": "image",
                    "data": {
                        "file": file_url
                    }
                }
            ]
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Success:", response.text)

            os.remove(absolute_path)
        else:
            print("Error:", response.text)
    else:
        get_result_image(meme_original_path)
        send_group_message_image(meme_original_path)

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


def get_meme_key():
    url = 'http://127.0.0.1:2233/memes/keys/'
    response = requests.get(url)
    keys = response.json()
    print(keys)
    key_length = len(keys)
    key_number = random.randrange(key_length)
    return keys[key_number]


def get_result_image(image_path):
    key = get_meme_key()
    url = 'http://127.0.0.1:2233/memes/' + str(key) + "/"
    print(url)
    with open(image_path, 'rb') as image:
        files = {'images': (image_path, image, 'multipart/form-data')}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            # The filename you wish to save the image as
            filename = 'result'

            # Try to guess the extension of the file based on the Content-Type header
            content_type = response.headers.get('Content-Type')
            if content_type:
                extension = content_type.split('/')[-1]  # Get the part after '/'
                filename += '.' + extension

            # Open a local file in binary write mode
            with open(filename, 'wb') as file:
                # Write the response content to the file
                file.write(response.content)
            print(f"Image saved as {filename}")
        else:
            print(f"Failed to retrieve the image. Status code: {response.status_code}")


bot_state = 'close'
bot_state_timer = 0
tem_message = None
meme_tem_path = None
while True:
    json_data = check_qq_json2()
    if json_data is not None:
        meme_image_path = check_and_save_image(json_data)
        if meme_image_path is not None:
            if meme_tem_path is not None:
                image1 = Image.open(meme_image_path)
                image2 = Image.open(meme_tem_path)
                if image1.mode != image2.mode:
                    image2 = image2.convert(image1.mode)
                if image1.size != image2.size:
                    image2 = image2.resize(image1.size)
                if list(image1.getdata()) != list(image2.getdata()):
                    meme_tem_path = meme_image_path
                    get_result_image(meme_image_path)
                    send_group_message_image(meme_image_path)
            else:
                meme_tem_path = meme_image_path
                get_result_image(meme_image_path)
                send_group_message_image(meme_image_path)
        tem_state = open_close_group_bot(json_data, bot_state_timer)
        if bot_state == 'close' and tem_state == 'open':
            bot_state_timer = 0
        elif bot_state == 'open' and tem_state == 'close':
            bot_state_timer = 0
        else:
            bot_state_timer = 1
        if tem_state is not None:
            bot_state = tem_state
        message_list = get_Mincraft_message2()
        if message_list is not None and message_list[1] != tem_message and bot_state == 'open':
            tem_message = message_list[1]
            send_group_message(message_list[0], message_list[1])
