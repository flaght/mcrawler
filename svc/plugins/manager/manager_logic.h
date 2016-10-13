//  Copyright (c) 2015-2015 The autocrawler Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry
#ifndef KID_MANAGER_MANAGER_LOGIC_
#define KID_MANAGER_MANAGER_LOGIC_

#define DUMP_PACKET 1


#include "core/common.h"
#include "manager/manager_db.h"
#include "crawler_schduler/crawler_schduler_engine.h"
#include "basic/basictypes.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"


namespace manager_logic {

class Managerlogic {
 public:
    Managerlogic();
    virtual ~Managerlogic();

 private:
    static Managerlogic    *instance_;

 public:
    static Managerlogic *GetInstance();
    static void FreeInstance();
    bool OnManagerConnect(struct server *srv, const int socket);

    bool OnManagerMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnManagerClose(struct server *srv, const int socket);

    bool OnBroadcastConnect(struct server *srv, const int socket,
            const void *data, const int len);

    bool OnBroadcastMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnBroadcastClose(struct server *srv, const int socket);

    bool OnIniTimer(struct server *srv);

    bool OnTimeout(struct server *srv, char* id, int opcode, int time);

 private:
    bool OnCrawlerReg(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg = NULL,
            int32 len = 0);

    bool OnGetMachineHardInfo(struct server* srv, int socket,
            struct PacketHead* packet, const void *msg = NULL,
            int32 len = 0);

    bool OnCrawlerAvailableResourceNum(struct server* srv, int socket,
            struct PacketHead* packet, const void *msg = NULL,
            int32 len = 0);

    template <typename SCHDULERTYPE>
    bool OnTemplateReg(const char* mac, const char* password, const int socket,
            const int32 type, const int64 session_id);

    bool OnCheckHeartPacket(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg = NULL,
            int32 len = 0);

 private:
    bool Init();
    scoped_ptr<manager_logic::ManagerDB>    manager_db_;
    crawler_schduler::SchdulerEngine*       crawler_schduler_engine_;
    scoped_ptr<base_logic::DataControllerEngine>          redis_engine_;
};
}  // namespace manager_logic

#endif

