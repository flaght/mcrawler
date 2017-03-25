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

XueqiuTaskManager::XueqiuTaskManager(console_logic::ConsoleKafka* producer) {
  //kafka_producer_ = producer;
  stock_manager_ = ConsoleStockEngine::GetConsoleStockManager();
}

XueqiuTaskManager::XueqiuTaskManager() {
  stock_manager_ = ConsoleStockEngine::GetConsoleStockManager();
}

XueqiuTaskManager::~XueqiuTaskManager() {

}

void XueqiuTaskManager::CreateTask(const console_logic::KafkaInfo& kafka, base_logic::TaskInfo& task) {
  int64 task_id = task.id();
  switch (task_id) {
    case SB_CN_SM_HEAT_HOUR_RANK: {
      CreateCNSMHourRank(kafka, task);
      break;
    }
    case SB_CN_SM_HEAT_DAY_RANK: {
      CreateCNSMDayRank(kafka, task);
      break;
    }
    case SB_CN_SM_STOCK_HEAT: {
      CreateCNSMStockHeat(kafka,task);
      break;
    }
    case SB_CN_SM_STOCK_DISCUSS: {
      CreateCNSMStockDiscuss(kafka, task);
      break;
    }

    case SB_USER_DISCUSS: {
      CreateUserDiscuss(kafka, task);
      break;
    }

    case SB_USER_MEMBERS: {
      CreateUserMembers(kafka, task);
      break;
    }
    case SB_USER_FOLLOWERS: {
      CreateUserFollowers(kafka, task);
      break;
    }
    default:
      break;
  }
}

void XueqiuTaskManager::CreateUser(const console_logic::KafkaInfo& kafka,const std::string& path,
                                   const base_logic::TaskInfo& task) {
  std::string s_fle_name = path;
  std::string content;
  int error_code;
  std::string error_str;
  file::FilePath file_name(s_fle_name);
  std::string symbol = "{%d}";
  bool r = file::ReadFileToString(file_name, &content);
  base_logic::ValueSerializer* serializer = base_logic::ValueSerializer::Create(
      base_logic::IMPL_JSON);
  base_logic::Value* value = serializer->Deserialize(&content, &error_code,
                                                     &error_str);
  if (value == NULL)
    return;
  base::ConnAddr conn(kafka.svc_id(),kafka.host(),0,"","",kafka.kafka_name());
  console_logic::ConsoleKafka* kafka_producer = new console_logic::ConsoleKafka(conn);
  base_logic::DictionaryValue* dict_value =
      (base_logic::DictionaryValue*) (value);
  base_logic::DictionaryValue::key_iterator it = dict_value->begin_keys();
  for (; it != dict_value->end_keys(); ++it) {
    std::string uid = base::BasicUtil::StringConversions::WideToASCII((*it));
    int64 max_page = 0;
    base_logic::DictionaryValue* value_t = NULL;
    r = dict_value->GetDictionary((*it), &value_t);
    if (!r)
      continue;
    r = value_t->GetBigInteger(L"max_page", &max_page);
    if (!r)
      continue;

    int64 index = 1;
    while (index < max_page) {
      std::string stock_url = task.url();
      stock_url = logic::SomeUtils::StringReplaceUnit(
          stock_url, symbol, base::BasicUtil::StringUtil::Int64ToString(index));
      stock_url = logic::SomeUtils::StringReplaceUnit(stock_url, symbol, uid);
      LOG_MSG2("%s", stock_url.c_str());
      kafka_producer->AddTaskInfo(task, task.base_polling_time(), stock_url);
      index++;
    }
  }LOG_DEBUG2("size %d",dict_value->size());
  if (kafka_producer) {delete kafka_producer; kafka_producer = NULL;}
}

void XueqiuTaskManager::CreateUserMembers(const console_logic::KafkaInfo& kafka, const base_logic::TaskInfo& task) {
  std::string s_fle_name = "./member.txt";
  CreateUser(kafka, s_fle_name, task);
}


void XueqiuTaskManager::CreateUserFollowers(const console_logic::KafkaInfo& kafka, const base_logic::TaskInfo& task) {
  std::string s_fle_name = "./follwer.txt";
  CreateUser(kafka,s_fle_name, task);
  //CreateUserDiscuss(task);
}

void XueqiuTaskManager::CreateUserMembersMax(const console_logic::KafkaInfo& kafka, const base_logic::TaskInfo& task) {
  CreateUserDiscuss(kafka,task);
}

