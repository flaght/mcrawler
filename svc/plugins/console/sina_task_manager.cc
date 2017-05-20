//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.10.2 Author: kerry

#include "sina_task_manager.h"
#include "logic/logic_unit.h"
#include "logic/logic_comm.h"

namespace console_logic {
SinaTaskManager::SinaTaskManager(){
  weibo_manager_ = ConsoleWeiboEngine::GetConsoleWeiboManager();
}

SinaTaskManager::SinaTaskManager(console_logic::ConsoleKafka* producer){
  weibo_manager_ = ConsoleWeiboEngine::GetConsoleWeiboManager();
}

SinaTaskManager::~SinaTaskManager() {
  
}

void SinaTaskManager::CreateTask(console_logic::ConsoleKafka* kafka,
                                 base_logic::TaskInfo& task) {
  int64 task_id = task.id();
   switch (task_id) {
      case SINA_WEIBO_INDEX_FIVE: {
        CreateWeiboIndex1HourReal(kafka,task);
        break;
      }
      default:
        break;
   }

}

void SinaTaskManager::CreateWeiboIndex1HourReal(console_logic::ConsoleKafka* kafka,
                                                const base_logic::TaskInfo& task) {                         
  std::list<console_logic::WeiboInfo> list;
  std::string key_symbol = "{%s}";
  weibo_manager_->Swap(list);
  //base::ConnAddr conn(kafka.svc_id(),kafka.host(),0,"","",kafka.kafka_name());
  //console_logic::ConsoleKafka* kafka_producer = new console_logic::ConsoleKafka(conn);
  while (list.size() > 0) {
    console_logic::WeiboInfo wb = list.front();
    base_logic::TaskInfo btask;
    list.pop_front();
    std::string weibo_url = task.url();
    weibo_url = logic::SomeUtils::StringReplaceUnit(weibo_url, key_symbol,
                                                    wb.weibo_index());
    LOG_MSG2("%s", weibo_url.c_str());
    kafka->AddTaskInfo(task, task.base_polling_time(), weibo_url);
  }
 // if (kafka_producer) {delete kafka_producer; kafka_producer = NULL;}
}

}
