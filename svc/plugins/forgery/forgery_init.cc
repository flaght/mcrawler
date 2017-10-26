//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月23日 Author: kerry
#include "forgery/forgery_init.h"
#include "forgery/forgery_logic.h"
#include "core/common.h"
#include "core/plugins.h"


struct forgeryplugin{
    char* id;
    char* name;
    char* version;
    char* provider;
};

static void *OnForgeryStart(struct server* srv) {
    signal(SIGPIPE, SIG_IGN);
    struct forgeryplugin* forgery =
            (struct forgeryplugin*)calloc(1, sizeof(struct forgeryplugin));

    forgery->id = "forgery";

    forgery->name = "forgery";

    forgery->version = "1.0.0";

    forgery->provider = "kerry";

    if (!forgery_logic::Forgerylogic::GetInstance())
        assert(0);
    return forgery;
}

static handler_t OnForgeryShutdown(struct server* srv, void* pd) {
    forgery_logic::Forgerylogic::FreeInstance();
    return HANDLER_GO_ON;
}

static handler_t OnForgeryConnect(struct server *srv, int fd,
        void *data, int len) {
    forgery_logic::Forgerylogic::GetInstance()->OnForgeryConnect(srv, fd);
    return HANDLER_GO_ON;
}


static handler_t OnForgeryMessage(struct server *srv, int fd,
        void *data, int len) {
    forgery_logic::Forgerylogic::GetInstance()->OnForgeryMessage(srv,
            fd, data, len);

    return HANDLER_GO_ON;
}

static handler_t OnForgeryClose(struct server *srv, int fd) {
    forgery_logic::Forgerylogic::GetInstance()->OnForgeryClose(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnUnknow(struct server *srv, int fd,
        void *data, int len) {
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastConnect(struct server* srv, int fd,
        void *data, int len) {
    forgery_logic::Forgerylogic::GetInstance()->OnBroadcastConnect(
            srv, fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastClose(struct server* srv, int fd) {
    forgery_logic::Forgerylogic::GetInstance()->OnBroadcastClose(
            srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastMessage(struct server* srv, int fd,
        void *data, int len) {
    forgery_logic::Forgerylogic::GetInstance()->OnBroadcastMessage(srv,
            fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnIniTimer(struct server* srv) {
    forgery_logic::Forgerylogic::GetInstance()->OnIniTimer(srv);
    return HANDLER_GO_ON;
}

static handler_t OnTimeOut(struct server* srv, char* id,
        int opcode, int time) {
    forgery_logic::Forgerylogic::GetInstance()->OnTimeout(srv,
            id, opcode, time);
    return HANDLER_GO_ON;
}


int forgery_plugin_init(struct plugin *pl) {
    pl->init = OnForgeryStart;

    pl->clean_up = OnForgeryShutdown;

    pl->connection = OnForgeryConnect;

    pl->connection_close = OnForgeryClose;

    pl->connection_close_srv = OnBroadcastClose;

    pl->connection_srv = OnBroadcastConnect;

    pl->handler_init_time = OnIniTimer;

    pl->handler_read = OnForgeryMessage;

    pl->handler_read_srv = OnBroadcastMessage;

    pl->handler_read_other = OnUnknow;

    pl->time_msg = OnTimeOut;

    pl->data = NULL;

    return 0;
}

