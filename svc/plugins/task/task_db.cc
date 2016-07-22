//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月22日 Author: kerry

#include <mysql.h>
#include <sstream>
#include "task/task_db.h"
#include "storage/storage.h"
#include "storage/storage_controller_engine.h"

namespace task_logic {

TaskDB::TaskDB() {
    mysql_engine_.reset(base_logic::DataControllerEngine::Create(MYSQL_TYPE));
}

TaskDB::~TaskDB() {
}

bool TaskDB::FecthBatchTask(std::list<base_logic::TaskInfo>* list,
        const bool is_new) {
    bool r = false;
    scoped_ptr<base_logic::DictionaryValue> dict(
                new base_logic::DictionaryValue());
    //  call proc_FecthBatchTask()
    std::string sql;
    if (is_new)
        sql  = "call proc_FecthNewTask()";
    else
        sql = "call proc_FecthBatchTask()";
    base_logic::ListValue* listvalue;
    dict->SetString(L"sql", sql);
    r = mysql_engine_->ReadData(0, (base_logic::Value*)(dict.get()),
            CallBackFectchBatchTask);
    if (!r)
        return false;
    dict->GetList(L"resultvalue", &listvalue);
    while (listvalue->GetSize()) {
        base_logic::TaskInfo task;
        base_logic::Value* result_value;
        listvalue->Remove(0, &result_value);
        base_logic::DictionaryValue* dict_result_value =
                (base_logic::DictionaryValue*)(result_value);
        task.ValueSerialization(dict_result_value);
        list->push_back(task);
    }
    return true;
}

bool TaskDB::FetchBatchHBase(std::list<base_logic::StorageHBase>* list) {
    //  call proc_FecthHBaseInfo()
    bool r = false;
    scoped_ptr<base_logic::DictionaryValue> dict(
                new base_logic::DictionaryValue());
    std::string sql = "call proc_FecthHBaseInfo()";
    base_logic::ListValue* listvalue;
    dict->SetString(L"sql", sql);
    r = mysql_engine_->ReadData(0, (base_logic::Value*)(dict.get()),
            CallBackFectchBatchHBase);
    if (!r)
        return r;
    dict->GetList(L"resultvalue", &listvalue);
    while (listvalue->GetSize()) {
        base_logic::StorageHBase hbase;
        base_logic::Value* result_value;
        listvalue->Remove(0, &result_value);
        base_logic::DictionaryValue* dict_result_value =
                (base_logic::DictionaryValue*)(result_value);
        hbase.ValueSerialization(dict_result_value);
        list->push_back(hbase);
    }
    return true;
}

bool TaskDB::UpdateHBaseState(std::list<base_logic::StorageHBase>* list) {
    scoped_ptr<base_logic::DictionaryValue> dict(
                new base_logic::DictionaryValue());
    std::stringstream os;
    while ((*list).size() > 0) {
        base_logic::StorageHBase hbase = (*list).front();
        os << "call proc_UpdateHBaseState("<< hbase.id() << ",2);";
        (*list).pop_front();
    }

    std::string sql = os.str();
    base_logic::ListValue* listvalue;
    dict->SetString(L"sql", sql);
    return mysql_engine_->ReadData(0, (base_logic::Value*)(dict.get()),
            NULL);
}

void TaskDB::CallBackFectchBatchHBase(void* param,
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
                info_value->SetBigInteger(L"taskid", atoll(rows[1]));
            if (rows[2] != NULL)
                info_value->SetInteger(L"attrid", atoll(rows[2]));
            if (rows[3] != NULL)
                info_value->SetString(L"name", rows[3]);
            if (rows[4] != NULL)
                info_value->SetString(L"hkey", rows[4]);
            if (rows[5] != NULL)
                info_value->SetString(L"time", rows[5]);
            list->Append((base_logic::Value*)(info_value));
        }
    }
    dict->Set(L"resultvalue", (base_logic::Value*)(list));
}

void TaskDB::CallBackFectchBatchTask(void* param,
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
                info_value->SetBigInteger(L"attrid", atoll(rows[1]));
            if (rows[2] != NULL)
                info_value->SetInteger(L"depth", atoi(rows[2]));
            if (rows[3] != NULL)
                info_value->SetInteger(L"machine", atoi(rows[3]));
            if (rows[4] != NULL)
                info_value->SetInteger(L"storage", atoi(rows[4]));
            if (rows[5] != NULL)
                info_value->SetInteger(L"islogin", atoi(rows[5]));
            if (rows[6] != NULL)
                info_value->SetInteger(L"isforge", atoi(rows[6]));
            if (rows[7] != NULL)
                info_value->SetInteger(L"isover", atoi(rows[7]));
            if (rows[8] != NULL)
                info_value->SetInteger(L"method", atoi(rows[8]));
            if (rows[9] != NULL)
                info_value->SetBigInteger(L"polling_time", atoll(rows[9])/2);
            if (rows[10] != NULL)
                info_value->SetString(L"url", rows[10]);
            list->Append((base_logic::Value*)(info_value));
        }
    }
    dict->Set(L"resultvalue", (base_logic::Value*)(list));
}
}  // namespace task_logic
