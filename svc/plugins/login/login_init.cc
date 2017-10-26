//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry
#include "login/login_init.h"
#include "core/common.h"
#include "core/plugins.h"
#include "login/login_logic.h"


struct loginplugin{
    char* id;
    char* name;
    char* version;
    char* provider;
};


static void *OnLoginStart(struct server* srv) {
    signal(SIGPIPE, SIG_IGN);
    struct loginplugin* login = (struct loginplugin*)calloc(1,
            sizeof(struct loginplugin));
    login->id = "login";
    login->name = "login";
    login->version = "1.0.0";
    login->provider = "wangqian";
    if (!login_logic::Loginlogic::GetInstance())
        assert(0);
    return login;
}

static handler_t OnLoginShutdown(struct server* srv, void* pd) {
    login_logic::Loginlogic::FreeInstance();

    return HANDLER_GO_ON;
}

static handler_t OnLoginConnect(struct server *srv, int fd, void *data,
        int len) {
    login_logic::Loginlogic::GetInstance()->OnLoginConnect(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnLoginMessage(struct server *srv, int fd, void *data,
        int len) {
    login_logic::Loginlogic::GetInstance()->OnLoginMessage(srv,
            fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnLoginClose(struct server *srv, int fd) {
    login_logic::Loginlogic::GetInstance()->OnLoginClose(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnUnknow(struct server *srv, int fd, void *data,
        int len) {
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastConnect(struct server* srv, int fd,
        void *data, int len) {
    login_logic::Loginlogic::GetInstance()->OnBroadcastConnect(
            srv, fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastClose(struct server* srv, int fd) {
    login_logic::Loginlogic::GetInstance()->OnBroadcastClose(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastMessage(struct server* srv, int fd, void *data,
        int len) {
    login_logic::Loginlogic::GetInstance()->OnBroadcastMessage(srv,
            fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnIniTimer(struct server* srv) {
    login_logic::Loginlogic::GetInstance()->OnIniTimer(srv);
    return HANDLER_GO_ON;
}

static handler_t OnTimeOut(struct server* srv, char* id, int opcode, int time) {
    login_logic::Loginlogic::GetInstance()->OnTimeout(srv,
            id, opcode, time);
    return HANDLER_GO_ON;
}


int login_plugin_init(struct plugin *pl) {
    pl->init = OnLoginStart;
    pl->clean_up = OnLoginShutdown;
    pl->connection = OnLoginConnect;
    pl->connection_close = OnLoginClose;
    pl->connection_close_srv = OnBroadcastClose;
    pl->connection_srv = OnBroadcastConnect;
    pl->handler_init_time = OnIniTimer;
    pl->handler_read = OnLoginMessage;
    pl->handler_read_srv = OnBroadcastMessage;
    pl->handler_read_other = OnUnknow;
    pl->time_msg = OnTimeOut;
    pl->data = NULL;
    return 0;
}

