from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
from django.contrib import auth
from django.contrib.auth.models import User

from IPython import embed
import json
import md5

ip = "localhost:8000"

@csrf_exempt
def login_with_face(request, **kwargs):
    env = settings.env
    if request.POST is not None:
        nparr = np.fromstring(request.body, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        m = md5.new()
        m.update(request.body)
        name = "{}.jpg".format(m.digest())
        path = op.join(settings.BASE_DIR + settings.STATIC_DIRS, 'snapshots', name)
        cv2.imwrite(path, img)
        url = "http://{}/static/snapshots/{}".format(ip, name)

        t = env.login_with_face(url)
        if 'error' in t:
            # Login failed
            return HttpResponseRedirect("/")
        else:
            username = t['username']
            user = User.objects.get(username=username)
            auth.login(request, user)
            return HttpResponseRedirect("/main")
    else:
        return HttpResponseRedirect("/")

@csrf_exempt
def login_with_password(request, **kwargs):
    if request.POST is not None:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        # TODO: failure

        return HttpResponseRedirect("/main")
    else:
        return HttpResponseRedirect("/")

@csrf_exempt
def logout(request, **kwargs):
    try:
        auth.logout(request)
    except:
        print ("Logout panic")
    return HttpResponseRedirect("/")