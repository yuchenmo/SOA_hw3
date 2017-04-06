# -*- coding: utf-8 -*-
# @Author: yuchen
# @Date:   2017-04-06 19:03:25
# @Last Modified by:   yuchen
# @Last Modified time: 2017-04-06 21:39:33

# This lib provides higher level APIs than faceAPI. 
# Through this lib, faceAPI should not be transparent to the back-end module.

from faceapi import FaceAPI

class LoginAPI(object):
	def __init__(self):
		self.env = FaceAPI()
		tmp = self.env.check_person_group()
		print (tmp)
		print (tmp is None)
		print ('error' in tmp)
		if tmp is None or 'error' in tmp:
			pass
		else:
			print ("Deleting...")
			tmp = self._ensure(self.env.delete_person_group())
		
		tmp = self._ensure(self.env.create_person_group())

		self.username_to_personid = {}
		self.personid_to_username = {}

	# Ensure FaceAPI status
	# Naive implementation
	def _ensure(self, data):
		# print ('Checking {}'.format(data))
		assert data is None or 'error' not in data, data['error']
		return data

	# Create person
	# Back-end should be (user name, password, faceid)
	# However, username-password mode can be done through Django User module
	def create_person(self, username):
		tmp = self._ensure(self.env.create_person(username))
		person_data = tmp
		self.username_to_personid[username] = person_data['personId']
		self.personid_to_username[person_data['personId']] = username

	# Train on the person group immediately after a new face was uploaded
	# Multiprocess?
	def add_face(self, username, img_url):
		tmp = self._ensure(self.env.detect(img_url))
		face_data = tmp
		# Choose the main face
		face_data = sorted(face_data, 
						   key=lambda x: (x['faceRectangle']['width'] * x['faceRectangle']['height']))[::-1] 

		faceId = face_data[0]['faceId']
		rect = face_data[0]['faceRectangle']
		print (rect)
		targetface = "{left},{top},{width},{height}".format(left=rect['left'], 
																	   top=rect['top'], 
																	   width=rect['width'], 
																	   height=rect['height'])
		print (targetface)
		tmp = self._ensure(self.env.add_face(self.username_to_personid[username], img_url, targetface=targetface))
		tmp = self._ensure(self.env.train_person_group())

	# Login
	def login_with_face(self, img_url):
		tmp = self._ensure(self.env.check_train_status())
		status = tmp['status']
		if status != "succeeded":
			return {'error': 'Model is under training'}

		tmp = self._ensure(self.env.detect(img_url))
		face_data = tmp
		print (face_data)
		# Choose the main face
		face_data = sorted(face_data, 
						   key=lambda x: (x['faceRectangle']['width'] * x['faceRectangle']['height']))[::-1] 

		faceId = face_data[0]['faceId']

		tmp = self._ensure(self.env.identify(faceId))
		# print (tmp)
		candidate = None
		for item in tmp:
			if item['faceId'] == faceId:
				candidate = item['candidates']
				break
		if candidate is None or not isinstance(candidate, list):
			return {'error': 'Cognitive Service API error'}

		if candidate[0]['confidence'] > 0.1:
			return {'username': self.personid_to_username[candidate[0]['personId']]}
		else:
			return {'error': 'User not found'}





