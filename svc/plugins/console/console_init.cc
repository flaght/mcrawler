//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry
#include "console/console_init.h"
#include "core/common.h"
#include "core/plugins.h"
#include "console/console_logic.h"

struct consoleplugin {
  char* id;
  char* name;
  char* version;
  char* provider;
};

static void *OnConsoleStart() {
  signal(SIGPIPE, SIG_IGN);
  struct consoleplugin* console = (struct consoleplugin*) calloc(
      1, sizeof(struct consoleplugin));
  console->id = "console";
  console->name = "console";
  console->version = "1.0.0";
  console->provider = "kerry";
  if (!console_logic::Consolelogic::GetInstance())
    assert(0);
  return console;
}

static handler_t OnConsoleShutdown(struct server* srv, void* pd) {
  console_logic::Consolelogic::FreeInstance();

  return HANDLER_GO_ON;
}



static handler_t OnUnknow(struct server *srv, int fd, void *data, int len) {
  return HANDLER_GO_ON;
}


static handler_t OnIniTimer(struct server* srv) {
  console_logic::Consolelogic::GetInstance()->OnIniTimer(srv);
  return HANDLER_GO_ON;
}

static handler_t OnTimeOut(struct server* srv, char* id, int opcode, int time) {
  console_logic::Consolelogic::GetInstance()->OnTimeout(srv, id, opcode, time);
  return HANDLER_GO_ON;
}

int console_plugin_init(struct plugin *pl) {
  pl->init = OnConsoleStart;
  pl->clean_up = OnConsoleShutdown;
  pl->handler_init_time = OnIniTimer;
  pl->handler_read_other = OnUnknow;
  pl->time_msg = OnTimeOut;
  pl->data = NULL;
  return 0;
}

