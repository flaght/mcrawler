//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//   Created on: 2016.12.23 Author: kerry

#include "gtest/gtest.h"
#include "logic/logic_comm.h"
#include "basic/basictypes.h"
#include "log/mig_log.h"
#include "basic/radom_in.h"
#include <string>

class XueQiuCookieTest: public testing::Test {
};

class XueQiuCookie{
 public:
  XueQiuCookie();
  virtual ~XueQiuCookie();
  void GetCookieInfo(std::string& cookie);
 private:
  std::string CreateS();
  std::string CreateU();
  std::string CreateRand(const char* src, int32 len);
 private:
  std::string basic_cookie_;
};

XueQiuCookie::XueQiuCookie() {
  srand(time(NULL));
  basic_cookie_ =
      "xq_a_token=ba3a563ac0e6e80f3ec726611f51b6c4ee183d0b;xq_r_token=e386c22c5442603d86294a718b13da436909b3f07;";
}

XueQiuCookie::~XueQiuCookie(){

}

std::string XueQiuCookie::CreateRand(const char* src, int32 len) {
  char* name = new char[len];
  memset(name,'\0',len);
  size_t str_len = strlen(src);
  for(int32 i = 0;i < len; i++){
    int64 trand = base::SysRadom::GetInstance()->GetRandomID();
    trand = trand > 0 ? trand : (0-trand);
    int pos = (trand % str_len);
    name[i] = src[pos];
  }
  std::string s;
  s.assgin(name, len);
  if (name) {delete [] name; name = NULL;}
  return s;
}

std::string XueQiuCookie::CreateS(){
  const char* str = "abcdefghijklmnopqrstuvwxyz0123456789";
  std::string s = CreateRand(str,10);
  return std::string("s=") + s + ";";
}

std::string XueQiuCookie::CreateU(){
  char* str = "0123456789";
  std::string u = CreateRand(str,15);
  return std::string("u=") + u + ";";
}

void XueQiuCookie::GetCookieInfo(std::string& cookie) {
  cookie =  basic_cookie_ + CreateS() + CreateU();
}


char *rand_str(char *name,const int len)
{
    char* str = "0123456789abcdefghijklmnopqrstuvwxyz";
    size_t str_len = strlen(str);
    int i;
    for(i=0;i<len;++i){
      int trand = rand();
      trand = trand > 0 ? trand : (0-trand);
      int pos = (trand % str_len);
      name[i]=str[pos];
    }
    return name;
}

TEST(XueQiuCookieTest, Basic){
  for(int32 i = 0; i < 10000; i++) {
    XueQiuCookie xq;
    std::string cookie;
    xq.GetCookieInfo(cookie);
    MIG_INFO(USER_LEVEL,"%s\n", cookie.c_str());
  }
}
