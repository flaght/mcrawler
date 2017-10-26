//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月14日 Author: kerry

#ifndef AUTO_CRAWLER_INFOS_H_
#define AUTO_CRAWLER_INFOS_H_

#include <string>
#include <map>
#include <list>

#include "basic/basictypes.h"
#include "logic/base_values.h"

enum TASKSTAE {
  TASK_WAIT = 0,
  TASK_SEND = 1,
  TASK_RECV = 2,
  TASK_READY = 3,
  TASK_EXECUING = 4,
  TASK_STORAGE = 5,
  TASK_STORAGED = 6,
  TASK_EXECUED = 7,
  TASK_ERROR = 10
};

enum TASKTYPE {
  UNKNOW_TASK = 0,
  MAIN_LASTING_TASK = 1,
  MAIN_SHORT_TASK = 2,
  TEMP_LASTING_TASK = 3,
  TEMP_SHORT_TASK = 4,
  NEWS_DETAIL_TASK = 5
};

enum ANALYTICALSTATE {
  ANALYTICAL_WAIT = 0,
  ANALYTICAL_EXECUTING = 1,
  ANALYTICAL_EXECUED = 2
};

enum CRAWLERTYPE {
  STORAGE_REDIS = 0,
  STORAGE_HBASE = 1,
  STORAGE_MYSQL = 2,
  STORAGE_TEXT = 3,
  STORAGE_MEMCACHE = 4
};

namespace base_logic {

class TaskInfo;
typedef std::map<int64, TaskInfo> TASKINFO_MAP;

class CrawlerScheduler {
 public:
  CrawlerScheduler(bool is_inlock = false);

  CrawlerScheduler(const CrawlerScheduler& crawler_scheduler);

  CrawlerScheduler& operator =(const CrawlerScheduler& crawler_scheduler);

  ~CrawlerScheduler() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  void set_id(const int32 id) {
    data_->id_ = id;
  }

  void set_task(TaskInfo& task);

  void del_task(TaskInfo& task);

  void sync_task_count() {
    data_->task_count_ = data_->task_infos_.size();
  }

  void set_socket(const int socket) {
    data_->socket_ = socket;
  }
  void set_port(const int port) {
    data_->port_ = port;
  }
  void set_ip(const std::string& ip) {
    data_->ip_ = ip;
  }
  void set_new_task_count(const int32 task_count) {
    data_->task_count_ = task_count;
  }

  void set_available_resource(const int32 available_resource_count) {
    data_->task_count_ = available_resource_count;
  }

  void set_mac(const std::string& mac) {
    data_->mac_ = mac;
  }
  void set_password(const std::string& password) {
    data_->password_ = password;
  }

  void set_recv_last_time(const time_t recv_last_time) {
    data_->recv_last_time_ = recv_last_time;
  }

  void set_send_last_time(const time_t send_last_time) {
    data_->send_last_time_ = send_last_time;
  }

  void set_is_effective(bool is_effective) {
    data_->is_effective_ = is_effective;
  }

  void add_send_error_count() {
    __sync_fetch_and_add(&data_->send_error_count_, 1);
  }

  void add_recv_error_count() {
    __sync_fetch_and_add(&data_->recv_error_count_, 1);
  }

  void add_task_num_count() {
    __sync_fetch_and_add(&data_->task_count_, 1);
  }

  int32 id() const {
    return data_->id_;
  }
  int task_count() const {
    return data_->task_count_;
  }
  int socket() const {
    return data_->socket_;
  }
  int port() const {
    return data_->port_;
  }
  time_t send_last_time() const {
    return data_->send_last_time_;
  }
  time_t recv_last_time() const {
    return data_->recv_last_time_;
  }
  int32 send_error_count() const {
    return data_->send_error_count_;
  }
  bool is_effective() const {
    return data_->is_effective_;
  }
  std::string& ip() const {
    return data_->ip_;
  }
  std::string& mac() const {
    return data_->mac_;
  }
  std::string& password() const {
    return data_->password_;
  }

