import random
from AI import AI
from User import User
import sqlite3
from Sender import Sender

check_data = 1
while True:
    user = User('897177775', 'data.json')
    user.get_user_data()
    if user.data is not None:
        if check_data != user.data:
            user.get_group_user_message()
            user.get_group_user_name()
            user.get_group_user_qq()
            data = user.data
            qq = user.qq
            username = user.username
            message = user.message
            if message is not None and qq is not None and username is not None:
                if user.group_qq is not None and user.group_qq == '897177775' and message[:2] == 'ai':
                    message = message[2:]
                    ai = AI(message)
                    ai.send_ai_message()
                    sender_group_qq = '897177775'
                    sender = Sender(sender_group_qq, ai.get_message())
                    sender.send_message()
                print(message)
                if message[:2] != 'ai' and user.group_qq == '897177775':
                    group_qq = user.group_qq
                    connection = sqlite3.connect('message.db')
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO people (name, qq, group_qq) VALUES (?, ?, ?)", (username, qq, group_qq))
                    people_id = cursor.lastrowid
                    cursor.execute("INSERT INTO message(content, people_id) VALUES (?, ?)", (message, people_id))
                    connection.commit()
                    message = user.message
                    random_percent = random.uniform(0, 1)
                    print(random_percent)
                    if random_percent >= 0.99:
                        results = cursor.execute("SELECT * FROM people WHERE group_qq = ?", (group_qq,)).fetchall()
                        ids = []
                        for result in results:
                            ids.append(result[3])
                        people_id = random.choice(ids)
                        message = cursor.execute("SELECT * FROM message WHERE people_id = ?", (people_id,)).fetchall()
                        message_content = message[0][0]
                        sender_group_qq = '897177775'
                        sender = Sender(sender_group_qq, message_content)
                        sender.send_message()
                    connection.close()
                check_data = user.data
                user = None
                sender = None
