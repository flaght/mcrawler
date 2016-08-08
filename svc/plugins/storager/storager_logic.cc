//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry

#include "storager/storager_logic.h"
#include <list>
#include <string>
#include "core/common.h"
#include "net/errno.h"
#include "basic/native_library.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "basic/radom_in.h"

#define DEFAULT_CONFIG_PATH     "./plugins/storager/storager_config.xml"

namespace storager_logic {

Storagerlogic*
Storagerlogic::instance_ = NULL;

Storagerlogic::Storagerlogic() {
    if (!Init())
      assert(0);
}

Storagerlogic::~Storagerlogic() {
}

bool Storagerlogic::Init() {
    bool r = false;
    crawler_schduler::SchdulerEngine* (*engine) (void);
    stroager_db_.reset(new storager_logic::StroagerDB());
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

    storage_logic::ShareDataManager* manager =
            storage_logic::ShareDataEngine::GetShareDataManager();
    storage_logic::ShareDataEngine::GetShareDataEngine();
    InitStorager(manager);

    stroager_kafka_.Test();
    return true;
}

void Storagerlogic::InitStorager(storage_logic::ShareDataManager* manager) {
    std::list<base_logic::TaskPlatDescription> list;
    stroager_db_->GetTaskPlatTaskDescription(&list);
    manager->BatchFectchTaskPlatInfo(&list);
}

Storagerlogic*
Storagerlogic::GetInstance() {
    if (instance_ == NULL)
        instance_ = new Storagerlogic();

    return instance_;
}



void Storagerlogic::FreeInstance() {
    delete instance_;
    instance_ = NULL;
}

bool Storagerlogic::OnStoragerConnect(struct server *srv, const int socket) {
    return true;
}


bool Storagerlogic::OnStoragerMessage(struct server *srv, const int socket,
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
      case CRAWL_HBASE_STORAGE_INFO : {
        net::PacketProsess::HexEncode(msg, len);
        net::PacketProsess::DumpPacket(packet);
        StorageMethod(srv, socket, packet, 1);
        break;
      }
      case CRAWL_FTP_STORAGE_INFO : {
        StorageMethod(srv, socket, packet, 2);
        break;
      }

      case ANALYTICAL_URL_SET: {
        TempCrawlerTaskRecord(srv, socket, packet);
        break;
      }
      default:
        break;
    }
    net::PacketProsess::DeletePacket(msg, len, packet);
    return true;
}

bool Storagerlogic::OnStoragerClose(struct server *srv, const int socket) {
    return true;
}



bool Storagerlogic::OnBroadcastConnect(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool Storagerlogic::OnBroadcastMessage(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}



bool Storagerlogic::OnBroadcastClose(struct server *srv, const int socket) {
    return true;
}

bool Storagerlogic::OnIniTimer(struct server *srv) {
    return true;
}



bool Storagerlogic::OnTimeout(struct server *srv, char *id,
        int opcode, int time) {
    return true;
}


void Storagerlogic::StorageMethod(struct server* srv, int socket,
        struct PacketHead *packet, int32 type, const void *msg,
        int32 len) {
    struct CrawlStorageInfo* storage =
                (struct CrawlStorageInfo*)packet;
    stroager_kafka_.AddStorageInfo(storage->storage_set, type);
}


void Storagerlogic::GetAnalyticalHBaseInfo(struct server* srv, int socket,
        struct PacketHead *packet, const void *msg,
        int32 len) {
    std::list<base_logic::StorageHBase> list;
    stroager_db_->GetHBaseInfo(&list);
}

void Storagerlogic::TempCrawlerTaskRecord(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg, int32 len) {
    std::list<base_logic::TaskInfo> list;
    struct AnalyticalURLSet* task = (struct AnalyticalURLSet*)(packet);
    std::list<AnalyticalURLUnit*>::iterator it =
            task->analytical_url_set.begin();

    for (; it != task->analytical_url_set.end(); it++) {
        base_logic::TaskInfo info;
        AnalyticalURLUnit* unit = (*it);
        int32  task_id = base::SysRadom::GetInstance()->GetRandomIntID();
        info.set_id(task_id);
        info.set_attrid(unit->attr_id);
        info.set_depth(unit->max_depth);
        info.set_current_depth(unit->current_depth);
        info.set_method(unit->method);
        info.set_url(unit->url);
        list.push_back(info);
    }

    storage_logic::ShareDataEngine::GetShareDataManager()->BatchUpdateTaskInfo(&list);
    RecordTempCrawlerTask(list);
}

void Storagerlogic::RecordTempCrawlerTask(
        const std::list<base_logic::TaskInfo>& list
        ) {
    // 暂时放入数据库
    stroager_db_->RecordTempCrawlerTask(list);
}


}  // namespace storager_logic