  static inline bool cmp(const CrawlerScheduler& t_scheduler,
                         const CrawlerScheduler& r_scheduler) {
    return t_scheduler.task_count() < r_scheduler.task_count();
  }

  int32 exec_task_count() {
    return data_->task_infos_.size();
  }

  void GetTaskSetId(std::list<int64>& list);

 private:
  class Data {
   public:
    Data(bool is_inlock)
        : id_(0),
          task_count_(0),
          send_error_count_(0),
          recv_error_count_(0),
          socket_(0),
          port_(0),
          is_effective_(true),
          send_last_time_(0),
          recv_last_time_(0),
          is_inlock_(false),
          refcount_(1){
    }

    ~Data() {
      task_infos_.clear();
      //if (is_inlock_)
      //DeinitThreadrw(lock_);
    }

   public:
    int32 id_;
    int32 task_count_;
    int32 send_error_count_;
    int32 recv_error_count_;
    int socket_;
    int port_;
    bool is_effective_;
    time_t send_last_time_;
    time_t recv_last_time_;
    std::string ip_;
    std::string password_;
    std::string mac_;
    std::map<int64, TaskInfo> task_infos_;
    bool is_inlock_;

    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }
    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }

   private:
    int refcount_;
  };
  Data* data_;
};

class TaskInfo {
 public:
  TaskInfo();

  TaskInfo(const TaskInfo& task);

  TaskInfo& operator =(const TaskInfo& task);

  TaskInfo& DeepCopy(const TaskInfo& task);

  ~TaskInfo() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  static bool cmp(const base_logic::TaskInfo& t_task,
                  const base_logic::TaskInfo& r_task) {
    //return t_task.totoal_polling_time() <= r_task.totoal_polling_time();
    return Data::cmp(t_task.data_,r_task.data_);
  }

  static bool create_time_sort(const base_logic::TaskInfo& t_task,
                               const base_logic::TaskInfo& r_task) {
    return t_task.create_time() <= r_task.create_time();
  }

  void set_id(const int64 id) {
    data_->id_ = id;
  }

  void set_pid(const int64 pid) {
    data_->pid_ = pid;
  }

  void set_depth(const int8 depth) {
    data_->depth_ = depth;
  }
  void set_machine(const int8 machine) {
    data_->machine_ = machine;
  }
  void set_storage(const int8 storage) {
    data_->storage_ = storage;
  }
  void set_method(const int8 method) {
    data_->method_ = method;
  }
  void set_is_login(const int8 is_login) {
    data_->is_login_ = is_login;
  }
  void set_is_finish(const int64 is_finish) {
    data_->is_finish_ = is_finish;
  }
  void set_is_forge(const int8 is_forge) {
    data_->is_forge_ = is_forge;
  }
  void set_is_over(const int8 is_over) {
    data_->is_over_ = is_over;
  }
  void set_state(const int8 state) {
    data_->state_ = state;
  }
  void set_url(const std::string& url) {
    data_->url_ = url;
  }
  void set_crawl_num(const int64 crawl_num) {
    data_->crawl_num_ = crawl_num;
  }
  void set_attrid(const int64 attrid) {
    data_->attrid_ = attrid;
  }
  void set_polling_time(const int64 polling_time) {
    data_->polling_time_ = polling_time;
  }

  void set_base_polling_time(const int64 base_polling_time) {
    data_->base_polling_time_ = base_polling_time;
  }

  void set_last_task_time(const int64 last_task_time) {
    data_->last_task_time_ = last_task_time;
  }

  void set_current_depth(const int8 current_depth) {
    data_->cur_depth_ = current_depth;
  }

  void set_type(const int8 type) {
    data_->type_ = type;
  }

  void set_svc_id(const int32 svc_id) {
    data_->svc_id_= svc_id;
  }

  void set_cralwer_id(const int32 crawler_id) {
    data_->crawler_id_ = crawler_id;
  }

