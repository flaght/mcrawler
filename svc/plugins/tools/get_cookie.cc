//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年11月28日 Author: jiaoyongqing

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>

#include <iostream>
#include <sstream>
#include <map>
#include <string>
#include <algorithm>
#include <vector>
#include <list>

#include "tools/get_cookie.h"
#include "tools/rsa.h"
#include "tools/tools_logic.h"
#include "http/http_method.h"
#include "tools/db_comm.h"
#include "net/comm_head.h"
#include "core/common.h"
#include "basic/base64.h"
#include "basic/basic_util.h"

static const char DEFAULT_CONFIG_PATH[] = "./plugins/tools/tools_config.xml";

static const int STR_LEN = 60;

static const int MESSAGE_LEN = 4097;

void GetCookie::InitUser() {
  username_[0] = "15857131750";
  password_[0] = "UUSU97A4VV";

  username_[1] = "2386183708@qq.com";
  password_[1] = "1293227197";

  username_[2] = "398077850@qq.com";
  password_[2] = "wang279wang";

  username_[3] = "1445236764@qq.com";
  password_[3] = "uusu97a4vv";

  username_[4] = "2736265581@qq.com";
  password_[4] = "uusu97a4vv";

  username_[5] = "3084025787@qq.com";
  password_[5] = "uusu97a4vv";

  /*username_[6] = "15857131750@163.com";
  password_[6] = "uusu97a4vv";

  USERNAME[7] = "ppag1750b4d837db@souhu.com";
  PASSWORD[7] = "uusu97a4vv";

  USERNAME[8] = "@qq.com";
  PASSWORD[8] = "";

  USERNAME[9] = "@qq.com";
  PASSWORD[9] = "";

  USERNAME[10] = "@qq.com";
  PASSWORD[10] = "";

  USERNAME[11] = "@qq.com";
  PASSWORD[11] = "";

  USERNAME[12] = "@qq.com";
  PASSWORD[12] = "";

  USERNAME[13] = "@qq.com";
  PASSWORD[13] = "";

  USERNAME[14] = "@qq.com";
  PASSWORD[14] = "";
  
  USERNAME[15] = "@qq.com";
  PASSWORD[15] = "";

  USERNAME[16] = "@qq.com";
  PASSWORD[16] = "";

  USERNAME[17] = "@qq.com";
  PASSWORD[17] = "";

  USERNAME[18] = "@qq.com";
  PASSWORD[18] = "";

  USERNAME[19] = "@qq.com";
  PASSWORD[19] = "";

  USERNAME[20] = "@qq.com";
  PASSWORD[20] = "";

  USERNAME[21] = "@qq.com";
  PASSWORD[21] = "";*/
}

//  加密帐号
std::string GetCookie::EncryptUsername(std::string username) {
  /*return Base64Encode((unsigned char const*)(username.c_str()), \
    username.length());*/
  return base64_encode((unsigned char const*)(username.c_str()), \
    username.length());
}

//  解析加密密码的参数
bool GetCookie::FindParam(const std::string &content, \
                      const std::string &neededparam, \
                        std::string * const outparam) {
  std::string::size_type start_p = content.find(neededparam);
  if (start_p == std::string::npos) {
    return false;
  }

  int offset = (neededparam == "servertime") ? \
    neededparam.length() + 2 : neededparam.length() + 3;

  start_p += offset;

  std::string::size_type end_p = content.find(',', start_p);
  if (end_p == std::string::npos) {
    end_p = content.length();  //  没有找到，把位子定位到末尾
  }
  offset = (neededparam == "servertime") ? 0 : -1;
  end_p += offset;

  *outparam = content.substr(start_p, end_p - start_p);
  return true;
}

