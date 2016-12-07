//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.16 Author: kerry

#include <map>
#include "logic/auto_crawler_infos.h"
#include "logic/mcontainer.h"
#include "console_stock_manager.h"
#include "console_kafka.h"

#define HX_DAY_STOCK_HEAT   588  //http://focus.stock.hexun.com/service/init_xml.jsp?scode={%stcode}&date={%Y-%M-%D}
#define HX_SEC_STOCK_HEAT 589 //http://focus.stock.hexun.com/service/init_xml_min.jsp?scode={%stcode}&date={%Y-%M-%D}
#define HX_DAY_ALL_HEAT   590 //http://focus.stock.hexun.com/service/market_xml.jsp?date={%Y-%M-%D}
#define HX_SEC_ALL_HEAT   591 //http://focus.stock.hexun.com/service/market_xml_min.jsp?date={%Y-%M-%D}

namespace console_logic {

class HexunCache {
 public:
  //base_logic::AutoMVector<base_logic::TaskInfo> all_stock_day_heat_task_;
};

class HexunTaskManager {
 public:
  HexunTaskManager(console_logic::ConsoleKafka* producer);
  virtual ~HexunTaskManager();
 public:
  void CreateTask(base_logic::TaskInfo& task);
 private:
  void CreateAllStockDayHeat(const base_logic::TaskInfo& task);
  void CreateAllStockQuarterHeat(const base_logic::TaskInfo& task);

  void CreateSecondaryStockDayHeat(const base_logic::TaskInfo& task);
  void CreateSecondaryStockQuarterHeat(const base_logic::TaskInfo& task);

 private:
  void CreateAllStockHeat(const base_logic::TaskInfo& task,
                          const int32 ago_day);

  void CreateSecondaryStockHeat(const base_logic::TaskInfo& task,
                                const int32 ago_day);
 public:
  void TempAllStockDayHeat();

 private:
  ConsoleStockManager*             stock_manager_;
  console_logic::ConsoleKafka*     kafka_producer_;
  HexunCache* cache_;
  struct threadrw_t*                     lock_;
};
}
