import requests


image_path = 'test.jpg'
url = 'http://127.0.0.1:2233/memes/anti_kidnap/'
with open(image_path, 'rb') as image:
    files = {'images': (image_path, image, 'multipart/form-data')}
    response = requests.post(url, files=files)


if response.status_code == 200:
    print('Success!')
    # Process response here
    print(response.text)
else:
    print('Failed with status code:', response.status_code)
    # Handle request failure here
    print(response.text)


