from requests import Session


class ConfigHeaders(object):
    sess = Session()
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' \
                 ' AppleWebKit/537.36 (KHTML, like Gecko)' \
                 ' Chrome/71.0.3578.98 Safari/537.36'

    def __init__(self):
        self.sess.headers.update({
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': self.user_agent,
        })


class PixivInitSay:
    init_run = 'Pixiver Initializing...'
    init_finished = 'Initialized!'


class BaseQueue(object):
    step_number = 0
    que_tar = []

    def __init__(self, argv=None):
        if argv:
            self.que_tar = argv

    def first(self):
        return self.que_tar[0]

    def curr(self):
        return self.que_tar[self.step_number]

    def prev(self):
        if self.step_number > 0:
            self.step_number -= 1
            return self.que_tar[self.step_number]
        else:
            print('Top!')

    def next(self):
        if self.step_number < len(self.que_tar) - 1:
            self.step_number += 1
            return self.que_tar[self.step_number]
        else:
            print('End!')

    def last(self):
        return self.que_tar[len(self.que_tar) - 1]

    def size(self):
        return len(self.que_tar)
