# -*- coding: utf-8 -*-
# @Author: yuchen
# @Date:   2017-04-06 13:38:20
# @Last Modified by:   yuchen
# @Last Modified time: 2017-04-06 21:29:45

import http
import urllib
from urllib import request, parse, error
import base64
import json

class FaceAPI(object):
    def __init__(self):
        self.person_group_id = "group1"
        self.headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': json.load(open("../utils/apikey.json", 'r'))['key'],
        }

        self.cognitive_url = "westus.api.cognitive.microsoft.com"
        self.person_group_url_root = "/face/v1.0/persongroups/"
        self.detect_url_root = "/face/v1.0/detect?"
        self.identify_url_root = "/face/v1.0/identify?"

    def _get_data(self, raw_data):
        if len(raw_data) > 0:
            data = json.loads(raw_data.decode())
        else:
            data = None
        return data

    # Output: contains 'error' key or not
    def check_person_group(self):
        params = urllib.parse.urlencode({})
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("GET", self.person_group_url_root + "{}?{}".format(self.person_group_id, params), 
                          None, self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            print (data)
            conn.close()
        except Exception as e:
            data = {'error': 'GET failed in check_person_group: {}'.format(e)}
        return data

    # Output: None
    def create_person_group(self):
        params = urllib.parse.urlencode({})
        body = {
            "name": "hw3",
            "userData": "Users registered in SOA_HW3"
        }

        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("PUT", self.person_group_url_root + "{}?{}".format(self.person_group_id, params), 
                         json.dumps(body), self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'PUT failed in create_person_group: {}'.format(e)}
        return data

    def delete_person_group(self):
        params = urllib.parse.urlencode({})
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("DELETE", self.person_group_url_root + "{}?{}".format(self.person_group_id, params), 
                         '', self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'DELETE failed in delete_person_group: {}'.format(e)}
        return data

    # Output: None
    def train_person_group(self):
        params = urllib.parse.urlencode({})
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("POST", self.person_group_url_root +  "{}/train?{}".format(self.person_group_id, params),
                         '', self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in train_person_group: {}'.format(e)}
        return data

    # Output: status("succeeded")
    def check_train_status(self):
        params = urllib.parse.urlencode({})
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("GET", self.person_group_url_root + "{}/training?{}".format(self.person_group_id, params),
                         '', self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'GET failed in check_train_status: {}'.format(e)}
        return data


    # Output: personId(string)
    def create_person(self, username, userdata=''):
        params = urllib.parse.urlencode({})
        body = {
            "name": username,
            "userData": userdata
        }   
        
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("POST", self.person_group_url_root + "{}/persons?{}".format(self.person_group_id, params),
                         json.dumps(body), self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in create_person: {}'.format(e)}
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
            conn.request("POST", self.person_group_url_root + "{personGroupId}/persons/{personId}/persistedFaces?{params}".format(
                         personGroupId=self.person_group_id, personId=personid, params=params),
                         json.dumps(body), self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in add_face: {}'.format(e)}
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
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in detect: {}'.format(e)}
        return data

    def identify(self, faceId):
        params = urllib.parse.urlencode({})
        body = {    
            "personGroupId": self.person_group_id,
            "faceIds": [faceId],
            "maxNumOfCandidatesReturned": 1,
            "confidenceThreshold": 0.5
        }

        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("POST", self.identify_url_root + params, json.dumps(body), self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in identify: {}'.format(e)}
        return data



