from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
@csrf_exempt
def main_view(request, **kwargs):
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}))
