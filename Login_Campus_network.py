import execjs
import requests
import time
import socket
from datetime import datetime
import json
from configparser import ConfigParser


class Login:
    def __init__(self, username, password, ip):
        # Only for yidong
        self.url = dict()
        self.url['preparation'] = 'http://10.0.0.55/cgi-bin/get_challenge'
        self.url['target'] = 'http://10.0.0.55/cgi-bin/srun_portal'
        # Urls
        self.headers = dict()
        self.headers['Referer'] = 'http://10.0.0.55/srun_portal_pc_yys.php?ac_id=8&'
        self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        self.headers['Host'] = '10.0.0.55'
        self.headers['Connection'] = 'keep - alive'
        # Headers
        self.username = username + '@yidong'
        self.password = password
        self.ip = ip
        self.acid = '8'
        self.enc = 'srun_bx1'
        self.n = 200
        self.type = 1
        self.token = ''
        self.token = '763e06af37781e26d0be7ab65d5a6bbb5e2894913819a1d768a00ad05422be08'
        self.info = ''
        self.hmd5 = ''
        self.chksum = ''
        self.timestamp = 0
        # Parameters
        f = open('js/main.js')
        script = f.read()
        self.js = execjs.compile(script)
        # JS
        self.session = requests.session()

    def get_token(self):
        self.timestamp = int(round(time.time() * 1000))
        data = dict()
        data['callback'] = 'jsonp' + str(self.timestamp)
        data['username'] = self.username
        data['ip'] = self.ip
        r = self.session.get(self.url['preparation'], params=data, headers=self.headers)
        # print(r.text)
        if r.status_code == 200:
            raw_data = r.text[19:-1]
            try:
                data = json.loads(raw_data)
            except:
                # Error in r.text
                return 1
            else:
                self.token = data['challenge']
                return 0

    def get_parameters(self):
        self.info = self.js.call('calInfo', self.username, self.password, self.ip, self.acid, self.enc, self.token)
        self.hmd5 = self.js.call('calHmd5', self.token)
        self.chksum = self.js.call('calChksum', self.username, self.hmd5, self.acid, self.ip, self.info, self.token)
        self.hmd5 = '{MD5}' + self.hmd5
        return 0

    def final_login(self):
        data = dict()
        data['callback'] = 'jsonp' + str(self.timestamp + 1)
        data['action'] = 'login'
        data['username'] = self.username
        data['password'] = self.hmd5
        data['ac_id'] = self.acid
        data['ip'] = self.ip
        data['info'] = self.info
        data['chksum'] = self.chksum
        data['n'] = self.n
        data['type'] = self.type
        r = self.session.get(self.url['target'], params=data, headers=self.headers)
        info = self.parse_json(r.text, 'error')
        ip = self.parse_json(r.text, 'client_ip')
        if info == 'ok':
            print('%s login successfully at %s!' % (ip, str(datetime.now())[:-7]))
            return 0
        else:
            error_info = self.parse_json(r.text, 'error_msg')
            print('%s failed to login at %s! (Error massage: %s)' % (ip, str(datetime.now())[:-7], error_info))
            return 1

    def login(self):
        self.get_token()
        self.get_parameters()
        res = self.final_login()
        return res

    @staticmethod
    def parse_json(json_, key):
        json_str = json_.split('(')[1][:-1]
        json_dict = json.loads(json_str)
        if key in json_dict:
            return json_dict[key]
        else:
            return ''


if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('.config.ini', encoding='utf-8')
    username = cfg.get('Login', 'Username')
    password = cfg.get('Login', 'Password')
    ip = cfg.get('Login', 'IP')
    if ip == '':
        ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    cur = Login(username, password, ip).login()
