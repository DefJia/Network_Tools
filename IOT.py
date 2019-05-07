import requests
import time
from datetime import datetime
from configparser import ConfigParser
import re
from Detect import Detect
from Login_Campus_network import Login


cfg = ConfigParser()
cfg.read('.config.ini', encoding='utf-8')


class AutoPadavan:
    def __init__(self):
        self.url = dict()
        self.url['main'] = cfg.get('Padavan', 'Url')
        self.url['get_wifi_list'] = self.url['main'] + 'wds_aplist_2g.asp'
        self.url['apply_wifi'] = self.url['main'] + 'start_apply.htm'
        self.url['re_connect'] = self.url['main'] + 'device-map/wan_action.asp'
        self.url['get_ip'] = self.url['main'] + 'device-map/internet.asp'
        self.url['detect_inner'] = 'http://10.0.0.55/'
        self.url['detect_outer'] = 'http://ip111.cn'
        self.url['pre_login'] = 'http://10.0.0.55/srun_portal_pc_yys.php?ac_id=8&'
        self.url['login'] = 'http://10.0.0.55/cgi-bin/get_challenge'
        # URl
        self.headers = dict()
        self.headers['Authorization'] = cfg.get('Padavan', 'Auth')
        # HEADERS
        self.detect = Detect()
        self.username = cfg.get('Login', 'Username')
        self.password = cfg.get('Login', 'Password')
        # self.login = Login(self.username, self.password, self.get_ip())

    def get_wifi_list(self):
        timestamp = int(round(time.time() * 1000))
        data = {'_': timestamp}
        r = requests.get(self.url['get_wifi_list'], headers=self.headers, params=data)
        raw_lst = r.text.split('=')[1]
        lst = list()
        exec(format('lst += %s' % raw_lst))
        return lst

    def connect_wifi(self):
        data = {'current_page':'/Advanced_WMode2g_Content.asp', 'next_page':'', 'next_host':'192.168.2.1', 'sid_list':'WLANConfig11b;', 'group_id':'rt_RBRList', 'action_mode':'Apply', 'action_script':'', 'rt_country_code':'CN', 'rt_wdsnum_x_0':'0', 'rt_sta_auto':'0', 'rt_sta_ssid_org':'BIT-Web', 'rt_sta_wpa_mode':'2', 'rt_sta_wpa_psk_org':'', 'rt_mode_x':'4', 'rt_sta_wisp':'1', 'rt_wdslist_x_0':'', 'rt_sta_ssid':'BIT-Web', 'rt_sta_auth_mode':'open'}
        try:
            lst = self.get_wifi_list()
        except:
            print('网络连接错误o(╥﹏╥)o...[ErrorCode:11, Time:%s]' % str(datetime.now())[:-7])
            return -1
        else:
            n = 0
            for i in lst:
                if i[1] == 'b0:8b:cf:e6:bd:03':
                    break
                n += 1
            if n < len(lst):
                channel = lst[n][2]
                data['rt_channel_org'] = channel
                data['rt_channel'] = channel
                try:
                    r = requests.post(self.url['apply_wifi'], headers=self.headers, data=data)
                except:
                    print('网络连接错误o(╥﹏╥)o[ErrorCode:12, Time:%s]' % str(datetime.now())[:-7])
                    return -1
                else:
                    print('Padavan连接BIT-Web成功！%s' % str(datetime.now())[:-7])
                    return 0
            else:
                print('Padavan没有搜索到BIT-Web...QAQ...%s' % str(datetime.now())[:-7])
                return 1

    def re_connect(self):
        data = dict()
        data['wan_action'] = 'Connect'
        data['modem_prio'] = 1
        try:
            r = requests.post(self.url['re_connect'], headers=self.headers, data=data)
            if r.status_code == 200:
                print('Padavan重新连接BIT-Web成功！%s' % str(datetime.now())[:-7])
                return 0
            else:
                print('Padavan重新连接BIT-Web失败...%s' % str(datetime.now())[:-7])
                return 1
        except:
            print('网络连接错误o(╥﹏╥)o[ErrorCode:21, Time:%s]' % str(datetime.now())[:-7])
            return -1

    def get_ip(self):
        r = requests.get(self.url['get_ip'], headers=self.headers)
        string = r"function wanlink_ip4_wan\(\) { return [0-9|.|']*;}"
        search = re.search(string, r.text)
        if search:
            search = search.group()
            string2 = r"[0-9]+.[0-9]+.[0-9]+.[0-9]+"
            ip = re.search(string2, search)
            if ip:
                return ip.group()
            else:
                return None
        else:
            return None

    def maintain_network(self):
        while True:
            r = self.detect.detect_outer()
            if r:
                rr = self.detect.detect_gateway()
                if rr:
                    self.re_connect()
                elif self.get_ip():
                    Login(self.username, self.password, self.get_ip()).login()
            time.sleep(1)


if __name__ == '__main__':
    cur = AutoPadavan()
    # cur.get_ip()
    cur.maintain_network()
    # cur.connect_wifi()