  void create_task_time(const int64 create_time = 0) {
    if (create_time == 0)
      data_->create_time_ = time(NULL);
    else
      data_->create_time_ = create_time;
  }

  void update_time(const int64 update_time = 0, const int64 radom_num = 0,
                   bool is_first = false) {
    if (update_time == 0)
      data_->last_task_time_ = time(NULL);
    else
      data_->last_task_time_ = update_time;

    //  更新下一轮时间 避免多个任务同一时间执行
    if (is_first)
      data_->polling_time_ = (time(NULL) + radom_num)
          % data_->base_polling_time_;
    else
      data_->polling_time_ = (time(NULL) + radom_num)
          % data_->base_polling_time_ + data_->base_polling_time_;
  }

  int64 id() const {
    return data_->id_;
  }

  int64 pid() const {
    return data_->pid_;
  }
  int64 crawl_num() const {
    return data_->crawl_num_;
  }
  int8 depth() const {
    return data_->depth_;
  }
  int8 cur_depth() const {
    return data_->cur_depth_;
  }
  int8 machine() const {
    return data_->machine_;
  }
  int8 storage() const {
    return data_->storage_;
  }
  int8 method() const {
    return data_->method_;
  }
  int8 state() const {
    return data_->state_;
  }
  int8 is_login() const {
    return data_->is_login_;
  }
  int8 is_forge() const {
    return data_->is_forge_;
  }
  int8 is_over() const {
    return data_->is_over_;
  }
  int8 type() const {
    return data_->type_;
  }

  int32 svc_id() const {
    return data_->svc_id_;
  }

  int64 is_finish() const {
    return data_->is_finish_;
  }
  int64 create_time() const {
    return data_->create_time_;
  }
  int64 polling_time() const {
    return data_->polling_time_;
  }
  int64 base_polling_time() const {
    return data_->base_polling_time_;
  }
  int64 last_task_time() const {
    return data_->last_task_time_;
  }
  int64 totoal_polling_time() const {
    return data_->last_task_time_ + data_->polling_time_;
  }
  int64 attrid() const {
    return data_->attrid_;
  }

  int32 crawler_id() const {
    return data_->crawler_id_;
  }

  std::string url() const {
    return data_->url_;
  }

  void release_isfinish() {
    __sync_fetch_and_sub(&data_->is_finish_, 1);
  }

  void ValueSerialization(base_logic::DictionaryValue* dict);

 private:
  class Data {
   public:
    Data()
        : id_(0),
          pid_(0),
          type_(UNKNOW_TASK),
          depth_(1),
          cur_depth_(1),
          machine_(0),
          storage_(0),
          is_login_(0),
          is_forge_(0),
          is_over_(0),
          state_(0),
          method_(0),
          svc_id_(0),
          is_finish_(0),
          attrid_(0),
          polling_time_(10),
          base_polling_time_(10),
          last_task_time_(time(NULL)),
          create_time_(time(NULL)),
          crawl_num_(0),
          crawler_id_(0),
          total_polling_time_(total_polling_time_ + last_task_time_),
          refcount_(1){
    }

   public:
    int64 id_;
    int64 pid_;  //任务父id
    int8 type_;
    int8 depth_;
    int8 cur_depth_;
    int8 machine_;
    int8 storage_;
    int8 is_login_;
    int8 is_forge_;
    int8 is_over_;
    int8 state_;
    int8 method_;
    int32 svc_id_;
    int64 is_finish_;
    int64 attrid_;
    int64 polling_time_;
    int64 base_polling_time_;
    int64 last_task_time_;
    int64 create_time_;
    int64 crawl_num_;  //Invalid
    int64 crawler_id_;
    int64 total_polling_time_;
    std::string url_;

    static bool cmp(const Data* t_data, const Data* r_data) {
      return (t_data->last_task_time_ + t_data->polling_time_)
          < (r_data->last_task_time_ + r_data->polling_time_);
    }

    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }

    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }

   private:
    int refcount_;
  };

  Data* data_;
};

class ForgeryIP {
 public:
  ForgeryIP();
  ForgeryIP(const ForgeryIP& ip);

