//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//   Created on: 2016.12.25 Author: kerry
#include "login/create_cookie.h"
#include "basic/radom_in.h"

namespace login_logic {

CreateCookieEngine *CreateCookieEngine::engine_ = NULL;

XueQiuCookie::XueQiuCookie(const std::string basic_cookie)
    : basic_cookie_(basic_cookie) {
  srand(time(NULL));
}

XueQiuCookie::~XueQiuCookie() {}

void XueQiuCookie::GetCookies(base_logic::LoginCookie &cookie, const int32 num,
                              std::list<base_logic::LoginCookie> &list) {
  for (int32 i = 0; i < num; i++) {
    base_logic::LoginCookie tcookie;
    std::string cookie_str;
    GetCookieInfo(cookie_str);
    tcookie.DeepCopy(cookie);
    tcookie.set_cookie_body(cookie_str);
    list.push_back(tcookie);
  }
}

void XueQiuCookie::GetCookieInfo(std::string &cookie) {
  cookie = basic_cookie_ + CreateS() + CreateU();
}

std::string XueQiuCookie::CreateS() {
  const char *str = "abcdefghijklmnopqrstuvwxyz0123456789";
  std::string s = CreateRand(str, 10);
  return std::string("s=") + s + ";";
}

std::string XueQiuCookie::CreateU() {
  char *str = "0123456789";
  std::string u = CreateRand(str, 15);
  return std::string("u=") + u + ";";
}

std::string XueQiuCookie::CreateRand(const char *src, int32 len) {
  char *name = new char[len];
  memset(name, '\0', len);
  size_t str_len = strlen(src);
  for (int32 i = 0; i < len; i++) {
    int64 trand = base::SysRadom::GetInstance()->GetRandomID();
    trand = trand > 0 ? trand : (0 - trand);
    int pos = (trand % str_len);
    name[i] = src[pos];
  }
  std::string s;
  s.assign(name, len);
  if (name) {
    delete[] name;
    name = NULL;
  }
  return s;
}

CreateCookieEngine::CreateCookieEngine() {}

CreateCookieEngine::~CreateCookieEngine() {}

bool CreateCookieEngine::OnCreateCreate(
    const int64 pid, base_logic::LoginCookie &info, const int32 num,
    std::list<base_logic::LoginCookie> &list) {
  switch (pid) {
  case 60006: {
    login_logic::XueQiuCookie xq(info.get_cookie_body());
    xq.GetCookies(info, num * 5, list);
    break;
  }
  default:
    break;
  }
  return true;
}
}
