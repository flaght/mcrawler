//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2017.5.17 Author: kerry
//
#include <map>
#include "console_kafka.h"
#include "console_infos.h"
#include "console_weibo_manager.h"
#define SINA_WEIBO_INDEX_FIVE 602//http://data.weibo.com/index/ajax/realtime1hour?key=1071301040000055205


namespace console_logic {

class SinaTaskManager {
 public:
  SinaTaskManager(console_logic::ConsoleKafka* producer);
  SinaTaskManager();
  virtual ~SinaTaskManager();
 public:
  void CreateTask(base_logic::TaskInfo& task);
  void CreateTask(console_logic::ConsoleKafka* kafka, base_logic::TaskInfo& task);

 private:
  void CreateWeiboIndex1HourReal(console_logic::ConsoleKafka* kafka, const base_logic::TaskInfo& task);//微博指数1小时实时指数请求
  void CreateWeiboIndex24HourReal(const console_logic::ConsoleKafka* kafka, const base_logic::TaskInfo& task);//微博指数24小时实时指数请求
 private:
  console_logic::ConsoleWeiboManager*   weibo_manager_;
};
}
