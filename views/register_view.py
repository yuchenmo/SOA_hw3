from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
from django.contrib import auth
from django.contrib.auth.models import User

import json

@csrf_exempt
def register(request, **kwargs):
    template = loader.get_template('register.html')
    print ("template = {}".format(template))
    data = {
        'info': ''
    }
    return HttpResponse(template.render(data))


@csrf_exempt
def register_jump(request, **kwargs):
    user_data = request.GET
    print (user_data)
    username, password, password_rep, email = user_data['username'], user_data['password1'], user_data['password2'], user_data['email']

    if password == password_rep:
        if User.objects.filter(username=username).exists():
            data = {
                'info': 'Username already exists'
            }
            template = loader.get_template('register.html')
            return HttpResponse(template.render(data))
        else:
            user = User.objects.create_user(username, email, password)
            auth.login(request, user)
            return HttpResponseRedirect("/")
    else:
        data = {
            'info': 'Password should be the same'
        }
        template = loader.get_template('register.html')
        return HttpResponse(template.render(data))

