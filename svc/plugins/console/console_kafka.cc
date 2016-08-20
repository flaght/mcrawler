//  Copyright (c) 2015-2016 The KID Authors. All rights reserved.
//  Created on: 2016.8.18 Author: kerry

#include "console_kafka.h"
#include "logic/logic_comm.h"

namespace console_logic {

ConsoleKafka::ConsoleKafka() {
  if (PRODUCER_INIT_SUCCESS !=
      kafka_producer_.Init(0, "kafka_newsparser_algo", "192.168.1.85:9092", NULL))
      LOG_ERROR("producer kafka_newsparser_algo init failed");
  else
    LOG_ERROR("producer kafka_newsparser_algo init success");
}

ConsoleKafka::~ConsoleKafka() {
  kafka_producer_.Close();
}

bool ConsoleKafka::AddKafkaTaskInfo(const int64 task_id, const int64 attr_id,
                                    const int32 max_depth, const int32 cur_depth,
                                    const int32 method,const int32 machine,const int32 storage,
                                    const int32 is_login, const int32 is_over,
                                    const int64 polling_time, const int64 last_time,
                                    const std::string& url) {

  base_logic::DictionaryValue* task_info = new base_logic::DictionaryValue();
  /*{"id":560, "attrid":14, "depth":3, "cur_depth":2, "method":2, "url":"http://tech.caijing.com.cn/index.html"}
   * */
  int re = PUSH_DATA_SUCCESS;
  task_info->Set(L"id",base_logic::Value::CreateBigIntegerValue(task_id));
  task_info->Set(L"attrid", base_logic::Value::CreateBigIntegerValue(attr_id));
  task_info->Set(L"depth", base_logic::Value::CreateIntegerValue(max_depth));
  task_info->Set(L"cur_depth", base_logic::Value::CreateIntegerValue(cur_depth));
  task_info->Set(L"method", base_logic::Value::CreateIntegerValue(method));
  task_info->Set(L"machine", base_logic::Value::CreateIntegerValue(machine));
  task_info->Set(L"storage", base_logic::Value::CreateIntegerValue(storage));
  task_info->Set(L"is_login", base_logic::Value::CreateIntegerValue(is_login));
  task_info->Set(L"is_over", base_logic::Value::CreateIntegerValue(is_over));
  task_info->Set(L"polling_time", base_logic::Value::CreateBigIntegerValue(polling_time));
  task_info->Set(L"last_time", base_logic::Value::CreateBigIntegerValue(last_time));
  task_info->Set(L"url", base_logic::Value::CreateStringValue(url));
  re = kafka_producer_.PushData(task_info);
  delete task_info;
  if (PUSH_DATA_SUCCESS == re)
      return true;
  else {
      LOG_ERROR("kafka producer send data failed");
      return false;
  }
}

}
