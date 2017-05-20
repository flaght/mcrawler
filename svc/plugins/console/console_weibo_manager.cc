//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#include "console/console_weibo_manager.h"
#include "logic/logic_comm.h"

namespace console_logic {

ConsoleWeiboManager* ConsoleWeiboEngine::console_weibo_manager_ = NULL;
ConsoleWeiboEngine* ConsoleWeiboEngine::console_weibo_engine_ = NULL;

ConsoleWeiboManager::ConsoleWeiboManager()
    : console_db_(NULL) {
  weibo_cache_ = new ConsoleWeiboCache();
  Init();
}

void ConsoleWeiboManager::Init() {
  InitThreadrw(&lock_);
}

ConsoleWeiboManager::~ConsoleWeiboManager() {
  DeinitThreadrw(lock_);
  if (weibo_cache_) {
    delete weibo_cache_;
    weibo_cache_ = NULL;
  }
}

void ConsoleWeiboManager::Init(console_logic::ConsoleDB* console_db) {
  console_db_ = console_db;
  console_db_->FetchWeiboInfo(weibo_cache_->weibo_map_);
}

void ConsoleWeiboManager::UpdateWeibo(){
  base_logic::RLockGd lk(lock_);
  console_db_->FetchWeiboInfo(weibo_cache_->weibo_map_);
  LOG_MSG2("stock size %d", weibo_cache_->weibo_map_.size());
}

void ConsoleWeiboManager::Test() {
  //LOG_DEBUG2("weibo_map_ %lld", weibo_cache_->weibo_map_.size());
}

void ConsoleWeiboManager::Swap(std::list<console_logic::WeiboInfo>& list) {
  base_logic::RLockGd lk(lock_);
  for (WEIBOINFO_MAP::iterator it = weibo_cache_->weibo_map_.begin();
      it != weibo_cache_->weibo_map_.end(); it++) {
    list.push_back(it->second);
  }
}


}
