from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader


@csrf_exempt
def error_view(request):
    template = loader.get_template('error.html')
    return HttpResponse(template.render({}))
