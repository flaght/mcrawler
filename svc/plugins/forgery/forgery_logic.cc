//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月23日 Author: kerry

#include "forgery/forgery_logic.h"
#include <list>
#include <string>
#include "forgery/forgery_cache.h"
#include "core/common.h"
#include "net/errno.h"
#include "basic/native_library.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"

#define DEFAULT_CONFIG_PATH     "./plugins/forgery/forgery_config.xml"

#define CHECK_FORGERY_IP   10000

namespace forgery_logic {

Forgerylogic*
Forgerylogic::instance_ = NULL;

Forgerylogic::Forgerylogic() {
    if (!Init())
      assert(0);
}

Forgerylogic::~Forgerylogic() {
}

bool Forgerylogic::Init() {
    bool r = false;
    crawler_schduler::SchdulerEngine* (*engine) (void);
    forgery_db_.reset(new forgery_logic::ForgeryDB());
    std::string path = DEFAULT_CONFIG_PATH;
    config::FileConfig* config = config::FileConfig::GetFileConfig();
    if (config == NULL)
        return false;
    r = config->LoadConfig(path);
    base_logic::DataControllerEngine::Init(config);

    basic::libhandle handle_lancher = NULL;
    handle_lancher = basic::load_native_library(
            "./crawler_schduler/crawler_schduler.so");
    if (handle_lancher == NULL) {
        LOG_ERROR("Cant't load path cralwer_schduler/crawler_schduler.so");
           return false;
    }

    engine = (crawler_schduler::SchdulerEngine* (*) (void))
               basic::get_function_pointer(handle_lancher,
                       "GetCrawlerSchdulerEngine");

    if (engine == NULL) {
        LOG_ERROR("Can't find GetSchdulerEngine");
        return false;
    }
    schduler_engine_ = (*engine) ();


    std::list<base_logic::ForgeryIP> foreryip_list;
    std::list<base_logic::ForgeryUA> foreryua_list;

    forgery_db_->FectchBatchForgeryIP(&foreryip_list);
    forgery_db_->FectchBatchForgeryUA(&foreryua_list);

    forgery_logic::ForgeryManager* forery_mgr =
            forgery_logic::ForgeryEngine::GetForgeryManager();
    forery_mgr->FetchBatchIP(&foreryip_list);
    forery_mgr->FetchBatchUA(&foreryua_list);
    return true;
}

Forgerylogic*
Forgerylogic::GetInstance() {
    if (instance_ == NULL)
        instance_ = new Forgerylogic();
    return instance_;
}

void Forgerylogic::FreeInstance() {
    delete instance_;
    instance_ = NULL;
}

bool Forgerylogic::OnForgeryConnect(struct server *srv, const int socket) {
    return true;
}

bool Forgerylogic::OnForgeryMessage(struct server *srv, const int socket,
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
    switch (packet->operate_code) {
      case GET_FORGEINFO : {
        OnGetForgeInfo(srv, socket, packet);
        break;
      }
      default:
        break;
    }
    net::PacketProsess::DeletePacket(msg, len, packet);
    packet = NULL;
    return true;
}

bool Forgerylogic::OnForgeryClose(struct server *srv, const int socket) {
    return true;
}


bool Forgerylogic::OnBroadcastConnect(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool Forgerylogic::OnBroadcastMessage(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool Forgerylogic::OnBroadcastClose(struct server *srv, const int socket) {
    return true;
}

bool Forgerylogic::OnIniTimer(struct server *srv) {
    if (srv->add_time_task != NULL) {
        srv->add_time_task(srv, "forgery", CHECK_FORGERY_IP, 180, -1);
    }
    return true;
}



bool Forgerylogic::OnTimeout(struct server *srv, char *id,
        int opcode, int time) {
    switch (opcode) {
      case CHECK_FORGERY_IP: {
          std::list<base_logic::ForgeryIP> foreryip_list;
          forgery_db_->FectchBatchForgeryIP(&foreryip_list);
          forgery_logic::ForgeryEngine::GetForgeryManager()->RestBatchIP(&foreryip_list);
          break;
      }
    }
    return true;
}

bool Forgerylogic::OnGetForgeInfo(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg,
            int32 len) {
    struct GetForgeInfo* forge_info =
                (struct GetForgeInfo*)packet;
    forgery_logic::ForgeryManager* forery_mgr =
                forgery_logic::ForgeryEngine::GetForgeryManager();
    if (forge_info->forge_type == 1) {
        forery_mgr->SendForgeryUA(socket, forge_info->num);
    } else {
        forery_mgr->SendProxyIP(socket, forge_info->num);
    }
    return true;
}

}  // namespace forgery_logic

