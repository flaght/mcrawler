//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//  Created on: 2016年1月5日 Author: kerry

#ifndef LOGIN_SCHDULER_ENGINE_H_
#define LOGIN_SCHDULER_ENGINE_H_

#include <map>
#include <list>
#include "basic/template.h"
#include "login/login_db.h"
#include "logic/auto_crawler_infos.h"
#include "thread/base_thread_handler.h"
#include "thread/base_thread_lock.h"

typedef std::list<base_logic::LoginCookie> COOKIE_LIST;

typedef struct CookiePlatform{
    COOKIE_LIST list;
    int64       current_pos_;
    time_t      update_time_;
};

typedef std::map<int64, CookiePlatform> COOKIE_MAP;

namespace login_logic {

class LoginSchdulerCache {
 public:
    COOKIE_MAP     cookie_map_;
    std::map<int64, int64> update_time_map_;
};


class LoginSchdulerManager {
 public:
    LoginSchdulerManager();
    virtual ~LoginSchdulerManager();

 public:
    void Init(login_logic::LoginDB* login_db);

    void SetBatchCookies();

    void CheckBatchCookie(const int64 plat_id);

    void SetBatchCookie(const int64 plat_id, const int64 from);

    bool FectchBacthCookies(const int64 plat_id, const int64 count,
            std::list<base_logic::LoginCookie>* list);

    void FecthAndSortCookies(const int64 count,
            std::list<base_logic::LoginCookie>& src_list,
            std::list<base_logic::LoginCookie>* dst_list, int64 plat_id);

    int64& GetDatabaseUpdateTimeByPlatId(const int64 plat_id);

    void SetUpdateTime(const int64 plat_id, const int64 update_time);

    void PrintInfo();

 private:
    void SetCookie(const base_logic::LoginCookie& info);

    void Init();

 private:
    struct threadrw_t*           lock_;
    LoginSchdulerCache*          login_cache_;
    login_logic::LoginDB*        login_db_;
};


class LoginSchdulerEngine {
 private:
    static LoginSchdulerManager    *schduler_mgr_;
    static LoginSchdulerEngine     *schduler_engine_;

    LoginSchdulerEngine() {}
    virtual ~LoginSchdulerEngine() {}

 public:
     static LoginSchdulerManager* GetLoginSchdulerManager() {
         if (schduler_mgr_ == NULL)
             schduler_mgr_ = new LoginSchdulerManager();
         return schduler_mgr_;
     }

     static LoginSchdulerEngine* GetLoginSchdulerEngine() {
         if (schduler_engine_ == NULL)
             schduler_engine_ = new LoginSchdulerEngine();
         return schduler_engine_;
     }
};

}  //  namespace login_logic

#endif /* LOGIN_SCHDULER_ENGINE_H_ */
