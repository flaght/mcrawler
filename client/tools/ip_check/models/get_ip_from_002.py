#!/usr/bin/env python
# coding: utf-8
import requests


class GetIPFrom002(object):
    """
    从API中获取IP
    """
    all_ip_list = []
    api_url = ''

    def __init__(self):
        """

        """
        self.api_url = 'http://www.ip002.com/api?order=1563356743683088&num=50&line=%E7%94%B5%E4%BF%A1&speed=%E5%BF%AB%E9%80%9F&port={}'

    def start_request(self):
        ports = ["80", "8080"]
        urls = [self.api_url.format(port) for port in ports]
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        header = {'User_Agent': user_agent}

        for request_url in urls:
            try:
                data = requests.get(request_url, headers=header, timeout=15)
            except Exception as e:
                print str(e)
            else:
                ip_port__list = data.content.split('\r\n')
                for ip_port in ip_port__list:
                    if len(ip_port) > 0:
                        one_dic = {'type': 1, 'ip': ip_port, 'refuse': 0, 'time_out': 0, 'used': 1}
                        self.all_ip_list.append(one_dic)


def get_ip_from_ip002():
    ports = ["80", "8080"]
    api_url = 'http://www.ip002.com/api?order=1563356743683088&num=50&line=%E7%94%B5%E4%BF%A1&speed=%E5%BF%AB%E9%80%9F&port={}'
    urls = [api_url.format(port) for port in ports]

    all_ip_list = []

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    header = {'User_Agent': user_agent}

    for request_url in urls:
        try:
            data = requests.get(request_url, headers=header, timeout=15)
        except Exception as e:
            get_ip_from_ip002()
            print str(e)
        else:
            ip_port__list = data.content.split('\r\n')
            for ip_port in ip_port__list:
                all_ip_list.append(ip_port)

    return all_ip_list


if __name__ == "__main__":
    t = GetIPFrom002()
    t.start_request()
    print t.all_ip_list
    #print get_ip_from_ip002()
