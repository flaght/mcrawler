//  Copyright (c) 2015-2015 The kid Authors. All rights reserved.
//  Created on: 2015年10月12日 Author: kerry

#ifndef KID_TASK_TIME_MANAGER_H_
#define KID_TASK_TIME_MANAGER_H_

#include "task/task_schduler_engine.h"
#include "task/task_db.h"


#define TIME_DISTRIBUTION_TASK       10000
#define TIME_FECTCH_TASK             10001
#define TIME_DISTRIBUTION_HBASE      10002
#define TIME_FECTB_HBASE             10003
#define TIME_CLEAN_HBASE             10004
#define TIME_CLEAN_NO_EFFECTIVE      10005
#define TIME_RECYCLINGTASK           10006

namespace task_logic {

class TaskTimeManager {
 public:
    explicit TaskTimeManager(task_logic::TaskDB* task_db);
    virtual ~TaskTimeManager();
 public:
    void TaskTimeEvent(int opcode, int time);
 private:
    void TimeFetchTask();

    void TimeFetchHBase();

    void TimeCheckTask();

    void CleanHBase();

    void CleanNoEffectCrawler();

 private:
    task_logic::TaskSchdulerManager*        schduler_mgr_;
    scoped_ptr<task_logic::TaskDB>          task_db_;
};

}  // namespace task_logic
#endif /* TASK_TIME_MANAGER_H_ */
