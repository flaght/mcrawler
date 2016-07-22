//  Copyright (c) 2015-2015 The kid Authors. All rights reserved.
//  Created on: 2015年11月7日 Author: kerry

#include "storager/share_data_engine.h"
#include <string>
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "basic/template.h"
#include "basic/radom_in.h"


namespace storage_logic {

ShareDataManager* ShareDataEngine::manager_ = NULL;
ShareDataEngine* ShareDataEngine::engine_ = NULL;

ShareDataManager::ShareDataManager() {
    data_cache_ = new ShareDataCache();
    Init();
}

ShareDataManager::~ShareDataManager() {
    DeinitThreadrw(lock_);
}

void ShareDataManager::Init() {
    InitThreadrw(&lock_);
}

void ShareDataManager::BatchFectchTaskPlatInfo(
        std::list<base_logic::TaskPlatDescription>* list) {
    base_logic::WLockGd lk(lock_);
    while ((*list).size() > 0) {
        base_logic::TaskPlatDescription info = (*list).front();
        (*list).pop_front();
        data_cache_->task_platform_[info.id()] = info;
    }
}

void ShareDataManager::BatchUpdateTaskInfo(
        std::list<base_logic::TaskInfo>* list) {
    base_logic::RLockGd lk(lock_);
    std::list<base_logic::TaskInfo>::iterator it =
            (*list).begin();
    for (; it != (*list).end(); it++) {
        bool r = false;
        base_logic::TaskInfo info = (*it);
        base_logic::TaskPlatDescription  descripition;
        r = base::MapGet<TASKPLAT_MAP, TASKPLAT_MAP::iterator,
                int64, base_logic::TaskPlatDescription>(
                  data_cache_->task_platform_,
                  info.attrid(), descripition);
        if (r) {
            info.set_is_forge(descripition.forge());
            info.set_machine(descripition.machine());
            info.set_storage(descripition.storage());
            info.set_is_over(descripition.over());
        } else {
            //  若id不存在，则需到数据库获取 是否有新的
            continue;
        }
    }
}

}  // namespace storage_logic
