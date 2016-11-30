# -.- coding:utf-8 -.-
"""
Created on 2016年11月30日

@author: kerry
"""

from urlparse import urlparse


class URLParseExt():
    def __init__(self, url, param=None):
        self.t_url = self.__parser(url)
        query = self.t_url.query
        self.qdict = {}
        sdict = query.split('&')
        for t in sdict:
            k = t.split('=')
            self.qdict[k[0]] = k[1]

    def __parser(self, url):
        return urlparse(url)

    def get_query_value(self, key):
        if len(self.qdict) == 0:
            return None
        return self.qdict[key]


def main():
    """

    Returns:

    """
    t = URLParseExt(
        'https://xueqiu.com/statuses/search.json?count=20&comment=0&symbol=SZ000625&hl=0&source=user&sort=time&page=1&_=1475722708502')

    print t


if __name__ == '__main__':
    main()
