from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from IPython import embed
import json
import numpy as np
import cv2
from hashlib import md5
from os import path as op
from face.loginapi import env

@login_required(login_url='/')
@csrf_exempt
def profile_view(request, **kwargs):
    username = request.user.username
    profile = env.get_profile(username)
    print (profile)
    age = profile['age']
    gender = profile['gender']
    emotion = np.array(profile['emotion']).argmax()
    facenum = profile['facenum']
    emotionkeys = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]

    data ={
        'age': age,
        'gender': 'male' if gender < 0.5 else 'female',
        'emotion': emotionkeys[emotion],
        'facenum': facenum
    }
    template = loader.get_template('profile.html')
    print ("PROFILE VIEW CHECKPOINT")
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
        print ("POST is None")
        return HttpResponseRedirect("/")

