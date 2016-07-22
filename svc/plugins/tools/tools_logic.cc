//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年11月27日 Author: jiaoyongqing

#include <string>

#include "core/common.h"
#include "basic/native_library.h"
#include "tools/tools_logic.h"
#include "net/errno.h"
#include "logic/logic_comm.h"
#include "algorithm/tea.h"
#include "tools/db_comm.h"
#include "tools/get_cookie.h"

#define DEFAULT_CONFIG_PATH     "./plugins/tools/tools_config.xml"

namespace tools_logic {

Toolslogic*
Toolslogic::instance_ = NULL;

Toolslogic::Toolslogic() {
    if (!Init())
        assert(0);
}

Toolslogic::~Toolslogic() {
  tools_sql::DbSql::Dest();
}

bool Toolslogic::Init() {
    bool r = false;
    std::string path = DEFAULT_CONFIG_PATH;
    config::FileConfig* config = config::FileConfig::GetFileConfig();
    if (config == NULL)
        return false;
    r = config->LoadConfig(path);

    tools_sql::DbSql::Init(config->mysql_db_list_);
    return true;
}

Toolslogic*
Toolslogic::GetInstance() {
    if (instance_ == NULL)
        instance_ = new Toolslogic();
    return instance_;
}



void Toolslogic::FreeInstance() {
    delete instance_;
    instance_ = NULL;
}

bool Toolslogic::OnToolsConnect(struct server *srv, const int socket) {
    return true;
}



bool Toolslogic::OnToolsMessage(struct server *srv, const int socket,
        const void *msg, const int len) {
    bool r = false;
    struct PacketHead* packet = NULL;
    if (srv == NULL || socket < 0 || msg == NULL
            || len < PACKET_HEAD_LENGTH)
        return false;

    if (!net::PacketProsess::UnpackStream(msg, len, &packet)) {
        LOG_ERROR2("UnpackStream Error socket %d", socket);
        net::PacketProsess::HexEncode(msg, len);
        return false;
    }
    assert(packet);
    net::PacketProsess::DumpPacket(packet);
    switch (packet->operate_code) {
      default:
        break;
    }
    return true;
}

bool Toolslogic::OnToolsClose(struct server *srv, const int socket) {
    return true;
}



bool Toolslogic::OnBroadcastConnect(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool Toolslogic::OnBroadcastMessage(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}



bool Toolslogic::OnBroadcastClose(struct server *srv, const int socket) {
    return true;
}

bool Toolslogic::OnIniTimer(struct server *srv) {
  get_cookie_.set_srv(srv);
  srv->add_time_task(srv, \
                 "tools", \
                 TIME_GET_COOKIE, \
  get_cookie_.cur_random_time(), \
                       1);
  return true;
}

bool Toolslogic::OnTimeout(struct server *srv, char *id,
        int opcode, int time) {
    switch (opcode) {
      case TIME_GET_COOKIE:
        {
          get_cookie_.Start();
          break;
        }
      default:
        break;
    }
    return true;
}

}  // namespace tools_logic

