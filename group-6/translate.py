import re
import urllib.parse
import requests

crontable = []
outputs = []

MASHAPE_KEY = "howswQ9Gy6msh8RzVT3JHnkYmPi6p1TNrLhjsn3h0VJthDYPDr"

MY_USER_ID = '<@U141M24MP>'

hashtag_re = re.compile(r'\#(\w+)')

def translate_yoda(sentence):
    url = "https://yoda.p.mashape.com/yoda"
    params = {'sentence': sentence}
    response = requests.get(url, params=params,
                            headers={"X-Mashape-Key": MASHAPE_KEY})
    response_content = str(response.text)
    return response_content


def process_message(data):
    if data['type'] != 'message' or MY_USER_ID  not in data['text']:
        return

    text = data['text']
    hashtags = hashtag_re.findall(text)

    for h in hashtags:
        text = text.replace('#' + h, '')

    text = text.replace(MY_USER_ID + ':', '')
    text = text.replace(MY_USER_ID, '')

    language = hashtags[0] if hashtags else None
    if language == 'yoda':
        translated = translate_yoda(text)
    else:
        translated = "Can't translate: {}".format(language)

    formatted_user = '<@{}>'.format(data['user'])
    formatted_response = '{}, you said: {}'.format(
        formatted_user, translated)

    outputs.append((data['channel'], formatted_response))
    text = text.replace(MY_USER_ID + ':', '')
    print("The text we're trying to translate is:", text)
    language = hashtags[0] if hashtags else None
    if language == 'yoda':
        translated = translate_yoda(text)
    else:
        translated = "Don't know how to translate: {}".format(language)

    formatted_user = '<@{}>'.format(data['user'])
    outputs.append([
        data['channel'],
        "{}, you said: {}".format(formatted_user, translated)])
