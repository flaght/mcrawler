//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月24日 Author: kerry


#include <mysql.h>
#include "forgery/forgery_db.h"
#include "logic/logic_unit.h"

namespace forgery_logic {

ForgeryDB::ForgeryDB(config::FileConfig* config) {
    //mysql_engine_.reset(base_logic::DataControllerEngine::Create(MYSQL_TYPE));
  mysql_engine_ = base_logic::DataEngine::Create(MYSQL_TYPE);
  mysql_engine_->InitParam(config->mysql_db_list_);
}

ForgeryDB::~ForgeryDB() {
  if (mysql_engine_) {
    delete mysql_engine_;
    mysql_engine_ = NULL;
  }
}

bool ForgeryDB::FectchBatchForgeryIP(std::list<base_logic::ForgeryIP>* list) {
    bool r = false;
    scoped_ptr<base_logic::DictionaryValue> dict(
                    new base_logic::DictionaryValue());
    std::string sql = "call proc_FetchBatchIP()";
    base_logic::ListValue* listvalue;
    dict->SetString(L"sql", sql);
    r = mysql_engine_->ReadData(0, (base_logic::Value*)(dict.get()),
            CallBackFectchBatchForgeryIP);
    if (!r)
        return false;
    dict->GetList(L"resultvalue", &listvalue);
    while (listvalue->GetSize()) {
        base_logic::ForgeryIP ip;
        base_logic::Value* result_value;
        listvalue->Remove(0, &result_value);
        base_logic::DictionaryValue* dict_result_value =
                (base_logic::DictionaryValue*)(result_value);
        ip.ValueSerialization(dict_result_value);
        list->push_back(ip);
        delete dict_result_value;
        dict_result_value = NULL;
    }
    return true;
}

bool ForgeryDB::FectchBatchForgeryUA(std::list<base_logic::ForgeryUA>* list) {
    bool r = false;
    scoped_ptr<base_logic::DictionaryValue> dict(
                    new base_logic::DictionaryValue());
    std::string sql = "call proc_FetchBatchUA()";
    base_logic::ListValue* listvalue;
    dict->SetString(L"sql", sql);
    r = mysql_engine_->ReadData(0, (base_logic::Value*)(dict.get()),
            CallBackFectchBatchForgeryUA);
    if (!r)
        return r;
    dict->GetList(L"resultvalue", &listvalue);
    while (listvalue->GetSize()) {
        base_logic::ForgeryUA ua;
        base_logic::Value* result_value;
        listvalue->Remove(0, &result_value);
        base_logic::DictionaryValue* dict_result_value =
                (base_logic::DictionaryValue*)(result_value);
        ua.ValueSerialization(dict_result_value);
        list->push_back(ua);
        delete dict_result_value;
        dict_result_value = NULL;
    }
    return true;
}
void ForgeryDB::CallBackFectchBatchForgeryIP(void* param,
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
                info_value->SetString(L"ip", rows[1]);
            if (rows[2] != NULL)
                info_value->SetCharInteger(L"type",
                        logic::SomeUtils::StringToIntChar(rows[2]));
            if (rows[3] != NULL)
                info_value->SetString(L"create_time", rows[3]);
            list->Append((base_logic::Value*)(info_value));
        }
    }
    dict->Set(L"resultvalue", (base_logic::Value*)(list));
}

void ForgeryDB::CallBackFectchBatchForgeryUA(void* param,
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
                info_value->SetString(L"ua", rows[1]);
            if (rows[2] != NULL)
                info_value->SetInteger(L"type", atoll(rows[2]));
            if (rows[3] != NULL)
                info_value->SetString(L"create_time", rows[3]);
            list->Append((base_logic::Value*)(info_value));
        }
    }
    dict->Set(L"resultvalue", (base_logic::Value*)(list));
}

}  // namespace forgery_logic
