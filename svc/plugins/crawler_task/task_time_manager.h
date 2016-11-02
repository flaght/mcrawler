//  Copyright (c) 2015-2015 The kid Authors. All rights reserved.
//  Created on: 2015年10月12日 Author: kerry

#ifndef KID_CRAWLER_TASK_TIME_MANAGER_H_
#define KID_CRAWLER_TASK_TIME_MANAGER_H_

#include "crawler_task/task_schduler_engine.h"
#include "crawler_task/crawler_task_db.h"
#include "crawler_task/crawler_task_kafka.h"

#define TIME_DISTRIBUTION_TASK       10000
#define TIME_FECTCH_TASK             10001
#define TIME_CLEAN_NO_EFFECTIVE      10005
#define TIME_RECYCLINGTASK           10006
#define TIME_FETCH_TEMP_TASK         10007
#define TIME_DISTRBUTION_TEMP_TASK   10008

namespace crawler_task_logic {

class TaskTimeManager {
 public:
    explicit TaskTimeManager(crawler_task_logic::CrawlerTaskDB* task_db,
                             crawler_task_logic::CrawlerTaskKafka* task_kafka);
    virtual ~TaskTimeManager();
 public:
    void TaskTimeEvent(int opcode, int time);
 private:
    void TimeFetchTask();

    void TimeCheckTask();

    void TimeFechTempTask();

    void CleanNoEffectCrawler();

 private:
    crawler_task_logic::TaskSchdulerManager*               schduler_mgr_;
    scoped_ptr<crawler_task_logic::CrawlerTaskDB>          task_db_;
    CrawlerTaskKafka*									                     task_kafka_;
};

}  //  namespace crawler_task_logic



#endif /* TASK_TIME_MANAGER_H_ */
