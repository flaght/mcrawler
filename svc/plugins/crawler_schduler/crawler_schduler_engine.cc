//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月14日 Author: kerry

#include "crawler_schduler/crawler_schduler_engine.h"
#include <errno.h>
#include <list>
#include <string>
#include "net/comm_head.h"
#include "net/packet_processing.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "basic/template.h"

#define DEFAULT_CONFIG_PATH  "./plugins/schduler_config.xml"

crawler_schduler::SchdulerEngine   *GetCrawlerSchdulerEngine(void) {
    return new crawler_schduler::SchdulerEngineImpl();
}

namespace crawler_schduler {

bool SchdulerEngineImpl::SetSchduler(const int32 id, void* schduler) {
    return SetCrawlerSchduler(id, (base_logic::CrawlerScheduler*)(schduler));
}


bool SchdulerEngineImpl::SetCrawlerSchduler(const int32 id,
        base_logic::CrawlerScheduler* schduler) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->SetCrawlerSchduler(id, schduler);
}

bool SchdulerEngineImpl::GetCrawlerSchduler(const int32 id,
        base_logic::CrawlerScheduler* schduler) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->GetCrawlerSchduler(id, schduler);
}

bool SchdulerEngineImpl::DelCrawlerSchduler(const int32 id) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->DelCrawlerSchduler(id);
}


bool SchdulerEngineImpl::FindCrawlerSchduler(const int socket,
    base_logic::CrawlerScheduler* schduler) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->FindCrawlerSchduler(socket, schduler);
}

bool SchdulerEngineImpl::CloseCrawlerSchduler(const int socket) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->CloseCrawlerSchduler(socket);
}

bool SchdulerEngineImpl::SetRecvTime(const int socket) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->SetRecvTime(socket);
}

bool SchdulerEngineImpl::SetSendTime(const int socket) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->SetRecvTime(socket);
}

bool SchdulerEngineImpl::CheckHeartPacket(const int socket) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->CheckHeartPacket(socket);
}

bool SchdulerEngineImpl::SendOptimalCrawler(const void* data,
        const int32 len) {
    CrawlerSchdulerManager* schduler_mgr =
                        CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->SendOptimalCrawler(data, len);
}

bool SchdulerEngineImpl::CheckOptimalCrawler() {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->CheckOptimalCrawler();
}

bool SchdulerEngineImpl::SetSendErrorCount(int socket) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->SetSendErrorCount(socket);
}

bool SchdulerEngineImpl::SetRecvErrorCount(int socket) {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    return schduler_mgr->SetRecvErrorCount(socket);
}

void SchdulerEngineImpl::CheckIsEffective() {
    CrawlerSchdulerManager* schduler_mgr =
            CrawlerSchdulerEngine::GetCrawlerSchdulerManager();
    schduler_mgr->CheckIsEffective();
}

CrawlerSchdulerManager* CrawlerSchdulerEngine::schduler_mgr_ = NULL;
CrawlerSchdulerEngine* CrawlerSchdulerEngine::schduler_engine_ = NULL;


CrawlerSchdulerManager::CrawlerSchdulerManager() {
    schduler_cache_ = new CrawlerSchdulerCache();
    Init();
}

CrawlerSchdulerManager::~CrawlerSchdulerManager() {
    DeinitThreadrw(lock_);
}


void CrawlerSchdulerManager::Init() {
    InitThreadrw(&lock_);

    bool r = false;
    std::string path = DEFAULT_CONFIG_PATH;
    config::FileConfig* config = config::FileConfig::GetFileConfig();
    if (config == NULL) {
        return;
    }
    r = config->LoadConfig(path);
}

bool CrawlerSchdulerManager::SetCrawlerSchduler(const int32 id,
         base_logic::CrawlerScheduler* schduler) {
    base_logic::WLockGd lk(lock_);
    int socket = schduler->socket();
    SOCKET_MAP::iterator it = schduler_cache_->socket_schduler_map_.find(socket);
    if (schduler_cache_->socket_schduler_map_.end() != it) {
        LOG_DEBUG2("find old socket reconnected, socket=%d", socket);
        return false;
    }
    schduler_cache_->crawler_schduler_list_.push_back((*schduler));
    base::MapAdd<SOCKET_MAP, int, base_logic::CrawlerScheduler>(
                schduler_cache_->socket_schduler_map_, schduler->socket(),
                (*schduler) );
    return base::MapAdd<SCHDULER_MAP, int32, base_logic::CrawlerScheduler>(
            schduler_cache_->crawler_schduler_map_, id, (*schduler));
}

