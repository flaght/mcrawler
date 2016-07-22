//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年11月28日 Author: jiaoyongqing
#ifndef TRUNK_PLUGINS_TOOLS_GET_COOKIE_H_
#define TRUNK_PLUGINS_TOOLS_GET_COOKIE_H_

#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>

#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <list>

#include "http/http_method.h"

#define USER_NUM 6

class GetCookie {
 public:
  GetCookie()
    :account_num_(USER_NUM),
    srv_(NULL),
    cur_p_(-1) {
    InitUser();

    set_random();
  }

  ~GetCookie() {
  }

 private:
  void InitUser();
  //  加密用户名
  std::string EncryptUsername(std::string username);

  //  解析加密参数
  bool FindParam(const std::string &content, \
             const std::string &neededparam, \
               std::string * const outparam);
  //  想新浪服务器请求加密参数
  bool GetParams(std::string * const servertime, \
                      std::string * const nonce, \
                      std::string * const rsakv, \
                     const std::string &username);
  //  颠倒字符窜
  void ReverseStr(char *str);

  //  10进制转16进制
  void TenToSixteen(int num, char* ret);

  //  2进制流转16进制
  std::string B2aHex(unsigned char*enc_data, int length);

  //  密码加密
  std::string EncryptPassword(const std::string &password, \
                            const std::string &servertime, \
                                 const std::string &nonce);

  std::string Encode(const std::string&str);

  //  解析出能过的登录cookie的地址
  bool GetRealAddress(const std::string &content, \
                 std::string * const real_address);
  //  制造随机时间
  void GetTime(std::vector<int> *const random_time, int start);

  void SetRandomTime(std::vector<int> *const random_time);

  // 制造随机用户
  void SetRandomUser();

  // 初始化需要post的数据
  void InitPostdata(std::string *const postdata, \
                    const std::string &username, \
                    const std::string &password, \
                  const std::string &servertime, \
                       const std::string &nonce, \
                       const std::string &rsakv);

  std::string GetTimeKey(int64 time);

  //  保存cookie
  void SaveCookie(const std::string &cookie, \
                const std::string &username, \
               const std::string &password);

  //  解析cookie
  void ParseCookie(http::HttpMethodGet *const get, \
                    const std::string &username, \
                    const std::string &password);

  void OnGetCookie();

  void set_random() {
    random_time_.clear();
    SetRandomTime(&random_time_);
    std::sort(random_time_.begin(), random_time_.end());
    SetRandomUser();
    cur_p_ = 0;
  }

  void NextHand();

  bool ParseCookie(std::list<std::string> *const l, \
                        std::string *const cookie);

 public:
  // 对外接口，该函数启动后，可获得cookie.
  void Start() {
    OnGetCookie();
  }

  int cur_random_time() {
    return random_time_[cur_p_];
  }

  void set_srv(struct server *s) {
    srv_ = s;
  }

 private:
  struct server *srv_;

  int account_num_;
  int cur_p_;
  std::string username_[USER_NUM];
  std::string password_[USER_NUM];

  std::vector<int> random_time_;
};

#endif  //  TRUNK_PLUGINS_TOOLS_GET_COOKIE_H_
