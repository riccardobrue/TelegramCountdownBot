import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import logging

logger = logging.getLogger(__name__)

def index(request):
    string = "Hello, I am a bot response." + str(request);

    # imposto l'URL per inviare i messaggi indietro al bot
    URL = 'https://api.telegram.org/bot543129108:AAE13LpVqITEfI-DmzGkQP1rRPvq6fzuLQc/sendMessage'

    # invio indietro alla chat ID il messaggio ricevuto
    richiesta = requests.get(URL, verify=False, data={'chat_id': request, 'text': string})

    return HttpResponse(string)



@csrf_exempt
@require_POST
def sended(request,sended):
    string = "Hello, I am a bot response." + str(request) + sended;

    if request.method == 'GET':
        string+=string+"GET";
    elif request.method == 'POST':
        string+=string+"POST";



    # imposto l'URL per inviare i messaggi indietro al bot
    URL = 'https://api.telegram.org/bot543129108:AAE13LpVqITEfI-DmzGkQP1rRPvq6fzuLQc/sendMessage'

    # invio indietro alla chat ID il messaggio ricevuto
    richiesta = requests.get(URL, verify=False, data={'chat_id': request, 'text': string})

    return HttpResponse(string)











def bot_response(request, bot_response_id):
    response_id=str(bot_response_id);
    string = "Hello, I am a bot response."+response_id;

    # imposto l'URL per inviare i messaggi indietro al bot
    URL='https://api.telegram.org/bot543129108:AAE13LpVqITEfI-DmzGkQP1rRPvq6fzuLQc/sendMessage'

    # invio indietro alla chat ID il messaggio ricevuto
    richiesta = requests.get(URL, verify=False, data={'chat_id': bot_response_id, 'text': string})
    logger.info("Loading handlers for telegram bot"+richiesta)
    return HttpResponse(string)



