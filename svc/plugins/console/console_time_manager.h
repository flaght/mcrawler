//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//  Created on: 2016年8月18日 Author: kerry

#ifndef CONSOLE_TIME_MANAGER_H__
#define CONSOLE_TIME_MANAGER_H__

#include "console/console_factory.h"

#define TIME_DISTRIBUTION_TASK       10000
#define TIME_FETCH_TASK              10001
#define TIME_UPDATE_STOCK            10002

namespace console_logic {

class ConsoleTimeManager {
 public:
  ConsoleTimeManager();
  virtual ~ConsoleTimeManager();
 public:
  void ConsoleTimeEvent(int opcode, int time);
 private:
  console_logic::ConsoleFactory*     factory_;
};
}
#endif
