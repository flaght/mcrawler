//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//    2 //  Created on: 2015.1.5 Author: kerry


#ifndef _LOGIN_DB_H_
#define _LOGIN_DB_H_

#include <string>
#include <list>
#include "storage/data_engine.h"
#include "config/config.h"
#include "basic/basictypes.h"
#include "logic/base_values.h"
#include "basic/scoped_ptr.h"
#include "logic/auto_crawler_infos.h"


namespace login_logic {

enum attr_id {
    special_id = 4,
    common_id = 1
};

class LoginDB {
 public:
    LoginDB(config::FileConfig* config);
    virtual ~LoginDB();

 public:
    bool GetCookie(std::list<base_logic::LoginCookie>* cookie_list, const int64 id,
            const int64 from, const int64 count, int64& plat_update_time);

    bool GetCookies(std::list<base_logic::LoginCookie>* cookies_list);

 public:
    static void CallBackGetCookie(void* param,
            base_logic::Value* value);

    static void CallBackGetCookies(void* param,
            base_logic::Value* value);

 private:
    //scoped_ptr<base_logic::DataControllerEngine> mysql_engine_;
    base_logic::DataEngine*      mysql_engine_;
};

}  //  namespace login_logic

#endif


