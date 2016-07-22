//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry

#include "task/task_logic.h"
#include <list>
#include <string>
#include "core/common.h"
#include "net/errno.h"
#include "basic/native_library.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "basic/radom_in.h"

#define DEFAULT_CONFIG_PATH     "./plugins/task/task_config.xml"


namespace task_logic {

Tasklogic*
Tasklogic::instance_ = NULL;

Tasklogic::Tasklogic() {
    if (!Init())
      assert(0);
}

Tasklogic::~Tasklogic() {
}

bool Tasklogic::Init() {
    bool r = false;
    crawler_schduler::SchdulerEngine* (*crawler_engine) (void);
    analytical_schduler::SchdulerEngine* (*analytical_engine) (void);
    task_db_.reset(new task_logic::TaskDB());
    task_time_mgr_.reset(new task_logic::TaskTimeManager(task_db_.get()));
    std::string path = DEFAULT_CONFIG_PATH;
    config::FileConfig* config = config::FileConfig::GetFileConfig();
    if (config == NULL)
        return false;
    r = config->LoadConfig(path);
    base_logic::DataControllerEngine::Init(config);

    std::string cralwer_library = "./crawler_schduler/crawler_schduler.so";
    std::string cralwer_func = "GetCrawlerSchdulerEngine";
    std::string analytical_library =
            "./analytical_schduler/analytical_schduler.so";
    std::string analytical_func = "GetAnalyticalSchdulerEngine";

    crawler_engine = (crawler_schduler::SchdulerEngine* (*) (void))
            logic::SomeUtils::GetLibraryFunction(
            cralwer_library, cralwer_func);

    analytical_engine = (analytical_schduler::SchdulerEngine* (*) (void))
            logic::SomeUtils::GetLibraryFunction(
                    analytical_library, analytical_func);

    crawler_schduler_engine_ = (*crawler_engine) ();
    if (crawler_schduler_engine_ == NULL)
        assert(0);
    analytical_schduler_engine_ = (*analytical_engine) ();
    if (analytical_schduler_engine_ == NULL)
        assert(0);

    task_logic::TaskSchdulerManager* schduler_mgr =
                task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();

    InitTask(schduler_mgr);

    schduler_mgr->Init(crawler_schduler_engine_, analytical_schduler_engine_);

    task_logic::TaskSchdulerEngine::GetTaskSchdulerEngine();
    return true;
}

void Tasklogic::InitTask(task_logic::TaskSchdulerManager* schduler_mgr) {
    std::list<base_logic::TaskInfo> task_list;
    std::list<base_logic::StorageHBase> hbase_list;
    task_db_->FecthBatchTask(&task_list);
    schduler_mgr->FetchBatchTask(&task_list);
    task_db_->FetchBatchHBase(&hbase_list);
    schduler_mgr->FetchBatchHbase(&hbase_list);
}

Tasklogic*
Tasklogic::GetInstance() {
    if (instance_ == NULL)
        instance_ = new Tasklogic();
    return instance_;
}



void Tasklogic::FreeInstance() {
    delete instance_;
    instance_ = NULL;
}

bool Tasklogic::OnTaskConnect(struct server *srv, const int socket) {
    return true;
}



bool Tasklogic::OnTaskMessage(struct server *srv, const int socket,
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
      case REPLY_TASK_STATE : {
        ReplyTaskState(srv, socket, packet);
        break;
      }
      case ANALYTICAL_STATE : {
        ReplyAnalyticalState(srv, socket, packet);
        break;
      }
      default:
        break;
    }
    return true;
}

bool Tasklogic::OnTaskClose(struct server *srv, const int socket) {
    return true;
}

bool Tasklogic::OnBroadcastConnect(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool Tasklogic::OnBroadcastMessage(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}



bool Tasklogic::OnBroadcastClose(struct server *srv, const int socket) {
    return true;
}

bool Tasklogic::OnIniTimer(struct server *srv) {
    if (srv->add_time_task != NULL) {
        srv->add_time_task(srv, "task", TIME_DISTRIBUTION_TASK, 8, -1);
        srv->add_time_task(srv, "task", TIME_FECTCH_TASK, 30, -1);
        srv->add_time_task(srv, "task", TIME_DISTRIBUTION_HBASE, 8, -1);
        srv->add_time_task(srv, "task", TIME_FECTB_HBASE, 30, -1);
        srv->add_time_task(srv, "task", TIME_CLEAN_HBASE, 13, -1);
        srv->add_time_task(srv, "task", TIME_RECYCLINGTASK,200, -1);
    }

    return true;
}



bool Tasklogic::OnTimeout(struct server *srv, char *id, int opcode, int time) {
    task_time_mgr_->TaskTimeEvent(opcode, time);
    return true;
}

void Tasklogic::ReplyTaskState(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg, int32 len) {
    struct ReplyTaskState* task_state =
                (struct ReplyTaskState*)packet;
    task_logic::TaskSchdulerManager* schduler_mgr =
                    task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    schduler_mgr->AlterTaskState(task_state->jobid, task_state->state);
}

void Tasklogic::ReplyAnalyticalState(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg,
            int32 len) {
    struct AnalysiState* analysi_state =
            (struct AnalysiState*)packet;
    task_logic::TaskSchdulerManager* schduler_mgr =
            task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    schduler_mgr->RemoveAnalyticalHBase(analysi_state->id);
}


void Tasklogic::RelpyCrawlNum(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg,
            int32 len) {
    struct ReplyCrawlContentNum* crawl_num =
            (struct ReplyCrawlContentNum*)packet;

    task_logic::TaskSchdulerManager* schduler_mgr =
                       task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    schduler_mgr->AlterCrawlNum(crawl_num->task_id, crawl_num->num);
}

void Tasklogic::TimeDistributionHBase() {
    task_logic::TaskSchdulerManager* schduler_mgr =
                task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    schduler_mgr->DistibutionHBase();
}

void Tasklogic::TimeDistributionTask() {
    task_logic::TaskSchdulerManager* schduler_mgr =
                task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    schduler_mgr->DistributionTask();
}

void Tasklogic::TimeFetchTask() {
    task_logic::TaskSchdulerManager* schduler_mgr =
                    task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    std::list<base_logic::TaskInfo> list;
    task_db_->FecthBatchTask(&list, true);
    schduler_mgr->FetchBatchTask(&list, true);
}

void Tasklogic::TimeFetchHBase() {
    std::list<base_logic::StorageHBase> hbase_list;
    task_logic::TaskSchdulerManager* schduler_mgr =
                    task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    task_db_->FetchBatchHBase(&hbase_list);
    schduler_mgr->FetchBatchHbase(&hbase_list);
}

}  // namespace task_logic

