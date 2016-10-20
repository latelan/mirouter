import os, sys
import requests
import uuid
import time
import random, math, hashlib, string
import config

KEY = config.KEY 
PWD = config.PASSWORD
BASE_URL = config.BASE_URL

class mirouter:
    def __init__(self):
        self.key = KEY
        self.nonce = self.create_nonce()
        self.enpwd = self.encrypt_pwd()
        self.s = requests.Session()
        self.token = None
        self.url = None
        self.login()

    def login(self):
        self.s.get(BASE_URL + '/cgi-bin/luci/web')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
        }
        postdata = {
            'logintype':'2',
            'username':'admin',
            'password':self.enpwd,
            'nonce':self.nonce
        }
        login_url = BASE_URL + '/cgi-bin/luci/api/xqsystem/login'
        result = self.s.post(login_url, headers=headers, data=postdata)
        s = result.json()
        if s['code'] == 0:
            self.token = s['token']
            self.url = s['url'].replace('/web/home', '')
        else:
            print 'Login Failed: ' + result.text
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
        result = self.s.get(deviceurl)
        s = result.json()
        if s['code'] == 0:
            return s['list']
        else:
            print 'Get Device List Failed: ' + result.text
            exit()

if __name__ == '__main__':
    mr = mirouter()
