//  Copyright (c) 2015-2015 The kid Authors. All rights reserved.
//  Created on: 2015年10月12日 Author: kerry

#include "task/task_time_manager.h"
#include <list>

namespace task_logic {

TaskTimeManager::TaskTimeManager(task_logic::TaskDB* task_db) {
    schduler_mgr_ =  task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    task_db_.reset(task_db);
}

TaskTimeManager::~TaskTimeManager() {
}

void TaskTimeManager::TaskTimeEvent(int opcode, int time) {
    switch (opcode) {
      case TIME_DISTRIBUTION_TASK:
        schduler_mgr_->DistributionTask();
        break;
      case TIME_FECTCH_TASK:
        TimeFetchTask();
        break;
      case TIME_DISTRIBUTION_HBASE:
        schduler_mgr_->DistibutionHBase();
        break;
      case TIME_CLEAN_NO_EFFECTIVE:
        schduler_mgr_->CheckIsEffective();
        break;
      case TIME_FECTB_HBASE:
        TimeFetchHBase();
        break;
      case TIME_CLEAN_HBASE:
        CleanHBase();
        break;
      case TIME_RECYCLINGTASK:
        schduler_mgr_->RecyclingTask();
        break;
      default:
        break;
    }
}

void TaskTimeManager::TimeFetchHBase() {
    std::list<base_logic::StorageHBase> hbase_list;
    task_db_->FetchBatchHBase(&hbase_list);
    schduler_mgr_->FetchBatchHbase(&hbase_list);
}

void TaskTimeManager::TimeFetchTask() {
    std::list<base_logic::TaskInfo> list;
    task_db_->FecthBatchTask(&list, true);
    schduler_mgr_->FetchBatchTask(&list);
}

void TaskTimeManager::CleanHBase() {
    std::list<base_logic::StorageHBase> list;
    schduler_mgr_->SwapRemoveHBase(&list);
    if (list.size() > 0) {
        task_db_->UpdateHBaseState(&list);
        list.clear();
    }
}

void TaskTimeManager::TimeCheckTask() {
    schduler_mgr_->RecyclingTask();
}

}  //  namespace task_logic


