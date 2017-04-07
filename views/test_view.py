from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import Context, loader
import cv2
import numpy as np
from os import path as op

@csrf_exempt
def test_view(request):
	# print ("REQUEST = {}. REQUEST.POST = {}".format(request, request.POST))

	if request.POST is not None:
		# save it somewhere
		nparr = np.fromstring(request.body, np.uint8)
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		path = op.join(settings.BASE_DIR + settings.STATIC_DIRS, 'snapshots/latest.jpg')
		cv2.imwrite(path, img)
		# return the URL
		return HttpResponse('http://localhost:8000/static/snapshots/latest.jpg')
	else:
		return HttpResponse('no data')