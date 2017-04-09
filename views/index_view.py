from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader


@csrf_exempt
def index_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/main")
    else:
        template = loader.get_template('new_index3.html')
        return HttpResponse(template.render({}))