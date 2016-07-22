//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年11月28日 Author: jiaoyongqing
#include "tools/get_cookie.h"
#include "tools/tools_init.h"
#include "core/common.h"
#include "core/plugins.h"
#include "tools/tools_logic.h"
#include "logic/logic_comm.h"
#include "tools/db_comm.h"

struct toolsplugin{
    char* id;
    char* name;
    char* version;
    char* provider;
};


static void *OnToolsStart() {
    signal(SIGPIPE, SIG_IGN);
    struct toolsplugin* tools = (struct toolsplugin*)calloc(1,
            sizeof(struct toolsplugin));
    tools->id = "tools";
    tools->name = "tools";
    tools->version = "1.0.0";
    tools->provider = "jiaoyongqing";
    if (!tools_logic::Toolslogic::GetInstance())
        assert(0);

    return tools;
}

static handler_t OnToolsShutdown(struct server* srv, void* pd) {
    tools_logic::Toolslogic::FreeInstance();

    return HANDLER_GO_ON;
}

static handler_t OnToolsConnect(struct server *srv, int fd, void *data,
        int len) {
    tools_logic::Toolslogic::GetInstance()->OnToolsConnect(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnToolsMessage(struct server *srv, int fd, void *data,
        int len) {
    tools_logic::Toolslogic::GetInstance()->OnToolsMessage(srv,
            fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnToolsClose(struct server *srv, int fd) {
    tools_logic::Toolslogic::GetInstance()->OnToolsClose(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnUnknow(struct server *srv, int fd, void *data,
        int len) {
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastConnect(struct server* srv, int fd,
        void *data, int len) {
    tools_logic::Toolslogic::GetInstance()->OnBroadcastConnect(
            srv, fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastClose(struct server* srv, int fd) {
    tools_logic::Toolslogic::GetInstance()->OnBroadcastClose(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastMessage(struct server* srv, int fd, void *data,
        int len) {
    tools_logic::Toolslogic::GetInstance()->OnBroadcastMessage(srv,
            fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnIniTimer(struct server* srv) {
    tools_logic::Toolslogic::GetInstance()->OnIniTimer(srv);
    return HANDLER_GO_ON;
}

static handler_t OnTimeOut(struct server* srv, char* id, int opcode, int time) {
    tools_logic::Toolslogic::GetInstance()->OnTimeout(srv,
            id, opcode, time);
    return HANDLER_GO_ON;
}

int tools_plugin_init(struct plugin *pl) {
    pl->init = OnToolsStart;
    pl->clean_up = OnToolsShutdown;
    pl->connection = OnToolsConnect;
    pl->connection_close = OnToolsClose;
    pl->connection_close_srv = OnBroadcastClose;
    pl->connection_srv = OnBroadcastConnect;
    pl->handler_init_time = OnIniTimer;
    pl->handler_read = OnToolsMessage;
    pl->handler_read_srv = OnBroadcastMessage;
    pl->handler_read_other = OnUnknow;
    pl->time_msg = OnTimeOut;
    pl->data = NULL;

    return 0;
}

