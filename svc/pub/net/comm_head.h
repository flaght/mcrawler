//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月7日 Author: kerry

#ifndef KID_PUB_NET_COMM_HEAD_H_
#define KID_PUB_NET_COMM_HEAD_H_

#include <list>
#include <string>

#include "basic/basictypes.h"

#define PASSWORD_SIZE   8 + 1
#define MAC_SIZE        16 + 1
#define TOKEN_SIZE      32 + 1
#define SIGNATURE_SIZE  16 ＋ 1
#define STORAGE_INFO_SIZE 32 + 1
#define IP_FORGEN_SIZE     31 + 1
#define UA_FORGEN_SIZE   251 + 1
#define HADRINFO_SIZE   16 + 1
#define URL_SIZE        256 + 1
#define NAME_SIZE       32 + 1
#define KEY_SIZE        32 + 1

enum PRS {
  NOZIP_AND_NOENCRYPT = 0,
  ZIP_AND_NOENCRYPT = 1,
  NOZIP_AND_ENCRYPT = 2,
  ZIP_AND_ENCRYPT = 3
};

enum operatorcode {
  HEART_PACKET = 0x64,

  CRAWLER_MGR_REG = 0x3E9,
  CRAWLER_MGR_REGSTATE = 0x3EA,
  GET_HARDINFO = 0x3EB,
  REPLY_HARDINFO = 0x3EC,
  CRAWLER_REG_FAILED = 0x3ED,

  ASSIGNMENT_SINGLE_TASK = 0x3F5,
  ASSIGNMENT_MULTI_TASK = 0x3F6,
  ASSIGNMENT_DETAIL_TASK = 0x42E,
  REPLY_TASK_STATE = 0x3F7,
  REPLY_DETAIL_STATE = 0x42F,

  GET_CRAWL_CONTENT_NUM = 0x3F8,
  REPLY_CRAWL_CONTENT_NUM = 0x3F9,

  CRAWL_HBASE_STORAGE_INFO = 0x3FA,

  GET_FORGEINFO = 0x3FB,
  REPLY_FOGEINFO_IP = 0x3FC,
  REPLY_FOGEINFO_UA = 0X3FD,
  CRAWL_FTP_STORAGE_INFO = 0x3FE,

  ANALYTICAL_INFO = 0x406,
  ANALYTICAL_REG = 0x407,
  ANALYTICAL_STATE = 0x408,
  ANALYTICAL_URL_SET = 0x409,

  LOGIN_REQUIRE_COOKIES = 0x41A,
  SPECIAL_PREASSIGN_COOKIES = 0x41B,
  DELIVERED_COOKIE_SET = 0x41C,
  COMMON_PREASSIGN_COOKIES = 0x41D,
  COOKIES_UPDATE = 0x41E,

  CRAWLER_AVAILABLE_RESOURCE_NUM = 0x424,

  TEMP_CRAWLER_OP = 20000,
  TEMP_ANALYTICAL = 30000

};

//  packet_length 长度为原始数据长度
struct PacketHead {
  int16 packet_length;
  int8 is_zip_encrypt;
  int8 type;
  int16 signature;
  int16 operate_code;
  int16 data_length;
  int32 timestamp;
  int64 session_id;
  int32 reserved;
};

#define PACKET_HEAD_LENGTH (sizeof(int16) * 4 + sizeof(int8) * 2 + \
    sizeof(int32) * 2 + sizeof(int64))

//  CRAWLER_MGR_REG = 1001
#define CRAWLER_MGR_REG_SIZE (sizeof(int16) + PASSWORD_SIZE - 1 + MAC_SIZE - 1)
struct CrawlerMgrReg : public PacketHead {
  int16 level;
  char password[PASSWORD_SIZE];
  char mac[MAC_SIZE];
};

//  ANALYTICAL_REG = 1031
struct AnalyticalMgrReg : public CrawlerMgrReg {
};

