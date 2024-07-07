from User import User
import sqlite3


check_data = 1
while True:
    user = User('1136693630', 'data.json')
    user.get_user_data()
    if check_data != user.data:
        user.get_group_user_message()
        user.get_group_user_name()
        user.get_group_user_qq()
        data = user.data
        qq = user.qq
        username = user.username
        message = user.message
        print(message)
        group_qq = user.group_qq
        connection = sqlite3.connect('message.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO people (name, qq, group_qq) VALUES (?, ?, ?)", (username, qq, group_qq))
        people_id = cursor.lastrowid
        cursor.execute("INSERT INTO message(content, people_id) VALUES (?, ?)", (message, people_id))
        connection.commit()
        connection.close()
        check_data = user.data
