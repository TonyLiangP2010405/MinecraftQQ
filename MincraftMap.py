import json
import os

import requests
import asyncio
from pyppeteer import launch
from openai import OpenAI
import aiohttp
from requests.adapters import HTTPAdapter
from urllib3 import Retry


async def send_message_to_MinecraftMap(url, input_selector, message):
    browser = await launch(headless=True)
    # Create a new page
    page = await browser.newPage()

    # Navigate to the URL
    await page.goto(url, {'waitUntil': 'networkidle0'})
    await page.waitForSelector(input_selector)
    await page.evaluate(f"""document.querySelector('{input_selector}').value = `{message}`;""")
    await page.click(input_selector)
    await page.type(input_selector, message)
    await page.keyboard.press('Enter')
    # If necessary, wait for a specific element that is dynamically loaded
    # await page.waitForSelector('yourSelector')

    # Evaluate page and return the content
    content = await page.evaluate('() => document.documentElement.outerHTML')

    # Close the browser
    await browser.close()


async def send_message_to_MinecraftMap2(url, input_selector, message):
    browser = await launch(headless=True)
    # Create a new page
    page = await browser.newPage()

    # Navigate to the URL
    await page.goto(url, {'waitUntil': 'networkidle0'})
    await page.waitForSelector(input_selector)
    # Removed the line that was directly setting the input value
    await page.click(input_selector)
    await page.type(input_selector, message)
    await page.keyboard.press('Enter')
    # If necessary, wait for a specific element that is dynamically loaded
    # await page.waitForSelector('yourSelector')

    # Evaluate page and return the content
    content = await page.evaluate('() => document.documentElement.outerHTML')

    # Close the browser
    await browser.close()


# The URL you want to scrape

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


# Run the asynchronous function
def get_message_from_qq(data):
    if data is not None:
        data_group_id = data.get('group_id', None)
        data_messages = data.get('message', None)
        sender = data.get('sender', None)
        if data_group_id is not None and data_messages is not None and sender is not None:
            for message in data_messages:
                if message['type'] == 'text' and data_group_id == 856708153 and message['data']['text'][:2] == 'mc':
                    content = message['data']['text'][2:]
                    nickname = sender['nickname']
                    card = sender['card']
                    if nickname != '':
                        return nickname + "说:" + content
                    else:
                        return card + "说:" + content
    return None


def get_Mincraft_information():
    url = 'http://main.wycraft.cn:45502/up/world/world/'
    response = requests.get(url)
    if response.status_code == 200:
        result_json = response.json()
        print('------------------------------------')
        print(result_json, '')
        print('------------------------------------')


def get_Mincraft_Map_players():
    url = 'http://main.wycraft.cn:45502/up/world/world/'
    s = requests.Session()
    response = s.get(url)
    if response.status_code == 200:
        result_json = response.json()
        players = result_json['players']
        return players
    else:
        print('Request failed with status code', response.status_code)


def get_Mincraft_timestamp():
    url = 'http://main.wycraft.cn:45502/up/world/world/'
    response = requests.get(url)
    if response.status_code == 200:
        result_json = response.json()
        return result_json['timestamp']


def get_Mincraft_timestamp_information(timestamp):
    url = 'http://main.wycraft.cn:45502/up/world/world/' + str(timestamp)
    response = requests.get(url)
    print(response.json())


def get_Mincraft_config_information():
    url = 'http://main.wycraft.cn:45502/up/configuration'
    response = requests.get(url)
    if response.status_code == 200:
        result_json = response.json()
        print('------------------------------------')
        print(result_json)
        print('------------------------------------')


def get_Mincraft_message():
    url = 'http://main.wycraft.cn:45502/up/world/world/'
    response = requests.get(url)
    result_json = response.json()
    update_information = result_json['updates']
    if len(update_information) != 0:
        for information_list in update_information:
            if information_list['type'] == 'chat':
                message = information_list['message']
                return message
    else:
        return None


def ask_Ai_model(message):
    client = OpenAI(api_key="sk-3ffd76d3e7be48cd9e52678305fae779", base_url="https://api.deepseek.com/v1")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": message + "The answer max length is 150"},
        ]
    )

    return response.choices[0].message.content


async def send_message_in_parts(page, selector, message, part_size):
    # Break the message into parts based on part_size
    parts = [message[i:i + part_size] for i in range(0, len(message), part_size)]

    # Focus on the input field
    await page.focus(selector)

    # Type each part of the message
    for part in parts:
        await page.type(selector, part)
        await asyncio.sleep(0.1)  # Wait a bit between chunks to simulate human typing


async def get_Minecraft_Map_information2(url, input_selector, message):
    max_length = 256
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    await page.waitForSelector(input_selector)

    # Send the message in parts, respecting the max_length restriction
    await send_message_in_parts(page, input_selector, message, max_length)

    # Press 'Enter' to submit the message
    await page.keyboard.press('Enter')

    # Wait for any necessary elements to load after sending the message
    # Replace 'yourSelector' with the actual selector you need to wait for
    # await page.waitForSelector('yourSelector')

    content = await page.evaluate('() => document.documentElement.outerHTML')
    await browser.close()
    return content


def split_string_into_chunks(input_string, chunk_size=256):
    return [input_string[i:i + chunk_size] for i in range(0, len(input_string), chunk_size)]


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
                    message = information_list['message']
                    return message
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


# players = get_Mincraft_Map_players()
# timestamp = get_Mincraft_timestamp()
# print(timestamp)
# get_Mincraft_information()
# for player in players:
#     print(player)
# get_Mincraft_timestamp_information(timestamp)
# send_message_to_server()
tem_message = None
tem_message2 = None
url = 'http://main.wycraft.cn:45502/'
input_selector = '#chatinput'
while True:
    user_send_message = get_Mincraft_message2()
    print(user_send_message)
    if tem_message is not None:
        print('------------------------------')
        print(tem_message)
    if user_send_message is not None and user_send_message[:2] == 'ai' and user_send_message != tem_message:
        tem_message = user_send_message
        out_message = ask_Ai_model(user_send_message[2:])
        out_message = out_message.replace(" ", "").replace("\n", "")
        asyncio.get_event_loop().run_until_complete(send_message_to_MinecraftMap2(url, input_selector, out_message))
    json_data = check_qq_json2()
    if json_data is not None:
        check_message = get_message_from_qq(json_data)
        print(check_message)
        if check_message is not None and check_message != tem_message2:
            tem_message2 = check_message
            check_message = check_message
            print('success')
            asyncio.get_event_loop().run_until_complete(
                send_message_to_MinecraftMap2(url, input_selector, check_message))
