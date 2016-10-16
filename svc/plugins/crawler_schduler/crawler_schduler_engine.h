//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月13日 Author: kerry

#ifndef CRAWLER_SCHDULER_ENGINE_H_
#define CRAWLER_SCHDULER_ENGINE_H_

#include <map>
#include <list>
#include "thread/base_thread_handler.h"
#include "thread/base_thread_lock.h"
#include "config/config.h"

#include "logic/auto_crawler_infos.h"

namespace crawler_schduler {

typedef std::map<int32, base_logic::CrawlerScheduler>   SCHDULER_MAP;
typedef std::map<int, base_logic::CrawlerScheduler>     SOCKET_MAP;
typedef std::list<base_logic::CrawlerScheduler>         SCHDULER_LIST;

class SchdulerEngine {
 public:
    virtual bool SetSchduler(const int32 id, void* schduler) = 0;

    virtual bool SetCrawlerSchduler(const int32 id,
            base_logic::CrawlerScheduler* schduler) = 0;

    virtual bool GetCrawlerSchduler(const int32 id,
            base_logic::CrawlerScheduler* schduler) = 0;

    virtual bool DelCrawlerSchduler(const int32 id) = 0;

    virtual bool FindCrawlerSchduler(const int socket,
        base_logic::CrawlerScheduler* schduler) = 0;

    virtual bool CloseCrawlerSchduler(const int socket) = 0;

    virtual bool SetRecvTime(const int socket) = 0;

    virtual bool SetSendTime(const int socket) = 0;

    virtual bool CheckHeartPacket(const int socket) = 0;

    virtual int32 SendOptimalCrawler(const void* data, const int32 len) = 0;

    virtual bool CheckOptimalCrawler() = 0;

    virtual bool SetSendErrorCount(int socket) = 0;

    virtual bool SetRecvErrorCount(int socket) = 0;

    virtual void CheckIsEffective() = 0;
};

class SchdulerEngineImpl : public SchdulerEngine {
 public:
    bool SetSchduler(const int32 id, void* schduler);

    bool SetCrawlerSchduler(const int32 id,
            base_logic::CrawlerScheduler* schduler);

    bool GetCrawlerSchduler(const int32 id,
            base_logic::CrawlerScheduler* schduler);

    bool DelCrawlerSchduler(const int32 id);

    bool FindCrawlerSchduler(const int socket,
        base_logic::CrawlerScheduler* schduler);

    bool CloseCrawlerSchduler(const int socket);

    bool SetRecvTime(const int socket);

    bool SetSendTime(const int socket);

    bool CheckHeartPacket(const int socket);

    int32 SendOptimalCrawler(const void* data, const int32 len);

    bool CheckOptimalCrawler();

    bool SetSendErrorCount(int socket);

    bool SetRecvErrorCount(int socket);

    void CheckIsEffective();
};

class CrawlerSchdulerCache {
 public:
     SCHDULER_MAP     crawler_schduler_map_;
     SOCKET_MAP       socket_schduler_map_;
     SCHDULER_LIST    crawler_schduler_list_;
};

__attribute__((visibility("default")))
class CrawlerSchdulerManager {
 public:
    CrawlerSchdulerManager();
    virtual ~CrawlerSchdulerManager();

 public:
    bool SetCrawlerSchduler(const int32 id,
           base_logic::CrawlerScheduler* schduler);

    bool GetCrawlerSchduler(const int32 id,
           base_logic::CrawlerScheduler* schduler);

    bool DelCrawlerSchduler(const int32 id);

    bool FindCrawlerSchduler(const int socket,
        base_logic::CrawlerScheduler* schduler);

    bool CloseCrawlerSchduler(const int socket);

    bool SetRecvTime(const int socket);

    bool SetSendTime(const int socket);

    bool CheckHeartPacket(const int socket);

    int32 SendOptimalCrawler(const void* data, const int32 len);

    bool CheckOptimalCrawler();

    bool SetSendErrorCount(int socket);

    bool SetRecvErrorCount(int socket);

    void CheckIsEffective();


 private:
    void Init();

 public:
    CrawlerSchdulerCache* GetFindCache() {return this->schduler_cache_;}

 private:
    struct threadrw_t*             lock_;
    CrawlerSchdulerCache*          schduler_cache_;
};

class CrawlerSchdulerEngine {
 private:
    static CrawlerSchdulerManager           *schduler_mgr_;
    static CrawlerSchdulerEngine            *schduler_engine_;

    CrawlerSchdulerEngine() {}
    virtual ~CrawlerSchdulerEngine() {}
 public:
    __attribute__((visibility("default")))
     static CrawlerSchdulerManager* GetCrawlerSchdulerManager() {
        if (schduler_mgr_ == NULL)
            schduler_mgr_ = new CrawlerSchdulerManager();
        return schduler_mgr_;
    }

    static CrawlerSchdulerEngine* GetCrawlerSchdulerEngine() {
        if (schduler_engine_ == NULL)
            schduler_engine_ = new CrawlerSchdulerEngine();

        return schduler_engine_;
    }
};


}  //  namespace crawler_schduler


#ifdef __cplusplus
extern "C" {
#endif
crawler_schduler::SchdulerEngine *GetCrawlerSchdulerEngine(void);
#ifdef __cplusplus
}
#endif

#endif /* CRAWLER_MANAGER_H_ */
