//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.16 Author: kerry

#include <map>
#include "console_stock_manager.h"
#include "console_kafka.h"

#define SB_CN_SM_HEAT_HOUR_RANK  595 //https://xueqiu.com/stock/rank.json?size=0&_type=12&type=12
#define SB_CN_SM_HEAT_DAY_RANK   596 //https://xueqiu.com/stock/rank.json?size=0&_type=12&type=22
#define SB_CN_SM_STOCK_HEAT      597 //https://xueqiu.com/recommend/pofriends.json?type=1&code=SH600172&start=0&count=0
#define SB_CN_SM_STOCK_DISCUSS   598 //https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SZ000625&hl=0&source=user&sort=time&page=1&_=1475722708502
namespace console_logic {

class XueqiuTaskManager {
 public:
  XueqiuTaskManager();
  virtual ~XueqiuTaskManager();
 public:
  void CreateTask(base_logic::TaskInfo& task);
 private:
  void CreateCNSMStockHeat(const base_logic::TaskInfo& task);
  void CreateCNSMHourRank(const base_logic::TaskInfo& task);
  void CreateCNSMDayRank(const base_logic::TaskInfo& task);
  void CreateCNSMStockDiscuss(const base_logic::TaskInfo& task);
 private:
  void CreateSMRank(const std::string& replace_str,const base_logic::TaskInfo& task);
 private:
  ConsoleStockManager* stock_manager_;
  console_logic::ConsoleKafka kafka_producer_;
};
}
