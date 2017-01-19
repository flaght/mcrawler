//  Copyright (c) 2015-2015 The autocrawler Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry
#ifndef KID_LOGIN_LOGIN_LOGIC_
#define KID_LOGIN_LOGIN_LOGIC_

#include "login/login_db.h"
#include "core/common.h"
#include "crawler_schduler/crawler_schduler_engine.h"
#include "basic/basictypes.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"
#include "basic/scoped_ptr.h"


namespace login_logic {

class Loginlogic {
 public:
    Loginlogic();
    virtual ~Loginlogic();

 private:
    static Loginlogic    *instance_;

 public:
    static Loginlogic *GetInstance();
    static void FreeInstance();

    bool OnLoginConnect(struct server *srv, const int socket);

    bool OnLoginMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnLoginClose(struct server *srv, const int socket);

    bool OnBroadcastConnect(struct server *srv, const int socket,
            const void *data, const int len);

    bool OnBroadcastMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnBroadcastClose(struct server *srv, const int socket);

    bool OnIniTimer(struct server *srv);

    bool OnTimeout(struct server *srv, char* id, int opcode, int time);

    bool OnDeliverCookies(struct server* srv, int socket,
                struct PacketHead *packet, const void *msg = NULL,
                int32 len = 0);

    bool OnUpdateCookies(struct server* srv, int socket,
                         struct PacketHead *packet, const void *msg = NULL,
                         int32 len = 0);

 private:
    bool Init();


    scoped_ptr<login_logic::LoginDB>        login_db_;
};

}  // namespace login_logic

#endif

