import execjs
import requests
import time
import json


class Login:
    def __init__(self, username, password, ip):
        # Only for yidong
        self.url = dict()
        self.url['preparation'] = 'http://10.0.0.55/cgi-bin/get_challenge'
        self.url['target'] = 'http://10.0.0.55/cgi-bin/srun_portal'
        # self.url['target'] = 'http://httpbin.org/get'
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
        print(r.text)
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
        print(r.text)


if __name__ == '__main__':
    cur = Login('jiazerui', 'jzr31415926535', '10.62.58.218')
    cur.get_token()
    cur.get_parameters()
    cur.final_login()
