//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月23日 Author: kerry

#ifndef KID_FORGERY_DB_H_
#define KID_FORGERY_DB_H_

#include <string>
#include <list>
#include "storage/storage_controller_engine.h"
#include "logic/auto_crawler_infos.h"
#include "basic/basictypes.h"
#include "logic/base_values.h"
#include "basic/scoped_ptr.h"

namespace forgery_logic {

class ForgeryDB {
 public:
    ForgeryDB();
    virtual ~ForgeryDB();
 public:
    bool FectchBatchForgeryIP(std::list<base_logic::ForgeryIP>* list);
    bool FectchBatchForgeryUA(std::list<base_logic::ForgeryUA>* list);

 public:
    static void CallBackFectchBatchForgeryIP(void* param,
            base_logic::Value* value);

    static void CallBackFectchBatchForgeryUA(void* param,
                base_logic::Value* value);

 private:
     scoped_ptr<base_logic::DataControllerEngine> mysql_engine_;
};
}  // namespace forgery_logic




#endif /* FORGERY_DB_H_ */
