//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月23日 Author: kerry
#include "task/task_schduler_engine.h"
#include <string>
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "basic/template.h"
#include "basic/radom_in.h"

namespace task_logic {

TaskSchdulerManager* TaskSchdulerEngine::schduler_mgr_ = NULL;
TaskSchdulerEngine* TaskSchdulerEngine::schduler_engine_ = NULL;

TaskSchdulerManager::TaskSchdulerManager()
:crawler_count_(0)
, analytical_count_(0) {
    task_cache_ = new TaskSchdulerCache();
    Init();
}

TaskSchdulerManager::~TaskSchdulerManager() {
    DeinitThreadrw(lock_);
}

void TaskSchdulerManager::Init() {
    InitThreadrw(&lock_);
}

void TaskSchdulerManager::Init(crawler_schduler::SchdulerEngine* crawler_engine,
        analytical_schduler::SchdulerEngine* analytical_engine ) {
    crawler_schduler_engine_ = crawler_engine;
    analytical_schduler_engine_ = analytical_engine;
}

/*
bool TaskSchdulerManager::SetIdleTaskInfo(const int64 task_id,
        base_logic::TaskInfo* task) {
    base_logic::WLockGd lk(lock_);
    return base::MapAdd<TASKINFO_MAP, int64, base_logic::TaskInfo>
    (task_cache_->task_idle_map_, task_id, (*task));
}

bool TaskSchdulerManager::GetIdleTaskInfo(const int64 task_id,
        base_logic::TaskInfo* task) {
    base_logic::RLockGd lk(lock_);
    return base::MapGet<TASKINFO_MAP, TASKINFO_MAP::iterator,
            int64, base_logic::TaskInfo>(task_cache_->task_idle_map_,
                    task_id, (*task));
}

bool TaskSchdulerManager::DelIdleTaskInfo(const int64 task_id) {
    base_logic::WLockGd lk(lock_);
    return base::MapDel<TASKINFO_MAP, TASKINFO_MAP::iterator, int64>
    (task_cache_->task_idle_map_, task_id);
}*/

void TaskSchdulerManager::FetchBatchTask(
        std::list<base_logic::TaskInfo>* list,
        bool is_first) {
    base_logic::WLockGd lk(lock_);
    time_t current_time = time(NULL);
    while ((*list).size() > 0) {
        base_logic::TaskInfo info = (*list).front();
        (*list).pop_front();
        // 更新时间
        info.update_time(current_time,
                base::SysRadom::GetInstance()->GetRandomID(),
                is_first);
        task_cache_->task_idle_map_[info.id()] = info;
    }
}

void TaskSchdulerManager::FetchBatchHbase(
        std::list<base_logic::StorageHBase>* list) {
    base_logic::WLockGd lk(lock_);
    while ((*list).size() > 0) {
        base_logic::StorageHBase info = (*list).front();
        (*list).pop_front();
        task_cache_->hbase_idle_map_[info.id()] = info;
    }
}

bool TaskSchdulerManager::AlterTaskState(const int64 task_id,
        const int8 state) {
    base_logic::WLockGd lk(lock_);
    base_logic::TaskInfo task;
    bool r = base::MapGet<TASKINFO_MAP, TASKINFO_MAP::iterator,
            int64, base_logic::TaskInfo>(task_cache_->task_exec_map_,
                    task_id, task);
    if (r) {
        if (state == TASK_EXECUED) {
            base::MapDel<TASKINFO_MAP, TASKINFO_MAP::iterator, int64>
            (task_cache_->task_exec_map_, task_id);
        }
        task.set_state(state);
    }
    return r;
}

bool TaskSchdulerManager::AlterCrawlNum(const int64 task_id, const int64 num) {
    base_logic::WLockGd lk(lock_);
    base_logic::TaskInfo task;
    bool r = base::MapGet<TASKINFO_MAP, TASKINFO_MAP::iterator,
            int64, base_logic::TaskInfo>(task_cache_->task_exec_map_,
                    task_id, task);
    if (r)
        task.set_crawl_num(num);
    return r;
}

bool TaskSchdulerManager::RemoveAnalyticalHBase(const int64 id) {
    base_logic::WLockGd lk(lock_);
    base_logic::StorageHBase hbase;
    bool r = base::MapGet<HBASE_MAP, HBASE_MAP::iterator,
            int64, base_logic::StorageHBase>(task_cache_->hbase_exec_map_,
            id, hbase);
    if (!r)
        return false;
    hbase.set_state(ANALYTICAL_EXECUED);

    r = base::MapDel<HBASE_MAP, HBASE_MAP::iterator,
            int64>(task_cache_->hbase_exec_map_, id);
    task_cache_->hbase_remove_list_.push_back(hbase);
    return true;
}


void TaskSchdulerManager::RecyclingTask() {
    LOG_MSG2("task_exec_map size %d", task_cache_->task_exec_map_.size());
    base_logic::WLockGd lk(lock_);
    TASKINFO_MAP::iterator it =
            task_cache_->task_exec_map_.begin();
    time_t current_time = time(NULL);
    for (; it != task_cache_->task_exec_map_.end();) {
        base_logic::TaskInfo task = it->second;
        // 检测当前时间大于 polling time 1.5倍  则回收
        if ((task.last_task_time() + task.base_polling_time() * (1.5))
              <  current_time) {
            task.set_state(TASK_WAIT);
            task_cache_->task_exec_map_.erase(it++);
        } else {
            it++;
        }
    }
}

bool TaskSchdulerManager::DistibutionHBase() {
    LOG_MSG2("hbase_idle_list size  %d", task_cache_->hbase_idle_map_.size());
    LOG_MSG2("hbase_exec_map size  %d", task_cache_->hbase_exec_map_.size());
    if (task_cache_->hbase_idle_map_.size() <= 0)
        return true;
    if (!analytical_schduler_engine_->CheckOptimalAnalytical()) {
        LOG_MSG("no have OptimalAnalytical");
        return true;
    }
    int32 base_num = 5;
    struct AnalysiInfo analysical_info;
    MAKE_HEAD(analysical_info, ANALYTICAL_INFO, 0, 0, 0, 0);
    base_logic::WLockGd lk(lock_);
    HBASE_MAP::iterator it =
            task_cache_->hbase_idle_map_.begin();


    for (; it != task_cache_->hbase_idle_map_.end();) {
        base_logic::StorageHBase info = it->second;
        struct AnalysiUnit* unit = new struct AnalysiUnit;
        unit->ayalysi_id = info.id();
        unit->task_id = info.taskid();
        unit->attr_id = info.attrid();
        memset(unit->key, '\0', KEY_SIZE);
        memcpy(unit->key, info.hkey().c_str(),
               (KEY_SIZE - 1) < info.hkey().length() ?
               (KEY_SIZE - 1) : info.hkey().length());
        memset(unit->name, '\0', NAME_SIZE);
        memcpy(unit->name, info.name().c_str(),
               (NAME_SIZE - 1) < info.name().length() ?
               (NAME_SIZE - 1) : info.name().length());
        analysical_info.analysi_set.push_back(unit);
        info.set_state(ANALYTICAL_EXECUTING);

        task_cache_->hbase_exec_map_[info.id()] = info;

        task_cache_->hbase_idle_map_.erase(it++);
        if (analysical_info.analysi_set.size() % base_num == 0 &&
                analysical_info.analysi_set.size() != 0) {
            analytical_schduler_engine_->SendOptimalAnalytical(
                    (const void*)&analysical_info, 0);
            net::PacketProsess::ClearHBaseAnalyticalTaskList(&analysical_info);
        }
    }

    if (analysical_info.analysi_set.size() > 0) {
        analytical_schduler_engine_->SendOptimalAnalytical(
                (const void*)&analysical_info, 0);
        net::PacketProsess::ClearHBaseAnalyticalTaskList(&analysical_info);
    }
    /*for (; it != task_cache_->hbase_idle_map_.end();) {
        base_logic::StorageHBase info = it->second;
        struct AnalysiUnit* unit = new struct AnalysiUnit;
        unit->ayalysi_id = info.id();
        unit->task_id = info.taskid();
        unit->attr_id = info.attrid();
        memset(unit->key, '\0', KEY_SIZE);
        memcpy(unit->key, info.hkey().c_str(),
               (KEY_SIZE - 1) < info.hkey().length() ?
               (KEY_SIZE - 1) : info.hkey().length());
        memset(unit->name, '\0', NAME_SIZE);
        memcpy(unit->name, info.name().c_str(),
               (NAME_SIZE - 1) < info.name().length() ?
               (NAME_SIZE - 1) : info.name().length());
        analysical_info.analysi_set.push_back(unit);

        info.set_state(ANALYTICAL_EXECUTING);
        task_cache_->hbase_idle_map_.erase(it++);

        task_cache_->hbase_exec_map_[info.id()] = info;
    }

    if (analysical_info.analysi_set.size() > 0)
        analytical_schduler_engine_->SendOptimalAnalytical(
                (const void*)&analysical_info, 0);
    */

    return true;
}

bool TaskSchdulerManager::DistributionTask() {
    LOG_MSG2("task_idle_list size  %d", task_cache_->task_idle_map_.size());
    LOG_MSG2("task_exec_map size  %d", task_cache_->task_exec_map_.size());
    int32 base_num = 5;
    if (task_cache_->task_idle_map_.size() <= 0)
        return true;
   /* if (!crawler_schduler_engine_->CheckOptimalCrawler()) {
        LOG_MSG("no have OptimalCrawler");
        return true;
    }
*/
    time_t current_time = time(NULL);

    struct AssignmentMultiTask  task;
    MAKE_HEAD(task, ASSIGNMENT_MULTI_TASK, 0, 0, 0, 0);
    base_logic::WLockGd lk(lock_);

    int32 count = task_cache_->task_idle_map_.size();
    int32 mutil = count / base_num;
    int32 residue = count % base_num;
    int32 index = 0;
    TASKINFO_MAP::iterator it = task_cache_->task_idle_map_.begin();

    for (; it != task_cache_->task_idle_map_.end(), index < count;
            it++, index++) {
        base_logic::TaskInfo info = it->second;
        /*LOG_MSG2("id %lld current %lld last_time %lld polling_time %lld",
                info.id(), current_time, info.last_task_time(),
                info.polling_time());
        info.update_time(current_time, base::SysRadom::GetInstance()->GetRandomID());*/
        if ((info.state() == TASK_WAIT || info.state() == TASK_EXECUED)
                        && (current_time >  info.last_task_time() +
                                      info.polling_time())) {
            struct TaskUnit* unit = new struct TaskUnit;
            unit->task_id = info.id();
            unit->attr_id = info.attrid();
            unit->max_depth = info.depth();
            unit->current_depth = info.cur_depth();
            unit->machine = info.machine();
            unit->storage = info.storage();
            unit->is_login = info.is_login();
            unit->is_over = info.is_over();
            unit->is_forge = info.is_forge();
            unit->method = info.method();
            memset(unit->url, '\0', URL_SIZE);
            memcpy(unit->url, info.url().c_str(),
                    (URL_SIZE - 1) < info.url().length() ?
                    (URL_SIZE - 1) : info.url().length());
            task.task_set.push_back(unit);
            info.set_state(TASK_SEND);
            task_cache_->task_exec_map_[info.id()] = info;
            info.update_time(current_time,
                    base::SysRadom::GetInstance()->GetRandomID());
            if (task.task_set.size() % base_num == 0 &&
                    task.task_set.size() != 0) {
                crawler_schduler_engine_->SendOptimalCrawler(
                        (const void*)&task, 0);
                net::PacketProsess::ClearCrawlerTaskList(&task);
            }
        }
    }

    //解决余数
    if (task.task_set.size() > 0) {
        crawler_schduler_engine_->SendOptimalCrawler((const void*)&task, 0);
        net::PacketProsess::ClearCrawlerTaskList(&task);
    }

    /*
    TASKINFO_MAP::iterator it =
            task_cache_->task_idle_map_.begin();
    for (; it != task_cache_->task_idle_map_.end(); it++) {
        base_logic::TaskInfo info = it->second;
        LOG_DEBUG2("state %d current_time %lld last_time %lld polling %lld",
                (int)(info.state()), current_time, info.last_task_time(),
                info.polling_time());
        if ((info.state() == TASK_WAIT || info.state() == TASK_EXECUED)
                && (current_time >  info.last_task_time() +
                              info.polling_time())) {
            struct TaskUnit* unit = new struct TaskUnit;
            unit->task_id = info.id();
            unit->attr_id = info.attrid();
            unit->depth = info.depth();
            unit->machine = info.machine();
            unit->storage = info.storage();
            unit->is_login = info.is_login();
            unit->is_over = info.is_over();
            unit->is_forge = info.is_forge();
            unit->method = info.method();
            memset(unit->url, '\0', URL_SIZE);
            memcpy(unit->url, info.url().c_str(),
                   (URL_SIZE - 1) < info.url().length() ?
                   (URL_SIZE - 1) : info.url().length());
            task.task_set.push_back(unit);
            info.set_state(TASK_SEND);
            task_cache_->task_exec_map_[info.id()] = info;
            info.update_time(current_time);
        }
    }

    // 发送最优的爬虫
    if (task.task_set.size() > 0)
        crawler_schduler_engine_->SendOptimalCrawler((const void*)&task, 0);
    else
        LOG_DEBUG2("task_set size %ld", task.task_set.size());
    */
    return true;
}

void TaskSchdulerManager::SwapRemoveHBase(
        std::list<base_logic::StorageHBase>* list,
        bool is_clean) {
    base_logic::WLockGd lk(lock_);
    if (task_cache_->hbase_remove_list_.size() > 0) {
       // (*list) = task_cache_->hbase_remove_list_;
        task_cache_->hbase_remove_list_.swap((*list));
        task_cache_->hbase_remove_list_.clear();
    }
}

void TaskSchdulerManager::CheckIsEffective() {
    crawler_schduler_engine_->CheckIsEffective();
}

}  // namespace task_logic
