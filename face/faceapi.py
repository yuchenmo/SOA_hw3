# -*- coding: utf-8 -*-
# @Author: yuchen
# @Date:   2017-04-06 13:38:20
# @Last Modified by:   yuchen
# @Last Modified time: 2017-04-08 13:21:17

import http
import urllib
from urllib import request, parse, error
import base64
import json
from os import path as op

class FaceAPI(object):
    def __init__(self):
        self.person_group_id = "group1"
        self.headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': json.load(open("key/apikey.json", 'r'))['key'],
        }

        self.file_header = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': json.load(open("key/apikey.json", 'r'))['key'],
        }

        self.cognitive_url = "westus.api.cognitive.microsoft.com"
        self.person_group_url_root = "/face/v1.0/persongroups/"
        self.detect_url_root = "/face/v1.0/detect?"
        self.identify_url_root = "/face/v1.0/identify?"
        self.null_params = urllib.parse.urlencode({})

    def _get_data(self, raw_data):
        if len(raw_data) > 0:
            data = json.loads(raw_data.decode())
        else:
            data = None
        return data

    def _inference_url(self, url):
        # TODO?
        return (url.lower()[:4] == 'http')

    # Output: contains 'error' key or not
    def check_person_group(self):
        print ("Checking person group")
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("GET", self.person_group_url_root + "{}?{}".format(self.person_group_id, self.null_params), 
                          None, self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'GET failed in check_person_group: {}'.format(e)}
        return data

    # Output: None
    def create_person_group(self):
        print ("Creating person group")
        body = {
            "name": "hw3",
            "userData": "Users registered in SOA_HW3"
        }

        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("PUT", self.person_group_url_root + "{}?{}".format(self.person_group_id, self.null_params), 
                         json.dumps(body), self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'PUT failed in create_person_group: {}'.format(e)}
        return data

    def delete_person_group(self):
        print ("Deleting person group")
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("DELETE", self.person_group_url_root + "{}?{}".format(self.person_group_id, self.null_params), 
                         '', self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'DELETE failed in delete_person_group: {}'.format(e)}
        return data

    # Output: None
    def train_person_group(self):
        print ("Traininng person group")
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("POST", self.person_group_url_root +  "{}/train?{}".format(self.person_group_id, self.null_params),
                         '', self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in train_person_group: {}'.format(e)}
        return data

    # Output: status("succeeded")
    def check_train_status(self):
        print ("Checking train status")
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("GET", self.person_group_url_root + "{}/training?{}".format(self.person_group_id, self.null_params),
                         '', self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'GET failed in check_train_status: {}'.format(e)}
        return data

    # Output: personId(string)
    def create_person(self, username, userdata=''):
        print ("Creating person: username = {}".format(username))
        body = {
            "name": username,
            "userData": userdata
        }   
        
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("POST", self.person_group_url_root + "{}/persons?{}".format(self.person_group_id, self.null_params),
                         json.dumps(body), self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in create_person: {}'.format(e)}
        return data

    # Input: personId(string)
    def update_person(self, personid, userdata=''):
        print ("Updating person: personid = {}".format(personid))
        body = {
            'userData': userdata 
        }
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("PATCH", self.person_group_url_root +  "{}/persons/{}?{}".format(
                         self.person_group_id, personId, self.null_params),
                         json.dumps(body), self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'PATCH failed in update_person: {}'.format(e)}
        return data

    # Input: personId(string)
    # Output: all data{'personId'(string), 'persistedFaceIds'(list), 'name'(string), 'userData'(string)}
    def get_person(self, personid):
        print ("Getting person: personid = {}".format(personid))
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("GET", self.person_group_url_root + "{}/persons/{}?{}".format(
                         self.person_group_id, personid, self.null_params), 
                         '', self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'GET failed in get_person: {}'.format(e)}
        return data

    # Input: personId(string), faceId(string)
    # Output: persistedFaceId(string), userData(string)
    def get_person_face(self, personid, faceid):
        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("GET", self.person_group_url_root + "{}/persons/{}/persistedFaces/{}?{}".format(
                         self.person_group_id, personid, faceid, self.null_params),
                         '', self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'GET failed in get_person_face: {}'.format(e)}
        return data

    # Input: personId, imgurl, userdata(optional)
    # Output: persistedFaceId(string)
    def add_face(self, personid, imgurl, targetface='', userdata=''):
        print ("Adding face")
        params = urllib.parse.urlencode({
            # Request parameters
            'userData': userdata,
            'targetFace': targetface,
        })

        if self._inference_url(imgurl):
            body = json.dumps({'url': imgurl})
            header = self.headers
        else:
            body = imgurl
            header = self.file_header

        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("POST", self.person_group_url_root + "{personGroupId}/persons/{personId}/persistedFaces?{params}".format(
                         personGroupId=self.person_group_id, personId=personid, params=params),
                         body, header)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in add_face: {}'.format(e)}
        return data

    # Input: image url
    # Output: faceId, faceRectangle, faceAttributes
    def detect(self, imgurl):
        print ("Detecting")
        face_id_attr_params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,glasses,emotion',
        })


        if self._inference_url(imgurl):
            body = json.dumps({'url': imgurl})
            header = self.headers
        else:
            body = imgurl
            header = self.file_header

        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            print ("BODY = {}".format(body))
            print ("HEADER = {}".format(header))
            conn.request("POST", self.detect_url_root + face_id_attr_params, body, header)
            response = conn.getresponse()
            data = self._get_data(response.read())
            print ("Raw response: {}".format(data))
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in detect: {}'.format(e)}
        return data

    # Input: faceId(string)
    # Output: error msg or corresponding username
    def identify(self, faceId):
        print ("Identifying")
        body = {    
            "personGroupId": self.person_group_id,
            "faceIds": [faceId],
            "maxNumOfCandidatesReturned": 1,
            "confidenceThreshold": 0.5
        }

        try:
            conn = http.client.HTTPSConnection(self.cognitive_url)
            conn.request("POST", self.identify_url_root + self.null_params, json.dumps(body), self.headers)
            response = conn.getresponse()
            data = self._get_data(response.read())
            conn.close()
        except Exception as e:
            data = {'error': 'POST failed in identify: {}'.format(e)}
        return data



