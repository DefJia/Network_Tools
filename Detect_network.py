import requests
import subprocess
import time


def test_network(username, password):
    re = 0
    for i in range(3):
        n = subprocess.check_call("ping baidu.com", shell=True)
        re *= n.returncode
    if re == 0:
        return login_network(username, password)
    else:
        tt = time.asctime(time.localtime(time.time()))
        print('Network is OK with %s at %s' % (url, tt))
        time.sleep(1)

def detect_network(username, password):
    try:
        url = 'http://class.defjia.top/net.html'
        r = requests.get(url)
        if ('10.0.0.55' or 'ac_detect.php?') in r.text:
            return login_network(username, password)
            # network w/o login
        else:
            tt = time.asctime(time.localtime(time.time()))
            print('Network is OK with %s at %s' % (url, tt))
            return 1  # network & login
    except:
        return 0  # no network


def login_network(username, password):
    _url = 'http://10.0.0.55/ac_detect.php?ac_id=1&url=a.b.c'
    url = requests.get(_url).url
    post = {'action': 'login', 'username': username, 'password': password, 'ajax': 1, 'ac_id': 1, 'user_ip': '',
            'nas_ip': '', 'user_mac': '', 'save_me': 0}
    # url = 'http://10.0.0.55:802/include/auth_action.php'#optional port:801/2/3/4
    try:
        r = requests.post(url, data=post)
    except:
        return 0  # return detect_network(username, password)#no network
    if r.text[:8] == 'login_ok':
        tt = time.asctime(time.localtime(time.time()))
        print('login successfully with %s:%s at %s' % (username, password, tt))
        return 1  # login successfully
    elif r.text == 'IP has been online, please logout.':
        rr = logout_network(username, password)
        if rr == 1:
            return login_network(username, password)
        else:
            return rr
    elif 'E2620' in r.text:
        rr = logout_network(username, password)
        if rr == 1:
            return login_network(username, password)
        else:
            return rr
    elif 'E2531' in r.text:
        print('User not found')
        return -1  # username is wrong
    elif 'E2553' in r.text:
        print('Password is error.')
        return -1  # password is wrong
    else:  # unknown error
        print(r.text)
        return -2


def logout_network(username, password):
    post = {'action': 'logout', 'username': username, 'password': password, 'ajax': 1}
    url = 'http://10.0.0.55:802/include/auth_action.php'
    try:
        r = requests.post(url, data=post)
    except:
        return 0  # no network
    r.encoding = 'utf-8'
    if r.text == 'logout successfully':
        return 1  # logout successfully
    else:
        print(r.text)
        return -2  # fail in logout, perhaps with wrong info


if __name__ == '__main__':
    test_network()
