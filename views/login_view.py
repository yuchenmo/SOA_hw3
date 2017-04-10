from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
from django.contrib import auth
from django.contrib.auth.models import User
from os import path as op
from hashlib import md5
import json

from face.loginapi import env
import numpy as np
import cv2
import base64
import time

from IPython import embed

ip = "localhost:8000"


@csrf_exempt
def login_with_face_jump(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/main")
    rawdata = request.FILES.get('webcam').read()
    # file_bytes = np.asarray(bytearray(rawdata), dtype=np.uint8)
    # img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # m = md5()
    # m.update(file_bytes)
    # name = "{}.jpg".format(m.hexdigest())
    # path = op.join(settings.BASE_DIR + settings.STATIC_DIRS,
    #                'snapshots', name)
    # cv2.imwrite(path, img)
    # url = "http://{}/static/snapshots/{}".format(ip, name)
    # with open(path, 'rb') as img_file:
    #   url = base64.b64encode(img_file.read())
    #   url = img_file.read()
    url = rawdata
    t = env.login_with_face(url)
    if 'error' in t:
        print("Login failed: {}".format(t))
        # Login failed
        return HttpResponseRedirect("/")
    else:
        print("Login successful")
        username = t['username']
        user = User.objects.get(username=username)
        auth.login(request, user)
        while not request.user.is_authenticated():
            time.sleep(0.1)
        print("It's time")
        # template = loader.get_template('main.html')
        # return HttpResponse(template.render({}))
        return HttpResponseRedirect("/main")


@csrf_exempt
def login_with_password(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        storage = messages.get_messages(request)
        data = {
            'msg': storage
        }
        storage.used = True

        template = loader.get_template('login_with_pwd.html')
        return HttpResponse(template.render(data))


@csrf_exempt
def login_with_password_jump(request, **kwargs):
    if request.POST is not None:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username = {}, password = {}".format(username, password))
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            print("Logged in")
            auth.login(request, user)
            return HttpResponseRedirect("/main")
        else:
            print("Incorrect username or password: username {}, password {}".
                  format(username, password))
            return HttpResponseRedirect('/')
    else:
        print("POST is None")
        return HttpResponseRedirect("/")


@csrf_exempt
def logout(request, **kwargs):
    try:
        auth.logout(request)
    except:
        print("Logout panic")
    return HttpResponseRedirect("/")
