import os, sys
import uuid
import time
import random, math, hashlib, string
import config

KEY = config.KEY 
PWD = config.PASSWORD
BASE_URL = config.BASE_URL
COOKIE_FILE = config.COOKIE_FILE

class mirouter:
	def __init__(self):
		self.key = KEY
		self.nonce = self.create_nonce()
		self.enpwd = self.encrypt_pwd()
		self.token = null
		self.url = null
		self.opener = null
		self.login(COOKIE_FILE)

	def login(self, COOKIE_FILE):
		cookie = cookielib.MozillaCookieJar(COOKIE_FILE)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		response = opener.open(BASE_URL)
		postdata = urllib.urlencode({
					'logintype':'2',
					'username':'admin',
					'password':self.enpwd,
					'nonce':self.nonce
			})
		login_url = BASE_URL + '/cgi-bin/luci/api/xqsystem/login'
		result = opener.open(BASE_URL, postdata)
		s = json.loads(result)
		if s["code"] == '0':
			self.opener = opener
			self.token = s["token"]
			self.url = s["url"].replace('/web/home', '')
		else:
			print 'Login Failed: ' + result.decode('unicode_escape')
			exit()

	def create_nonce(self):
		type = 0
		deviceId = self.get_mac_address()
		timestamp = int(time.time())
		randomstr = random.randint(1,10000)
		return "%s_%s_%s_%s" % (type, deviceId, timestamp, randomstr)

	def get_mac_address(self):
		mac = uuid.UUID(int = uuid.getnode()).hex[-12:] 
		return ":".join([mac[e:e+2] for e in range(0,11,2)])

	def encrypt_pwd(self, pwd=PWD):
		return hashlib.sha1(self.nonce + hashlib.sha1(pwd + self.key).hexdigest()).hexdigest()

	def get_devlist(self):
		deviceurl = BASE_URL + self.url + '/api/misystem/devicelist'
		result = self.opener(deviceurl)
		if s["code"] == '0':
			return s["list"]
		else:
			print 'Get Device List Failed: ' + result.decode('unicode_escape')
			exit()

if __name__ = '__main__':
	mr = mirouter()
	mr.login()
