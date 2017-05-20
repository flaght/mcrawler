//  Copyright (c) 2016-2016 The KID Authors. All rights reserved.
//  Created on: 2016年8月14日 Author: kerry
#ifndef KID_CONSOLE_FACTORY_H__
#define KID_CONSOLE_FACTORY_H__

#include "config/config.h"
#include "console_db.h"
#include "console_kafka.h"
#include "console_stock_manager.h"
#include "console_weibo_manager.h"
#include "hexun_task_manager.h"
#include "xueqiu_task_manager.h"
#include "sina_task_manager.h"

typedef std::map<int64, base_logic::TaskInfo> TASKINFO_MAP;
//存储各个控制服务器kafka信息
typedef std::map<int32, console_logic::ConsoleKafka*> CONSOLE_KAFKA_MAP;

enum PLTFORM {
  HEXUN_PLATFORM_ID =  60008,
  XUEQIU_PLATFORM_ID = 60006,
  SINA_PLATFORM_ID = 60009
};

namespace console_logic {
class ConsoleCache {
 public:
  TASKINFO_MAP task_idle_map_;
  //SVC_MAP      svc_map_;
  CONSOLE_KAFKA_MAP  console_kafka_map_;
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

  void SetKafkaInfo(console_logic::KafkaInfo& kafka);
  	
  void ClearKafkaInfo();
 // bool GetKafkaInfo(const int32 svc_id, console_logic::KafkaInfo& kafka);
  console_logic::ConsoleKafka* GetKafkaInfo(const int32 svc_id);
  void DistributionTask();

  void TimeFetchTask();

  void UpdateStock();


 private:
  ConsoleCache*     console_cache_;
  struct threadrw_t*                     lock_;
  console_logic::ConsoleStockManager*  stock_mgr_;
  console_logic::ConsoleWeiboManager*  weibo_mgr_;
  console_logic::ConsoleDB* console_db_;
  console_logic::ConsoleKafka*  kafka_producer_;
  console_logic::HexunTaskManager*  hexun_task_mgr_;
  console_logic::XueqiuTaskManager*  xueqiu_task_mgr_;
  console_logic::SinaTaskManager* sina_task_mgr_;
};
}
#endif
