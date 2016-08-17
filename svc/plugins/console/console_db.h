//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.6.13 Author: kerry

#ifndef KID_CONSOL_DB_H__
#define KID_CONSOL_DB_H__

#include "console/console_infos.h"
#include "logic/auto_crawler_infos.h"
#include "storage/data_engine.h"
#include "basic/scoped_ptr.h"

namespace console_logic {

class ConsoleDB {
 public:
  ConsoleDB(config::FileConfig* config);
  virtual ~ConsoleDB();
 public:
  bool FetchBatchRuleTask(std::list<base_logic::TaskInfo>* list,
                          const bool is_new = false);

  bool FectchStCode(std::map<std::string, console_logic::StockInfo>& map);

 public:
  static void CallBackFetchBatchRuleTask(void* param, base_logic::Value* value);

  static void CallFectchStCode(void* param, base_logic::Value* value);
 private:
  base_logic::DataEngine* mysql_engine_;
};
}

#endif  /* CONSOL_DB_H_ */