//  取加密密码的参数
bool GetCookie::GetParams(std::string * const servertime, \
                               std::string * const nonce, \
                               std::string * const rsakv, \
                             const std::string &username) {
  std::string url("http://login.sina.com.cn/sso/");
  url += std::string("prelogin.php?entry=sso&callback=");
  url += std::string("sinaSSOController.preloginCallBack&su=");
  url += username;
  url += std::string("&rsakt=mod&client=ssologin.js(1.4.18)");

  http::HttpMethodGet get(url);
  get.Get();
  std::string content("");
  get.GetContent(content);
  if (content == "") {
    LOG_ERROR2("get请求加密参数失败 %d", socket);
  }

  bool ret = false;
  ret = FindParam(content, std::string("servertime"), servertime) && ret;
  ret = FindParam(content, std::string("rsakv"), rsakv) && ret;
  ret = FindParam(content, std::string("nonce"), nonce) && ret;

  return ret;
}

//  颠倒字符串
void GetCookie::ReverseStr(char *str) {
  if (str == NULL) {
    exit(0);
  }
  int i = 0;
  int j = strlen(str) - 1;
  while (i <= j) {
    std::swap(str[i], str[j]);
    ++i;
    --j;
  }
}

//  10进制转16进制
void GetCookie::TenToSixteen(int num, char* ret) {
  if (num == 0) {
    ret[0] = '0';
    ret[1] = '0';
    return;
  }

  int l;
  int i;
  for (i = 0; num != 0; ++i) {
    l = num % 16;
    num /= 16;
    l = (l < 10) ? l + '0' : l % 10 + 'a';
    ret[i] = l;
  }
  if (i == 1) {
    ret[i] = '0';
    ++i;
  }
  ret[i] = '\0';
  ReverseStr(ret);
}

//  二进制流转16进制
std::string GetCookie::B2aHex(unsigned char*enc_data, int length) {
  int int_ch;
  std::string str_ch;
  std::string str_ret;
  char *ret = NULL;
  const int size = 100;
  ret = new char[size];
  for (int i = 0; i < length; ++i) {
    int_ch = enc_data[i];
    TenToSixteen(int_ch, ret);
    str_ch = std::string(ret);
    str_ret += str_ch;
  }
  return str_ret;
}

//  密码加密
std::string GetCookie::EncryptPassword(const std::string &password, \
                                     const std::string &servertime, \
                                          const std::string &nonce) {
  std::string weibo_rsa_n("EB2A38568661887FA180BDDB5CABD5F2");
  weibo_rsa_n += "1C7BFD59C090CB2D245A87AC25306288";
  weibo_rsa_n += "2729293E5506350508E7F9AA3BB77F43";
  weibo_rsa_n += "33231490F915F6D63C55FE2F08A49B35";
  weibo_rsa_n += "3F444AD3993CACC02DB784ABBB8E42A9";
  weibo_rsa_n += "B1BBFFFB38BE18D78E87A0E41B9B8F73";
  weibo_rsa_n += "A928EE0CCEE1F6739884B9777E4FE9E8";
  weibo_rsa_n += "8A1BBE495927AC4A799B3181D6442443";

  int weibo_rsa_e = 65537;

  std::string message = servertime + \
                 std::string("\t") + \
                             nonce + \
                 std::string("\n") + \
                         password;

  char origin_text[MESSAGE_LEN];
  snprintf(origin_text, message.length() + 1, "%s", message.c_str());
  int origin_len = strlen(origin_text);

  unsigned char *enc_data = NULL;
  int enc_len = 0;

  RsaOp ro;
  ro.set_params();
  ro.OpenPubkey();

  ro.PubkeyEncrypt((const unsigned char *)origin_text, \
                                           origin_len, \
                          (unsigned char **)&enc_data, \
                                             &enc_len);

  std::string ret = B2aHex(enc_data, enc_len);

  return ret;
}

std::string GetCookie::Encode(const std::string& str) {
  std::string::size_type start = 1;
  std::string::size_type end;
  std::string ret;
  std::string tmp;
  std::string tmp_out;
  while (true) {
    end = str.find('\'', start);
    tmp = str.substr(start, end - start);
    base::BasicUtil::UrlEncode(tmp, tmp_out);
    ret += tmp_out;
    ret += std::string(1, str[end+1]);
    start = end + 3;
    if (start > str.length()) {
      break;
    }
  }

  return ret;
}

