//  Copyright (c) 2015-2015 The kid Authors. All rights reserved.
//  Created on: 2015年11月7日 Author: kerry

#ifndef KID_SHARE_DATA_ENGINE_H_
#define KID_SHARE_DATA_ENGINE_H_

#include <map>
#include <list>
#include "logic/auto_crawler_infos.h"
#include "thread/base_thread_handler.h"
#include "thread/base_thread_lock.h"
#include "config/config.h"


namespace storage_logic {

typedef std::map<int32, base_logic::TaskPlatDescription> TASKPLAT_MAP;

class ShareDataCache {
 public:
    TASKPLAT_MAP       task_platform_;
};

class ShareDataManager {
 public:
    ShareDataManager();
    virtual ~ShareDataManager();

    void BatchFectchTaskPlatInfo(
            std::list<base_logic::TaskPlatDescription>* list);

    void BatchUpdateTaskInfo(std::list<base_logic::TaskInfo>* list);

 private:
    void Init();
 private:
    struct threadrw_t*     lock_;
    ShareDataCache*        data_cache_;
};


class ShareDataEngine {
 private:
    static ShareDataManager     *manager_;
    static ShareDataEngine      *engine_;

    ShareDataEngine() {}
    virtual ~ShareDataEngine() {}
 public:
    static ShareDataManager* GetShareDataManager() {
        if (manager_ == NULL)
            manager_ = new ShareDataManager();
        return manager_;
    }

    static ShareDataEngine* GetShareDataEngine() {
        if (engine_ == NULL)
            engine_ = new ShareDataEngine();
        return engine_;
    }
};

}   // namespace storage_logic



#endif /* KID_SHARE_DATA_ENGINE_H_ */
