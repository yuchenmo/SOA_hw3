from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from voice.voiceapi import voice_seq
import requests
import base64
import json


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
    '''
    https://speech.platform.bing.com/recognize

    POST /recognize?scenarios=catsearch&appid=f84e364c-ec34-4773-a783-73707bd9a585&locale=en-US&
    device.os=wp7&version=3.0&format=xml&
    requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&
    instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66 HTTP/1.1
    Host: speech.platform.bing.com
    Content-Type: audio/wav; samplerate=16000
    Authorization: Bearer [Base64 access_token]

    (audio data)
    '''
    data = requests.post("https://speech.platform.bing.com/recognize",
                         params={
                             'senarios': 'ulm',
                             'appid': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5',
                             'locale': 'en-US',
                             'device.os': 'Windows OS',
                             'version': '3.0',
                             'format': 'json',
                             'requestid': 'test',
                             'instanceid': 'test'
                         },
                         headers={
                             'Content-Type': 'audio/wav; samplerate=16000',
                             'Authorization': 'Bearer {}'.format(base64.b64encode(access_token.encode()))
                         },
                         data=full_voice)
    print(data.text)
    txt = data.text
    # txt = 'show profile'
    return HttpResponseRedirect('/luis?content={}'.format(txt))