//  CRAWLER_MGR_REGSTATE = 1002
#define CRAWLER_MGR_REG_STATE_SIZE (sizeof(int32) + TOKEN_SIZE - 1)
struct CrawlerMgrRegState : public PacketHead {
  int32 id;
  char token[TOKEN_SIZE];
};

//  GET_HARDINFO = 1003 PACKHEAD

//  REPLY_HARDINFO = 1004
#define REPLY_HARDINFO_SIZE (sizeof(int32) +\
        TOKEN_SIZE - 1 + (HADRINFO_SIZE - 1) * 2)\

struct ReplyHardInfo : public PacketHead {
  int32 id;
  char token[TOKEN_SIZE];
  char cpu[HADRINFO_SIZE];
  char mem[HADRINFO_SIZE];
};

//  CRAWLER_FAILED = 1005
#define CRAWLER_FAILED_SIZE (sizeof(int32))
struct CrawlerFailed : public PacketHead {
  int32 erron_code;
};

//  ASSIGNMENT_SINGLE_TASK = 1013
#define ASSIGNMENT_SINGLE_TASK_SIZE (sizeof(int32)\
        + sizeof(64) + sizeof(8) * 2 + URL_SIZE -1)
struct AssignmentSingleTask : public PacketHead {
  int32 id;
  int64 task_id;
  int8 depth;
  int8 machine;
  int8 storage;
  char url[URL_SIZE];
};

#define TASK_UNIT_SIZE (sizeof(int64) * 4 + sizeof(int8) * 8\
         + URL_SIZE - 1)
struct TaskUnit {
  int64 task_id;
  int64 pid;
  int64 attr_id;
  int64 unix_time;
  int8 max_depth;
  int8 current_depth;
  int8 machine;
  int8 storage;
  int8 is_login;
  int8 is_over;
  int8 is_forge;
  int8 method;
  char url[URL_SIZE];
};

//  ASSIGNMENT_MULTI_TASK = 1014
struct AssignmentMultiTask : public PacketHead {
  int32 id;
  std::list<struct TaskUnit*> task_set;
};

//  ASSIGNMENT_DETAIL_TASK = 1070
struct AssignmentDetailTask : public PacketHead {
  int32 id;
  std::list<struct TaskUnit*> task_set;
};

//  REPLY_TASK_STATE = 1015
#define REPLYTASKTATE_SIZE (sizeof(int32) + TOKEN_SIZE - 1\
    + sizeof(int64) + sizeof(int8))
struct ReplyTaskState : public PacketHead {
  int32 id;
  char token[TOKEN_SIZE];
  int64 jobid;
  int8 state;
};

//  REPLY_DETAIL_STATE = 1071
#define REPLYDETAILTATE_SIZE (sizeof(int32) + TOKEN_SIZE - 1\
    + sizeof(int64) + sizeof(int8))
struct ReplyDetailState : public PacketHead {
  int32 id;
  char token[TOKEN_SIZE];
  int64 jobid;
  int8 state;
};

//  GET_CRAWL_CONTENT_NUM =1016
#define CRAWLCONTENTNUM_SIZE (sizeof(int32) + sizeof(int64))
struct CrawlContentNum : public PacketHead {
  int32 id;
  int64 jobid;
};

//  REPLY_CRAWL_CONTENT_NUM = 1017
#define REPLYCRAWLCONTENTNUM_SIZE (sizeof(int32) * 2 + sizeof(int64)\
    + TOKEN_SIZE - 1)
struct ReplyCrawlContentNum : public PacketHead {
  int32 id;
  char token[TOKEN_SIZE];
  int64 task_id;
  int32 num;
};

#define CRAWLSTORAGEINFO_SIZE ((STORAGE_INFO_SIZE - 1) + (URL_SIZE - 1)\
        + sizeof(int64) * 2 + sizeof(int8) * 2)
struct StorageUnit {
  int64 task_id;
  int64 attr_id;
  int8 max_depth;
  int8 cur_depth;
  char key_name[STORAGE_INFO_SIZE];  //位置
  char pos_name[URL_SIZE];  //文件名
};

