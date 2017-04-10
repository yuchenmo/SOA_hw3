from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

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
