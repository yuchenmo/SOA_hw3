from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.contrib.auth.decorators import login_required

from IPython import embed
import numpy as np

from face.loginapi import env


@login_required(login_url='/')
@csrf_exempt
def profile_view(request, **kwargs):
    username = request.user.username
    profile = env.get_profile(username)
    print(profile)
    age = profile['age']
    gender = profile['gender']
    emotion = np.array(profile['emotion']).argmax()
    facenum = profile['facenum']
    emotionkeys = ["anger", "contempt", "disgust", "fear", "happiness",
                   "neutral", "sadness", "surprise"]

    gender = ('male' if gender < 0.35
              else ('female' if gender > 0.65 else 'unknown'))
    if profile['emotion'][emotion] > 0.1:
        emotion = profile['emotion'][emotion]
    else:
        emotion = 'unknown'

    data = {
        'age': age,
        'gender': gender,
        'emotion': emotion,
        'facenum': facenum
    }
    template = loader.get_template('profile.html')
    print("PROFILE VIEW CHECKPOINT")
    return HttpResponse(template.render(data))


@login_required(login_url='/')
@csrf_exempt
def add_face(request, **kwargs):
    template = loader.get_template('add_face.html')
    return HttpResponse(template.render({}))


@login_required(login_url='/')
@csrf_exempt
def add_face_jump(request, **kwargs):

    username = request.user.username
    if request.POST is not None:
        rawdata = request.FILES.get('webcam').read()
        url = rawdata
        t = env.add_face(username, url)
        return HttpResponseRedirect("/profile")
    else:
        print("POST is None")
        return HttpResponseRedirect("/")
