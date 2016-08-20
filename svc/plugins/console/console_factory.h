//  Copyright (c) 2016-2016 The KID Authors. All rights reserved.
//  Created on: 2016年8月14日 Author: kerry
#ifndef KID_CONSOLE_FACTORY_H__
#define KID_CONSOLE_FACTORY_H__

#include "config/config.h"
#include "console_db.h"
#include "console_stock_manager.h"
#include "hexun_task_manager.h"

typedef std::map<int64, base_logic::TaskInfo> TASKINFO_MAP;

enum PLTFORM {
  HEXUN_PLATFORM_ID =  60008
};

namespace console_logic {
class ConsoleCache {
 public:
  TASKINFO_MAP task_idle_map_;
};

class ConsoleFactory {
 public:
  ConsoleFactory();
  virtual ~ConsoleFactory();
 public:
  void Init();
  void Dest();
 private:
  static ConsoleFactory* instance_;
 public:
  static ConsoleFactory* GetInstance();
  static void FreeInstance();

  void InitParam(config::FileConfig* config);

  void Test();

  void DistributionTask();

  void TimeFetchTask();

 private:
  ConsoleCache*     console_cache_;
  struct threadrw_t*                     lock_;
  console_logic::ConsoleStockManager*  stock_mgr_;
  console_logic::ConsoleDB* console_db_;
  console_logic::HexunTaskManager*  hexun_task_mgr_;
};
}
#endif
