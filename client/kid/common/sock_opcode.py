# -.- coding:utf-8 -.-
'''
Created on 2015年9月7日

@author: chenyitao
'''

class KidSockOpcode(object):
    '''
    爬虫sock消息操作码
    '''
    #心跳包
    s_heart = 100
    # 爬虫管理注册
    c_manager_register = 1001
    # 爬虫管理器注册成功
    s_manager_register = 1002
    # 获取客户端设备信息
    s_device_info = 1003
    # 提交客户端本地设备信息
    c_device_info = 1004
    # 服务器登录错误码
    s_error_code = 1005
    # 分配任务
    s_distribute_task = 1014
    # 任务状态回复
    c_distribute_task = 1015
    # 获取任务爬取的内容个数
    s_crawling_amount = 1016
    # 提交爬取内容个数
    c_crawling_amount = 1017
    # 提交爬取内容存储信息
    c_data_save_info = 1018
    # 获取伪造UA、IP
    c_achieve_UA_IP = 1019
    # 返回IP
    s_IP_info = 1020
    # 返回UA
    s_UA_info = 1021
    # 提交ftp存储信息
    c_ftp_save_info = 1022
    # 获取平台cookies
    c_cookies = 1050
    # 获得平台cookies
    s_cookies = 1052
    # 反馈未完成任务个数
    c_task_num = 1060
    # 新闻详情任务
    s_news_deatil_task = 1070
    # 新闻详情任务状态回复
    c_news_detail_state = 1071
