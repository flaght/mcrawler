//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.6.13 Author: kerry

#ifndef KID_CONSOL_DB_H__
#define KID_CONSOL_DB_H__

#include "console/console_infos.h"
#include "logic/auto_crawler_infos.h"
#include "storage/data_engine.h"
#include "basic/scoped_ptr.h"
#include <map>


namespace console_logic {

class ConsoleDB {
 public:
  ConsoleDB(config::FileConfig* config);
  virtual ~ConsoleDB();
 public:
  bool FetchBatchRuleTask(std::map<int64,base_logic::TaskInfo>* map,
                          const bool is_new = false);

  bool FetchBatchCountTask(std::map<int64,base_logic::TaskInfo>* map,
                           const bool is_new = false);


  bool FetchBatchRuleTask(std::list<base_logic::TaskInfo>* list,
                          const bool is_new = false);


  bool FectchStCode(std::map<std::string, console_logic::StockInfo>& map);


  bool FetchWeiboInfo(std::map<std::string, console_logic::WeiboInfo>& map);


 private:
  bool FetchBatchListTask(const std::string& sql,
                          std::list<int64,base_logic::TaskInfo>* list);

  template<typename ContainerTrains>
  bool FetchBatchTaskT(const std::string& sql,
                    typename ContainerTrains::container_type* container);

 public:
  static void CallBackFetchBatchRuleTask(void* param, base_logic::Value* value);

  static void CallFectchStCode(void* param, base_logic::Value* value);
  	
  static void CallFetchWeiboInfo(void* param, base_logic::Value* value);

 
 private:
  base_logic::DataEngine* mysql_engine_;
};
}

#endif  /* CONSOL_DB_H_ */
