//  Copyright (c) 2015-2015 The restful Authors. All rights reserved.
//  Created on: 2015/11/24 Author: jiaoyongqing

#include "tools/db_comm.h"
#include <sstream>

namespace tools_sql {
  void DbSql::Init(std::list<base::ConnAddr>& addrlist) {
    base_db::MysqlDBPool::Init(addrlist);
  }

  void DbSql::Dest() {
    base_db::MysqlDBPool::Dest();
  }

  base_storage::DBStorageEngine* DbSql::GetEntine() {
    base_db::AutoMysqlCommEngine auto_engine;
    base_storage::DBStorageEngine* engine  = NULL;

    engine = auto_engine.GetDBEngine();
    if (engine == NULL) {
      LOG_ERROR("GetConnection Error");
      exit(0);
    }
    return engine;
  }
}  //  namespace tools_sql
