from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader


@csrf_exempt
def main_view(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}))