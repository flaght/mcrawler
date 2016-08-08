//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015.9.28 Author: kerry

#include <mysql.h>
#include <sstream>
#include "storager/storager_db.h"
#include "storage/storage.h"
#include "logic/logic_unit.h"
#include "storage/storage_controller_engine.h"
#include "basic/basic_util.h"
#include "basic/radom_in.h"

namespace storager_logic {

StroagerDB::StroagerDB() {
    mysql_engine_.reset(base_logic::DataControllerEngine::Create(MYSQL_TYPE));
}

StroagerDB::~StroagerDB() {
}

bool StroagerDB::RecordTempCrawlerTask(
        const std::list<base_logic::TaskInfo>& list) {
    return true;
}

bool StroagerDB::AddStorageInfo(const std::list<struct StorageUnit*>& list,
        const int32 type) {
    scoped_ptr<base_logic::DictionaryValue> dict(
                    new base_logic::DictionaryValue());
    std::list<struct StorageUnit*>::const_iterator it =
            list.begin();
    int re = PUSH_DATA_SUCCESS;
    for (; it != list.end(); it++) {
        struct StorageUnit* hbase = (*it);
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
        //re = kafka_producer_.PushData(task_info);
        delete task_info;
    }
    if (PUSH_DATA_SUCCESS == re)
        return true;
    else {
        LOG_ERROR("kafka producer send data failed");
        return false;
    }
}

bool StroagerDB::GetHBaseInfo(std::list<base_logic::StorageHBase>* list) {
    //  call crawler.proc_GetHBaseInfo()
    bool r = false;
    scoped_ptr<base_logic::DictionaryValue> dict(
                        new base_logic::DictionaryValue());
    std::string sql = "call proc_GetHBaseInfo()";
    base_logic::ListValue* listvalue;
    dict->SetString(L"sql", sql);
    r = mysql_engine_->ReadData(0, (base_logic::Value*)(dict.get()),
            CallBackGetHBaseInfo);
    if (!r)
        return false;
    dict->GetList(L"resultvalue", &listvalue);
    while (listvalue->GetSize()) {
        base_logic::StorageHBase hbase;
        bool r = false;
        base_logic::Value* result_value;
        listvalue->Remove(0, &result_value);
        base_logic::DictionaryValue* dict_result_value =
                (base_logic::DictionaryValue*)(result_value);
        hbase.ValueSerialization(dict_result_value);
        list->push_back(hbase);
        delete dict_result_value;
        dict_result_value = NULL;
    }
    return true;
}

bool StroagerDB::GetTaskPlatTaskDescription(
        std::list<base_logic::TaskPlatDescription>* list) {
    //  call crawler.proc_GetTaskPlatInfo()
    bool r = false;
    scoped_ptr<base_logic::DictionaryValue> dict(
                        new base_logic::DictionaryValue());
    std::string sql = "call proc_GetTaskPlatInfo()";
    base_logic::ListValue* listvalue;
    dict->SetString(L"sql", sql);
    r = mysql_engine_->ReadData(0, (base_logic::Value*)(dict.get()),
            CallBackGetTaskPlatDescription);
    if (!r)
        return false;

    dict->GetList(L"resultvalue", &listvalue);
    while (listvalue->GetSize()) {
        base_logic::TaskPlatDescription description;
        base_logic::Value* result_value;
        listvalue->Remove(0, &result_value);
        description.ValueSerialization(
                (base_logic::DictionaryValue*)(result_value));
        list->push_back(description);
    }
    return true;
}
void StroagerDB::CallBackGetHBaseInfo(void* param,
                base_logic::Value* value) {
    base_logic::DictionaryValue* dict =
             (base_logic::DictionaryValue*)(value);
     base_logic::ListValue* list = new base_logic::ListValue();
     base_storage::DBStorageEngine* engine =
             (base_storage::DBStorageEngine*)(param);
     MYSQL_ROW rows;
     int32 num = engine->RecordCount();
     if (num > 0) {
         while (rows = (*(MYSQL_ROW*)(engine->FetchRows())->proc)) {
             base_logic::DictionaryValue* info_value =
                     new base_logic::DictionaryValue();
             if (rows[0] != NULL)
                 info_value->SetBigInteger(L"taskid", atoll(rows[0]));
             if (rows[1] != NULL)
                 info_value->SetString(L"name", rows[1]);
             if (rows[2] != NULL)
                 info_value->SetString(L"key", rows[2]);
             list->Append((base_logic::Value*)(info_value));
         }
     }
     dict->Set(L"resultvalue", (base_logic::Value*)(list));
}

void StroagerDB::CallBackGetTaskPlatDescription(void* param,
                base_logic::Value* value) {
    base_logic::DictionaryValue* dict =
            (base_logic::DictionaryValue*)(value);
    base_logic::ListValue* list = new base_logic::ListValue();
    base_storage::DBStorageEngine* engine =
            (base_storage::DBStorageEngine*)(param);
    MYSQL_ROW rows;
    int32 num = engine->RecordCount();
    if (num > 0) {
        while (rows = (*(MYSQL_ROW*)(engine->FetchRows())->proc)) {
            base_logic::DictionaryValue* info_value =
                    new base_logic::DictionaryValue();
            if (rows[0] != NULL)
                info_value->SetBigInteger(L"id", atoll(rows[0]));
            if (rows[1] != NULL)
                info_value->SetCharInteger(L"depth",
                    logic::SomeUtils::StringToIntChar(rows[1]));
            if (rows[2] != NULL)
                info_value->SetCharInteger(L"machine",
                    logic::SomeUtils::StringToIntChar(rows[2]));
            if (rows[3] != NULL)
                info_value->SetCharInteger(L"storage",
                    logic::SomeUtils::StringToIntChar(rows[3]));
            if (rows[4] != NULL)
                info_value->SetCharInteger(L"isforge",
                    logic::SomeUtils::StringToIntChar(rows[4]));
            if (rows[5] != NULL)
                info_value->SetCharInteger(L"isover",
                    logic::SomeUtils::StringToIntChar(rows[5]));
            if (rows[6] != NULL)
                info_value->SetString(L"description", rows[6]);
            list->Append((base_logic::Value*)(info_value));
        }
    }
    dict->Set(L"resultvalue", (base_logic::Value*)(list));
}

}  // namespace storager_logic
