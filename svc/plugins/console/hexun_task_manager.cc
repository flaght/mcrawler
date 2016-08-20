//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#include "hexun_task_manager.h"
#include "console_stock_manager.h"
#include "logic/logic_unit.h"
#include "logic/logic_comm.h"
#include "logic/time.h"

namespace console_logic {

HexunTaskManager::HexunTaskManager(){
  stock_manager_ = ConsoleStockEngine::GetConsoleStockManager();
  cache_ = new HexunCache();
  InitThreadrw(&lock_);
}

HexunTaskManager::~HexunTaskManager() {
  DeinitThreadrw(lock_);
  if (cache_) {delete cache_; cache_ = NULL;}
}

void HexunTaskManager::CreateTask(base_logic::TaskInfo& task) {
  int64 task_id = task.id();
  switch (task_id) {
    case HX_DAY_HEAT: {
      CreateAllStockDayHeat(task);
      break;
    }
  }
}

void HexunTaskManager::CreateAllStockDayHeat(const base_logic::TaskInfo& task) {

  //http://focus.stock.hexun.com/service/init_xml.jsp?scode={%stcode}&date={%Y-%M-%D}
  std::string stcode_symbol = "{%stcode}";
  std::string time_symbol = "{%Y-%M-%D}";
  std::list<console_logic::StockInfo> list;
  std::string url = task.url();
  stock_manager_->Swap(list);
  base::Time time = base::Time::NowFromSystemTime();
  base::Time::Exploded exploded;
  time.LocalExplode(&exploded);
  std::string time_format = base::BasicUtil::StringUtil::Int64ToString(
      exploded.year) + "-"
      + base::BasicUtil::StringUtil::Int64ToString(exploded.month) + "-"
      + base::BasicUtil::StringUtil::Int64ToString(exploded.day_of_month);
  while (list.size() > 0) {
    console_logic::StockInfo stock = list.front();
    base_logic::TaskInfo btask;
    list.pop_front();
    std::string stock_url = url;
    stock_url = logic::SomeUtils::StringReplace(stock_url, stcode_symbol,
                                                stock.symbol());
    stock_url = logic::SomeUtils::StringReplace(stock_url, time_symbol,
                                                time_format);
    LOG_DEBUG2("%s",stock_url.c_str());
    btask.set_attrid(task.attrid());
    btask.set_base_polling_time(task.base_polling_time());
    btask.set_crawl_num(task.crawl_num());
    btask.set_current_depth(task.cur_depth());
    btask.set_id(task.id());
    btask.set_is_forge(task.is_forge());
    btask.set_is_login(task.is_login());
    btask.set_machine(task.machine());
    btask.set_method(task.method());
    btask.set_storage(task.storage());
    btask.set_type(task.type());
    btask.set_url(stock_url);
    base_logic::RLockGd lk(lock_);
    //cache_->all_stock_day_heat_task_.PushBack(btask);
    //kafka_producer_.AddKafkaTaskInfo(task.id(), task.attrid(), 1, 1,
      //                               method, stock_url);
    kafka_producer_.AddKafkaTaskInfo(task.id(), task.attrid(),1,1,task.method(),
                                   task.machine(),task.storage(),0,0,stock_url);
  }
}
}
