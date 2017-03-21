# -*- coding: utf-8 -*-

"""
Created on 2017年1月24日

@author: kerry
"""

class PltOpcode:
    XUE_QIU = 60006
    HE_XUN = 60005

plt_opcode = PltOpcode()


class NetTaskOpcode:
    HEXUN_STOCK_DAY_HEAT = 588 #从和讯接口json内容解析单支股票的每天热度值
    HEXUN_STOCK_QUARTER_HEAT = 589 #从和讯接口jsonn内容解析单支股票每十五分钟的热度
    XUEQIU_GET_STOCK_DISCUSSION = 598 #从雪球接口json解析基于个股的讨论内容
    XUEQIU_GET_PERSONAL_TIMELINE_COUNT = 599 #从雪球接口json内容获取用户动态的个数
    #XUEQIU_GET_MEMBER_COUT = 600 #从雪球接口json内容获取每个用户关注个数
    XUEQIU_GET_ALL_MEMBER = 600 # 从雪球接口json内容中获每个用户关注的用户信息
    XUEQIU_GET_FLLOWER_COUNT = 601 #从雪球接口json内容中获取每个用户粉丝的个数

net_task_opercode = NetTaskOpcode()

class LocalTaskOpcode:
    XUEQIU_DISCUSSION = -598 #清洗雪球讨论数据,主要将讨论中的转发进行结构拆分
    XUEQIU_GET_DISCUSSION_UID = -599 #获取讨论结构中,讨论用户的ID
    XUEQIU_GET_MEMBER_MAX = -600 #解析出每个用户对应的关注列表的最大值 可查看 member_max.txt
    XUEQIU_GET_FOLLWER_MAX = -601 #解析出每个用户对应的粉丝列表最大值

local_task_opercode = LocalTaskOpcode()

