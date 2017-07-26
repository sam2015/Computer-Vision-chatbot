from __future__ import print_function
import json
import requests


MESSENGER_PROFILE_URL = ("https://graph.facebook.com/v2.6/me/"
                         "messenger_profile?access_token={access_token}")


THREAD_SETTINGS_URL = ("https://graph.facebook.com/v2.6/me/"
                       "thread_settings?access_token={access_token}")


MESSAGES_URL = ("https://graph.facebook.com/v2.6/me/"
                "messages?access_token={access_token}")



MESSENGER_PROFILE_URL = ("https://graph.facebook.com/v2.6/me/"
                         "messenger_profile?access_token={access_token}")



PAGE_ACCESS_TOKEN = "EAAGqvw8s9JcBAMBpbJpVI69aalr2VJTwH2cQ2HyEZAVHFuFP4ztUcVZBLYApUrvK82cua2zSUAIwQZCPoqiD9wSsLrkPZAdMISDPqGRd27TS2hJ1kydR5TDup9FsqXKq7KEesFj1V9PNcH7CYubXzxkLw8QPR5hiV4gjeQX8TSD0nChbnyCe"


HEADER = {"Content-Type": "application/json"}




def post_template_w_quickreplies(fbid):
    quick_replies = [{
                    "content_type": "text",
                    "title": "Hi",
                    "payload": "Hi"
                    }]

    payload = payload = {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Welcome to CV bot",
                        "image_url": "http://www.avaamo.com/wp-content/uploads/2016/12/chatbot-ecommerce.png",
                        "subtitle": "We've got the power of image captioning and ocr",
                    }
                ]
            }
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    request_payload = {}
    request_payload["recipient"] = {"id": fbid}
    attachment = {}
    attachment['type'] = 'template'
    attachment['payload'] = payload
    request_payload["message"] = {
        "attachment": attachment,
        "quick_replies": quick_replies
    }
    data = json.dumps(request_payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status



def post_start_button(payload='START'):
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload_data = {}
    payload_data['get_started'] = {'payload': payload}
    data = json.dumps(payload_data)
    status = requests.post(url, headers=HEADER, data=data)
    return status




#def post_settings(greeting_text):
#    url = THREAD_SETTINGS_URL.format(access_token=PAGE_ACCESS_TOKEN)
#    txtpayload = {}
#    txtpayload['setting_type'] = 'greeting'
#    txtpayload['greeting'] = {'text': greeting_text}
#    data = json.dumps(txtpayload)
#    greeting_text_status = requests.post(
#        url, headers=HEADER, data=data
#    )
#    # Set the start button
#    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
#    btpayload = {}
#    btpayload['get_started'] = {'payload': 'USER_START'}
#    data = json.dumps(btpayload)
#    get_started_button_status = requests.post(
#        url, headers=HEADER, data=data
#    )
#    return (greeting_text_status, get_started_button_status)


if __name__ == '__main__':


    #greet = "Hello i am computer vision bot!!!"
    #print("greeting........")
    #post_settings(greet)
    print("satrt button....")
    post_start_button()

