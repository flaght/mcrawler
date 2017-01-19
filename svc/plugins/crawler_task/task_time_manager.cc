//  Copyright (c) 2015-2015 The kid Authors. All rights reserved.
//  Created on: 2015年10月12日 Author: kerry

#include "crawler_task/task_time_manager.h"
#include "logic/logic_comm.h"
#include <list>

namespace crawler_task_logic {

TaskTimeManager::TaskTimeManager(
    crawler_task_logic::CrawlerTaskDB *task_db,
    crawler_task_logic::CrawlerTaskKafka *task_kafka) {
  schduler_mgr_ =
      crawler_task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
  task_db_ = task_db;
  task_kafka_ = task_kafka;
}

TaskTimeManager::~TaskTimeManager() {}

void TaskTimeManager::TaskTimeEvent(int opcode, int time) {
  switch (opcode) {
  case TIME_DISTRIBUTION_TASK:
    schduler_mgr_->DistributionTask();
    break;
  case TIME_FECTCH_TASK:
    TimeFetchTask();
    break;
  case TIME_CLEAN_NO_EFFECTIVE:
    schduler_mgr_->CheckIsEffective();
    break;
  case TIME_RECYCLINGTASK:
    schduler_mgr_->RecyclingTask();
    break;
  case TIME_FETCH_TEMP_TASK:
    TimeFechTempTask();
    break;
  case TIME_DISTRBUTION_TEMP_TASK:
    schduler_mgr_->DistributionTempTask();
    break;
  default:
    break;
  }
  // LOG_DEBUG("task time event");
}

void TaskTimeManager::TimeFetchTask() {
  std::list<base_logic::TaskInfo> list;
  task_db_->FetchBatchTask(&list, true);
  schduler_mgr_->FetchBatchTask(&list);
}

void TaskTimeManager::TimeFechTempTask() {
  std::list<base_logic::TaskInfo> list;
  task_kafka_->FectchBatchTempTask(&list);
  task_db_->BatchUpdateTaskInfo(&list);
  schduler_mgr_->FetchBatchTemp(&list);
}

void TaskTimeManager::TimeCheckTask() { schduler_mgr_->RecyclingTask(); }

} // namespace crawler_task_logic
