//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月23日 Author: kerry

#ifndef KID_FORGERY_FORGERY_LOGIC_
#define KID_FORGERY_FORGERY_LOGIC_
#include "core/common.h"
#include "forgery/forgery_db.h"
#include "crawler_schduler/crawler_schduler_engine.h"
#include "basic/basictypes.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"


namespace forgery_logic {

class Forgerylogic {
 public:
    Forgerylogic();
    virtual ~Forgerylogic();

 private:
    static Forgerylogic    *instance_;

 public:
    static Forgerylogic *GetInstance();
    static void FreeInstance();

 public:
    bool OnForgeryConnect(struct server *srv, const int socket);

    bool OnForgeryMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnForgeryClose(struct server *srv, const int socket);

    bool OnBroadcastConnect(struct server *srv, const int socket,
            const void *data, const int len);

    bool OnBroadcastMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnBroadcastClose(struct server *srv, const int socket);

    bool OnIniTimer(struct server *srv);

    bool OnTimeout(struct server *srv, char* id, int opcode, int time);
 private:
    bool OnGetForgeInfo(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg = NULL,
            int32 len = 0);

 private:
    bool Init();

 private:
    scoped_ptr<forgery_logic::ForgeryDB>          forgery_db_;
    crawler_schduler::SchdulerEngine*       schduler_engine_;
};


}   // namespace forgery_logic

#endif

