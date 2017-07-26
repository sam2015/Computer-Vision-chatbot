from __future__ import print_function
import httplib, urllib, base64, json, time
from flask import Flask, session, request
from profile_ import post_template_w_quickreplies
from wit import Wit
import requests
import json



ACCESS_TOKEN = "EAAGqvw8s9JcBAMBpbJpVI69aalr2VJTwH2cQ2HyEZAVHFuFP4ztUcVZBLYApUrvK82cua2zSUAIwQZCPoqiD9wSsLrkPZAdMISDPqGRd27TS2hJ1kydR5TDup9FsqXKq7KEesFj1V9PNcH7CYubXzxkLw8QPR5hiV4gjeQX8TSD0nChbnyCe"
WIT_TOKEN = "THQXPBETYADIF33EZWSL5ZFXATTBP33P"
VERIFY_TOKEN = "see_the_image"




app = Flask(__name__)



g_context = {}
print(g_context)




@app.route('/', methods=['GET'])
def verify():
    # our endpoint echos back the 'hub.challenge' value specified when we setup the webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        print('Verifying........')
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return 'Hello World (from Flask!)', 200



@app.route('/', methods=['POST'])
def handle_incoming_messages():
    if request.method == "POST":
        data = request.json
        print(data)
        print('fb post message data enters here.....')
        print
        senderId = data['entry'][0]['messaging'][0]['sender']['id'] # sender id
        req = data['entry'][0]['messaging'][0]
        print(req)
        DEFAULT_MAX_STEPS = 5
        global g_context
        if "message" in req:
            print ('enter message')
            if "text" in req['message']:
                text = req['message']['text']
                print
                print('text message :.....',text)
                g_context = client.run_actions(session_id=senderId, message=text,context=g_context, max_steps=DEFAULT_MAX_STEPS)
                return "ok"
            elif "attachments" in req['message']:
                print('entering attachment:.......')
                print(g_context)
                if "text_done" in g_context:
                    del g_context['text_done']
                    return "ok"
                if req['message']['attachments'][0]['type'] == 'image':
                    print('image.......')
                    url = req['message']['attachments'][0]['payload']['url']
                    g_context = client.run_actions(session_id=senderId, message=str(url),context=g_context, max_steps=DEFAULT_MAX_STEPS)
                    print("status code 200")
                    print ("url__ : ",url)
                    return "ok"
            else:
                return "Different Event"
        elif "postback" in req:
            post_back = req['postback']['payload']
            if post_back == "START":
                post_template_w_quickreplies(senderId)
                return "ok"
            else:
                print("no postback...")
                return "ok"
                




def make_quickreplies(reply):
    return {
          'content_type': 'text',
           'title': reply,
          'payload': reply,
            }



def send(request, response):
    message = {}
    fb_id = request['session_id']
    if 'text' in response:
        message['text'] = response['text']
    if 'quickreplies' in response:
        if response['quickreplies']:
            if response['quickreplies'][0] == "image captioning":
                message['quick_replies'] = map(make_quickreplies, response["quickreplies"])
    fb_message(fb_id, message)




def loading_action(sender_id):
    data = {
    "recipient": {"id": sender_id},
    "sender_action":"typing_on"
    }
    qs = 'access_token=' + ACCESS_TOKEN
    resp = requests.post('https://graph.facebook.com/v2.6/me/messages?' + qs,
                         json=data)
    print(resp.content)





def first_entity_value(entities, entity):
    """
    Returns first entity value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def fb_message(sender_id, message):

    data = {
    'recipient': {'id': sender_id},
    'message': message
            }
    print(message)
    qs = 'access_token=' + ACCESS_TOKEN
    resp = requests.post('https://graph.facebook.com/v2.6/me/messages?' + qs,
                         json=data)
    print(resp.content)













def image_captioning(url="https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg"):
    uri_base = 'westcentralus.api.cognitive.microsoft.com'
    headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': "10b90e1918b145388a24bbfc9a2fb134",
    }
    params = urllib.urlencode({
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
    })
    body = {'url': url}
    try:
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        parsed = json.loads(data)
        conn.close()
        return str(parsed['description']['captions'][0]['text'])
    except Exception as e:
        print('Error:')
        print(e)



def handwritten_to_text(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Cursive_Writing_on_Notebook_paper.jpg/800px-Cursive_Writing_on_Notebook_paper.jpg'):
    subscription_key = "10b90e1918b145388a24bbfc9a2fb134"
    uri_base = 'westcentralus.api.cognitive.microsoft.com'
    headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
    }
    body = {'url': url}
    
    params = urllib.urlencode({'handwriting' : 'true'})
    try:
        conn = httplib.HTTPSConnection(uri_base)
        conn.request("POST", "/vision/v1.0/RecognizeText?%s" % params, str(body), headers)
        response = conn.getresponse()
        if response.status != 202:
            parsed = json.loads(response.read())
            print ("Error:")
            print (json.dumps(parsed, sort_keys=True, indent=2))
            conn.close()
            exit()
        
        operationLocation = response.getheader('Operation-Location')
        parsedLocation = operationLocation.split(uri_base)
        answerURL = parsedLocation[1]
        print('\nHandwritten text submitted.retrieve the recognized text.\n')
        time.sleep(10)
        conn = httplib.HTTPSConnection(uri_base)
        conn.request("GET", answerURL, '', headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        parsed = json.loads(data)
        conn.close()
        return parsed
    except Exception as e:
        print('Error:')
        print(e)



def hnd_to_text(url):
    text = handwritten_to_text(url=url)
    get_text = []
    for i in range(len(text['recognitionResult']['lines'])):
        get_text.append(str(text['recognitionResult']['lines'][i]['text']))
    string = ' '.join([get_text[::-1][i] for i in range(len(get_text[::-1]))])
    return string 











def get_text(request):
    context = request['context']
    entities = request['entities']
    sender_id = request['session_id']

    intent = first_entity_value(entities, 'intent')
    if "url" in intent:
        url = first_entity_value(entities, 'url')
        print (url)
        fb_message(sender_id, {"text": "Showing text"})
        loading_action(sender_id)
        text = hnd_to_text(url=str(url))
        fb_message(sender_id, {"text": text})
        context['text_done'] = True
    return context





def get_image_cap(request):
    context = request['context']
    entities = request['entities']
    sender_id = request['session_id']

    intent = first_entity_value(entities, 'intent')
    if "url" in intent:
        url = first_entity_value(entities, "url")
        print(url)
        fb_message(sender_id, {"text": "Showing text"})
        loading_action(sender_id)
        text = image_captioning(url= str(url))
        fb_message(sender_id, {"text": text})
        context['cap_done'] = True
    return context



actions = {
    'send':send,
    'getText' :get_text,
    'getImageCap':get_image_cap,
}


client = Wit(access_token=WIT_TOKEN, actions=actions)







if __name__ == '__main__':


    app.run(debug=True,port=8080)