bool GetCookie::GetRealAddress(const std::string &content, \
                         std::string * const real_address) {
  std::string::size_type start = content.find("location.replace(");
  start += 18;
  std::string::size_type end = content.find(")", start);
  end -= 1;

  if (start == std::string::npos || end == std::string::npos) {
    return false;
  }
  *real_address = content.substr(start, end - start);

  return true;
}

void GetCookie::GetTime(std::vector<int> *const random_time, int start ) {
  int random_num;
  std::vector<int> tmp;
  unsigned sed = time(NULL);
  for (int i = 0; i < 6;) {
    random_num = rand_r(&sed) % (3600 * 6) + start;
    std::vector<int>::iterator it = tmp.begin();
    for (; it != tmp.end(); ++it) {
      if (*it == random_num) {break;}
    }
    if (it == tmp.end()) {
      ++i;
      tmp.push_back(random_num);
    }
  }

  random_time->insert(random_time->end(), \
                             tmp.begin(), \
                              tmp.end());
}

void GetCookie::SetRandomTime(std::vector<int> *const random_time) {
  int interval[4]={0, 21600, 43200, 64800};

  for (int i = 0; i < 4; ++i) {
    GetTime(random_time, interval[i]);
  }
}

void GetCookie::SetRandomUser() {
  int random_num;
  unsigned sed = time(NULL);
  for (int i = 0; i < account_num_; ++i) {
    random_num = rand_r(&sed) % account_num_;
    std::swap(username_[0], username_[random_num]);
    std::swap(password_[0], password_[random_num]);
  }
}

void GetCookie::InitPostdata(std::string *const postdata, \
                             const std::string &username, \
                             const std::string &password, \
                           const std::string &servertime, \
                                const std::string &nonce, \
                                const std::string &rsakv) {
  *postdata = "\'entry\'=\'weibo\'&\'gateway\'=";
  *postdata += "\'1\'&\'from\'=\'\'&\'savestate\'";
  *postdata += "=\'7\'&\'useticket\'=\'1\'&";
  *postdata += "\'pagerefer\'=\'\'&\'vsnf\'=\'1\'&\'su";
  *postdata += "\'=\'";
  *postdata += username;
  *postdata += "\'&\'service\'=";
  *postdata += "\'miniblog\'&\'servertime\'=\'";
  *postdata += servertime;
  *postdata += "\'&\'nonce\'=\'";
  *postdata += nonce;
  *postdata += "\'&\'pwencode\'=\'rsa2\'";
  *postdata += "&\'rsakv\'=\'";
  *postdata += rsakv;
  *postdata += "\'&\'sp\'=\'";
  *postdata += password;
  *postdata += "\'&\'sr\'=\'1920*1080\'&\'encoding\'";
  *postdata += "\'UTF-8\'&\'prelt\'=\'402\'&\'url\'=";
  *postdata += "\'http://weibo.com/ajaxlogin.php?";
  *postdata += "framelogin=1&callback=";
  *postdata += "parent.sinaSSOController.feedBackUrlCallBack\'&";
  *postdata += "\'returntype\'=\'META\'";
}

std::string GetCookie::GetTimeKey(int64 time) {
  struct tm timeTm;
  int64 s = time;
  localtime_r(&s, &timeTm);
  char s_char[32];
  memset(s_char, '\0', sizeof(s_char));
  snprintf(s_char, sizeof(s_char),
               "%4d-%02d-%02d %02d",
               timeTm.tm_year+1900,
               timeTm.tm_mon+1,
               timeTm.tm_mday,
               timeTm.tm_hour);
  std::string str_time = s_char;
  return str_time;
}

