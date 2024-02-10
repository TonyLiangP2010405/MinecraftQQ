import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


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
        'group_id': '897177775',
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

tem_message = None
while True:
    message_list = get_Mincraft_message2()
    if message_list != None and message_list[1] != tem_message:
        tem_message = message_list[1]
        send_group_message(message_list[0], message_list[1])
