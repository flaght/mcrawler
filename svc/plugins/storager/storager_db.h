//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015.9.28 Author: kerry

#ifndef KID_STORAGER_DB_H_
#define KID_STORAGER_DB_H_

#include <string>
#include <list>
#include "net/comm_head.h"
#include "storage/data_engine.h"
#include "logic/auto_crawler_infos.h"
#include "config/config.h"
#include "basic/basictypes.h"
#include "logic/base_values.h"
#include "basic/scoped_ptr.h"
#include "queue/kafka_producer.h"

namespace storager_logic {

class StroagerDB {
 public:
    StroagerDB(config::FileConfig* config);
    virtual ~StroagerDB();

 public:
    bool AddStorageInfo(const std::list<struct StorageUnit*>& list,
            const int32 type = 1);

    bool GetHBaseInfo(std::list<base_logic::StorageHBase>* list);

    bool RecordTempCrawlerTask(const std::list<base_logic::TaskInfo>& list);

    bool GetTaskPlatTaskDescription(
            std::list<base_logic::TaskPlatDescription>* list);

 public:
    static void CallBackGetHBaseInfo(void* param,
                base_logic::Value* value);

    static void CallBackGetTaskPlatDescription(void* param,
                base_logic::Value* value);

 private:
    base_logic::DataEngine*      mysql_engine_;
    //scoped_ptr<base_logic::DataControllerEngine> mysql_engine_;
};
}  // namespace storager_logic





#endif /* STORAGE_DB_H_ */
