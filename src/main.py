from flask import Flask, request

from helper.openai_api import generate_image, text_complition
from helper.telegram_api import sendMessage, sendPhoto

app = Flask(__name__)

@app.route('/')
def home():
    return 'OK', 200

@app.route('/telegram', methods=['POST', 'GET'])
def telegram():
    try:
        data = request.get_json()
        
        message = data['message']

        query = message['text']
        sender_id = message['from']['id']
        '''
        I will separate the query into two parts
        if the query starts with /ask then I will use text completion
        if the query starts qith /img then I will use image genartion
        otherwise I will say use /ask or /img command 
        '''
        '''
        /ask what is sos?
        '''
        words = query.split(' ')

        if words[0] == '/ask':
            query = ' '.join(words[1:])
            response = text_complition(query)
            sendMessage(sender_id, response['response'])
        elif words[0] == '/img':
            query = ' '.join(words[1:])
            response = generate_image(query)
            sendPhoto(sender_id, response['url'], 'Generated by Openai.')
        else:
            # Change your message
            sendMessage(sender_id, 'Please use /ask and /img commands before your query.')
    except:
        pass
    finally:
        return 'OK', 200
