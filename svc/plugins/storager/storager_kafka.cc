//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015.9.28 Author: kerry

#include <sstream>
#include "storager/storager_kafka.h"
#include "storage/storage.h"
#include "logic/logic_unit.h"
#include "basic/basic_util.h"
#include "basic/radom_in.h"

namespace storager_logic {

StroagerKafka::StroagerKafka() {
    if (PRODUCER_INIT_SUCCESS !=
        kafka_producer_.Init(0, "newsparser_task_algo", "192.168.1.245:9092", NULL))
        LOG_ERROR("producer newsparser_task_test init failed");
    else
    	LOG_ERROR("producer newsparser_task_test init success");
}

StroagerKafka::~StroagerKafka() {
    kafka_producer_.Close();
}

void PrintTaskInfo(const base_logic::DictionaryValue* task_info) {
    if(NULL == task_info) return;
    int id;
    std::string value;
    task_info->GetInteger(L"analyze_id", &id);
    task_info->GetString(L"pos_name", &value);
    LOG_DEBUG2("analyze_id = %d pos_name=%s", id, value.c_str());
}

void StroagerKafka::Test() {
	const std::string test = "TTTTTTT";
	kafka_producer_.PushData(test.c_str(),test.length());
}

bool StroagerKafka::AddStorageInfo(const std::list<struct StorageUnit*>& list,
        const int32 type) {
    scoped_ptr<base_logic::DictionaryValue> dict(
                    new base_logic::DictionaryValue());
    std::list<struct StorageUnit*>::const_iterator it =
            list.begin();
    int re = PUSH_DATA_SUCCESS;
    for (; it != list.end(); it++) {
        struct StorageUnit* hbase = (*it);
        LOG_DEBUG("push data to newsparser_task");
        base_logic::DictionaryValue* task_info = new base_logic::DictionaryValue();
        task_info->Set(L"analyze_id",
            base_logic::Value::CreateIntegerValue(base::SysRadom::GetInstance()->GetRandomIntID()));
        task_info->Set(L"task_id", base_logic::Value::CreateBigIntegerValue(hbase->task_id));
        task_info->Set(L"attr_id", base_logic::Value::CreateBigIntegerValue(hbase->attr_id));
        task_info->Set(L"key_name", base_logic::Value::CreateStringValue(hbase->key_name));
        task_info->Set(L"pos_name", base_logic::Value::CreateStringValue(hbase->pos_name));
        task_info->Set(L"max_depth", base_logic::Value::CreateIntegerValue(hbase->max_depth));
        task_info->Set(L"cur_depth", base_logic::Value::CreateIntegerValue(hbase->cur_depth));
        task_info->Set(L"type", base_logic::Value::CreateIntegerValue(type));
        re = kafka_producer_.PushData(task_info);
        LOG_DEBUG2("key_name=%s", hbase->key_name);
        LOG_DEBUG2("pos_name=%s", hbase->pos_name);
        PrintTaskInfo(task_info);
        delete task_info;
    }
    if (PUSH_DATA_SUCCESS == re)
        return true;
    else {
        LOG_ERROR("kafka producer send data failed");
        return false;
    }
}

}  // namespace storager_logic
