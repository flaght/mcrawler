//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.16 Author: kerry

#include "logic/auto_crawler_infos.h"
#include "console_stock_manager.h"
#include "console_kafka.h"


#define HX_DAY_HEAT   588

namespace console_logic {

class HexunTaskManager {
 public:
  HexunTaskManager();
  virtual ~HexunTaskManager();
 public:
  void CreateTask(base_logic::TaskInfo& task);
 private:
  void CreateAllStockDayHeat(base_logic::TaskInfo& task);

 private:
  ConsoleStockManager*     stock_manager_;
  console_logic::ConsoleKafka   kafka_producer_;
};

}
