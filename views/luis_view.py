from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from LUIS.luis import get_luis_response

@login_required(login_url='/')
@csrf_exempt
def luis_view(request, **kwargs):
    content = request.GET.get('content')
    result = get_luis_response(content)

    if 'error' in result:
        return HttpResponseRedirect("/main")

    indent = result['indent']
    entities = result['entities']

    print (indent)
    print (entities)

    if indent == "ResetEmail":
        email = None
        for item in entities:
            if item[1] == 'builtin.email':
                email = item[0]
                break
        if email:
            User.objects.filter(username=request.user.username).update(email=email)
        return HttpResponseRedirect("/profile")
    if indent == "ResetPassword":
        password = None
        for item in entities:
            if item[1] == 'password':
                password = item[0]
                break
        if password:
            print ("New password = {}".format(password))
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(password)
            u.save()
        return HttpResponseRedirect("/main")
    elif indent == "CheckMainPage":
        return HttpResponseRedirect("/main")
    elif indent == "PredictAutomobile":
        return HttpResponseRedirect("/main")
    elif indent == "CheckProfile":
        return HttpResponseRedirect("/profile")
    elif indent == "Logout":
        return HttpResponseRedirect("/logout")
    elif indent == "TakeSnap":
        return HttpResponseRedirect("/add_face")
    else:
        return HttpResponseRedirect("/main")
