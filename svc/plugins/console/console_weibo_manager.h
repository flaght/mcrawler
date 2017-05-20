//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#ifndef KID_CONSOLE_WEIBO_MANAGER_H__
#define KID_CONSOLE_WEIBO_MANAGER_H__

#include <map>
#include <string>
#include "thread/base_thread_lock.h"
#include "console/console_db.h"
namespace console_logic {

typedef std::map<int32, console_logic::WeiboInfo> WEIBOINFO_MAP;

class ConsoleWeiboCache {
 public:
  WEIBOINFO_MAP weibo_map_;
};

class ConsoleWeiboManager {
 public:
  ConsoleWeiboManager();
  virtual ~ConsoleWeiboManager();
 private:
  void Init();
 public:
  void Init(console_logic::ConsoleDB* console_db);
  void Swap(std::list<console_logic::WeiboInfo>& list);
  void Test();
  void UpdateWeibo();
 private:
  struct threadrw_t* lock_;
  ConsoleWeiboCache* weibo_cache_;
  console_logic::ConsoleDB* console_db_;
};

class ConsoleWeiboEngine {
 private:
  static ConsoleWeiboEngine* console_weibo_engine_;
  static ConsoleWeiboManager* console_weibo_manager_;
  ConsoleWeiboEngine() {
  }
  virtual ~ConsoleWeiboEngine() {
  }

 public:
  static ConsoleWeiboEngine* GetConsoleWeiboEngine() {
    if (console_weibo_engine_ == NULL)
      console_weibo_engine_ = new ConsoleWeiboEngine();
    return console_weibo_engine_;
  }

  static ConsoleWeiboManager* GetConsoleWeiboManager() {
    if (console_weibo_manager_ == NULL)
      console_weibo_manager_ = new ConsoleWeiboManager();
    return console_weibo_manager_;
  }

  static void FreeConsoleWeiboEngine(){
    delete console_weibo_engine_;
    console_weibo_engine_ = NULL;
  }

  static void FreeConsoleWeiboManager() {
    delete console_weibo_manager_;
    console_weibo_manager_ = NULL;
  }
};

}

#endif
