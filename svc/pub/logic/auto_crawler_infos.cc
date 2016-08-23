//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月14日 Author: kerry
#include "logic/auto_crawler_infos.h"

namespace base_logic {

CrawlerScheduler::CrawlerScheduler() {
  data_ = new Data();
}

CrawlerScheduler::CrawlerScheduler(const CrawlerScheduler& crawler_scheduler)
    : data_(crawler_scheduler.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

CrawlerScheduler& CrawlerScheduler::operator =(
    const CrawlerScheduler& crawler_scheduler) {
  if (crawler_scheduler.data_ != NULL) {
    crawler_scheduler.data_->AddRef();
  }

  if (data_ != NULL) {
    data_->Release();
  }

  data_ = crawler_scheduler.data_;
  return (*this);
}

TaskInfo::TaskInfo() {
  data_ = new Data();
}

TaskInfo::TaskInfo(const TaskInfo& task)
    : data_(task.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

TaskInfo& TaskInfo::operator =(const TaskInfo& task) {
  if (task.data_ != NULL) {
    task.data_->AddRef();
  }
  if (data_ != NULL) {
    data_->Release();
  }

  data_ = task.data_;
  return (*this);
}

TaskInfo& TaskInfo::DeepCopy(const TaskInfo& task) {
  if (task.data_ != NULL){
    this->set_attrid(task.attrid());
    this->set_base_polling_time(task.base_polling_time());
    this->set_crawl_num(task.crawl_num());
    this->set_current_depth(task.cur_depth());
    this->set_depth(task.depth());
    this->set_id(task.id());
    this->set_is_finish(task.is_finish());
    this->set_is_forge(task.is_forge());
    this->set_is_login(task.is_login());
    this->set_is_over(task.is_over());
    this->set_last_task_time(task.last_task_time());
    this->set_machine(task.machine());
    this->set_method(task.method());
    this->set_polling_time(task.polling_time());
    this->set_state(task.state());
    this->set_storage(task.storage());
    this->set_type(task.type());
    this->set_url(task.url());
  }

  return (*this);
}

void TaskInfo::ValueSerialization(base_logic::DictionaryValue* dict) {
  dict->GetBigInteger(L"id", &data_->id_);
  dict->GetCharInteger(L"depth", &data_->depth_);
  dict->GetCharInteger(L"machine", &data_->machine_);
  dict->GetCharInteger(L"storage", &data_->storage_);
  dict->GetCharInteger(L"islogin", &data_->is_login_);
  dict->GetCharInteger(L"isforge", &data_->is_forge_);
  dict->GetCharInteger(L"isover", &data_->is_over_);
  dict->GetCharInteger(L"method", &data_->method_);

  int8 cur_depth = 1;
  if (dict->GetCharInteger(L"cur_depth", &cur_depth))
    data_->cur_depth_ = cur_depth;

  int64 cur_time = time(NULL);
  if (dict->GetBigInteger(L"cur_time", &cur_time))
    data_->create_time_ = cur_depth;

  dict->GetBigInteger(L"attrid", &data_->attrid_);
  dict->GetBigInteger(L"polling_time", &data_->base_polling_time_);
  dict->GetString(L"url", &data_->url_);
}

ForgeryIP::ForgeryIP() {
  data_ = new Data();
}

ForgeryIP::ForgeryIP(const ForgeryIP& ip)
    : data_(ip.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

ForgeryIP& ForgeryIP::operator =(const ForgeryIP& ip) {
  if (ip.data_ != NULL) {
    ip.data_->AddRef();
  }
  if (data_ != NULL) {
    data_->Release();
  }

  data_ = ip.data_;
  return (*this);
}
bool ForgeryIP::cmp(const ForgeryIP& t_info, const ForgeryIP& r_info) {
  return t_info.count() < r_info.count();
}

void ForgeryIP::ValueSerialization(base_logic::DictionaryValue* dict) {
  dict->GetInteger(L"id", &data_->id_);
  //dict->GetInteger(L"type", reinterpret_cast<int32*>(&data_->type_));
  dict->GetCharInteger(L"type", &data_->type_);
  dict->GetString(L"ip", &data_->ip_);
  dict->GetString(L"create_time", &data_->create_time_);
}

ForgeryUA::ForgeryUA() {
  data_ = new Data();
}

ForgeryUA::ForgeryUA(const ForgeryUA& ua)
    : data_(ua.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

ForgeryUA& ForgeryUA::operator =(const ForgeryUA& ua) {
  if (ua.data_ != NULL) {
    ua.data_->AddRef();
  }

  if (data_ != NULL) {
    data_->Release();
  }
  data_ = ua.data_;
  return (*this);
}

void ForgeryUA::ValueSerialization(base_logic::DictionaryValue* dict) {
  dict->GetInteger(L"id", &data_->id_);
  //dict->GetInteger(L"type", reinterpret_cast<int32*>(&data_->type_));
  dict->GetCharInteger(L"type", &data_->type_);
  dict->GetString(L"ua", &data_->ua_);
  dict->GetString(L"create_time", &data_->create_time_);
}

TaskPlatDescription::TaskPlatDescription() {
  data_ = new Data();
}

TaskPlatDescription::TaskPlatDescription(const TaskPlatDescription& task_info)
    : data_(task_info.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

TaskPlatDescription& TaskPlatDescription::operator =(
    const TaskPlatDescription& task_info) {
  if (task_info.data_ != NULL) {
    task_info.data_->AddRef();
  }
  if (data_ != NULL) {
    data_->Release();
  }
  data_ = task_info.data_;
  return (*this);
}

void TaskPlatDescription::ValueSerialization(
    base_logic::DictionaryValue* dict) {
  dict->GetBigInteger(L"id", &data_->id_);
  dict->GetCharInteger(L"depth", &data_->depth_);
  dict->GetCharInteger(L"machine", &data_->machine_);
  dict->GetCharInteger(L"storage", &data_->storage_);
  dict->GetCharInteger(L"isforge", &data_->forge_);
  dict->GetCharInteger(L"isover", &data_->over_);
  /*    dict->GetInteger(L"depth", reinterpret_cast<int32*>(&data_->depth_));
   dict->GetInteger(L"machine", reinterpret_cast<int32*>(&data_->machine_));
   dict->GetInteger(L"storge", reinterpret_cast<int32*>(&data_->storage_));
   dict->GetInteger(L"forge", reinterpret_cast<int32*>(&data_->forge_));
   dict->GetInteger(L"over", reinterpret_cast<int32*>(&data_->over_));
   */
  dict->GetString(L"description", &data_->description_);
}

StorageInfo::StorageInfo() {
  data_ = new Data();
}

StorageInfo::StorageInfo(const StorageInfo& info)
    : data_(info.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

StorageInfo& StorageInfo::operator =(const StorageInfo& info) {
  if (info.data_ != NULL) {
    info.data_->AddRef();
  }
  if (data_ != NULL) {
    data_->Release();
  }
  data_ = info.data_;
  return (*this);
}

void StorageInfo::ValueSerialization(base_logic::DictionaryValue* dict) {
  dict->GetBigInteger(L"id", &data_->id_);
  dict->GetBigInteger(L"taskid", &data_->task_id_);
  int8 temp_depth = 0;
  /*dict->GetInteger(L"max_depth", reinterpret_cast<int32*>(&temp_depth));
   data_->max_depth_ = temp_depth;

   int8 cur_temp_depth = 0;
   dict->GetInteger(L"cur_depth", reinterpret_cast<int32*>(&cur_temp_depth));
   data_->cur_depth_ = cur_temp_depth;*/

  dict->GetCharInteger(L"max_depth", &data_->max_depth_);
  dict->GetCharInteger(L"cur_depth", &data_->cur_depth_);
  dict->GetString(L"name", &data_->key_name_);
  dict->GetString(L"pos", &data_->pos_name_);
  dict->GetString(L"time", &data_->time_);
  dict->GetInteger(L"attrid", &data_->attr_id_);
}

StorageHBase::StorageHBase() {
  data_ = new Data();
}

StorageHBase::StorageHBase(const StorageHBase& hbase)
    : data_(hbase.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

StorageHBase& StorageHBase::operator =(const StorageHBase& hbase) {
  if (hbase.data_ != NULL) {
    hbase.data_->AddRef();
  }
  if (data_ != NULL) {
    data_->Release();
  }
  data_ = hbase.data_;
  return (*this);
}

void StorageHBase::ValueSerialization(base_logic::DictionaryValue* dict) {
  dict->GetBigInteger(L"id", &data_->id_);
  dict->GetBigInteger(L"taskid", &data_->task_id_);
  int8 temp_depth = 0;
  /*dict->GetInteger(L"max_depth", reinterpret_cast<int32*>(&temp_depth));
   data_->max_depth_ = temp_depth;

   int8 cur_temp_depth = 0;
   dict->GetInteger(L"cur_depth", reinterpret_cast<int32*>(&cur_temp_depth));
   data_->cur_depth_ = cur_temp_depth;*/

  dict->GetCharInteger(L"max_depth", &data_->max_depth_);
  dict->GetCharInteger(L"cur_depth", &data_->cur_depth_);
  dict->GetString(L"name", &data_->name_);
  dict->GetString(L"hkey", &data_->hkey_);
  dict->GetString(L"time", &data_->time_);
  dict->GetInteger(L"attrid", &data_->attr_id_);
}

LoginCookie::LoginCookie() {
  data_ = new Data();
}

LoginCookie::LoginCookie(const LoginCookie& login_cookie)
    : data_(login_cookie.data_) {
  if (data_ != NULL)
    data_->AddRef();
}

LoginCookie& LoginCookie::operator=(const LoginCookie& login_cookie) {
  if (login_cookie.data_ != NULL)
    login_cookie.data_->AddRef();
  if (data_ != NULL)
    data_->Release();
  data_ = login_cookie.data_;
  return (*this);
}

void LoginCookie::ValueSerialization(base_logic::DictionaryValue* dict) {
  dict->GetBigInteger(L"cookie_id", &data_->cookie_id_);
  dict->GetBigInteger(L"cookie_attr_id", &data_->cookie_attr_id_);
  dict->GetBigInteger(L"last_time", &data_->update_last_time_);
  dict->GetString(L"cookie_body", &data_->cookie_body);
  dict->GetString(L"username", &data_->username);
  dict->GetString(L"passwd", &data_->passwd);
}

}  // namespace base_logic
