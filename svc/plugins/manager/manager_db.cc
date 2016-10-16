//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月17日 Author: kerry
#include <mysql.h>
#include "manager/manager_db.h"
#include "basic/basic_util.h"

namespace manager_logic {

ManagerDB::ManagerDB(config::FileConfig* config) {
  //mysql_engine_.reset(base_logic::DataControllerEngine::Create(MYSQL_TYPE));
  mysql_engine_ = base_logic::DataEngine::Create(MYSQL_TYPE);
  mysql_engine_->InitParam(config->mysql_db_list_);
}

ManagerDB::~ManagerDB() {
  if (mysql_engine_) {
    delete mysql_engine_;
    mysql_engine_ = NULL;
  }
}

bool ManagerDB::CrawlerManagerLogin(void* data) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());
  base_logic::CrawlerScheduler* scheduler =
      (base_logic::CrawlerScheduler*) (data);
  //call crawler.proc_CrawlerManagerLogin('A0999B04D047','12345678','127.0.0.1',9999);
  std::string sql = "call proc_CrawlerManagerLogin(\'" + scheduler->mac()
      + "\',\'" + scheduler->password() + "\',\'" + scheduler->ip() + "\',"
      + base::BasicUtil::StringUtil::Int64ToString(scheduler->port()) + ");";
  dict->SetString(L"sql", sql);
  r = mysql_engine_->ReadData(0, (base_logic::Value*) (dict.get()),
                              CallBackManagerLogin);
  if (!r)
    return r;
  int32 manager_id = 0;
  r = dict->GetInteger(L"manager_id", &manager_id);
  if (r) {
    scheduler->set_id(manager_id);
  }
  return true;
}

void ManagerDB::CallBackManagerLogin(void* param, base_logic::Value* value) {
  base_logic::DictionaryValue* dict = (base_logic::DictionaryValue*) (value);

  base_storage::DBStorageEngine* engine =
      (base_storage::DBStorageEngine*) (param);
  MYSQL_ROW rows;
  int32 num = engine->RecordCount();
  if (num > 0) {
    while (rows = (*(MYSQL_ROW*) (engine->FetchRows())->proc)) {
      if (rows[0] != NULL)
        dict->SetInteger(L"manager_id", atol(rows[0]));
    }
  }
}
}  // namespace manager_logic