//  CRAWL_HBASE_STORAGE_INFO = 1018 //CRAWL_FTP_STORAGE_INFO = 1019
struct CrawlStorageInfo : public PacketHead {
  int32 id;
  char token[TOKEN_SIZE];
  std::list<struct StorageUnit*> storage_set;
};

//  GET_FORGEINFO = 1019
#define GETFORGEINFO_SIZE (sizeof(int32) + TOKEN_SIZE - 1\
    +sizeof(int64) + sizeof(int8) * 2)
struct GetForgeInfo : public PacketHead {
  int32 id;
  char token[TOKEN_SIZE];
  int64 task_id;
  int8 forge_type;
  int8 num;
};

//  REPLY_FOGEINFO_IP = 1020
#define IPFORGEINFO_SIZE (sizeof(int32) + sizeof(int8) + IP_FORGEN_SIZE - 1)
struct IPForgeInfo {
  int32 id;
  int8 type;
  char forgen_info[IP_FORGEN_SIZE];
};
struct ReplyIPForgeInfo : public PacketHead {
  int32 id;
  int64 task_id;
  std::list<struct IPForgeInfo*> forgen_set;
};

//  REPLY_FOGEINFO_UA = 1021
#define UAFORGEINFO_SIZE (sizeof(int32) + sizeof(int8) + UA_FORGEN_SIZE - 1)
struct UAForgeInfo {
  int32 id;
  int8 type;
  char forgen_info[UA_FORGEN_SIZE];
};
struct ReplyUAForgeInfo : public PacketHead {
  int32 id;
  int64 task_id;
  std::list<struct UAForgeInfo*> forgen_set;
};

#define ANALYIUNIT_SIZE  ((NAME_SIZE - 1) + (KEY_SIZE - 1)\
    + sizeof(int64) * 2 + sizeof(int32) + sizeof(int8) * 3 )
struct AnalysiUnit {
  int64 ayalysi_id;
  int64 task_id;
  int32 attr_id;
  int8 type;
  int8 max_depth;
  int8 cur_depth;
  char name[NAME_SIZE];
  char key[KEY_SIZE];
};

//  ANALYTICAL_INFO
struct AnalysiInfo : public PacketHead {
  std::list<struct AnalysiUnit*> analysi_set;
};

//  ANALYTICAL_STATE
#define ANALYSISTATE_SIZE (sizeof(int64) + sizeof(int8))
struct AnalysiState : public PacketHead {
  int64 id;
  int8 state;
};

//  ANALYTICAL_URL_SET = 1033
#define ANALYTICAL_URL_UNIT_SIZE (sizeof(int8) * 3\
        +sizeof(int64) * 2 + URL_SIZE - 1)
struct AnalyticalURLUnit {
  int64 task_id;
  int64 attr_id;
  int8 max_depth;
  int8 current_depth;
  int8 method;
  char url[URL_SIZE];
};

struct AnalyticalURLSet : public PacketHead {
  int32 id;
  char token[TOKEN_SIZE];
  std::list<AnalyticalURLUnit*> analytical_url_set;
};

#define REQUIRE_LOGIN_COOKIE_LENGTH (32 + sizeof(int64) + \
    sizeof(int32) + sizeof(int8))

struct LoginCookieUnit {
  int16 len;
  std::string login_cookie_body;
  //std::string login_last_time;
};

struct LoginCookieSet : public PacketHead {
  int32 manage_id;
  int64 attr_id;
  std::list<LoginCookieUnit*> login_cookie_set;
};

struct RequireLoginCookie : public PacketHead {
  int32 manage_id;
  char token[TOKEN_SIZE];
  int64 attr_id;
  int8 amount;
};

#define CRAWLER_AVAILABLE_RESOURCE_NUM_SIZE (sizeof(int32) + sizeof(int16))
struct CrawlerAvailableResourceNum : public PacketHead {
  int32 manage_id;
  int16 task_num;
};

#endif /*KID_PUB_NET_COMM_HEAD_H_*/
