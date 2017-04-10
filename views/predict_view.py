from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User

import json
from automobile.model import predict


@csrf_exempt
def predict_view(request, **kwargs):
    inp = {}
    show_inp = {}
    namelist = ['make', 'body-style', 'wheel-base', 'engine-size',
                'horsepower', 'peak-rpm', 'highway-mpg']
    for item in namelist:
        inp[item] = str(request.POST.get(item))
        show_inp[item.replace('-', '_')] = str(request.POST.get(item))
    ans = predict(inp)
    show_inp['price'] = str(ans)

    template = loader.get_template('main.html')
    return HttpResponse(template.render(show_inp))
