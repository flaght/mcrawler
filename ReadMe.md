              ==================================
               The MCrawler -Distributed crawler
              ==================================

基于scrapy框架进行开发的分布式爬虫系统，服务端采用C/C++开发，客户端则基于scrapy爬虫框架，通过进程间管理方式调度scrapy进行爬取

Features
========
 * 服务端采用插件框架,将每个独立逻辑层封装在一个插件里，方便任意扩展，采用多线程模式及响应事件模型处理承受大规模用户并发及大规模数据处理。
 * 服务端可调度任意爬虫客户端，实现最优资源使用
 * 爬虫客户端采用爬虫管理端调度爬虫，并通过进程间通讯来实现数据交互
 

Structure
========
....\\svc  
....\\...\\plugins  
....\\...\\...\\crawler_schduler(爬虫调度器)  
....\\...\\...\\crawler_task(爬虫任务分配管理)  
....\\...\\...\\forgery(反防爬管理)  
....\\...\\...\\login(模拟登录管理)  
....\\...\\...\\manager(注册管理)  
....\\...\\...\\storager(存储管理)  
....\\...\\...\\task(已经停用)  
....\\...\\...\\tools(已经停用)  
....\\...\\pub  
....\\...\\...\\activemq(已经停用)  
....\\...\\...\\activemq_client(已经停用)  
....\\...\\...\\activemq_client_bak(已经停用)  
....\\...\\...\\arithmetic(算法相关)  
....\\...\\...\\logic(逻辑相关共用)  
....\\...\\...\\net(网络协议相关)  
....\\...\\...\\storage(存储相关)  
....\\...\\...\\zip(暂未使用)  
  
...\\client  
...\\...\\analysis  
...\\...\\...\\base  
...\\...\\...\\common  
...\...\crawler  

Example
========



Building
========


Definitions
========


Design
========


Tests
========
测试FTP信息:  
地址 192.168.1.100
账号 crawler
密码 123456x
