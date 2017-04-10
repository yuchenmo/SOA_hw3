# -*- coding: utf-8 -*-
# @Author: yuchen
# @Date:   2017-04-06 19:03:25
# @Last Modified by:   yuchen
# @Last Modified time: 2017-04-10 11:36:06

# This lib provides higher level APIs than faceAPI.
# Through this lib, faceAPI should not be transparent to the back-end module.

from .faceapi import FaceAPI
import json
import numpy as np
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoginAPI(metaclass=Singleton):

    def __init__(self):
        self._env = FaceAPI()
        tmp = self._env.check_person_group()
        # TODO: serialize two dicts and check the existing person group everytime
        #       instead of deleting them?
        if tmp is None or 'error' in tmp:
            pass
        else:
            tmp = self._ensure(self._env.delete_person_group())

        self.username_to_personid = {}
        self.personid_to_username = {}

        self.faceid_to_attr_dict = "attribute.json"
        self._init_attr()

        tmp = self._ensure(self._env.create_person_group())
        tmp = self.create_person('JieTang')
        tmp = self.add_face(
            'JieTang', 'http://am-cdn-s0.b0.upaiyun.com/picture/01823/Jie_Tang_1348889820664.jpg!160?ran=0.6222543733421229')
        tmp = self._ensure(self._env.train_person_group())
        print("New LoginAPI object created")

    # Ensure FaceAPI status
    # Naive implementation
    def _ensure(self, data):
        # print ('Checking {}'.format(data))
        assert data is None or 'error' not in data, data['error']
        return data

    # Initialize faceId - Attribute db
    def _init_attr(self):
        if os.path.exists(self.faceid_to_attr_dict):
            os.remove(self.faceid_to_attr_dict)
            json.dump({}, open(self.faceid_to_attr_dict, 'w'))

    # Save faceId - Attribute locally
    def _save_attr(self, faceid, attribute):
        if not os.path.exists(self.faceid_to_attr_dict):
            json.dump({}, open(self.faceid_to_attr_dict, 'w'))
        with open(self.faceid_to_attr_dict, 'r') as f:
            data = json.load(f)

        emotionkeys = ["anger", "contempt", "disgust", "fear",
                       "happiness", "neutral", "sadness", "surprise"]
        serial_emotion = lambda x: [x[y] for y in emotionkeys]
        data[faceid] = {
            'age': float(attribute['age']),
            'gender': (1.0 if attribute['gender'] == 'male' else 0.0),
            'emotion': attribute['emotion']
        }
        json.dump(data, open(self.faceid_to_attr_dict, 'w'))

    # Load faceId - Attribute locally to accelerate profile view
    def _load_attr(self, faceid):
        with open(self.faceid_to_attr_dict, 'r') as f:
            data = json.load(f)
        return None if faceid not in data else data[faceid]

    # Create person
    # Back-end should be (user name, password, faceid)
    # However, username-password mode can be done through Django User module
    def create_person(self, username):
        person_data = self._ensure(self._env.create_person(username))
        self.username_to_personid[username] = person_data['personId']
        self.personid_to_username[person_data['personId']] = username

    # Train on the person group immediately after a new face was uploaded
    # Multiprocess?
    def add_face(self, username, img_url):
        face_data = self._ensure(self._env.detect(img_url))
        face_data = sorted(face_data,
                           key=lambda x: (x['faceRectangle']['width'] * x['faceRectangle']['height']))[::-1]

        faceId = face_data[0]['faceId']
        rect = face_data[0]['faceRectangle']
        attribute = face_data[0]['faceAttributes']

        targetface = "{left},{top},{width},{height}".format(left=rect['left'],
                                                            top=rect['top'],
                                                            width=rect[
                                                                'width'],
                                                            height=rect['height'])
        persisted_faceid = self._ensure(self._env.add_face(self.username_to_personid[
                                        username], img_url, targetface=targetface, userdata=json.dumps(attribute)))['persistedFaceId']
        self._save_attr(persisted_faceid, {'age': attribute['age'], 'gender': attribute[
                        'gender'], 'emotion': attribute['emotion']})
        tmp = self._ensure(self._env.train_person_group())

    # Login
    def login_with_face(self, img_url):
        status = self._ensure(self._env.check_train_status())['status']
        if status != "succeeded":
            return {'error': 'Model is under training'}

        face_data = self._ensure(self._env.detect(img_url))
        if len(face_data) == 0:
            return {'error': 'No face detected'}

        face_data = sorted(face_data,
                           key=lambda x: (x['faceRectangle']['width'] * x['faceRectangle']['height']))[::-1]
        faceId = face_data[0]['faceId']

        tmp = self._ensure(self._env.identify(faceId))
        candidate = None
        print("Identify result: {}".format(tmp))
        for item in tmp:
            if item['faceId'] == faceId:
                candidate = item['candidates']
                break
        if candidate is None or not isinstance(candidate, list):
            return {'error': 'Cognitive Service API error'}

        if len(candidate) == 0:
            return {'error': 'No reliable identification found'}
        if candidate[0]['confidence'] > 0.5:
            return {'username': self.personid_to_username[candidate[0]['personId']]}
        else:
            return {'error': 'User not found'}

    # Get profile
    def get_profile(self, username):
        if username not in self.username_to_personid:
            return {'error': 'User not found'}
        personid = self.username_to_personid[username]
        person_data = self._ensure(self._env.get_person(personid))
        agelist = []
        genderlist = []
        emotionlist = []
        emotionkeys = ["anger", "contempt", "disgust", "fear",
                       "happiness", "neutral", "sadness", "surprise"]
        serial_emotion = lambda x: [x[y] for y in emotionkeys]
        for faceid in person_data['persistedFaceIds']:
            tmp = self._load_attr(faceid)
            if tmp is None:
                face_data = json.loads(self._ensure(
                    self._env.get_person_face(personid, faceid))['userData'])
            else:
                face_data = tmp
            agelist.append(float(face_data['age']))
            genderlist.append(1.0 if face_data['gender'] == 'male' else 0.0)
            emotionlist.append(serial_emotion(face_data['emotion']))

        age = '-' if len(agelist) == 0 else np.array(agelist).mean()
        gender = 0.5 if len(genderlist) == 0 else np.array(genderlist).mean()
        emotion = [0.0 for _ in emotionkeys] if len(
            emotionlist) == 0 else np.array(emotionlist).mean(axis=0)
        facenum = len(agelist)
        return {'age': age, 'gender': gender, 'emotion': emotion, 'facenum': facenum}

env = LoginAPI()
