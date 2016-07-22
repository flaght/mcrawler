//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry

#ifndef KID_STORAGER_STORAGE_LOGIC_
#define KID_STORAGER_STORAGE_LOGIC_

#include <list>
#include "core/common.h"
#include "storager/storager_db.h"
#include "storager/storager_kafka.h"
#include "storager/share_data_engine.h"
#include "crawler_schduler/crawler_schduler_engine.h"
#include "basic/basictypes.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"


namespace storager_logic {

class Storagerlogic {
 public:
    Storagerlogic();
    virtual ~Storagerlogic();

    void InitStorager(storage_logic::ShareDataManager* manager);

 private:
    static Storagerlogic    *instance_;

 public:
    static Storagerlogic *GetInstance();
    static void FreeInstance();

 public:
    bool OnStoragerConnect(struct server *srv, const int socket);

    bool OnStoragerMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnStoragerClose(struct server *srv, const int socket);

    bool OnBroadcastConnect(struct server *srv, const int socket,
            const void *data, const int len);

    bool OnBroadcastMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnBroadcastClose(struct server *srv, const int socket);

    bool OnIniTimer(struct server *srv);

    bool OnTimeout(struct server *srv, char* id, int opcode, int time);

    void StorageMethod(struct server* srv, int socket,
                struct PacketHead *packet, int32 type = 1,
                const void *msg = NULL,
                int32 len = 0);

    void GetAnalyticalHBaseInfo(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg = NULL,
            int32 len = 0);

    void GetAnalyticalFTP(struct server* srv, int socket,
            struct PacketHead* packet, const void* msg = NULL,
            int32 len = 0);

    void TempCrawlerTaskRecord(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg = NULL,
            int32 len = 0);

 private:
    bool Init();

    void RecordTempCrawlerTask(const std::list<base_logic::TaskInfo>& list);

 private:
    scoped_ptr<storager_logic::StroagerDB>     stroager_db_;
    crawler_schduler::SchdulerEngine*          schduler_engine_;
    storager_logic::StroagerKafka              stroager_kafka_;
};
}   // namespace storager_logic

#endif