void GetCookie::SaveCookie(const std::string &cookie, \
                         const std::string &username, \
                         const std::string &password) {
  time_t t;
  time(&t);
  std::string insert_time = GetTimeKey(t);
  std::stringstream os("");
  os << "call proc_insert_cookie(" << 5 \
                                   << ",\'" \
                                   << username\
                                   << "\',\'" \
                                   << password \
                                   << "\',\'" \
                                   << cookie \
                                   << "\',\'" \
                                   << insert_time \
                                   << "\'," \
                                   << 1 \
                                   << ");";
  std::string sql = os.str();
  base_storage::DBStorageEngine* engine  = tools_sql::DbSql::GetEntine();
  bool r = engine->SQLExec(sql.c_str());
  if (!r) {
    LOG_ERROR("exec sql error");
  }
}

bool GetCookie::ParseCookie(std::list<std::string> *const l, \
                                  std::string *const cookie) {
  std::list<std::string>::iterator it = l->begin();
  std::string tmp;
  for (; it != l->end(); ++it) {
    tmp = *it;
    if (std::string::npos != tmp.find("SUB=", 0) && \
       std::string::npos != tmp.find("domain=", 0)) {
      *cookie = tmp;
      return true;
    }
  }
  LOG_DEBUG2("\n%s\n", "解析cookie出错");
  return false;
}
void GetCookie::ParseCookie(http::HttpMethodGet *const get, \
                             const std::string &username, \
                             const std::string &password) {
  std::string cookie_key = "#LWP-Cookies-2.0\r\nSet-Cookie3: ";
  std::string cookie;
  std::list<std::string> l;
  get->GetHeader(std::string("Set-Cookie"), l);
  bool ret = ParseCookie(&l, &cookie);
  if (ret == true) {
    std::string tmp("");
    for (int i = 0; i < cookie.length(); ++i) {
      if (cookie[i] == '=') {
        tmp.append(1, cookie[i]);
        tmp.append(1, '\"');
      } else if (cookie[i] == ';') {
        tmp.append(1, '\"');
        tmp.append(1, cookie[i]);
      } else {
        tmp.append(1, cookie[i]);
      }
    }
    tmp.append(1, ';');
    cookie = tmp;
    cookie = cookie_key + cookie;

    SaveCookie(cookie, username, password);
  }
}

void GetCookie::OnGetCookie() {
  std::string url("http://login.sina.com.cn/sso/");
  url += "login.php?client=ssologin.js(v1.4.18)";

  std::string head("User-Agent':'Mozilla/5.0 ");
  head += "(X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0";

  std::string username;
  std::string password;
  std::string content;
  std::string servertime;
  std::string rsakv;
  std::string nonce;
  std::string cookie;
  std::string postdata;
  std::string real_address;

  http::HttpMethodPost post(url);
  post.SetHeaders(head);

  username = username_[cur_p_];
  password = password_[cur_p_];

  GetParams(&servertime, &nonce, &rsakv, username);
  username = EncryptUsername(username);
  password = EncryptPassword(password, servertime, nonce);

  InitPostdata(&postdata, \
                 username, \
                 password, \
               servertime, \
                    nonce, \
                    rsakv);

  postdata = Encode(postdata);

  post.Post(postdata.c_str());
  content = "";
  post.GetContent(content);

  if (false == GetRealAddress(content, &real_address)) {
     exit(0);
  }
  http::HttpMethodGet get(real_address);
  get.SetHeaders(head);
  get.Get();

  ParseCookie(&get, username_[cur_p_], password_[cur_p_]);

  NextHand();
}

void GetCookie::NextHand() {
  ++cur_p_;
  if (cur_p_ == USER_NUM) {
    set_random();
  }

  int sleep_time = cur_p_ == 0 ? random_time_[cur_p_] : \
    random_time_[cur_p_] - random_time_[cur_p_ - 1];

  srv_->add_time_task(srv_, "tools", TIME_GET_COOKIE, sleep_time, 1);
}
