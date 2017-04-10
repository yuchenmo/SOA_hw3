from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
@csrf_exempt
def main_view(request, **kwargs):
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}))
