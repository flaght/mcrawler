//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#include "console_db.h"
#include "basic/basic_util.h"
#include "logic/logic_unit.h"
#include <mysql.h>

namespace console_logic {

class TaskContainerMap {
 public:
  typedef std::map<int64,base_logic::TaskInfo> container_type;
  static inline void c_func(container_type* container,
                            base_logic::TaskInfo& task) {
    (*container)[task.id()] = task;
  }
};

class TaskContainerList {
 public:
  typedef std::list<base_logic::TaskInfo> container_type;
  static inline void c_func(container_type* container,
                            base_logic::TaskInfo& task) {
    (*container).push_back(task);
  }
};

ConsoleDB::ConsoleDB(config::FileConfig* config) {
  mysql_engine_ = base_logic::DataEngine::Create(MYSQL_TYPE);
  mysql_engine_->InitParam(config->mysql_db_list_);
}

ConsoleDB::~ConsoleDB(void) {
  if (mysql_engine_) {
    delete mysql_engine_;
    mysql_engine_ = NULL;
  }
}


bool ConsoleDB::FetchWeiboInfo(std::map<int32,console_logic::WeiboInfo>& map) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());
  
  std::string sql;
  sql = "call proc_GetWeiboIndex()";
  base_logic::ListValue* listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->ReadData(0, (base_logic::DictionaryValue*)(dict.get()),
                             CallFetchWeiboInfo);
  if (!r)
    return false;
  dict->GetList(L"resultvalue", & listvalue);
  while (listvalue->GetSize()) {
    console_logic::WeiboInfo wb;
    base_logic::Value* result_value;
    listvalue->Remove(0, &result_value);
    base_logic::DictionaryValue* dict_result_value = 
        (base_logic::DictionaryValue*)(result_value);
    wb.ValueSerialization(dict_result_value);
   map[wb.id()] = wb;
   delete dict_result_value;
   dict_result_value = NULL;
  }
  return true;
}

bool ConsoleDB::FectchStCode(
    std::map<std::string, console_logic::StockInfo>& map) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());

  std::string sql;
  sql = "call proc_GetStcode()";
  base_logic::ListValue* listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->ReadData(0, (base_logic::Value*) (dict.get()),
                              CallFectchStCode);
  if (!r)
    return false;
  dict->GetList(L"resultvalue", &listvalue);
  while (listvalue->GetSize()) {
    console_logic::StockInfo stock;
    base_logic::Value* result_value;
    listvalue->Remove(0, &result_value);
    base_logic::DictionaryValue* dict_result_value =
        (base_logic::DictionaryValue*) (result_value);
    stock.ValueSerialization(dict_result_value);
    map[stock.symbol()] = stock;
    delete dict_result_value;
    dict_result_value = NULL;
  }

  return true;
}

bool ConsoleDB::FetchBatchCountTask(std::map<int64,base_logic::TaskInfo>* map,
                           const bool is_new) {
  std::string sql;
  if (is_new)
    sql = "call proc_FetchNewTask()";
  else
    sql = "call proc_FetchCountTask()";

  return FetchBatchTaskT<TaskContainerMap>(sql,map);
}

bool ConsoleDB::FetchBatchRuleTask(std::map<int64, base_logic::TaskInfo>* map,
                                   const bool is_new) {
  std::string sql;
  if (is_new)
    sql = "call proc_FetchNewTask()";
  else
    sql = "call proc_FetchBatchRuleTask()";

  return FetchBatchTaskT<TaskContainerMap>(sql,map);

}

bool ConsoleDB::FetchBatchRuleTask(std::list<base_logic::TaskInfo>* list,
                                   const bool is_new) {
  std::string sql;
  if (is_new)
    sql = "call proc_FetchBatchNewRuleTask()";
  else
    sql = "call proc_FetchBatchRuleTask()";
  return FetchBatchTaskT<TaskContainerList>(sql,list);
}

template<typename ContainerTrains>
bool ConsoleDB::FetchBatchTaskT(
    const std::string& sql,
    typename ContainerTrains::container_type* container) {
  bool r = false;
  typedef ContainerTrains traits;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());

  base_logic::ListValue* listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->ReadData(0, (base_logic::Value*) (dict.get()),
                              CallBackFetchBatchRuleTask);
  if (!r)
    return false;
  dict->GetList(L"resultvalue", &listvalue);
  while (listvalue->GetSize()) {
    base_logic::TaskInfo task;
    base_logic::Value* result_value;
    listvalue->Remove(0, &result_value);
    base_logic::DictionaryValue* dict_result_value =
        (base_logic::DictionaryValue*) (result_value);
    task.ValueSerialization(dict_result_value);
    task.set_type(MAIN_LASTING_TASK);
    traits::c_func(container,task);
    delete dict_result_value;
    dict_result_value = NULL;
  }

  return true;
}


