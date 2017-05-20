//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月23日 Author: kerry
#include "crawler_task/task_schduler_engine.h"
#include "basic/radom_in.h"
#include "basic/template.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "logic/time.h"
#include <string>

namespace crawler_task_logic {

TaskSchdulerManager *TaskSchdulerEngine::schduler_mgr_ = NULL;
TaskSchdulerEngine *TaskSchdulerEngine::schduler_engine_ = NULL;

TaskSchdulerManager::TaskSchdulerManager()
    : crawler_count_(0),
      task_db_(NULL) {
  task_cache_ = new TaskSchdulerCache();
  Init();
}

TaskSchdulerManager::~TaskSchdulerManager() {
  DeinitThreadrw(lock_);
  LOG_MSG("clear task_cache_ cache");
  task_cache_->task_check_map_.clear();
  task_cache_->task_complete_map_.clear();
  task_cache_->task_exec_map_.clear();
  task_cache_->task_idle_map_.clear();
  task_cache_->task_temp_list_.clear();
  task_cache_->task_temp_map_.clear();
  if (task_cache_) {
    delete task_cache_;
    task_cache_ = NULL;
  }
}

void TaskSchdulerManager::Init() {
  InitThreadrw(&lock_);
  // Test();
}

void TaskSchdulerManager::Test() {
  std::list<base_logic::TaskInfo> list;
  int32 count = 100;
  while (count > 0) {
    base_logic::TaskInfo info;
    info.set_id(count);
    info.set_is_finish(0);
    info.set_attrid(60008);
    info.set_is_login(0);
    info.set_method(2);
    info.create_task_time(base::SysRadom::GetInstance()->GetRandomID() / 10000);
    list.push_back(info);
    count--;
  }
  list.sort(base_logic::TaskInfo::create_time_sort);

  while (list.size() > 0) {
    base_logic::TaskInfo info = list.front();
    list.pop_front();
    LOG_DEBUG2("count %lld create_time %lld", info.id(), info.create_time());
  }
  /* base_logic::TaskInfo info;
   info.set_id(base::SysRadom::GetInstance()->GetRandomID());
   info.set_url(
   "http://focus.stock.hexun.com/service/init_xml.jsp?scode=600149&date=2016-08-08");
   info.set_is_finish(0);
   info.set_attrid(60008);
   info.set_is_login(0);
   info.set_method(2);
   info.set_base_polling_time(30);
   task_cache_->task_temp_list_.push_back(info);*/
}
void TaskSchdulerManager::InitDB(crawler_task_logic::CrawlerTaskDB *task_db) {
  task_db_ = task_db;
}

void TaskSchdulerManager::Init(
    crawler_schduler::SchdulerEngine *crawler_engine) {
  crawler_schduler_engine_ = crawler_engine;
}

void TaskSchdulerManager::FetchBatchTask(std::list<base_logic::TaskInfo> *list,
                                         bool is_first) {
  base_logic::WLockGd lk(lock_);
  time_t current_time = time(NULL);
  while ((*list).size() > 0) {
    base_logic::TaskInfo info = (*list).front();
    (*list).pop_front();
    // 更新时间
    info.update_time(current_time, base::SysRadom::GetInstance()->GetRandomID(),
                     is_first);
    task_cache_->task_idle_map_[info.id()] = info;
  }
}

void TaskSchdulerManager::FetchBatchTemp(
    std::list<base_logic::TaskInfo> *list) {
  base_logic::WLockGd lk(lock_);
  while ((*list).size() > 0) {
    base_logic::TaskInfo info = (*list).front();
    task_cache_->task_check_map_[info.id()] = info;
    (*list).pop_front();
    if (task_cache_->task_temp_map_.find(info.id())
        == task_cache_->task_temp_map_.end()) {
      task_cache_->task_temp_list_.push_back(info);
      task_cache_->task_temp_map_[info.id()] = info;
    }
  }
}

bool TaskSchdulerManager::AlterTaskState(const int socket, const int64 task_id,
                                         const int8 state) {
  base_logic::WLockGd lk(lock_);
  base_logic::TaskInfo info = task_cache_->task_exec_map_[task_id];
  info.set_state(state);

  time_t current_time = time(NULL);
  base_logic::CrawlerScheduler scheduler;
  bool r = crawler_schduler_engine_->FindCrawlerSchduler(socket, &scheduler);
  if (r && scheduler.id() == info.crawler_id()) {
    r = true;
  } else {
    r = false;
  }

  if (TASK_EXECUED == state || TASK_ERROR == state) {  //已经不在执行状态
    task_cache_->task_exec_map_.erase(task_id);
    if (r)
      scheduler.del_task(info);
    if (TASK_EXECUED == state)
      task_cache_->task_complete_map_[task_id] = info;
    else if (TASK_ERROR == state) {  //直接回收
      info.set_state(TASK_WAIT);    //回收任务调整状态
      info.update_time(current_time,
                       base::SysRadom::GetInstance()->GetRandomID());  //更新下次任务时间
      task_cache_->task_temp_list_.push_back(info);
      task_cache_->task_temp_map_[info.id()] = info;
    }
  } else {  //在执行状态
    scheduler.set_task(info);
  }
  scheduler.sync_task_count();

  // LOG_DEBUG2("crawler id(%d), task count(%d) task id(%lld) task
  // state(%d)",scheduler.id(),
  //   scheduler.exec_task_count(),info.id(),info.state());
  return true;
}

bool TaskSchdulerManager::AlterCrawlNum(const int64 task_id, const int64 num) {
  base_logic::WLockGd lk(lock_);
  base_logic::TaskInfo task;
  bool r = base::MapGet<TASKINFO_MAP, TASKINFO_MAP::iterator, int64,
      base_logic::TaskInfo>(task_cache_->task_exec_map_, task_id, task);
  if (r)
    task.set_crawl_num(num);
  return r;
}

void TaskSchdulerManager::RecyclingTask() {  //只回收临时任务
  base_logic::WLockGd lk(lock_);
  TASKINFO_MAP::iterator it = task_cache_->task_exec_map_.begin();
  time_t current_time = time(NULL);
  for (; it != task_cache_->task_exec_map_.end();) {
    base_logic::TaskInfo &task = it->second;
    if (((current_time >= task.create_time() + 60)
        && (task.state() == TASK_SEND || task.state() == TASK_RECV
            || task.state() == TASK_EXECUING))
        || (task.state() == TASK_ERROR)) {
      //如果已经存储 则保留上次状态
      if (task_cache_->task_temp_map_.find(task.id())
          == task_cache_->task_temp_map_.end()) {
        task.set_state(TASK_WAIT);  //回收任务调整状态
        task.update_time(current_time,
                         base::SysRadom::GetInstance()->GetRandomID());  //更新下次任务时间
        task_cache_->task_temp_list_.push_back(task);
        task_cache_->task_temp_map_[task.id()] = task;
      }
      task_cache_->task_exec_map_.erase(it++);
    } else {
      it++;
    }
  }
}

bool TaskSchdulerManager::DistributionTempTask() {
  base_logic::WLockGd lk(lock_);
  //分配任务控制 每个爬虫数不超过500个  故 500 * 爬虫个数
  int32 surplus = GetSurplusTaskCount();
  LOG_MSG2("task_check_map_ size %d", task_cache_->task_check_map_.size());
  LOG_MSG2("task_temp_list_ size %d", task_cache_->task_temp_list_.size());
  LOG_MSG2("task_temp_map_ size %d", task_cache_->task_temp_map_.size());
  LOG_MSG2("task_exec_map_ size %d", task_cache_->task_exec_map_.size());
  LOG_MSG2("task_complete_map_ size %d",
           task_cache_->task_complete_map_.size());
  LOG_MSG2("surplus %d", surplus);

  if (task_cache_->task_temp_list_.size() <= 0)
    return true;

  if (!crawler_schduler_engine_->CheckOptimalCrawler()) {
    LOG_MSG("no have OptimalCrawler");
    return true;
  }

  int32 base_num = 5;
  time_t current_time = time(NULL);
  std::list<base_logic::TaskInfo> log_list;
  struct AssignmentMultiTask task;
  MAKE_HEAD(task, ASSIGNMENT_MULTI_TASK, 0, 0, 0, 0);

  task_cache_->task_temp_list_.sort(base_logic::TaskInfo::cmp);
  // DumpTask();
  while (task_cache_->task_temp_list_.size() > 0 && surplus > 0) {
    base_logic::TaskInfo info = task_cache_->task_temp_list_.front();
    // LOG_DEBUG2("url=%s attr_id=%ld", info.url().c_str(), info.attrid());
    if ((info.state() == TASK_WAIT || info.state() == TASK_EXECUED)
        && (current_time >= info.totoal_polling_time())) {
      // LOG_DEBUG2("id %lld url %s",info.id(),info.url().c_str());
      struct TaskUnit *unit = new struct TaskUnit;
      unit->task_id = info.id();
      unit->pid = info.pid();
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
      memcpy(
          unit->url,
          info.url().c_str(),
          (URL_SIZE - 1) < info.url().length() ?
              (URL_SIZE - 1) : info.url().length());
      task.task_set.push_back(unit);
      info.set_state(TASK_SEND);
      info.create_task_time();
      log_list.push_back(info);
      task_cache_->task_exec_map_[info.id()] = info;
      task_cache_->task_temp_list_.pop_front();
      base::MapDel<TASKINFO_MAP, TASKINFO_MAP::iterator, const int64>(
          task_cache_->task_temp_map_, info.id());
      surplus--;
      if (task.task_set.size() % base_num == 0 && task.task_set.size() != 0) {
        int32 crawler_id = crawler_schduler_engine_->SendOptimalCrawler(
            (const void *) &task, 0);

        LOG_MSG2("crawler_id %d task size %d", crawler_id, task.task_set.size());
        
        if (crawler_id > 0) {
          SetTaskInfosCrawlerId(&task, crawler_id);
          // task_db_->CreateTaskLog(crawler_id, &log_list);
        }
        net::PacketProsess::ClearCrawlerTaskList(&task);
      }
    } else {
      LOG_MSG2("state==>%d  current_time==>%ld totoal_polling_time==%ld "
               "last_time==>%ld polling_time===>%ld",
               info.state(), current_time, info.totoal_polling_time(),
               info.last_task_time(), info.polling_time());
      break;
    }
  }

  //解决余数
  if (task.task_set.size() > 0) {
    LOG_MSG2("task_set size %d  log_list size %d", task.task_set.size(),
             log_list.size());
    int32 crawler_id = crawler_schduler_engine_->SendOptimalCrawler(
        (const void *) &task, 0);

   LOG_MSG2("crawler_id %d task size %d", crawler_id, task.task_set.size());
   if (crawler_id > 0) {

      SetTaskInfosCrawlerId(&task, crawler_id);
      //新增日志
      // task_db_->CreateTaskLog(crawler_id, &log_list);
    }
    net::PacketProsess::ClearCrawlerTaskList(&task);
  }

  // LOG_MSG2("task_temp_list_ size %d", task_cache_->task_temp_list_.size());
  return true;
}

bool TaskSchdulerManager::DistributionTask() {
  int32 base_num = 5;
  time_t current_time = time(NULL);
  if (task_cache_->task_idle_map_.size() <= 0) {
    LOG_MSG2(
        "distrubute task current_time=%d task_cache_->task_idle_map_.size=%d",
        (int) current_time, task_cache_->task_idle_map_.size());
    return true;
  }
  if (!crawler_schduler_engine_->CheckOptimalCrawler()) {
    LOG_MSG("no have OptimalCrawler");
    return true;
  }

  LOG_MSG2(
      "distrubute task current_time=%d task_cache_->task_idle_map_.size=%d",
      (int) current_time, task_cache_->task_idle_map_.size());
  struct AssignmentMultiTask task;
  MAKE_HEAD(task, ASSIGNMENT_MULTI_TASK, 0, 0, 0, 0);
  base_logic::WLockGd lk(lock_);
  int32 count = task_cache_->task_idle_map_.size();
  int32 index = 0;
  TASKINFO_MAP::iterator it = task_cache_->task_idle_map_.begin();
  for (; it != task_cache_->task_idle_map_.end(), index < count;
      it++, index++) {
    base_logic::TaskInfo &info = it->second;
    // task_db_->RecordTaskState(info, 0);
    // task_db_->CreateTaskLog(info);
    LOG_MSG2("id %lld current %lld last_time %lld polling_time %lld state %d",
             info.id(), current_time, info.last_task_time(),
             info.polling_time(), info.state());
    if ((info.state() == TASK_WAIT
        || info.last_task_time() + info.polling_time() < current_time)) {
      LOG_MSG2("DistributionTask task_id=%d", info.id());
      struct TaskUnit *unit = new struct TaskUnit;
      unit->task_id = info.id();
      unit->pid = info.id();
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
      memcpy(
          unit->url,
          info.url().c_str(),
          (URL_SIZE - 1) < info.url().length() ?
              (URL_SIZE - 1) : info.url().length());
      task.task_set.push_back(unit);
      info.set_state(TASK_SEND);
      info.create_task_time();
      info.update_time(current_time,
                       base::SysRadom::GetInstance()->GetRandomID());
      task_cache_->task_exec_map_[info.id()] = info;
      if (task.task_set.size() % base_num == 0 && task.task_set.size() != 0) {
        crawler_schduler_engine_->SendOptimalCrawler((const void *) &task, 0);
        net::PacketProsess::ClearCrawlerTaskList(&task);
      }
    }
  }

  //解决余数
  if (task.task_set.size() > 0) {
    crawler_schduler_engine_->SendOptimalCrawler((const void *) &task, 0);
    net::PacketProsess::ClearCrawlerTaskList(&task);
  }
  return true;
}

void TaskSchdulerManager::SetTaskInfosCrawlerId(const PacketHead *packet,
                                                const int32 crawler_id) {
  struct AssignmentMultiTask *multi = (struct AssignmentMultiTask *) packet;
  std::list<struct TaskUnit *>::iterator it = multi->task_set.begin();
  for (; it != multi->task_set.end(); it++) {
    struct TaskUnit *unit = (*it);
    SetTaskInfoCrawlerId(unit->task_id, crawler_id);
  }
}

void TaskSchdulerManager::SetTaskInfoCrawlerId(const int64 task_id,
                                               const int32 crawler_id) {
  bool r = false;
  base_logic::TaskInfo task;
  r = base::MapGet<TASKINFO_MAP, TASKINFO_MAP::iterator, int64,
      base_logic::TaskInfo>(task_cache_->task_exec_map_, task_id, task);
  if (!r)
    return;
  task.set_cralwer_id(crawler_id);
}

void TaskSchdulerManager::CheckIsEffective() {
  crawler_schduler_engine_->CheckIsEffective();
}

void TaskSchdulerManager::DumpTask() {
  task_cache_->task_temp_list_.sort(base_logic::TaskInfo::cmp);
  TASKINFO_LIST::iterator it = task_cache_->task_temp_list_.begin();
  for (; it != task_cache_->task_temp_list_.end(); it++) {
    base_logic::TaskInfo task = (*it);
    time_t polling_time = task.totoal_polling_time();
    time_t create_time = task.create_time();
    struct tm *polling_local = localtime(&polling_time);
    struct tm *create_local = localtime(&create_time);

    LOG_DEBUG2("==> id-->%lld  polling_time-->%lld(%d-%d %d:%d:%d) "
               "create_time-->%lld(%d-%d %d:%d:%d)",
               task.id(), task.totoal_polling_time(), polling_local->tm_mon + 1,
               polling_local->tm_mday, polling_local->tm_hour,
               polling_local->tm_min, polling_local->tm_sec, task.create_time(),
               create_local->tm_mon + 1, create_local->tm_mday,
               create_local->tm_hour, create_local->tm_min,
               create_local->tm_sec);
  }
}

/*
 void TaskSchdulerManager::SetDeepTask(const int socket, base_logic::TaskInfo& task) {
 //查找是否存在
 TASKINFO_MAP t_map;
 bool r =  base::MapGet<DEEP_TASKINFO_MAP, DEEP_TASKINFO_MAP::iterator, TASKINFO_MAP>
 (task_cache_->task_deep_exec_map_, socket, t_map);
 t_map[task.id()]
 }*/

int32 TaskSchdulerManager::GetSurplusTaskCount() {
  std::map<int32, base_logic::CrawlerScheduler> crawler_map;
  crawler_schduler_engine_->GetAllCrawler(crawler_map);
  int32 crawler_count = crawler_map.size();
  int32 task_count = 0;
  std::map<int32, base_logic::CrawlerScheduler>::iterator it =
      crawler_map.begin();

  for (; it != crawler_map.end(); it++) {
    base_logic::CrawlerScheduler crawler = it->second;
    task_count += crawler.exec_task_count();
    LOG_DEBUG2("crawler id %d  exec_task_count %d", crawler.id(),
               crawler.exec_task_count());
  }

  int32 exec_count =
      task_count > task_cache_->task_exec_map_.size() ?
          task_count : task_cache_->task_exec_map_.size();

  //int32 surplus = crawler_count * 100 - exec_count;
  int32 surplus = crawler_count * 100 - (task_cache_->task_exec_map_.size());

  LOG_MSG2("surplus [%d] exec_count[%d] crawler_count[%d][%d]", surplus,
           exec_count, crawler_count, crawler_count * 500);

  return surplus > 0 ? surplus : 0;
}

}  // namespace crawler_task_logic
