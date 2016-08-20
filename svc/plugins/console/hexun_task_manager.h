//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.16 Author: kerry

#include <map>
#include "logic/auto_crawler_infos.h"
#include "logic/mcontainer.h"
#include "console_stock_manager.h"
#include "console_kafka.h"

#define HX_DAY_HEAT   588


namespace console_logic {

class HexunCache {
 public:
  //base_logic::AutoMVector<base_logic::TaskInfo> all_stock_day_heat_task_;
};

class HexunTaskManager {
 public:
  HexunTaskManager();
  virtual ~HexunTaskManager();
 public:
  void CreateTask(base_logic::TaskInfo& task);
 private:
  void CreateAllStockDayHeat(const base_logic::TaskInfo& task);

 public:
  void TempAllStockDayHeat();

 private:
  ConsoleStockManager* stock_manager_;
  console_logic::ConsoleKafka kafka_producer_;
  HexunCache* cache_;
  struct threadrw_t*                     lock_;
};
}
