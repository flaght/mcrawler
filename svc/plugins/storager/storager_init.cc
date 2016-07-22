//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月28日 Author: kerry

#include "storager/storager_init.h"
#include "storager/storager_logic.h"
#include "core/common.h"
#include "core/plugins.h"


struct storagerplugin{
    char* id;
    char* name;
    char* version;
    char* provider;
};


static void *OnStoragerStart() {
    signal(SIGPIPE, SIG_IGN);
    struct storagerplugin* storager = (struct storagerplugin*)calloc(1,
            sizeof(struct storagerplugin));

    storager->id = "storager";

    storager->name = "storager";

    storager->version = "1.0.0";

    storager->provider = "kerry";

    if (!storager_logic::Storagerlogic::GetInstance())
        assert(0);

    return storager;
}

static handler_t OnStoragerShutdown(struct server* srv, void* pd) {
    storager_logic::Storagerlogic::FreeInstance();

    return HANDLER_GO_ON;
}

static handler_t OnStoragerConnect(struct server *srv, int fd,
        void *data, int len) {
    storager_logic::Storagerlogic::GetInstance()->OnStoragerConnect(srv, fd);

    return HANDLER_GO_ON;
}

static handler_t OnStoragerMessage(struct server *srv, int fd,
        void *data, int len) {
    storager_logic::Storagerlogic::GetInstance()->OnStoragerMessage(
            srv, fd, data, len);

    return HANDLER_GO_ON;
}

static handler_t OnStoragerClose(struct server *srv, int fd) {
    storager_logic::Storagerlogic::GetInstance()->OnStoragerClose(srv, fd);

    return HANDLER_GO_ON;
}

static handler_t OnUnknow(struct server *srv, int fd,
        void *data, int len) {
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastConnect(struct server* srv, int fd,
        void *data, int len) {
    storager_logic::Storagerlogic::GetInstance()->OnBroadcastConnect(
            srv, fd, data, len);

    return HANDLER_GO_ON;
}

static handler_t OnBroadcastClose(struct server* srv, int fd) {
    storager_logic::Storagerlogic::GetInstance()->OnBroadcastClose(
            srv, fd);

    return HANDLER_GO_ON;
}

static handler_t OnBroadcastMessage(struct server* srv, int fd,
        void *data, int len) {
    storager_logic::Storagerlogic::GetInstance()->OnBroadcastMessage(
            srv, fd, data, len);

    return HANDLER_GO_ON;
}

static handler_t OnIniTimer(struct server* srv) {
    storager_logic::Storagerlogic::GetInstance()->OnIniTimer(srv);

    return HANDLER_GO_ON;
}

static handler_t OnTimeOut(struct server* srv, char* id, int opcode, int time) {
    storager_logic::Storagerlogic::GetInstance()->OnTimeout(
            srv, id, opcode, time);
    return HANDLER_GO_ON;
}


int storager_plugin_init(struct plugin *pl) {
    pl->init = OnStoragerStart;

    pl->clean_up = OnStoragerShutdown;

    pl->connection = OnStoragerConnect;

    pl->connection_close = OnStoragerClose;

    pl->connection_close_srv = OnBroadcastClose;

    pl->connection_srv = OnBroadcastConnect;

    pl->handler_init_time = OnIniTimer;

    pl->handler_read = OnStoragerMessage;

    pl->handler_read_srv = OnBroadcastMessage;

    pl->handler_read_other = OnUnknow;

    pl->time_msg = OnTimeOut;

    pl->data = NULL;

    return 0;
}

