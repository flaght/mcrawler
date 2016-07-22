//  Copyright (c) 2015-2015 The autocrawler Authors. All rights reserved.
//  Created on: 2015年11月28日 Author:jiaoyongqing

#ifndef TRUNK_PLUGINS_TOOLS_TOOLS_LOGIC_H_
#define TRUNK_PLUGINS_TOOLS_TOOLS_LOGIC_H_

#include "core/common.h"
#include "crawler_schduler/crawler_schduler_engine.h"
#include "analytical_schduler/analytical_schduler.h"
#include "basic/basictypes.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"
#include "tools/get_cookie.h"

#define TIME_GET_COOKIE      10001

namespace tools_logic {

class Toolslogic {
 public:
    Toolslogic();
    virtual ~Toolslogic();

 private:
    static Toolslogic    *instance_;

 public:
    static Toolslogic *GetInstance();
    static void FreeInstance();
    bool OnToolsConnect(struct server *srv, const int socket);

    bool OnToolsMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnToolsClose(struct server *srv, const int socket);

    bool OnBroadcastConnect(struct server *srv, const int socket,
            const void *data, const int len);

    bool OnBroadcastMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnBroadcastClose(struct server *srv, const int socket);

    bool OnIniTimer(struct server *srv);

    bool OnTimeout(struct server *srv, char* id, int opcode, int time);

 private:
    bool Init();

 private:
    GetCookie get_cookie_;
};
}  // namespace tools_logic

#endif  //  TRUNK_PLUGINS_TOOLS_TOOLS_LOGIC_H_

