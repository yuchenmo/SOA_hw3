# -*- coding: utf-8 -*-
# @Author: yuchen
# @Date:   2017-04-06 13:38:20
# @Last Modified by:   yuchen
# @Last Modified time: 2017-04-06 19:33:20

from http import client
from urllib import request, parse, error
import base64
import json

class FaceAPI(object):
	def __init__(self):
		self.person_group_id = 'SOA_HW3'
		self.headers = {
		    # Request headers
		    'Content-Type': 'application/json',
		    'Ocp-Apim-Subscription-Key': json.load(open("../utils/apikey.json", 'r'))['key'],
		}

		self.cognitive_url = "westus.api.cognitive.microsoft.com"
		self.person_group_url_root = "/face/v1.0/persongroups/"
		self.detect_url_root = "/face/v1.0/detect?"
		self.identify_url_root = "/face/v1.0/identify?"

	# Output: None
	def create_person_group(self):
		body = {
			"name": "SOA_HW3",
    		"userData": "Users registered in SOA_HW3"
		}

		try:
		    conn = http.client.HTTPSConnection(self.cognitive_url)
		    conn.request("PUT", self.person_group_url_root + "{personGroupId}?%s" % self.person_group_id, 
		    			 json.dumps(body), self.headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
			data = {'error': 'PUT failed in create_person_group: [Errno {0}] {1}'.format(e.errno, e.strerror)}
		return data

	# Output: None
	def train_person_group(self):
		try:
		    conn = http.client.HTTPSConnection(self.cognitive_url)
		    conn.request("POST", self.person_group_url_root +  "{personGroupId}/train?%s" % self.person_group_id, 
		    			 None, self.headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
			data = {'error': 'POST failed in train_person_group: [Errno {0}] {1}'.format(e.errno, e.strerror)}
		return data

	# Output: status("succeeded")
	def check_train_status(self):
		try:
		    conn = http.client.HTTPSConnection(self.cognitive_url)
		    conn.request("GET", self.person_group_url_root + "{personGroupId}/training?%s" % self.person_group_id, 
		    			 None, self.headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
			data = {'error': 'GET failed in check_train_status: [Errno {0}] {1}'.format(e.errno, e.strerror)}
		return data

	# Output: personId(string)
	def create_person(self, username, userdata=''):
		body = {
	    	"name": username,
    		"userData": userdata
		}	
		
		try:
		    conn = http.client.HTTPSConnection(self.cognitive_url)
		    conn.request("POST", self.person_group_url_root + "{personGroupId}/persons?%s" % self.person_group_id, 
		    	 		 json.dumps(body), self.headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
			data = {'error': 'POST failed in create_person: [Errno {0}] {1}'.format(e.errno, e.strerror)}
		return data

	# Input: personId, imgurl, userdata(optional)
	# Output: persistedFaceId(string)
	def add_face(self, personid, imgurl, targetface='', userdata=''):
		params = urllib.parse.urlencode({
		    # Request parameters
		    'userData': userdata,
    		'targetFace': targetface,
		})
		body = {
			'url': imgurl
		}

		try:
		    conn = http.client.HTTPSConnection(self.cognitive_url)
		    conn.request("POST", self.person_group_url_root + "{personGroupId}/persons/{personId}/persistedFaces?%s".format(
		    			 personGroupId=self.person_group_id, personId=personid),
		    			 json.dumps(body), self.headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
			data = {'error': 'POST failed in add_face: [Errno {0}] {1}'.format(e.errno, e.strerror)}
		return data

	# Input: image url
	# Output: faceId, faceRectangle, faceAttributes
	def detect(self, url):
		face_id_attr_params = urllib.parse.urlencode({
		    # Request parameters
		    'returnFaceId': 'true',
		    'returnFaceLandmarks': 'false',
		    'returnFaceAttributes': 'age,gender,glasses,emotion',
		})
		body = json.dumps({'url': url})

		try:
		    conn = http.client.HTTPSConnection(self.cognitive_url)
		    conn.request("POST", self.detect_url_root + face_id_attr_params, body, self.headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
			data = {'error': 'POST failed in detect: [Errno {0}] {1}'.format(e.errno, e.strerror)}
		return data

	def identify(self, faceId):
		params = urllib.parse.urlencode({})
		body = {    
		    "personGroupId": self.person_group_id,
		    "faceIds": faceId,
		    "maxNumOfCandidatesReturned": 1,
		    "confidenceThreshold": 0.5
		}

		try:
		    conn = http.client.HTTPSConnection(self.cognitive_url)
		    conn.request("POST", self.identify_url_root + params, json.dumps(body), self.headers)
		    response = conn.getresponse()
		    data = response.read()
		    conn.close()
		except Exception as e:
			data = {'error': 'POST failed in identify: [Errno {0}] {1}'.format(e.errno, e.strerror)}
		return data