void XueqiuTaskManager::CreateUserDiscuss(const console_logic::KafkaInfo& kafka, const base_logic::TaskInfo& task) {
  std::string symbol = "{%d}";
  //读取文件
  std::string s_fle_name = "./user_discus_max.txt";
  std::string content;
  int error_code;
  std::string error_str;
  file::FilePath file_name(s_fle_name);
  bool r = file::ReadFileToString(file_name, &content);
  base_logic::ValueSerializer* serializer = base_logic::ValueSerializer::Create(
      base_logic::IMPL_JSON);
  base_logic::Value* value = serializer->Deserialize(&content, &error_code,
                                                     &error_str);
  if (value == NULL)
    return;

  base::ConnAddr conn(kafka.svc_id(),kafka.host(),0,"","","",kafka.kafka_name());
  console_logic::ConsoleKafka* kafka_producer = new console_logic::ConsoleKafka(conn);
  base_logic::DictionaryValue* dict_value =
      (base_logic::DictionaryValue*) (value);
  base_logic::DictionaryValue::key_iterator it = dict_value->begin_keys();
  for (; it != dict_value->end_keys(); ++it) {
    std::string uid = base::BasicUtil::StringConversions::WideToASCII((*it));
    //LOG_DEBUG2("uid %s", uid.c_str());
    std::string stock_url = task.url();
    stock_url = logic::SomeUtils::StringReplaceUnit(stock_url, symbol, uid);
    stock_url = logic::SomeUtils::StringReplaceUnit(stock_url, symbol,
                                                    "10000");
    LOG_MSG2("%s", stock_url.c_str());
    //kafka_producer->AddTaskInfo(task, task.base_polling_time(), stock_url);
  }LOG_DEBUG2("size %d",dict_value->size());
  if (kafka_producer) {delete kafka_producer; kafka_producer = NULL;}
}

void XueqiuTaskManager::CreateCNSMStockDiscuss(
    const console_logic::KafkaInfo& kafka, const base_logic::TaskInfo& task) {
  // https://xueqiu.com/statuses/search.json?count={%d}&comment=0&symbol={%tstcode}&hl=0&source=user&sort=time&page={%d}
  std::list<console_logic::StockInfo> list;

  std::string count_symbol = "{%d}";
  std::string stock_symbol = "{%tstcode}";
  std::string page_symbol = "{%d}";
  int32 max_page = 100;
  stock_manager_->Swap(list); 
  base::ConnAddr conn(kafka.svc_id(),kafka.host(),0,"","","",kafka.kafka_name());
  console_logic::ConsoleKafka* kafka_producer = new console_logic::ConsoleKafka(conn);
  while (list.size() > 0) {
    console_logic::StockInfo stock = list.front();
    base_logic::TaskInfo btask;
    list.pop_front();
    std::string stock_url = task.url();
    stock_url = logic::SomeUtils::StringReplaceUnit(stock_url, count_symbol,
                                                    "20");
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
      kafka_producer->AddTaskInfo(task, task.base_polling_time(), i_url);

    }

  }
  if (kafka_producer) {delete kafka_producer; kafka_producer = NULL;}

}

void XueqiuTaskManager::CreateCNSMStockHeat(const console_logic::KafkaInfo& kafka, const base_logic::TaskInfo& task) {
  std::list<console_logic::StockInfo> list;
  std::string tstock_symbol = "{%tstcode}";
  stock_manager_->Swap(list);
  base::ConnAddr conn(kafka.svc_id(),kafka.host(),0,"","","",kafka.kafka_name());
  console_logic::ConsoleKafka* kafka_producer = new console_logic::ConsoleKafka(conn);
  while (list.size() > 0) {
    console_logic::StockInfo stock = list.front();
    list.pop_front();
    std::string stock_url = task.url();
    stock_url = logic::SomeUtils::StringReplace(stock_url, tstock_symbol,
                                                stock.symbol_ext());

    LOG_MSG2("%s", stock_url.c_str());
    kafka_producer->AddTaskInfo(task, task.base_polling_time(), stock_url);
  }
  if (kafka_producer) {delete kafka_producer; kafka_producer = NULL;}
}

void XueqiuTaskManager::CreateCNSMHourRank(const console_logic::KafkaInfo& kafka, const base_logic::TaskInfo& task) {
  CreateSMRank(kafka,"12", task);
}

void XueqiuTaskManager::CreateCNSMDayRank(const console_logic::KafkaInfo& kafka, const base_logic::TaskInfo& task) {
  CreateSMRank(kafka,"22", task);
}

void XueqiuTaskManager::CreateSMRank(const console_logic::KafkaInfo& kafka, const std::string& replace_str,
                                     const base_logic::TaskInfo& task) {
  base_logic::TaskInfo btask;
  std::string symbol = "{%d}";
  std::string s_url = task.url();
  s_url = logic::SomeUtils::StringReplace(s_url, symbol, replace_str); 
  base::ConnAddr conn(kafka.svc_id(),kafka.host(),0,"","","",kafka.kafka_name());
  console_logic::ConsoleKafka* kafka_producer = new console_logic::ConsoleKafka(conn);
  kafka_producer->AddTaskInfo(task, task.base_polling_time(), s_url);
  if (kafka_producer) {delete kafka_producer; kafka_producer = NULL;}
}

}