void ConsoleDB::CallFetchWeiboInfo(void* param, base_logic::Value* value) {
  base_logic::DictionaryValue* dict = (base_logic::DictionaryValue*)(value);
  base_logic::ListValue* list = new base_logic::ListValue();
  base_storage::DBStorageEngine* engine = 
     (base_storage::DBStorageEngine*)(param);
  MYSQL_ROW rows;
  int32 num = engine->RecordCount();
  if (num > 0) {
    while (rows = (*(MYSQL_ROW*) (engine->FetchRows())->proc)) {
      base_logic::DictionaryValue* info_value =
          new base_logic::DictionaryValue();
      if (rows[0] != NULL)
        info_value->SetInteger(L"id", atoll(rows[0]));
      if (rows[1] != NULL)
        info_value->SetString(L"weibo_id", rows[1]);
      if (rows[2] != NULL)
        info_value->SetString(L"weibo_index_id", rows[2]);
      if (rows[3] != NULL)
        info_value->SetString(L"weibo_name", rows[3]);

      list->Append((base_logic::Value*)(info_value));
    }
  }
  dict->Set(L"resultvalue", (base_logic::Value*) (list));
}


void ConsoleDB::CallFectchStCode(void* param, base_logic::Value* value) {
  base_logic::DictionaryValue* dict = (base_logic::DictionaryValue*) (value);
  base_logic::ListValue* list = new base_logic::ListValue();
  base_storage::DBStorageEngine* engine =
      (base_storage::DBStorageEngine*) (param);
  MYSQL_ROW rows;
  int32 num = engine->RecordCount();
  if (num > 0) {
    while (rows = (*(MYSQL_ROW*) (engine->FetchRows())->proc)) {
      base_logic::DictionaryValue* info_value =
          new base_logic::DictionaryValue();
      if (rows[0] != NULL)
        info_value->SetString(L"symbol", rows[0]);
      if (rows[1] != NULL)
        info_value->SetString(L"sename", rows[1]);
      if (rows[2] != NULL)
        info_value->SetString(L"exchange", rows[2]);

      list->Append((base_logic::Value*) (info_value));
    }
  }
  dict->Set(L"resultvalue", (base_logic::Value*) (list));
}

void ConsoleDB::CallBackFetchBatchRuleTask(void* param,
                                           base_logic::Value* value) {
  base_logic::DictionaryValue* dict = (base_logic::DictionaryValue*) (value);
  base_logic::ListValue* list = new base_logic::ListValue();
  base_storage::DBStorageEngine* engine =
      (base_storage::DBStorageEngine*) (param);
  MYSQL_ROW rows;
  int32 num = engine->RecordCount();
  if (num > 0) {
    while (rows = (*(MYSQL_ROW*) (engine->FetchRows())->proc)) {
      base_logic::DictionaryValue* info_value =
          new base_logic::DictionaryValue();
      if (rows[0] != NULL)
        info_value->SetBigInteger(L"id", atoll(rows[0]));
      if (rows[1] != NULL)
        info_value->SetBigInteger(L"attrid", atoll(rows[1]));
      if (rows[2] != NULL)
        info_value->SetCharInteger(L"depth",
                                   logic::SomeUtils::StringToIntChar(rows[2]));
      if (rows[3] != NULL)
        info_value->SetCharInteger(L"machine",
                                   logic::SomeUtils::StringToIntChar(rows[3]));
      if (rows[4] != NULL)
        info_value->SetCharInteger(L"storage",
                                   logic::SomeUtils::StringToIntChar(rows[4]));
      if (rows[5] != NULL)
        info_value->SetCharInteger(L"islogin",
                                   logic::SomeUtils::StringToIntChar(rows[5]));
      if (rows[6] != NULL)
        info_value->SetCharInteger(L"isforge",
                                   logic::SomeUtils::StringToIntChar(rows[6]));
      if (rows[7] != NULL)
        info_value->SetCharInteger(L"isover",
                                   logic::SomeUtils::StringToIntChar(rows[7]));
      if (rows[8] != NULL)
        info_value->SetCharInteger(L"method",
                                   logic::SomeUtils::StringToIntChar(rows[8]));
      if (rows[9] != NULL)
        info_value->SetBigInteger(L"polling_time", atoll(rows[9]) / 2);

      if (rows[10] != NULL)
        info_value->SetBigInteger(L"isfinish",
                                   atoll(rows[10]));
      if (rows[11] != NULL)
        info_value->SetInteger(L"svc_id", atoi(rows[11]));

      if (rows[12] != NULL)
        info_value->SetString(L"url", rows[12]);
      list->Append((base_logic::Value*) (info_value));
    }
  }
  dict->Set(L"resultvalue", (base_logic::Value*) (list));
}

}

