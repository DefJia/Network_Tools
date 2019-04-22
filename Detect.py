import platform
import os


class Detect:
    def __init__(self):
        self.interval = 1
        self.system = platform.system()
        self.gateway_url = '10.0.0.55'
        self.inner_url = '10.1.123.155'
        self.outer_url = '123.125.114.144'
        pass

    def detect(self, url):
        ping = format('ping %s' % url)
        if self.system != 'Windows':
            ping += ' -c 3'
        ping += ' >> Logs/ping_log.txt'
        res = os.system(ping)
        if res:
            print('%s 连接失败，重连中...' % url)
            return 1
        else:
            return 0

    def detect_outer(self):
        return self.detect(self.outer_url)

    def detect_gateway(self):
        return self.detect(self.gateway_url)


if __name__ == '__main__':
    a = Detect()
    a.detect_outer()
