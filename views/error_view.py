from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
from django.contrib.auth.decorators import login_required

@csrf_exempt
def error_view(request):
    template = loader.get_template('error.html')
    return HttpResponse(template.render({}))
