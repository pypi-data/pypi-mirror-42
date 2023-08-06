from VpyK.methods import methods
from VpyK.longpoll import longpoll


class vkapi(methods, longpoll):
    def __init__(self, token, v = 'last', polling = 1, group = 0):
        self.token = token
        self.log = 1
        self.group = group

        if v == 'last':
            from bs4 import BeautifulSoup
            import requests

            soup = BeautifulSoup(requests.get('https://vk.com/dev/versions').text, 'lxml')
            v = soup.find('span', {'class': 'dev_version_num'}).text
            self.logging(v)

        self.v = v
        

        if polling:
            longpoll.get_longpoll(self)