  ForgeryIP& operator =(const ForgeryIP& ip);

  ~ForgeryIP() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  void set_id(const int32 id) {
    data_->id_ = id;
  }
  void set_type(const int8 type) {
    data_->type_ = type;
  }
  void set_create_time(const std::string& create_time) {
    data_->create_time_ = create_time;
  }
  void set_ip(const std::string& ip) {
    data_->ip_ = ip;
  }

  void Addcount() {
    __sync_fetch_and_add(&data_->count_, 1);
  }

  void Refcount() {
    __sync_fetch_and_sub(&data_->count_, 1);
  }

  int32 id() const {
    return data_->id_;
  }
  int8 type() const {
    return data_->type_;
  }
  int64 count() const {
    return data_->count_;
  }
  const std::string& create_time() const {
    return data_->create_time_;
  }
  const std::string& ip() const {
    return data_->ip_;
  }

  static bool cmp(const ForgeryIP& t_info, const ForgeryIP& r_info);

  void ValueSerialization(base_logic::DictionaryValue* dict);

  class Data {
   public:
    Data()
        : id_(0),
          type_(0),
          count_(0),
          refcount_(1){
    }

   public:
    int32 id_;
    int8 type_;
    int64 count_;
    std::string create_time_;
    std::string ip_;
    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }

    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }
   private:
    int refcount_;
  };

  Data* data_;
};

class ForgeryUA {
 public:
  ForgeryUA();
  ForgeryUA(const ForgeryUA& ua);

  ForgeryUA& operator =(const ForgeryUA& ua);

  ~ForgeryUA() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  void set_id(const int32 id) {
    data_->id_ = id;
  }
  void set_type(const int8 type) {
    data_->type_ = type;
  }
  void set_create_time(const std::string& create_time) {
    data_->create_time_ = create_time;
  }
  void set_ua(const std::string& ua) {
    data_->ua_ = ua;
  }

  void Addcount() {
    __sync_fetch_and_add(&data_->count_, 1);
  }

  void Refcount() {
    __sync_fetch_and_sub(&data_->count_, 1);
  }

  int32 id() const {
    return data_->id_;
  }
  int8 type() const {
    return data_->type_;
  }
  const std::string& create_time() const {
    return data_->create_time_;
  }
  const std::string& ua() const {
    return data_->ua_;
  }
  int64 count() const {
    return data_->count_;
  }
  void ValueSerialization(base_logic::DictionaryValue* dict);

  class Data {
   public:
    Data()
        : id_(0),
          type_(0),
          count_(0),
          refcount_(1){
    }

   public:
    int32 id_;
    int8 type_;
    int64 count_;
    std::string create_time_;
    std::string ua_;
    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }

    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }
   private:
    int refcount_;
  };

  Data* data_;
};

class TaskPlatDescription {
 public:
  TaskPlatDescription();
  TaskPlatDescription(const TaskPlatDescription& task_info);

  TaskPlatDescription& operator =(const TaskPlatDescription& task_info);
  ~TaskPlatDescription() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  void set_id(const int64 id) {
    data_->id_ = id;
  }
  void set_depth(const int8 depth) {
    data_->depth_ = depth;
  }
  void set_machine(const int8 machine) {
    data_->machine_ = machine;
  }
  void set_storage(const int8 storage) {
    data_->storage_ = storage;
  }
  void set_over(const int8 over) {
    data_->over_ = over;
  }
  void set_forge(const int8 forge) {
    data_->forge_ = forge;
  }
  void set_description(const std::string& description) {
    data_->description_ = description;
  }

  int64 id() const {
    return data_->id_;
  }
  int8 depth() const {
    return data_->depth_;
  }
  int8 machine() const {
    return data_->machine_;
  }
  int8 storage() const {
    return data_->storage_;
  }
  int8 over() const {
    return data_->over_;
  }
  int8 forge() const {
    return data_->forge_;
  }
  const std::string& description() const {
    return data_->description_;
  }

