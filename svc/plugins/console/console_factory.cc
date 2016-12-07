//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016年8月14日 Author: kerry

#include "console_factory.h"
#include "basic/template.h"
#include "logic/logic_comm.h"
#include "basic/radom_in.h"

namespace console_logic {

ConsoleFactory* ConsoleFactory::instance_ = NULL;

ConsoleFactory*
ConsoleFactory::GetInstance() {
  if (instance_ == NULL)
    instance_ = new ConsoleFactory();
  return instance_;
}

void ConsoleFactory::FreeInstance(){
  if (instance_ != NULL){
    delete instance_;
    instance_ = NULL;
  }
}
ConsoleFactory::ConsoleFactory() {
  Init();
  InitThreadrw(&lock_);
  base::SysRadom::GetInstance();
}

ConsoleFactory::~ConsoleFactory() {
  console_logic::ConsoleStockEngine::FreeConsoleStockManager();
  if (hexun_task_mgr_) {
    delete hexun_task_mgr_;
    hexun_task_mgr_ = NULL;
  }
  if (xueqiu_task_mgr_) {
    delete xueqiu_task_mgr_;
    xueqiu_task_mgr_ = NULL;
  }
  if (console_db_) {
    delete console_db_;
    console_db_ = NULL;
  }
  if (console_cache_){
    delete console_cache_;
    console_cache_ = NULL;
  }

  if (kafka_producer_) {
    delete kafka_producer_;
    kafka_producer_ = NULL;
  }
  DeinitThreadrw(lock_);
}

void ConsoleFactory::Init() {
  stock_mgr_ = console_logic::ConsoleStockEngine::GetConsoleStockManager();
  console_cache_ = new ConsoleCache();
}

void ConsoleFactory::InitParam(config::FileConfig* config) {
  console_db_ = new console_logic::ConsoleDB(config);
  stock_mgr_->Init(console_db_);
  TimeFetchTask();
  console_db_->FetchBatchRuleTask(&console_cache_->task_idle_map_);
  console_db_->FetchBatchCountTask(&console_cache_->task_idle_map_);
  kafka_producer_ = new ConsoleKafka(config);
  hexun_task_mgr_ = new console_logic::HexunTaskManager(kafka_producer_);
  xueqiu_task_mgr_ = new console_logic::XueqiuTaskManager(kafka_producer_);

}

void ConsoleFactory::Dest() {
  if (console_db_) {
    delete console_db_;
    console_db_ = NULL;
  }
}

void ConsoleFactory::TimeFetchTask() {
  std::list<base_logic::TaskInfo> list;
  console_db_->FetchBatchRuleTask(&list);
  base_logic::WLockGd lk(lock_);
  if(list.size() > 0) {
    base_logic::TaskInfo info = list.front();
    list.pop_front();
    console_cache_->task_idle_map_[info.id()] = info;
  }
}


void ConsoleFactory::DistributionTask() {
  time_t current_time = time(NULL);
  base_logic::RLockGd lk(lock_);
  if (console_cache_->task_idle_map_.size() <= 0) {
    LOG_MSG2("distrubute task current_time=%d console_cache_->task_idle_map_.size=%d",
               (int)current_time, console_cache_->task_idle_map_.size());
    return;
  }

  int32 count = console_cache_->task_idle_map_.size();
  int32 index = 0;

  TASKINFO_MAP::iterator it = console_cache_->task_idle_map_.begin();
  for (; it != console_cache_->task_idle_map_.end(), index < count;
      it++, index++) {
    base_logic::TaskInfo& info = it->second;
    if (info.is_finish()==0)
      continue;
    LOG_MSG2("id %lld current %lld last_time %lld polling_time %lld state %d",
        info.id(), current_time, info.last_task_time(),
        info.polling_time(), info.state());
    if (info.last_task_time() + info.polling_time() < current_time) {
      info.release_isfinish();
      info.update_time(0,base::SysRadom::GetInstance()->GetRandomID());
      switch (info.attrid()) {
        case HEXUN_PLATFORM_ID: {
          hexun_task_mgr_->CreateTask(info);
          break;
        }
        case XUEQIU_PLATFORM_ID: {
          xueqiu_task_mgr_->CreateTask(info);
          break;
        }
        default:
          break;
      }
    }
  }
}

void ConsoleFactory::Test() {
  /*
  std::map<int64,base_logic::TaskInfo> lst;
  console_db_->FetchBatchRuleTask(&list);
  //LOG_DEBUG2("list size %lld", list.size());
  // stock_mgr_->Test();

  while (list.size() > 0) {
    base_logic::TaskInfo task = list.front();
    list.pop_front();
    if (task.attrid() == 60008)
      hexun_task_mgr_->CreateTask(task);
  }
  */

}

}
