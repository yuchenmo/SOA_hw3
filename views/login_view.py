from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.contrib import auth
from django.contrib.auth.models import User

from face.loginapi import env
import time

ip = "localhost:8000"


@csrf_exempt
def login_with_face_jump(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/main")
    rawdata = request.FILES.get('webcam').read()
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
            time.sleep(0.05)
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