bool CrawlerSchdulerManager::GetCrawlerSchduler(const int32 id,
         base_logic::CrawlerScheduler* schduler) {
    base_logic::RLockGd lk(lock_);
    return base::MapGet<SCHDULER_MAP, SCHDULER_MAP::iterator,
            int32, base_logic::CrawlerScheduler>(
            schduler_cache_->crawler_schduler_map_, id, (*schduler));
}

bool CrawlerSchdulerManager::DelCrawlerSchduler(const int32 id) {
    base_logic::WLockGd lk(lock_);
    base_logic::CrawlerScheduler schduler;
    base::MapGet<SCHDULER_MAP, SCHDULER_MAP::iterator,
                int32, base_logic::CrawlerScheduler>(
                schduler_cache_->crawler_schduler_map_, id, schduler);
    schduler.set_is_effective(false);
    base::MapDel<SOCKET_MAP, SOCKET_MAP::iterator, int>(
                schduler_cache_->socket_schduler_map_, schduler.socket());
    return base::MapDel<SCHDULER_MAP, SCHDULER_MAP::iterator, int32>(
            schduler_cache_->crawler_schduler_map_, id);
}

bool CrawlerSchdulerManager::FindCrawlerSchduler(const int socket,
        base_logic::CrawlerScheduler* schduler) {
    base_logic::RLockGd lk(lock_);
    return base::MapGet<SOCKET_MAP, SOCKET_MAP::iterator,
            int32, base_logic::CrawlerScheduler>(
            schduler_cache_->socket_schduler_map_, socket, (*schduler));
}

bool CrawlerSchdulerManager::CloseCrawlerSchduler(int socket) {
    base_logic::WLockGd lk(lock_);
    base_logic::CrawlerScheduler schduler;
    base::MapGet<SOCKET_MAP, SOCKET_MAP::iterator,
            int32, base_logic::CrawlerScheduler>(
            schduler_cache_->socket_schduler_map_, socket, schduler);
    schduler.set_is_effective(false);
    base::MapDel<SOCKET_MAP, SOCKET_MAP::iterator, int>(
                  schduler_cache_->socket_schduler_map_, socket);
    return base::MapDel<SCHDULER_MAP, SCHDULER_MAP::iterator, int32>(
            schduler_cache_->crawler_schduler_map_, schduler.id());
}

bool CrawlerSchdulerManager::SetSendTime(int socket) {
    base_logic::WLockGd lk(lock_);
    base_logic::CrawlerScheduler& schduler = schduler_cache_->socket_schduler_map_[socket];
    schduler.set_send_last_time(time(NULL));
    return true;
}


bool CrawlerSchdulerManager::SetRecvTime(int socket) {
    base_logic::WLockGd lk(lock_);
    base_logic::CrawlerScheduler& schduler = schduler_cache_->socket_schduler_map_[socket];
    schduler.set_recv_last_time(time(NULL));
    return true;
}

bool CrawlerSchdulerManager::SetSendErrorCount(int socket) {
    base_logic::WLockGd lk(lock_);
    base_logic::CrawlerScheduler& schduler = schduler_cache_->socket_schduler_map_[socket];
    schduler.add_send_error_count();
    return true;
}

bool CrawlerSchdulerManager::SetRecvErrorCount(int socket) {
    base_logic::WLockGd lk(lock_);
    base_logic::CrawlerScheduler& schduler = schduler_cache_->socket_schduler_map_[socket];
    schduler.add_recv_error_count();
    return true;
}