  void ValueSerialization(base_logic::DictionaryValue* dict);

  class Data {
   public:
    Data()
        : id_(0),
          depth_(0),
          machine_(0),
          storage_(0),
          over_(0),
          forge_(0),
          refcount_(1){
    }

   public:
    int64 id_;
    int8 depth_;
    int8 machine_;
    int8 storage_;
    int8 over_;
    int8 forge_;
    std::string description_;

    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }

    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }

   private:
    int refcount_;
  };

  Data* data_;
};

class StorageInfo {
 public:
  StorageInfo();
  StorageInfo(const StorageInfo& info);

  StorageInfo& operator =(const StorageInfo& info);

  ~StorageInfo() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  void set_id(const int64 id) {
    data_->id_ = id;
  }
  void set_taskid(const int64 task_id) {
    data_->task_id_ = task_id;
  }
  void set_type(const int8 type) {
    data_->type_ = type;
  }
  void set_max_depth(const int8 max_depth) {
    data_->max_depth_ = max_depth;
  }
  void set_cur_depth(const int8 cur_depth) {
    data_->cur_depth_ = cur_depth;
  }
  void set_name(const std::string& key_name) {
    data_->key_name_ = key_name;
  }
  void set_hkey(const std::string& pos_name) {
    data_->pos_name_ = pos_name;
  }
  void set_time(const std::string& time) {
    data_->time_ = time;
  }
  void set_attrid(const int32 attr_id) {
    data_->attr_id_ = attr_id;
  }
  void set_state(const int8 state) {
    data_->state_ = state;
  }

  int64 id() const {
    return data_->id_;
  }
  int64 taskid() const {
    return data_->task_id_;
  }
  int32 attrid() const {
    return data_->attr_id_;
  }
  int8 max_depth() const {
    return data_->max_depth_;
  }
  int8 cur_depth() const {
    return data_->cur_depth_;
  }
  int8 state() const {
    return data_->state_;
  }
  int8 type() const {
    return data_->type_;
  }
  const std::string& key_name() const {
    return data_->key_name_;
  }
  const std::string& pos_name() const {
    return data_->pos_name_;
  }
  const std::string& time() const {
    return data_->time_;
  }

  void ValueSerialization(base_logic::DictionaryValue* dict);

  class Data {
   public:
    Data()
        : id_(0),
          task_id_(0),
          attr_id_(0),
          max_depth_(1),
          cur_depth_(1),
          state_(ANALYTICAL_WAIT),
          type_(0),
          refcount_(1){
    }

   public:
    int64 id_;
    int64 task_id_;
    int32 attr_id_;
    int8 max_depth_;
    int8 cur_depth_;
    int8 state_;
    int8 type_;
    std::string key_name_;
    std::string pos_name_;
    std::string time_;

    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }

    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }

   private:
    int refcount_;
  };
  Data* data_;
};

class StorageHBase {
 public:
  StorageHBase();
  StorageHBase(const StorageHBase& hbase);

  StorageHBase& operator =(const StorageHBase& hbase);

  ~StorageHBase() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  void set_id(const int64 id) {
    data_->id_ = id;
  }
  void set_taskid(const int64 task_id) {
    data_->task_id_ = task_id;
  }
  void set_max_depth(const int8 max_depth) {
    data_->max_depth_ = max_depth;
  }
  void set_cur_depth(const int8 cur_depth) {
    data_->cur_depth_ = cur_depth;
  }
  void set_name(const std::string& name) {
    data_->name_ = name;
  }
  void set_hkey(const std::string& hkey) {
    data_->hkey_ = hkey;
  }
  void set_time(const std::string& time) {
    data_->time_ = time;
  }
  void set_attrid(const int32 attr_id) {
    data_->attr_id_ = attr_id;
  }
  void set_state(const int8 state) {
    data_->state_ = state;
  }

