//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry
#include "core/common.h"
#include "core/plugins.h"
#include "task/task_init.h"
#include "task/task_logic.h"


struct taskplugin{
    char* id;
    char* name;
    char* version;
    char* provider;
};


static void *OnTaskStart() {
    signal(SIGPIPE, SIG_IGN);
    struct taskplugin* task = (struct taskplugin*)calloc(
            1, sizeof(struct taskplugin));

    task->id = "task";

    task->name = "task";

    task->version = "1.0.0";

    task->provider = "kerry";

    if (!task_logic::Tasklogic::GetInstance())
        assert(0);

    return task;
}

static handler_t OnTaskShutdown(struct server* srv, void* pd) {
    task_logic::Tasklogic::FreeInstance();
    return HANDLER_GO_ON;
}

static handler_t OnTaskConnect(struct server *srv, int fd,
        void *data, int len) {
    task_logic::Tasklogic::GetInstance()->OnTaskConnect(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnTaskMessage(struct server *srv, int fd, void *data,
        int len) {
    task_logic::Tasklogic::GetInstance()->OnTaskMessage(srv, fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnTaskClose(struct server *srv, int fd) {
    task_logic::Tasklogic::GetInstance()->OnTaskClose(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnUnknow(struct server *srv, int fd, void *data,
        int len) {
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastConnect(struct server* srv,
        int fd, void *data, int len) {
    task_logic::Tasklogic::GetInstance()->OnBroadcastConnect(srv,
            fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastClose(struct server* srv, int fd) {
    task_logic::Tasklogic::GetInstance()->OnBroadcastClose(srv, fd);
    return HANDLER_GO_ON;
}

static handler_t OnBroadcastMessage(struct server* srv, int fd,
        void *data, int len) {
    task_logic::Tasklogic::GetInstance()->OnBroadcastMessage(srv,
            fd, data, len);
    return HANDLER_GO_ON;
}

static handler_t OnIniTimer(struct server* srv) {
    task_logic::Tasklogic::GetInstance()->OnIniTimer(srv);
    return HANDLER_GO_ON;
}

static handler_t OnTimeOut(struct server* srv, char* id,
        int opcode, int time) {
    task_logic::Tasklogic::GetInstance()->OnTimeout(srv, id, opcode, time);
    return HANDLER_GO_ON;
}

int task_plugin_init(struct plugin *pl) {
    pl->init = OnTaskStart;

    pl->clean_up = OnTaskShutdown;

    pl->connection = OnTaskConnect;

    pl->connection_close = OnTaskClose;

    pl->connection_close_srv = OnBroadcastClose;

    pl->connection_srv = OnBroadcastConnect;

    pl->handler_init_time = OnIniTimer;

    pl->handler_read = OnTaskMessage;

    pl->handler_read_srv = OnBroadcastMessage;

    pl->handler_read_other = OnUnknow;

    pl->time_msg = OnTimeOut;

    pl->data = NULL;

    return 0;
}

