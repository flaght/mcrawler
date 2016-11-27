//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.10.2 Author: kerry

#include "xueqiu_task_manager.h"
#include "console_stock_manager.h"
#include "logic/logic_unit.h"
#include "logic/logic_comm.h"
#include "file/file_path.h"
#include "file/file_util.h"
#include "basic/basic_util.h"

namespace console_logic {

XueqiuTaskManager::XueqiuTaskManager() {
  stock_manager_ = ConsoleStockEngine::GetConsoleStockManager();
}

XueqiuTaskManager::~XueqiuTaskManager() {

}

void XueqiuTaskManager::CreateTask(base_logic::TaskInfo& task) {
  int64 task_id = task.id();
  switch (task_id) {
    case SB_CN_SM_HEAT_HOUR_RANK: {
      CreateCNSMHourRank(task);
      break;
    }
    case SB_CN_SM_HEAT_DAY_RANK: {
      CreateCNSMDayRank(task);
      break;
    }
    case SB_CN_SM_STOCK_HEAT: {
      CreateCNSMStockHeat(task);
      break;
    }
    case SB_CN_SM_STOCK_DISCUSS: {
      CreateCNSMStockDiscuss(task);
      break;
    }

    case SB_USER_DISCUSS: {
      CreateUserDiscuss(task);
      break;
    }
    default:
      break;
  }
}

void XueqiuTaskManager::CreateUserDiscuss(const base_logic::TaskInfo& task) {
  std::string symbol = "{%d}";
  //读取文件
  std::string s_fle_name = "./xueqiuinit.txt";
  std::string content;
  int error_code;
  std::string error_str;
  file::FilePath file_name(s_fle_name);
  bool r = file::ReadFileToString(file_name, &content);
  base_logic::ValueSerializer* serializer = base_logic::ValueSerializer::Create(base_logic::IMPL_JSON);
  base_logic::Value* value = serializer->Deserialize(&content, &error_code, &error_str);
  if (value == NULL)
    return;
  base_logic::DictionaryValue* dict_value = (base_logic::DictionaryValue*)(value);
  base_logic::DictionaryValue::key_iterator it = dict_value->begin_keys();
  for (; it != dict_value->end_keys(); ++it){
    std::string uid = base::BasicUtil::StringConversions::WideToASCII((*it));
    //LOG_DEBUG2("uid %s", uid.c_str());
    std::string stock_url = task.url();
    stock_url = logic::SomeUtils::StringReplaceUnit(stock_url, symbol, uid);
    stock_url = logic::SomeUtils::StringReplaceUnit(stock_url, symbol, "100000");
    LOG_MSG2("%s", stock_url.c_str());
    //kafka_producer_.AddTaskInfo(task,task.base_polling_time(),i_url);
  }
}

void XueqiuTaskManager::CreateCNSMStockDiscuss(
    const base_logic::TaskInfo& task) {
  // https://xueqiu.com/statuses/search.json?count={%d}&comment=0&symbol={%tstcode}&hl=0&source=user&sort=time&page={%d}
  std::list<console_logic::StockInfo> list;

  std::string count_symbol = "{%d}";
  std::string stock_symbol = "{%tstcode}";
  std::string page_symbol = "{%d}";
  int32 max_page = 100;
  stock_manager_->Swap(list);
  while (list.size() > 0) {
    console_logic::StockInfo stock = list.front();
    base_logic::TaskInfo btask;
    list.pop_front();
    std::string stock_url = task.url();
    stock_url = logic::SomeUtils::StringReplaceUnit(stock_url, count_symbol, "20");
    stock_url = logic::SomeUtils::StringReplace(stock_url, stock_symbol,
                                                stock.symbol_ext());
    int64 index = 1;
    while (index <= 100) {
      std::string i_url = stock_url;
      i_url = logic::SomeUtils::StringReplaceUnit(
          i_url, page_symbol,
          base::BasicUtil::StringUtil::Int64ToString(index));
      index++;
      LOG_MSG2("%s", i_url.c_str());
      kafka_producer_.AddTaskInfo(task,task.base_polling_time(),i_url);

    }

  }

}

void XueqiuTaskManager::CreateCNSMStockHeat(const base_logic::TaskInfo& task) {
  std::list<console_logic::StockInfo> list;
  std::string tstock_symbol = "{%tstcode}";
  stock_manager_->Swap(list);
  while (list.size() > 0) {
    console_logic::StockInfo stock = list.front();
    list.pop_front();
    std::string stock_url = task.url();
    stock_url = logic::SomeUtils::StringReplace(stock_url, tstock_symbol,
                                                stock.symbol_ext());

    LOG_MSG2("%s", stock_url.c_str());
    kafka_producer_.AddTaskInfo(task,task.base_polling_time(),stock_url);
  }
}

void XueqiuTaskManager::CreateCNSMHourRank(const base_logic::TaskInfo& task) {
  CreateSMRank("12", task);
}

void XueqiuTaskManager::CreateCNSMDayRank(const base_logic::TaskInfo& task) {
  CreateSMRank("22", task);
}

void XueqiuTaskManager::CreateSMRank(const std::string& replace_str,
                                     const base_logic::TaskInfo& task) {
  base_logic::TaskInfo btask;
  std::string symbol = "{%d}";
  std::string s_url = task.url();
  s_url = logic::SomeUtils::StringReplace(s_url, symbol, replace_str);
  kafka_producer_.AddTaskInfo(task,task.base_polling_time(),s_url);
}

}