bool CrawlerSchdulerManager::SendOptimalCrawler(const void* data,
        const int32 len) {
    base_logic::WLockGd lk(lock_);
    if (schduler_cache_->crawler_schduler_list_.size() <= 0)
        return false;

    {
    	SCHDULER_LIST::iterator it = schduler_cache_->crawler_schduler_list_.begin();
    	    for (; it != schduler_cache_->crawler_schduler_list_.end(); it++) {
    	        if ((*it).is_effective()) {
    	            LOG_DEBUG2("it->id() = %d it->taskNum = %d", it->id(), it->task_count());
    	        }
    	    }
    	LOG_DEBUG2("schduler_cache_->crawler_schduler_list_.size=%d", schduler_cache_->crawler_schduler_list_.size());
    }

    base_logic::CrawlerScheduler schduler;
    SCHDULER_LIST::iterator it = schduler_cache_->crawler_schduler_list_.begin();
    for (; it != schduler_cache_->crawler_schduler_list_.end(); it++) {
        if ((*it).is_effective()) {
            schduler = (*it);
            break;
        }
    }
    LOG_DEBUG2("schduler->id()=%d", schduler.id());
    if (schduler.id() == 0)
        return false;
    struct PacketHead* packet = (struct PacketHead*)data;
    struct AssignmentMultiTask* multi_task =
            (struct AssignmentMultiTask*)packet;
    multi_task->id = schduler.id();
    if (!send_message(schduler.socket(), packet)) {
        schduler.add_send_error_count();
        schduler.set_is_effective(false);
        LOG_MSG2("schduler.socket()=%d,error msg=%s", (int)schduler.socket(), strerror(errno));
    } else {
        schduler_cache_->crawler_schduler_list_.sort(
                       base_logic::CrawlerScheduler::cmp);
    }
    return true;
}

bool CrawlerSchdulerManager::CheckOptimalCrawler() {
    base_logic::RLockGd lk(lock_);
    return schduler_cache_->crawler_schduler_map_.size() > 0?true:false;
}


bool CrawlerSchdulerManager::CheckHeartPacket(const int socket) {
    time_t current_time = time(NULL);
    bool r = false;
    base_logic::WLockGd lk(lock_);

    if(0 != socket) {
    	//update recv_last_time
    	base_logic::CrawlerScheduler& crawler_schduler = schduler_cache_->socket_schduler_map_[socket];
    	base_logic::CrawlerScheduler& crawler_schduler_from_schduler_map = schduler_cache_->crawler_schduler_map_[crawler_schduler.id()];
    	crawler_schduler_from_schduler_map.set_recv_last_time(current_time);
		LOG_DEBUG2("location of crawler_schduler = %p set crawler schduler recv_last_time socket=%d current_time=%d recv_last_time=%d",
				&crawler_schduler_from_schduler_map, socket, (int)current_time, crawler_schduler_from_schduler_map.recv_last_time());
    	return true;
    }
    SCHDULER_MAP::iterator it =
            schduler_cache_->crawler_schduler_map_.begin();
    for (; it != schduler_cache_->crawler_schduler_map_.end(); it++) {
        base_logic::CrawlerScheduler& schduler = it->second;
        if((current_time - schduler.recv_last_time() > 300)) {
        	schduler.add_send_error_count();
             LOG_DEBUG2("location of schduler=%p current_time=%d crawler_schduler out of time %d socket=%d send_error_count=%d",
             		&schduler, (int)current_time, (int)schduler.recv_last_time(), schduler.socket(), schduler.send_error_count());
                }

        if (schduler.send_error_count() > 3) {
        LOG_DEBUG("close connection");
            schduler.set_is_effective(false);
            base::MapDel<SOCKET_MAP, SOCKET_MAP::iterator, int>(
                          schduler_cache_->socket_schduler_map_, schduler.socket());
            base::MapDel<SCHDULER_MAP, SCHDULER_MAP::iterator, int32>(
                    schduler_cache_->crawler_schduler_map_, schduler.id());
            closelockconnect(schduler.socket());
            continue;
        }
    }
    return true;
}

void CrawlerSchdulerManager::CheckIsEffective() {
    base_logic::WLockGd lk(lock_);
    SCHDULER_LIST::iterator it =
            schduler_cache_->crawler_schduler_list_.begin();
    for (; it != schduler_cache_->crawler_schduler_list_.end();) {
        base_logic::CrawlerScheduler schduler = (*it);
        if (!schduler.is_effective()) {
            base::MapDel<SOCKET_MAP, SOCKET_MAP::iterator, int>(
                          schduler_cache_->socket_schduler_map_, schduler.socket());
            base::MapDel<SCHDULER_MAP, SCHDULER_MAP::iterator, int32>(
                    schduler_cache_->crawler_schduler_map_, schduler.id());
            schduler_cache_->crawler_schduler_list_.erase(it++);
        }
        else
            it++;
    }
}

}  //  namespace crawler_schduler
