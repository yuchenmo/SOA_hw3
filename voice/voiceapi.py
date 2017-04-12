# -*- coding: utf-8 -*-
# @Author: yuchen
# @Date:   2017-04-11 21:40:58
# @Last Modified by:   yuchen
# @Last Modified time: 2017-04-12 15:22:31


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class VoiceAPI(metaclass=Singleton):

	def __init__(self):
		self.clear()

	def update(self, data):
		if self.clear_flag:
			self.clear_flag = False
			self.bindata = []
		self.bindata.append(data)

	def digest(self):
		self.clear_flag = True
		return b''.join(self.bindata)

	def clear(self):
		self.bindata = []
		self.clear_flag = False


voice_seq = VoiceAPI()