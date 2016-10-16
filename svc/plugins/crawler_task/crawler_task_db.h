//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015.9.22 Author: kerry

#ifndef KID_CRAWLER_TASK_DB_H_
#define KID_CRAWLER_TASK_DB_H_

#include <string>
#include <list>
#include <map>
#include "storage/data_engine.h"
#include "logic/auto_crawler_infos.h"
#include "config/config.h"
#include "basic/basictypes.h"
#include "logic/base_values.h"
#include "basic/scoped_ptr.h"

namespace crawler_task_logic {

typedef std::map<int32, base_logic::TaskPlatDescription> TASKPLAT_MAP;

class CrawlerTaskDB {
 public:
    CrawlerTaskDB(config::FileConfig* config);
    virtual ~CrawlerTaskDB();

 public:
    bool FecthBatchTask(std::list<base_logic::TaskInfo>* list,
            const bool is_new = false);

    bool RecordTaskState(base_logic::TaskInfo& task, const int32 type);

    bool GetTaskPlatTaskDescription(
            std::list<base_logic::TaskPlatDescription>* list);

    void BatchFectchTaskPlatInfo(
            std::list<base_logic::TaskPlatDescription>* list);

    void BatchUpdateTaskInfo(std::list<base_logic::TaskInfo>* list);

    void CreateTaskLog(const int32 id, base_logic::TaskInfo& task);

    void CreateTaskLog(const int32 id, std::list<base_logic::TaskInfo>* list);

    void UpdateTaskLog(const int64 task_id,
                       const int8 state);

 public:
    static void CallBackFectchBatchTask(void* param,
            base_logic::Value* value);

    static void CallBackFectchBatchTempTask(void* param,
            base_logic::Value* value);

    static void CallBackGetTaskPlatDescription(void* param,
                base_logic::Value* value);

 private:
    //scoped_ptr<base_logic::DataControllerEngine> mysql_engine_;
    base_logic::DataEngine* mysql_engine_;
    TASKPLAT_MAP   task_platform_;
    bool task_platform_inited_;
};
}  // namespace crawler_task_logic


#endif /* TASK_DB_H_ */
