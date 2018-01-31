from django.http import HttpResponse
import requests

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def bot_response(request, bot_response_id):
    response_id=str(bot_response_id);
    string = "Hello, I am a bot response."+response_id;



    # imposto l'URL per inviare i messaggi indietro al bot
    URL='https://api.telegram.org/bot' + "543129108:AAE13LpVqITEfI-DmzGkQP1rRPvq6fzuLQc" + '/sendMessage'

    # invio indietro alla chat ID il messaggio ricevuto
    richiesta = requests.get(URL, verify=False, data={'chat_id': bot_response_id, 'text': string})

    return HttpResponse(richiesta)

