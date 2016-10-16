//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月14日 Author: kerry
#include  <string>
#include "core/common.h"
#include "basic/native_library.h"
#include "manager/manager_logic.h"
#include "manager/manager_db.h"
#include "net/errno.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"

#define DEFAULT_CONFIG_PATH     "./plugins/manager/manager_config.xml"

#define TIME_CRALWER_MANAGER_LIVE       10000

namespace manager_logic {

Managerlogic*
Managerlogic::instance_ = NULL;

Managerlogic::Managerlogic() {
    if (!Init())
        assert(0);
}

Managerlogic::~Managerlogic() {
}

bool Managerlogic::Init() {
    bool r = false;
    crawler_schduler::SchdulerEngine* (*crawler_engine) (void);
    std::string path = DEFAULT_CONFIG_PATH;
    config::FileConfig* config = config::FileConfig::GetFileConfig();
    if (config == NULL)
        return false;
    r = config->LoadConfig(path);
    manager_db_.reset(new manager_logic::ManagerDB(config));
    //base_logic::DataControllerEngine::Init(config);
    std::string cralwer_library = "./crawler_schduler/crawler_schduler.so";
    std::string cralwer_func = "GetCrawlerSchdulerEngine";
    crawler_engine = (crawler_schduler::SchdulerEngine* (*) (void))
            logic::SomeUtils::GetLibraryFunction(
            cralwer_library, cralwer_func);
    crawler_schduler_engine_ = (*crawler_engine) ();
    if (crawler_schduler_engine_ == NULL)
        assert(0);
    //redis_engine_.reset(base_logic::DataControllerEngine::Create(REIDS_TYPE));
    return true;
}

Managerlogic*
Managerlogic::GetInstance() {
    if (instance_ == NULL)
        instance_ = new Managerlogic();
    return instance_;
}



void Managerlogic::FreeInstance() {
    delete instance_;
    instance_ = NULL;
}

bool Managerlogic::OnManagerConnect(struct server *srv, const int socket) {
    return true;
}



bool Managerlogic::OnManagerMessage(struct server *srv, const int socket,
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
    //LOG_MSG2("packet->operate_code=%d", (int)packet->operate_code);
    switch (packet->operate_code) {
      case CRAWLER_MGR_REG : {
        OnCrawlerReg(srv, socket, packet);
        break;
      }
      case CRAWLER_AVAILABLE_RESOURCE_NUM : {
          OnCrawlerAvailableResourceNum(srv, socket, packet);
          break;
      }
      case HEART_PACKET : {
          OnCheckHeartPacket(srv, socket, packet);
          break;
      }
      default:
        break;
    }
    net::PacketProsess::DeletePacket(msg, len, packet);
    return true;
}

bool Managerlogic::OnManagerClose(struct server *srv, const int socket) {
    crawler_schduler_engine_->CloseCrawlerSchduler(socket);
    return true;
}



bool Managerlogic::OnBroadcastConnect(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool Managerlogic::OnBroadcastMessage(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}



bool Managerlogic::OnBroadcastClose(struct server *srv, const int socket) {
    return true;
}

bool Managerlogic::OnIniTimer(struct server *srv) {
    if (srv->add_time_task != NULL) {
        srv->add_time_task(srv, "manager", TIME_CRALWER_MANAGER_LIVE, 60, -1);
    }
    return true;
}



bool Managerlogic::OnTimeout(struct server *srv, char *id,
        int opcode, int time) {
    switch (opcode) {
      case TIME_CRALWER_MANAGER_LIVE:
          crawler_schduler_engine_->CheckHeartPacket(0);
        break;
      default:
        break;
    }
    return true;
}

template <typename SCHDULERTYPE>
bool Managerlogic::OnTemplateReg(const char* mac, const char* password,
        const int socket, const int32 type, const int64 session_id) {
    SCHDULERTYPE scheduler;
    std::string token;
    std::string ip;
    int port;
    logic::SomeUtils::GetIPAddress(socket,ip, port);

    scheduler.set_mac(std::string(mac));
    scheduler.set_password(std::string(password));
    scheduler.set_socket(socket);
    scheduler.set_port(port);
    scheduler.set_ip(ip);

    if (type == 0)
        manager_db_->CrawlerManagerLogin(
                reinterpret_cast<void*>(&scheduler));

    LOG_MSG2("scheduler.id()=%d", (int)scheduler.id());
    if (scheduler.id() == 0) {
        logic::SendUtils::SendErronMessage(socket, CRAWLER_REG_FAILED, 0, 0,
                session_id, 0,
                USER_NOT_EXIST, __FILE__, __LINE__);
        return true;
    }
    LOG_MSG2("type=%d", type);
    bool r = true;
    if (type == 0) {
        r = crawler_schduler_engine_->SetSchduler(scheduler.id(),
                reinterpret_cast<void*>(&scheduler));
    }

    if (!r)
        return false;

    logic::SomeUtils::CreateToken(scheduler.id(),
            scheduler.password(), &token);

    struct CrawlerMgrRegState reg_state;
    MAKE_HEAD(reg_state, CRAWLER_MGR_REGSTATE,
            0, 0, session_id, 0);
    reg_state.id = scheduler.id();
    memset(reg_state.token, '\0', TOKEN_SIZE - 1);
    memcpy(reg_state.token, token.c_str(),
            token.length() < (TOKEN_SIZE - 1) ?
            token.length() : (TOKEN_SIZE - 1));
    if (!send_message(socket, &reg_state))
        scheduler.add_send_error_count();
    LOG_MSG("register success");
    return true;
}

bool Managerlogic::OnCrawlerReg(struct server* srv, int socket,
        struct PacketHead *packet, const void *msg,
        int32 len) {
    struct CrawlerMgrReg* crawler_mgr_reg =
            (struct CrawlerMgrReg*)packet;

    return OnTemplateReg<base_logic::CrawlerScheduler>(
            crawler_mgr_reg->mac, crawler_mgr_reg->password,
            socket, 0, crawler_mgr_reg->session_id);
}

bool Managerlogic::OnCheckHeartPacket(struct server* srv, int socket,
        struct PacketHead *packet, const void *msg,
        int32 len) {
	crawler_schduler_engine_->CheckHeartPacket(socket);
	return true;
}

bool Managerlogic::OnGetMachineHardInfo(struct server* srv, int socket,
            struct PacketHead* packet, const void *msg, int32 len) {
    struct ReplyHardInfo* hard_info = (struct ReplyHardInfo*)(packet);
    return true;
}

bool Managerlogic::OnCrawlerAvailableResourceNum(struct server* srv, int socket,
            struct PacketHead* packet, const void *msg, int32 len) {
    struct CrawlerAvailableResourceNum* resource_num =
        (struct CrawlerAvailableResourceNum*)(packet);
    base_logic::CrawlerScheduler scheduler;
    bool r = crawler_schduler_engine_->GetCrawlerSchduler(resource_num->manage_id, &scheduler);
    if (!r)
        return false;
    else {
    	//LOG_DEBUG2("scheduler.id = %d get scheduler task count for test before set %d", scheduler.id(), scheduler.task_count());
    	scheduler.set_available_resource(resource_num->task_num);
    	//LOG_DEBUG2("resource_num->task_num=%d set scheduler task count %d", resource_num->task_num, scheduler.task_count());
    	crawler_schduler_engine_->GetCrawlerSchduler(resource_num->manage_id, &scheduler);
    	//LOG_DEBUG2("get scheduler task count for test after set %d", scheduler.task_count());
    }
    return true;
}

}  // namespace manager_logic

