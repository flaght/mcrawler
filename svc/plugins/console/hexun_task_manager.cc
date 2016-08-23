//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#include "hexun_task_manager.h"
#include "console_stock_manager.h"
#include "logic/time.h"
#include "logic/logic_unit.h"
#include "logic/logic_comm.h"
#include "logic/time.h"
#include "basic/radom_in.h"

namespace console_logic {

HexunTaskManager::HexunTaskManager() {
  stock_manager_ = ConsoleStockEngine::GetConsoleStockManager();
  cache_ = new HexunCache();
  InitThreadrw(&lock_);
}

HexunTaskManager::~HexunTaskManager() {
  DeinitThreadrw(lock_);
  if (cache_) {
    delete cache_;
    cache_ = NULL;
  }
}

void HexunTaskManager::CreateTask(base_logic::TaskInfo& task) {
  int64 task_id = task.id();
  switch (task_id) {
    case HX_DAY_ALL_HEAT: {
      CreateAllStockDayHeat(task);
      break;
    }
    case HX_DAY_STOCK_HEAT: {
      CreateSecondaryStockQuarterHeat(task);
      break;
    }
    case HX_SEC_STOCK_HEAT: {
      CreateSecondaryStockDayHeat(task);
      break;
    }
    case HX_SEC_ALL_HEAT: {
      CreateAllStockQuarterHeat(task);
      break;
    }
    default:
      break;
  }
}

void HexunTaskManager::CreateAllStockHeat(const base_logic::TaskInfo& task,
                                          const int32 ago_day) {
  std::string time_symbol = "{%Y-%M-%D}";
  base::Time time = base::Time::NowFromSystemTime();
  base::Time::Exploded exploded;
  base_logic::TaskInfo btask;
  time.LocalExplode(&exploded);
  // 多少天开始计算到现在为止
  for (int32 i = 0; i <= ago_day; i++) {
    std::string s_url = task.url();
    std::string time_format = base::BasicUtil::StringUtil::Int64ToString(
        exploded.year) + "-"
        + base::BasicUtil::StringUtil::Int64ToString(exploded.month) + "-"
        + base::BasicUtil::StringUtil::Int64ToString(exploded.day_of_month - i);

    s_url = logic::SomeUtils::StringReplace(s_url, time_symbol, time_format);
    btask.DeepCopy(task);
    btask.set_url(s_url);
    btask.set_base_polling_time(task.base_polling_time());
    btask.update_time(0, base::SysRadom::GetInstance()->GetRandomID());

    LOG_DEBUG2("%s",btask.url().c_str());
    kafka_producer_.AddKafkaTaskInfo(task.id(), task.attrid(), 1, 1,
                                     task.method(), task.machine(),
                                     task.storage(), 0, 0, btask.polling_time(),
                                     btask.last_task_time(), s_url);
  }
}

void HexunTaskManager::CreateAllStockQuarterHeat(
    const base_logic::TaskInfo& task) {
  CreateAllStockHeat(task, 1);
}

void HexunTaskManager::CreateAllStockDayHeat(const base_logic::TaskInfo& task) {
  CreateAllStockHeat(task, 0);
}

void HexunTaskManager::CreateSecondaryStockDayHeat(
    const base_logic::TaskInfo& task) {
  CreateSecondaryStockHeat(task, 1);

  /*
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

   btask.DeepCopy(task);
   btask.set_url(stock_url);
   btask.set_base_polling_time(task.base_polling_time());
   btask.update_time(0, base::SysRadom::GetInstance()->GetRandomID());
   LOG_DEBUG2("btask polling_time %lld",btask.polling_time());
   //cache_->all_stock_day_heat_task_.PushBack(btask);
   //kafka_producer_.AddKafkaTaskInfo(task.id(), task.attrid(), 1, 1,
   //                               method, stock_url);
   kafka_producer_.AddKafkaTaskInfo(task.id(), task.attrid(), 1, 1,
   task.method(), task.machine(),
   task.storage(), 0, 0, btask.polling_time(),
   btask.last_task_time(), stock_url);
   }*/
}

void HexunTaskManager::CreateSecondaryStockQuarterHeat(
    const base_logic::TaskInfo& task) {
  CreateSecondaryStockHeat(task, 1);
}

void HexunTaskManager::CreateSecondaryStockHeat(
    const base_logic::TaskInfo& task, const int32 ago_day) {
  std::string stcode_symbol = "{%stcode}";
  std::string time_symbol = "{%Y-%M-%D}";
  std::list<console_logic::StockInfo> list;
  stock_manager_->Swap(list);
  base::Time time = base::Time::NowFromSystemTime();
  base::Time::Exploded exploded;
  time.LocalExplode(&exploded);
  // 多少天开始计算到现在为止
  for (int32 i = 0; i <= ago_day; i++) {
    //格式必须为08-08不能8-8
    std::string month_str;
    std::string day_str;
    if (exploded.month < 10)
      month_str = "0";

    month_str += base::BasicUtil::StringUtil::Int64ToString(exploded.month);

    if ((exploded.day_of_month - i) < 10) {
      day_str = "0";
    }
    day_str += base::BasicUtil::StringUtil::Int64ToString(
        exploded.day_of_month - i);

    std::string time_format = base::BasicUtil::StringUtil::Int64ToString(
        exploded.year) + "-"
        + month_str + "-"
        + day_str;
    while (list.size() > 0) {
      std::string url = task.url();
      console_logic::StockInfo stock = list.front();
      base_logic::TaskInfo btask;
      list.pop_front();
      std::string stock_url = url;
      stock_url = logic::SomeUtils::StringReplace(stock_url, stcode_symbol,
                                                  stock.symbol());
      stock_url = logic::SomeUtils::StringReplace(stock_url, time_symbol,
                                                  time_format);
      LOG_DEBUG2("%s",stock_url.c_str());

      btask.DeepCopy(task);
      btask.set_url(stock_url);
      btask.set_base_polling_time(task.base_polling_time());
      btask.update_time(0, base::SysRadom::GetInstance()->GetRandomID());
      LOG_DEBUG2("btask polling_time %lld",btask.polling_time());
      kafka_producer_.AddKafkaTaskInfo(btask.id(), btask.attrid(), 1, 1,
                                       btask.method(), btask.machine(),
                                       btask.storage(), 0, 0,
                                       btask.polling_time(),
                                       btask.last_task_time(), stock_url);
    }
  }
}

}
