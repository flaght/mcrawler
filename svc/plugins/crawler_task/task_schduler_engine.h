//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月22日 Author: kerry

#ifndef KID_CRAWLER_TASK_SCHDULER_ENGINE_H_
#define KID_CRAWLER_TASK_SCHDULER_ENGINE_H_

#include <map>
#include <list>
#include "crawler_task/crawler_task_db.h"
#include "crawler_schduler/crawler_schduler_engine.h"
#include "thread/base_thread_handler.h"
#include "thread/base_thread_lock.h"
#include "config/config.h"

#include "logic/auto_crawler_infos.h"

typedef std::map<int64, base_logic::TaskInfo> TASKINFO_MAP;
typedef std::list<base_logic::TaskInfo>  TASKINFO_LIST;


namespace crawler_task_logic {
class TaskSchdulerCache {
 public:
    TASKINFO_MAP          task_idle_map_;
    TASKINFO_MAP          task_exec_map_;
    TASKINFO_LIST         task_temp_list_;
    TASKINFO_MAP          task_temp_map_;
    TASKINFO_MAP          task_check_map_;
    TASKINFO_MAP          task_complete_map_;
};

class TaskSchdulerManager {
 public:
    TaskSchdulerManager();
    virtual ~TaskSchdulerManager();

    void Init(crawler_schduler::SchdulerEngine* crawler_engine);

    void InitDB(crawler_task_logic::CrawlerTaskDB*     task_db);

    void FetchBatchTask(std::list<base_logic::TaskInfo>* list,
            bool is_first = false);

    void FetchBatchTemp(std::list<base_logic::TaskInfo>* list);

 public:
    bool DistributionTask();

    bool DistributionTempTask();

    void RecyclingTask();

    bool AlterTaskState(const int64 task_id, const int8 state);

    bool AlterCrawlNum(const int64 task_id, const int64 num);

    void CheckIsEffective();

    void DumpTask();

 private:
    void Init();

    void Test(void);

 private:
    struct threadrw_t*                     lock_;
    TaskSchdulerCache*                     task_cache_;
    crawler_schduler::SchdulerEngine*      crawler_schduler_engine_;
    int32                                  crawler_count_;
    crawler_task_logic::CrawlerTaskDB*     task_db_;
};

class TaskSchdulerEngine {
 private:
    static TaskSchdulerManager    *schduler_mgr_;
    static TaskSchdulerEngine     *schduler_engine_;

    TaskSchdulerEngine() {}
    virtual ~TaskSchdulerEngine() {}
 public:
    static TaskSchdulerManager* GetTaskSchdulerManager() {
        if (schduler_mgr_ == NULL)
            schduler_mgr_ = new TaskSchdulerManager();
        return schduler_mgr_;
    }

    static TaskSchdulerEngine* GetTaskSchdulerEngine() {
        if (schduler_engine_ == NULL)
            schduler_engine_ = new TaskSchdulerEngine();
        return schduler_engine_;
    }
};
}  // namespace crawler_task_logic

#endif /* TASK_SCHDULER_ENGINE_CC_ */
