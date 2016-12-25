//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//   Created on: 2016.1.5 Author: kerry

#include "login/login_db.h"
#include <mysql.h>
#include <string>
#include "logic/logic_unit.h"
#include "logic/auto_crawler_infos.h"
#include "login_schduler_engine.h"

namespace login_logic {

LoginDB::LoginDB(config::FileConfig* config) {
  mysql_engine_ = base_logic::DataEngine::Create(MYSQL_TYPE);
  mysql_engine_->InitParam(config->mysql_db_list_);
  //mysql_engine_.reset(base_logic::DataControllerEngine::Create(MYSQL_TYPE));
}

LoginDB::~LoginDB() {
  if (mysql_engine_) {
    delete mysql_engine_;
    mysql_engine_ = NULL;
  }
}

bool LoginDB::GetCookie(std::list<base_logic::LoginCookie>* cookie_list,
                        const int64 id, const int64 from, const int64 count,
                        int64& plat_update_time) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());
  std::string sql;
  sql = "call proc_GetCookieV4("
      + base::BasicUtil::StringUtil::Int64ToString(id) + ","
      + base::BasicUtil::StringUtil::Int64ToString(count) + ","
      + base::BasicUtil::StringUtil::Int64ToString(plat_update_time) + ");";

  base_logic::ListValue* listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->ReadData(0, (base_logic::Value*) (dict.get()),
                              CallBackGetCookies);
  if (!r)
    return r;

  dict->GetList(L"resultvalue", &listvalue);
  LOG_MSG2("listvalue->GetSize() %d", listvalue->GetSize());
  while (listvalue->GetSize()) {
    base_logic::LoginCookie login_cookie;
    base_logic::Value* result_value;
    listvalue->Remove(0, &result_value);
    base_logic::DictionaryValue* dict_result_value =
        (base_logic::DictionaryValue*) (result_value);

    login_cookie.ValueSerialization(dict_result_value);
    login_cookie.set_is_read(false);
    cookie_list->push_back(login_cookie);
    delete dict_result_value;
    dict_result_value = NULL;
  }
  return true;
}

bool LoginDB::GetCookies(std::list<base_logic::LoginCookie>* cookies_list) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());
  std::string sql;
  sql = "call proc_GetCookiesV5()";

  base_logic::ListValue* listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->ReadData(0, (base_logic::Value*) (dict.get()),
                              CallBackGetCookies);
  if (!r)
    return r;

  dict->GetList(L"resultvalue", &listvalue);
  while (listvalue->GetSize()) {
    base_logic::LoginCookie login_cookie;
    base_logic::Value* result_value;
    listvalue->Remove(0, &result_value);
    base_logic::DictionaryValue* dict_result_value =
        (base_logic::DictionaryValue*) (result_value);

    login_cookie.ValueSerialization(dict_result_value);
    login_cookie.update_send_time(0);
    cookies_list->push_back(login_cookie);
    delete dict_result_value;
    dict_result_value = NULL;
  }
  return true;
}

void LoginDB::CallBackGetCookie(void* param, base_logic::Value* value) {
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
        info_value->SetBigInteger(L"cookie_attr_id", atoll(rows[0]));
      if (rows[1] != NULL)
        info_value->SetString(L"cookie_body", rows[1]);

      if (rows[2] != NULL)
        info_value->SetString(L"username", rows[2]);

      if (rows[3] != NULL)
        info_value->SetString(L"passwd", rows[3]);

      /*
       if (rows[2] != NULL)
       info_value->SetString(L"last_time", rows[2]);
       */
      list->Append((base_logic::Value*) (info_value));
    }
  }
  dict->Set(L"resultvalue", (base_logic::Value*) (list));
}

void LoginDB::CallBackGetCookies(void* param, base_logic::Value* value) {
  base_logic::DictionaryValue* dict = (base_logic::DictionaryValue*) (value);
  base_logic::ListValue* list = new base_logic::ListValue();
  base_storage::DBStorageEngine* engine =
      (base_storage::DBStorageEngine*) (param);
  MYSQL_ROW rows;
  int32 num = engine->RecordCount();
  int64 attr_id;
  LoginSchdulerManager* schduler_manager =
      LoginSchdulerEngine::GetLoginSchdulerManager();
  if (num > 0) {
    while (rows = (*(MYSQL_ROW*) (engine->FetchRows())->proc)) {
      base_logic::DictionaryValue* info_value =
          new base_logic::DictionaryValue();
      if (rows[0] != NULL)
        info_value->SetBigInteger(L"cookie_id", atoll(rows[0]));
      if (rows[1] != NULL) {
        attr_id = atoll(rows[1]);
        info_value->SetBigInteger(L"cookie_attr_id", attr_id);
      }
      if (rows[2] != NULL) {
        int64 last_time = atoll(rows[2]);
        info_value->SetBigInteger(L"last_time", last_time);
        int64& last_update_time = schduler_manager
            ->GetDatabaseUpdateTimeByPlatId(attr_id);
        if (last_time > last_update_time)
          last_update_time = last_time;
      }
      if (rows[3] != NULL)
        info_value->SetString(L"cookie_body", rows[3]);

      if (rows[4] != NULL)
        info_value->SetString(L"username", rows[4]);

      if (rows[5] != NULL)
        info_value->SetString(L"passwd", rows[5]);

      if (rows[6] != NULL)
        info_value->SetInteger(L"rule", atol(rows[6]));

      list->Append((base_logic::Value*) (info_value));
    }
  }
  dict->Set(L"resultvalue", (base_logic::Value*) (list));
}

}  // namespace login_logic
