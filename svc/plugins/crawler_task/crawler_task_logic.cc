//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry

#include "crawler_task/crawler_task_logic.h"
#include <list>
#include <string>
#include "core/common.h"
#include "net/errno.h"
#include "basic/native_library.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "basic/radom_in.h"

#define DEFAULT_CONFIG_PATH     "./plugins/crawler_task/crawler_task_config.xml"


namespace crawler_task_logic {

CrawlerTasklogic*
CrawlerTasklogic::instance_ = NULL;

CrawlerTasklogic::CrawlerTasklogic() {
    if (!Init())
      assert(0);
}

CrawlerTasklogic::~CrawlerTasklogic() {
}

bool CrawlerTasklogic::Init() {
    bool r = false;
    crawler_schduler::SchdulerEngine* (*crawler_engine) (void);
    std::string path = DEFAULT_CONFIG_PATH;
    config::FileConfig* config = config::FileConfig::GetFileConfig();
    if (config == NULL)
        return false;
    r = config->LoadConfig(path);
    //base_logic::DataControllerEngine::Init(config);
    task_db_.reset(new crawler_task_logic::CrawlerTaskDB(config));
    task_kafka_.reset(new crawler_task_logic::CrawlerTaskKafka(config));
    task_time_mgr_.reset(
           new crawler_task_logic::TaskTimeManager(task_db_.get(), task_kafka_.get()));

    std::string cralwer_library = "./crawler_schduler/crawler_schduler.so";
    std::string cralwer_func = "GetCrawlerSchdulerEngine";

    crawler_engine = (crawler_schduler::SchdulerEngine* (*) (void))
            logic::SomeUtils::GetLibraryFunction(
            cralwer_library, cralwer_func);


    crawler_schduler_engine_ = (*crawler_engine) ();
    if (crawler_schduler_engine_ == NULL)
        assert(0);

    crawler_task_logic::TaskSchdulerManager* schduler_mgr =
            crawler_task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();

    InitTask(schduler_mgr);

    schduler_mgr->Init(crawler_schduler_engine_);
    schduler_mgr->InitDB(task_db_.get());

    crawler_task_logic::TaskSchdulerEngine* engine =
            crawler_task_logic::TaskSchdulerEngine::GetTaskSchdulerEngine();

    schduler_mgr->DistributionTask();
    base::SysRadom::GetInstance()->InitRandom();
    return true;
}

void CrawlerTasklogic::InitTask(crawler_task_logic::TaskSchdulerManager* schduler_mgr) {
    std::list<base_logic::TaskInfo> task_list;
    task_db_->FecthBatchTask(&task_list);
    schduler_mgr->FetchBatchTask(&task_list);
    base::SysRadom::GetInstance()->DeinitRandom();
}

CrawlerTasklogic*
CrawlerTasklogic::GetInstance() {
    if (instance_ == NULL)
        instance_ = new CrawlerTasklogic();
    return instance_;
}



void CrawlerTasklogic::FreeInstance() {
    delete instance_;
    instance_ = NULL;
}

bool CrawlerTasklogic::OnTaskConnect(struct server *srv, const int socket) {
    return true;
}



bool CrawlerTasklogic::OnTaskMessage(struct server *srv, const int socket,
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
      case REPLY_TASK_STATE : {
        ReplyTaskState(srv, socket, packet);
        break;
      }

      case TEMP_CRAWLER_OP: {
          TimeDistributionTask();
          break;
      }

      default:
        break;
    }
    net::PacketProsess::DeletePacket(msg, len, packet);
    return true;
}

bool CrawlerTasklogic::OnTaskClose(struct server *srv, const int socket) {
    return true;
}

bool CrawlerTasklogic::OnBroadcastConnect(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}

bool CrawlerTasklogic::OnBroadcastMessage(struct server *srv, const int socket,
        const void *msg, const int len) {
    return true;
}



bool CrawlerTasklogic::OnBroadcastClose(struct server *srv, const int socket) {
    return true;
}

bool CrawlerTasklogic::OnIniTimer(struct server *srv) {
    //LOG_DEBUG("init crawler_task timer");
    if (srv->add_time_task != NULL) {
        //LOG_DEBUG("srv->add_time_task != NULL");
        srv->add_time_task(srv, "crawler_task", TIME_DISTRIBUTION_TASK, 10, -1);
        srv->add_time_task(srv, "crawler_task", TIME_FECTCH_TASK, 30, -1);
        srv->add_time_task(srv, "crawler_task", TIME_RECYCLINGTASK, 20, -1);
        srv->add_time_task(srv, "crawler_task", TIME_FETCH_TEMP_TASK, 8, -1);
        srv->add_time_task(srv, "crawler_task", TIME_DISTRBUTION_TEMP_TASK, 10, -1);
        srv->add_time_task(srv, "crawler_task", TIME_CLEAN_NO_EFFECTIVE, 20, -1);
    }

    return true;
}



bool CrawlerTasklogic::OnTimeout(struct server *srv, char *id, int opcode, int time) {
    task_time_mgr_->TaskTimeEvent(opcode, time);
    return true;
}

void CrawlerTasklogic::ReplyTaskState(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg, int32 len) {
    struct ReplyTaskState* task_state =
                (struct ReplyTaskState*)packet;
    crawler_task_logic::TaskSchdulerManager* schduler_mgr =
            crawler_task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    schduler_mgr->AlterTaskState(task_state->jobid, task_state->state);
}


void CrawlerTasklogic::RelpyCrawlNum(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg,
            int32 len) {
    struct ReplyCrawlContentNum* crawl_num =
            (struct ReplyCrawlContentNum*)packet;

    crawler_task_logic::TaskSchdulerManager* schduler_mgr =
            crawler_task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    schduler_mgr->AlterCrawlNum(crawl_num->task_id, crawl_num->num);
}


void CrawlerTasklogic::TimeDistributionTask() {
    crawler_task_logic::TaskSchdulerManager* schduler_mgr =
            crawler_task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    schduler_mgr->DistributionTask();
}

void CrawlerTasklogic::TimeFetchTask() {
    crawler_task_logic::TaskSchdulerManager* schduler_mgr =
            crawler_task_logic::TaskSchdulerEngine::GetTaskSchdulerManager();
    std::list<base_logic::TaskInfo> list;
    task_db_->FecthBatchTask(&list, true);
    schduler_mgr->FetchBatchTask(&list, true);
}

}  // namespace crawler_task_logic

