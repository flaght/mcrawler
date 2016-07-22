//  Copyright (c) 2015-2015 The restful Authors. All rights reserved.
//  Created on: 2015/11/24 Author: jiaoyongqing

#ifndef TRUNK_PLUGINS_TOOLS_DB_COMM_H_
#define TRUNK_PLUGINS_TOOLS_DB_COMM_H_

#include <mysql.h>

#include <list>

#include "config/config.h"
#include "db/base_db_mysql_auto.h"

namespace tools_sql {

class DbSql {
 public:
  DbSql();
  virtual ~DbSql();
 public:
  static void Init(std::list<base::ConnAddr>& addrlist);
  static void Dest();
 public:
  static base_storage::DBStorageEngine* GetEntine();
};

}  //  namespace tools_sql
#endif  //  TRUNK_PLUGINS_TOOLS_DB_COMM_H_
