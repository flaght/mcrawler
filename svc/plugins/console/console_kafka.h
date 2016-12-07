//  Copyright (c) 2015-2016 The KID Authors. All rights reserved.
//  Created on: 2016.8.18 Author: kerry

#ifndef KID_CONSOLE_KAFKA_H__
#define KID_CONSOLE_KAFKA_H__

#include <list>
#include "logic/auto_crawler_infos.h"
#include "queue/kafka_producer.h"

namespace console_logic {

class ConsoleKafka {
 public:
  ConsoleKafka(config::FileConfig* config);
  virtual ~ConsoleKafka();
 public:
  void AddTaskInfo(const base_logic::TaskInfo& task,
                   const int64 base_polling_time,
                   const std::string& url);

  bool AddKafkaTaskInfo(const int64 task_id, const int64 attr_id,
                        const int32 max_depth, const int32 cur_depth,
                        const int32 method,const int32 machine,const int32 storage,
                        const int32 is_login, const int32 is_over,
                        const int64 polling_time, const int64 last_time,
                        const std::string& url);
 private:
  kafka_producer     kafka_producer_;
};
}
#endif
