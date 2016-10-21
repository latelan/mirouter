import os, sys
import requests
import uuid
import time
import random, math, hashlib, string, re
import config

PWD = config.PASSWORD
BASE_URL = config.BASE_URL

class mirouter:
    def __init__(self):
        self.s = requests.Session()
        self.token = None
        self.url = None
        self.login()

    def login(self):
        req = self.s.get(BASE_URL + '/cgi-bin/luci/web/home')
        key = re.findall(r'key: \'(.*)\',', req.text)[0]
        mac = re.findall(r'deviceId = \'(.*)\';', req.text)[0]

        nonce = "%s_%s_%s_%s" % (0, mac, int(time.time()), random.randint(1000, 10000))
        encodepwd = hashlib.sha1(nonce + hashlib.sha1(PWD + key).hexdigest()).hexdigest()
        postdata = {
            'logintype':'2',
            'username':'admin',
            'password':encodepwd,
            'nonce':nonce
        }
        login_url = BASE_URL + '/cgi-bin/luci/api/xqsystem/login'
        result = self.s.post(login_url, data=postdata)
        s = result.json()
        if s['code'] == 0:
            self.token = s['token']
        else:
            print 'Login Failed: ' + result.text
            exit()

    def get_mac_address(self):
        mac = uuid.UUID(int = uuid.getnode()).hex[-12:] 
        return ":".join([mac[e:e+2] for e in range(0,11,2)])

    def encrypt_pwd(self, pwd=PWD):
        return hashlib.sha1(self.nonce + hashlib.sha1(pwd + self.key).hexdigest()).hexdigest()

    def get_devlist(self):
        deviceurl = BASE_URL + '/cgi-bin/luci/;stok=' + self.token + '/api/misystem/devicelist'
        result = self.s.get(deviceurl)
        s = result.json()
        if s['code'] == 0:
            return s['list']
        else:
            print 'Get Device List Failed: ' + result.text
            exit()

if __name__ == '__main__':
    mr = mirouter()