  int64 id() const {
    return data_->id_;
  }
  int64 taskid() const {
    return data_->task_id_;
  }
  int32 attrid() const {
    return data_->attr_id_;
  }
  int8 max_depth() const {
    return data_->max_depth_;
  }
  int8 cur_depth() const {
    return data_->cur_depth_;
  }
  int8 state() const {
    return data_->state_;
  }
  const std::string& name() const {
    return data_->name_;
  }
  const std::string& hkey() const {
    return data_->hkey_;
  }
  const std::string& time() const {
    return data_->time_;
  }

  void ValueSerialization(base_logic::DictionaryValue* dict);

  class Data {
   public:
    Data()
        : id_(0),
          task_id_(0),
          attr_id_(0),
          max_depth_(1),
          cur_depth_(1),
          state_(ANALYTICAL_WAIT),
          refcount_(1){
    }

   public:
    int64 id_;
    int64 task_id_;
    int32 attr_id_;
    int8 max_depth_;
    int8 cur_depth_;
    int8 state_;
    std::string name_;
    std::string hkey_;
    std::string time_;

    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }

    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }

   private:
    int refcount_;
  };
  Data* data_;
};

class LoginCookie {
 public:
  LoginCookie();
  LoginCookie(const LoginCookie& login_cookie);
  LoginCookie& operator=(const LoginCookie& login_cookie);
  ~LoginCookie() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  void update_time() {
    data_->send_last_time_ = time(NULL);
  }

  void set_cookie_id(const int64 id) {
    data_->cookie_id_ = id;
  }

  void set_cookie_attr_id(const int64 id) {
    data_->cookie_attr_id_ = id;
  }
  void set_cookie_body(const std::string& cookie_body) {
    data_->cookie_body = cookie_body;
  }

  void set_cookie_last_time(time_t send_last_time) {
    data_->send_last_time_ = send_last_time;
  }

  void set_username(const std::string& username) {
    data_->username = username;
  }

  void set_passwd(const std::string& passwd) {
    data_->passwd = passwd;
  }

  void set_is_read(bool IsRead) {
    data_->is_read = IsRead;
  }

  bool is_over_time(time_t appoint_time) {
    if (!data_->is_first) {
      data_->is_first = true;
      return true;
    } else {
      return (data_->send_last_time_ + 3600) < appoint_time ? true : false;
    }
  }

  void update_send_time(time_t appoint_time) {
    data_->send_last_time_ = appoint_time;
  }

  time_t send_last_time() const {
    return data_->send_last_time_;
  }

  int64 get_cookie_id() const {
    return data_->cookie_id_;
  }
  int64 get_cookie_attr_id() const {
    return data_->cookie_attr_id_;
  }
  const std::string& get_cookie_body() const {
    return data_->cookie_body;
  }

  const std::string& get_username() const {
    return data_->username;
  }

  const std::string& get_passwd() const {
    return data_->passwd;
  }

  bool get_is_read() const {
    return data_->is_read;
  }

  time_t get_update_time() const {
    return data_->update_last_time_;
  }

  int32 rule() const {
    return data_->rule_;
  }

  LoginCookie& DeepCopy(const LoginCookie& cookie);

  static inline bool cmp(const LoginCookie& t_login_cookie,
                         const LoginCookie& r_login_cookie) {
    return t_login_cookie.send_last_time() > r_login_cookie.send_last_time();
  }

  void ValueSerialization(base_logic::DictionaryValue* dict);

  class Data {
   public:
    Data()
        : cookie_id_(0),
          cookie_attr_id_(0),
          rule_(0),
          send_last_time_(0),
          update_last_time_(0),
          is_read(false),
          is_first(false),
          refcount_(1){
    }
   public:
    int64 cookie_id_;
    int64 cookie_attr_id_;
    int32 rule_;
    time_t send_last_time_;
    time_t update_last_time_;
    std::string cookie_body;
    std::string username;
    std::string passwd;
    bool is_read;
    bool is_first;

    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }
    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }
   private:
    int refcount_;
  };
  Data* data_;
};

}  // namespace base_logic

#endif /* CRAWLER_MANGER_INFOS_H_ */
