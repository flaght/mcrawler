//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月23日 Author: kerry
#include "crawler_task/task_schduler_engine.h"
#include <string>
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "basic/template.h"
#include "basic/radom_in.h"

namespace crawler_task_logic {

TaskSchdulerManager* TaskSchdulerEngine::schduler_mgr_ = NULL;
TaskSchdulerEngine* TaskSchdulerEngine::schduler_engine_ = NULL;

TaskSchdulerManager::TaskSchdulerManager()
:crawler_count_(0)
, task_db_(NULL) {
    task_cache_ = new TaskSchdulerCache();
    Init();
}

TaskSchdulerManager::~TaskSchdulerManager() {
    DeinitThreadrw(lock_);
}

void TaskSchdulerManager::Init() {
    InitThreadrw(&lock_);
}

void TaskSchdulerManager::InitDB(crawler_task_logic::CrawlerTaskDB* task_db) {
    task_db_ = task_db;
}

void TaskSchdulerManager::Init(crawler_schduler::SchdulerEngine* crawler_engine) {
    crawler_schduler_engine_ = crawler_engine;
}


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

void TaskSchdulerManager::FetchBatchTemp(
        std::list<base_logic::TaskInfo>* list) {
    base_logic::WLockGd lk(lock_);
    while ((*list).size() > 0) {
        base_logic::TaskInfo info = (*list).front();
        (*list).pop_front();
        task_cache_->task_temp_list_.push_back(info);
    }
}

bool TaskSchdulerManager::AlterTaskState(const int64 task_id,
        const int8 state) {
    base_logic::WLockGd lk(lock_);
    task_cache_->task_exec_map_[task_id].set_state(state);
    if (TASK_EXECUED == state)
        task_cache_->task_exec_map_.erase(task_id);
    return true;
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



void TaskSchdulerManager::RecyclingTask() {
    base_logic::WLockGd lk(lock_);
    TASKINFO_MAP::iterator it =
            task_cache_->task_exec_map_.begin();
    time_t current_time = time(NULL);
    for (; it != task_cache_->task_exec_map_.end();) {
        base_logic::TaskInfo& task = it->second;
        task_db_->RecordTaskState(task, 2);
        if ((task.last_task_time() + 50)
              <  current_time) {
            task.set_state(TASK_WAIT);
            task_cache_->task_exec_map_.erase(it++);
        } else {
            it++;
        }
    }
}

bool TaskSchdulerManager::DistributionTempTask() {
   LOG_MSG2("task_temp_list_ size %d", task_cache_->task_temp_list_.size());
   if (task_cache_->task_temp_list_.size() <= 0)
        return true;
    if (!crawler_schduler_engine_->CheckOptimalCrawler()) {
         LOG_MSG("no have OptimalCrawler");
         return true;
     }
    int32 base_num = 5;
    time_t current_time = time(NULL);
    struct AssignmentMultiTask  task;
    MAKE_HEAD(task, ASSIGNMENT_MULTI_TASK, 0, 0, 0, 0);
    base_logic::WLockGd lk(lock_);

    task_cache_->task_temp_list_.sort(base_logic::TaskInfo::cmp);
    while (task_cache_->task_temp_list_.size() > 0) {
        base_logic::TaskInfo info = task_cache_->task_temp_list_.front();
        LOG_DEBUG2("url=%s attr_id=%ld", info.url().c_str(), info.attrid());
        //task_db_->RecordTaskState(info, 1);
        if ((info.state() == TASK_WAIT || info.state() == TASK_EXECUED)&&
            (current_time >= info.totoal_polling_time())) {
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
            task_cache_->task_temp_list_.pop_front();
            if (task.task_set.size() % base_num == 0 &&
                    task.task_set.size() != 0) {
                crawler_schduler_engine_->SendOptimalCrawler((const void*)&task, 0);
                net::PacketProsess::ClearCrawlerTaskList(&task);
            }
        }else{
          break;
        }
    }

    //解决余数
    if (task.task_set.size() > 0) {
        crawler_schduler_engine_->SendOptimalCrawler((const void*)&task, 0);
        net::PacketProsess::ClearCrawlerTaskList(&task);
    }

    LOG_MSG2("task_temp_list_ size %d", task_cache_->task_temp_list_.size());
    return true;
}


bool TaskSchdulerManager::DistributionTask() {
    int32 base_num = 5;
    time_t current_time = time(NULL);
    if (task_cache_->task_idle_map_.size() <= 0) {
    	LOG_DEBUG2("distrubute task current_time=%d task_cache_->task_idle_map_.size=%d", (int)current_time, task_cache_->task_idle_map_.size());
    	return true;
    }
    if (!crawler_schduler_engine_->CheckOptimalCrawler()) {
        LOG_MSG("no have OptimalCrawler");
        return true;
    }

    LOG_DEBUG2("distrubute task current_time=%d task_cache_->task_idle_map_.size=%d", (int)current_time, task_cache_->task_idle_map_.size());
    struct AssignmentMultiTask  task;
    MAKE_HEAD(task, ASSIGNMENT_MULTI_TASK, 0, 0, 0, 0);
    base_logic::WLockGd lk(lock_);
    int32 count = task_cache_->task_idle_map_.size();
    int32 index = 0;
    TASKINFO_MAP::iterator it = task_cache_->task_idle_map_.begin();
    for (; it != task_cache_->task_idle_map_.end(), index < count; it++, index++) {
        base_logic::TaskInfo& info = it->second;
        task_db_->RecordTaskState(info, 0);
        LOG_MSG2("id %lld current %lld last_time %lld polling_time %lld state %d",
                info.id(), current_time, info.last_task_time(),
                info.polling_time(), info.state());
        if ((info.state() == TASK_WAIT || info.last_task_time() + info.polling_time() < current_time)) {
	    LOG_MSG2("DistributionTask task_id=%d", info.id());
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
            info.update_time(current_time, base::SysRadom::GetInstance()->GetRandomID());
            task_cache_->task_exec_map_[info.id()] = info;
            if (task.task_set.size() % base_num == 0 &&
                    task.task_set.size() != 0) {
                crawler_schduler_engine_->SendOptimalCrawler((const void*)&task, 0);
                net::PacketProsess::ClearCrawlerTaskList(&task);
            }
        }
    }

    //解决余数
    if (task.task_set.size() > 0) {
        crawler_schduler_engine_->SendOptimalCrawler((const void*)&task, 0);
        net::PacketProsess::ClearCrawlerTaskList(&task);
    }
    return true;
}

void TaskSchdulerManager::CheckIsEffective() {
    crawler_schduler_engine_->CheckIsEffective();
}

}  // namespace crawler_task_logic
