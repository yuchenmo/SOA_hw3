from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
from django.contrib import auth
from django.contrib.auth.models import User

from IPython import embed
import json
import numpy as np
from face.loginapi import env

@csrf_exempt
def profile_view(request, **kwargs):
    username = request.user.username
    profile = env.get_profile(username)
    age = profile['age']
    gender = profile['gender']
    smile = profile['smile']
    emotion = np.array(profile['emotion']).argmax()
    emotionkeys = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]

    data ={
        'age': age,
        'gender': 'male' if gender < 0.5 else 'female',
        'smile': '=)' if smile > 0.5 else 'Stay determined-_-',
        'emotion': emotionkeys[emotion]
    }
    template = loader.get_template('profile.html')
    # TODO: Add face button
    return render_to_response(template.render(data))

