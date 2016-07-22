//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月22日 Author: kerry

#ifndef KID_TASK_DB_H_
#define KID_TASK_DB_H_

#include <string>
#include <list>
#include "storage/storage_controller_engine.h"
#include "logic/auto_crawler_infos.h"
#include "basic/basictypes.h"
#include "logic/base_values.h"
#include "basic/scoped_ptr.h"

namespace task_logic {

class TaskDB {
 public:
    TaskDB();
    virtual ~TaskDB();
 public:
    bool FecthBatchTask(std::list<base_logic::TaskInfo>* list,
            const bool is_new = false);

    bool FetchBatchHBase(std::list<base_logic::StorageHBase>* list);

    bool UpdateHBaseState(std::list<base_logic::StorageHBase>* list);

 public:
    static void CallBackFectchBatchTask(void* param,
            base_logic::Value* value);

    static void CallBackFectchBatchHBase(void* param,
                base_logic::Value* value);
 private:
    scoped_ptr<base_logic::DataControllerEngine> mysql_engine_;
};
}  // namespace task_logic


#endif /* TASK_DB_H_ */
