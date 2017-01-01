//  Copyright (c) 2015-2015 The kid Authors. All rights reserved.
//  Created on: 2015年10月12日 Author: kerry
#include <list>
#include "console/console_time_manager.h"
#include "logic/logic_unit.h"

namespace console_logic {

ConsoleTimeManager::ConsoleTimeManager() {
  factory_ = console_logic::ConsoleFactory::GetInstance();
}

ConsoleTimeManager::~ConsoleTimeManager() {

}

void ConsoleTimeManager::ConsoleTimeEvent(int opcode, int time) {
  LOG_MSG2("opcode %d  time %d", opcode, time);
  switch (opcode) {
    case TIME_DISTRIBUTION_TASK:
      factory_->DistributionTask();
      break;
    case TIME_FETCH_TASK:
      factory_->TimeFetchTask();
      break;

    case TIME_UPDATE_STOCK:
      factory_->UpdateStock();
      break;
    default:
      break;
  }
}
}
