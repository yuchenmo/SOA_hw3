from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from voice.voiceapi import voice_seq
import requests
import json
import uuid
from hashlib import md5


@login_required(login_url='/')
@csrf_exempt
def voice_acc(request, **kwargs):
    voice_seq.update(request.FILES.get('audio-blob').read())
    print("Got voice fragment")
    return HttpResponseRedirect("/main")


@login_required(login_url='/')
@csrf_exempt
def voice_view(request, **kwargs):

    full_voice = voice_seq.digest()
    access_token = requests.post("https://api.cognitive.microsoft.com/sts/v1.0/issueToken",
                                 headers={
                                     "Content-Length": "0",
                                     "Ocp-Apim-Subscription-Key": json.load(open("key/apikey.json", 'r'))['STT_api_key']
                                 }
                                 ).text
    data = requests.post("https://speech.platform.bing.com/recognize",
                         params={
                             'scenarios': 'ulm',
                             'appid': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5',
                             'locale': 'en-US',
                             'device.os': 'wp7',
                             'version': '3.0',
                             'format': 'json',
                             'requestid': uuid.uuid4(),
                             'instanceid': uuid.uuid4(),
                             "result.profanitymarkup": "0",
                         },
                         headers={
                             'Content-Type': 'audio/wav; samplerate=16000',
                             'Authorization': 'Bearer {}'.format(access_token)
                         },
                         data=full_voice)
    print(data.text)
    try:
        txt = sorted(json.loads(data.text)['results'], key=lambda x: float(
            x['confidence']))[::-1][0]['lexical']
    except:
        txt = 'None'
    return HttpResponseRedirect('/luis?content={}'.format(txt))
