# -.- coding:utf-8 -.-
"""
Created on 2016年11月25日

@author: kerry
"""

import os
class LocalManager:
    def __init__(self):
        pass

    def get_file_list(self,path):
        file_list = []
        for root,dirs,files in os.walk(path):
            for dir in dirs:
                for fn in files:
                    file_list.append(root + '/' + dir + '/'+ fn)

        return file_list

    def get_file(self,path,filename):
        return path + '/' + filename

def main():
    local = LocalManager()
    print local.get_file_list("/Users/kerry/work/pj/gitfork/mcrawler/client/analysis")

if __name__ == '__main__':
    main()