import json
import os

import requests
import sqlite3


class User:
    def __init__(self, group_qq, file_path):
        self.message = None
        self.qq = None
        self.data = None
        self.username = None
        self.group_qq = group_qq
        self.file_path = file_path

    def get_user_data(self):
        file_path = self.file_path
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            print(f'File {file_path} is empty or does not exist.')
            return None  # or return {}, depending on how you want to handle this case

        # If the file exists and is not empty, attempt to parse it as JSON
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.data = data
        except json.JSONDecodeError as e:
            print(f'JSON decode error in file {file_path}: {e}')
            return None  # or handle the error as needed
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            return None  # or handle the error as needed

    def get_group_user_name(self):
        data = self.data
        message_type = data['message_type']
        if message_type == "group":
            username = data['sender']['nickname']
            self.username = username
        else:
            self.username = None

    def get_group_user_qq(self):
        data = self.data
        message_type = data['message_type']
        if message_type == 'group':
            qq = data['sender']['user_id']
            self.qq = qq

    def get_group_user_message(self):
        data = self.data
        if data['message'][0]["type"] == "text":
            text = data['message'][0]['data']['text']
            self.message = text

    # def record_group_message(self):
    #     filename = 'message.db'
    #     conn = None
    #     try:
    #         conn = sqlite3.connect(filename)
    #         cur = conn.cursor()
    #         cur.execute('''INSERT INTO people (name, qq, group_qq) VALUES ('')''')
    #         print("Connected to database")
    #     except sqlite3.Error as e:
    #         print(e)
    #     finally:
    #         if conn:
    #             conn.close()
