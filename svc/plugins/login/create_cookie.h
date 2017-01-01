//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//   Created on: 2016.12.25 Author: kerry

#ifndef CREATE_COOKIE_H_
#define CREATE_COOKIE_H_
#include "logic/auto_crawler_infos.h"
#include <string>

namespace login_logic {

class XueQiuCookie {
public:
  XueQiuCookie(const std::string basic_cookie);
  virtual ~XueQiuCookie();

  void GetCookies(base_logic::LoginCookie &cookie, const int32 num,
                  std::list<base_logic::LoginCookie> &list);

private:
  std::string CreateS();
  std::string CreateU();
  std::string CreateRand(const char *src, int32 len);
  void GetCookieInfo(std::string &cookie);

private:
  std::string basic_cookie_;
};

class CreateCookieEngine {
public:
  CreateCookieEngine();
  virtual ~CreateCookieEngine();

public:
  static CreateCookieEngine *GetCookiesInstance() {
    if (engine_ == NULL)
      engine_ = new CreateCookieEngine();
    return engine_;
  }

  static void FreeCookiesInstance() {
    if (engine_ != NULL) {
      delete engine_;
      engine_ = NULL;
    }
  }

private:
  static CreateCookieEngine *engine_;

public:
  bool OnCreateCreate(const int64 pid, base_logic::LoginCookie &info,
                      const int32 num,
                      std::list<base_logic::LoginCookie> &list);
};
}

#endif /* CREATE_COOKIE_H_ */
