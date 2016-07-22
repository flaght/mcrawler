//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月22日 Author: kerry

#ifndef KID_TASK_SCHDULER_ENGINE_H_
#define KID_TASK_SCHDULER_ENGINE_H_

#include <map>
#include <list>
#include "crawler_schduler/crawler_schduler_engine.h"
#include "analytical_schduler/analytical_schduler.h"
#include "thread/base_thread_handler.h"
#include "thread/base_thread_lock.h"
#include "config/config.h"

#include "logic/auto_crawler_infos.h"

typedef std::map<int64, base_logic::TaskInfo> TASKINFO_MAP;
typedef std::list<base_logic::TaskInfo>  TASKINFO_LIST;

typedef std::map<int64, base_logic::StorageHBase> HBASE_MAP;
typedef std::list<base_logic::StorageHBase> HBASE_LIST;

namespace task_logic {
class TaskSchdulerCache {
 public:
    TASKINFO_MAP          task_idle_map_;
    TASKINFO_MAP          task_exec_map_;

    HBASE_MAP             hbase_idle_map_;
    HBASE_MAP             hbase_exec_map_;
    HBASE_LIST            hbase_remove_list_;  //  批量修改状态
};

class TaskSchdulerManager {
 public:
    TaskSchdulerManager();
    virtual ~TaskSchdulerManager();

    void Init(crawler_schduler::SchdulerEngine* crawler_engine,
            analytical_schduler::SchdulerEngine* analytical_engine);

    void FetchBatchTask(std::list<base_logic::TaskInfo>* list,
            bool is_first = false);

    void FetchBatchHbase(std::list<base_logic::StorageHBase>* list);

    bool RemoveAnalyticalHBase(const int64 id);

 public:
    bool DistributionTask();

    bool DistibutionHBase();

    void SwapRemoveHBase(std::list<base_logic::StorageHBase>* list,
            bool is_clean = true);

    void RecyclingTask();  //  用于发出爬虫异常崩溃，无法执行任务

    bool AlterTaskState(const int64 task_id, const int8 state);

    bool AlterCrawlNum(const int64 task_id, const int64 num);

    void CheckIsEffective();

 private:
    void Init();

 private:
    struct threadrw_t*                     lock_;
    TaskSchdulerCache*                     task_cache_;
    crawler_schduler::SchdulerEngine*      crawler_schduler_engine_;
    analytical_schduler::SchdulerEngine*   analytical_schduler_engine_;
    int32                                  crawler_count_;
    int32                                  analytical_count_;
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
}  // namespace task_logic

#endif /* TASK_SCHDULER_ENGINE_CC_ */
