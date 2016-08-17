//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#include "hexun_task_manager.h"
#include "console_stock_manager.h"
#include "logic/logic_unit.h"
#include "logic/logic_comm.h"
#include "logic/time.h"

namespace console_logic{

HexunTaskManager::HexunTaskManager(){
  stock_manager_ = ConsoleStockEngine::GetConsoleStockManager();
}

HexunTaskManager::~HexunTaskManager() {

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

void HexunTaskManager::CreateAllStockDayHeat(base_logic::TaskInfo& task) {

  //http://focus.stock.hexun.com/service/init_xml.jsp?scode={%stcode}&date={%Y-%M-%D}
  std::string stcode_symbol = "{%stcode}";
  std::string time_symbol = "{%Y-%M-%D}";
  std::list<console_logic::StockInfo> list;
  std::string url = task.url();
  stock_manager_->Swap(list);
  base::Time time = base::Time::NowFromSystemTime();
  base::Time::Exploded exploded;
  time.LocalExplode(&exploded);
  std::string time_format = base::BasicUtil::StringUtil::Int64ToString(exploded.year)
        + "-" + base::BasicUtil::StringUtil::Int64ToString(exploded.month)
        + "-" + base::BasicUtil::StringUtil::Int64ToString(exploded.day_of_month);
  while(list.size() > 0) {
    console_logic::StockInfo stock = list.front();
    list.pop_front();
    std::string stock_url = url;
    stock_url = logic::SomeUtils::StringReplace(stock_url,stcode_symbol,stock.symbol());
    stock_url = logic::SomeUtils::StringReplace(stock_url,time_symbol,time_format);
    LOG_DEBUG2("%s",stock_url.c_str());
  }
}
}
