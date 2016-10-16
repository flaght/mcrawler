//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月14日 Author: kerry


#include "login/login_logic.h"
#include  <string>
#include <list>
#include "core/common.h"
#include "login/login_schduler_engine.h"
#include "logic/auto_crawler_infos.h"
#include "login/login_db.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "net/packet_processing.h"

#define DEFAULT_CONFIG_PATH     "./plugins/login/login_config.xml"

namespace login_logic {

Loginlogic*
Loginlogic::instance_ = NULL;

Loginlogic::Loginlogic() {
    if (!Init())
        assert(0);
}

Loginlogic::~Loginlogic() {
  if (logic::SendUtils::socket_lock_!=NULL)
    DeinitThreadrw(logic::SendUtils::socket_lock_);
}

bool Loginlogic::Init() {
    bool r = false;
    std::string path = DEFAULT_CONFIG_PATH;
    config::FileConfig* config = config::FileConfig::GetFileConfig();
    if (config == NULL)
        return false;
    r = config->LoadConfig(path);
    //base_logic::DataControllerEngine::Init(config);
    login_db_.reset(new login_logic::LoginDB(config));

    login_logic::LoginSchdulerManager* schduler_mgr =
            login_logic::LoginSchdulerEngine::GetLoginSchdulerManager();
    schduler_mgr->Init(login_db_.get());
    return true;
}

Loginlogic*
Loginlogic::GetInstance() {
    if (instance_ == NULL)
        instance_ = new Loginlogic();
    return instance_;
}



void Loginlogic::FreeInstance() {
    delete instance_;
    instance_ = NULL;
}

bool Loginlogic::OnLoginConnect(struct server *srv, const int socket) {
    return true;
}



bool Loginlogic::OnLoginMessage(struct server *srv, const int socket,
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
    //LOG_DEBUG("dump packet packet");
    net::PacketProsess::DumpPacket(packet);
    switch (packet->operate_code) {
        case LOGIN_REQUIRE_COOKIES: {
            OnDeliverCookies(srv, socket, packet);
            break;
        }
        default:
            break;
    }
    net::PacketProsess::DeletePacket(msg, len, packet);
    return true;
}

bool Loginlogic::OnLoginClose(struct server *srv, const int socket) {
    return true;
}



bool Loginlogic::OnBroadcastConnect(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool Loginlogic::OnBroadcastMessage(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool Loginlogic::OnBroadcastClose(struct server *srv, const int socket) {
    return true;
}

bool Loginlogic::OnIniTimer(struct server *srv) {
    return true;
}

bool Loginlogic::OnTimeout(struct server *srv, char *id,
        int opcode, int time) {
    switch (opcode) {
     default:
        break;
    }
    return true;
}

bool Loginlogic::OnDeliverCookies(struct server* srv, int socket,
            struct PacketHead* packet, const void* msg,
            int32 len) {
    login_logic::LoginSchdulerManager* schduler_mgr =
                login_logic::LoginSchdulerEngine::GetLoginSchdulerManager();
    RequireLoginCookie* require_packet =
            (RequireLoginCookie*)packet;

    int amount =(int)(require_packet->amount);
    int64 attr_id = require_packet->attr_id;
    int32 manage_id = require_packet->manage_id;

    struct LoginCookieSet delivered_login_cookie_set;

    MAKE_HEAD(delivered_login_cookie_set, DELIVERED_COOKIE_SET, 0, 0, 0, 0);

    delivered_login_cookie_set.manage_id = manage_id;
    delivered_login_cookie_set.attr_id = attr_id;

    std::list<base_logic::LoginCookie> list;
    //LOG_DEBUG2("before FectchBacthCookies attr_id=%ld", attr_id);
    schduler_mgr->PrintInfo();
    bool r = schduler_mgr->FectchBacthCookies(attr_id, amount, &list);
    if (!r) {
        LOG_ERROR2("error info attr_id:%lld manager_id %d count %d", attr_id,
                manage_id, (int)amount);
        return false;
    }
    schduler_mgr->PrintInfo();
    int32 base_num = 5;
    int32 count = list.size();
    //LOG_DEBUG2("list.size=%d", list.size());
    int32 index = 0;

    while (list.size() > 0) {
        base_logic::LoginCookie info = list.front();
        list.pop_front();
        LoginCookieUnit* tmp_cookie_unit = new LoginCookieUnit();
        tmp_cookie_unit->login_cookie_body = info.get_cookie_body();
        tmp_cookie_unit->len = info.get_cookie_body().size();
        delivered_login_cookie_set.login_cookie_set.push_back(
                tmp_cookie_unit);

        if (delivered_login_cookie_set.login_cookie_set.size() % base_num == 0 &&
                delivered_login_cookie_set.login_cookie_set.size() != 0) {
            send_message(socket, &delivered_login_cookie_set);
            net::PacketProsess::ClearLoginCookieList(&delivered_login_cookie_set);
        }
    }

    if (delivered_login_cookie_set.login_cookie_set.size() > 0) {
        send_message(socket, &delivered_login_cookie_set);
        net::PacketProsess::ClearLoginCookieList(&delivered_login_cookie_set);
    }
    if (amount > count)
        schduler_mgr->CheckBatchCookie(attr_id);
    return true;
}

}  // namespace login_logic

