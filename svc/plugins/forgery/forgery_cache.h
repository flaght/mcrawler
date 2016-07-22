//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月24日 Author: kerry

#ifndef KID_FORGERY_CACHE_H_
#define KID_FORGERY_CACHE_H_

#include <map>
#include <list>
#include "thread/base_thread_handler.h"
#include "thread/base_thread_lock.h"
#include "config/config.h"

#include "logic/auto_crawler_infos.h"

typedef std::list<base_logic::ForgeryIP> FORGERYIP_MAP;
typedef std::list<base_logic::ForgeryUA> FORGERYUA_MAP;


namespace forgery_logic {

class ForgeryCache {
 public:
    FORGERYIP_MAP   forgery_ip_;
    FORGERYUA_MAP   forgery_ua_;
};

class ForgeryManager {
 public:
    ForgeryManager();
    virtual ~ForgeryManager();

    void Init();

    void FetchBatchIP(std::list<base_logic::ForgeryIP>* list);
    void FetchBatchUA(std::list<base_logic::ForgeryUA>* list);

    void RestBatchIP(std::list<base_logic::ForgeryIP>* list);

    void SendProxyIP(const int socket, const int8 num);
    void SendForgeryUA(const int socket, const int8 num);

 private:
    struct threadrw_t*         lock_;
    ForgeryCache*              forgery_cache_;
};

class ForgeryEngine {
 private:
    static ForgeryManager       *forgery_mgr_;
    static ForgeryEngine        *forgery_engine_;

    ForgeryEngine() {}
    virtual ~ForgeryEngine() {}
 public:
    static ForgeryManager* GetForgeryManager() {
        if (forgery_mgr_ == NULL)
            forgery_mgr_ = new ForgeryManager();
        return forgery_mgr_;
    }

    static ForgeryEngine* GetForgeryEngine() {
        if (forgery_engine_ == NULL)
            forgery_engine_ = new ForgeryEngine();
        return forgery_engine_;
    }
};
}  // namespace forgery_logic

#endif /* FORGERY_CACHE_H_ */
