//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月24日 Author: kerry
#include "forgery/forgery_cache.h"
#include <string>
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include "basic/template.h"


namespace forgery_logic {

ForgeryManager* ForgeryEngine::forgery_mgr_ = NULL;
ForgeryEngine* ForgeryEngine::forgery_engine_ = NULL;

ForgeryManager::ForgeryManager() {
    forgery_cache_ = new ForgeryCache();
    Init();
}

ForgeryManager::~ForgeryManager() {
    DeinitThreadrw(lock_);
}

void ForgeryManager::Init() {
    InitThreadrw(&lock_);
}

void ForgeryManager::FetchBatchIP(std::list<base_logic::ForgeryIP>* list) {
    base_logic::WLockGd lk(lock_);
    while ((*list).size() > 0) {
        base_logic::ForgeryIP ip = (*list).front();
        (*list).pop_front();
        forgery_cache_->forgery_ip_.push_back(ip);
    }
}

void ForgeryManager::FetchBatchUA(std::list<base_logic::ForgeryUA>* list) {
    base_logic::WLockGd lk(lock_);
    while ((*list).size() > 0) {
        base_logic::ForgeryUA ua = (*list).front();
        (*list).pop_front();
        forgery_cache_->forgery_ua_.push_back(ua);
    }
}

void ForgeryManager::RestBatchIP(std::list<base_logic::ForgeryIP>* list) {
    base_logic::WLockGd lk(lock_);
    forgery_cache_->forgery_ip_.clear();
    while ((*list).size() > 0) {
        base_logic::ForgeryIP ip = (*list).front();
        (*list).pop_front();
        forgery_cache_->forgery_ip_.push_back(ip);
    }
}


void ForgeryManager::SendForgeryUA(const int socket, const int8 num) {
    std::list<base_logic::ForgeryUA>::iterator it =
            forgery_cache_->forgery_ua_.begin();
    int32 i = 0;
    struct ReplyUAForgeInfo reply_forge;
    MAKE_HEAD(reply_forge, REPLY_FOGEINFO_UA, 0, 0, 0, 0);
    for (; it != forgery_cache_->forgery_ua_.end() && i < 5; it++, i++) {
        struct UAForgeInfo* info = new struct UAForgeInfo;
        info->id = (*it).id();
        info->type = (*it).type();
        memset(info->forgen_info, '\0', UA_FORGEN_SIZE);
        memcpy(info->forgen_info, (*it).ua().c_str(),
                (UA_FORGEN_SIZE - 1) < (*it).ua().length()?
                        (UA_FORGEN_SIZE - 1):(*it).ua().length());
        reply_forge.forgen_set.push_back(info);
    }
    send_message(socket, &reply_forge);

    for (std::list<struct UAForgeInfo*>::iterator UAIt = reply_forge.forgen_set.begin();
            UAIt != reply_forge.forgen_set.end(); UAIt++) {
        delete *UAIt;
    }
}
void ForgeryManager::SendProxyIP(const int socket, const int8 num) {
    std::list<base_logic::ForgeryIP>::iterator it =
            forgery_cache_->forgery_ip_.begin();
    int32 i = 0;
    struct ReplyIPForgeInfo reply_forge;
    MAKE_HEAD(reply_forge, REPLY_FOGEINFO_IP, 0, 0, 0, 0);
    for (; it != forgery_cache_->forgery_ip_.end() && i < 5; it++, i++) {
        struct IPForgeInfo* info = new struct IPForgeInfo;
        info->id = (*it).id();
        info->type = (*it).type();
        memset(info->forgen_info, '\0', IP_FORGEN_SIZE);
        memcpy(info->forgen_info, (*it).ip().c_str(),
                       (IP_FORGEN_SIZE - 1) < (*it).ip().length()?
                               (IP_FORGEN_SIZE - 1):(*it).ip().length());
        reply_forge.forgen_set.push_back(info);
    }
    send_message(socket, &reply_forge);

    for (std::list<struct IPForgeInfo*>::iterator IPIt = reply_forge.forgen_set.begin();
            IPIt != reply_forge.forgen_set.end(); IPIt++) {
        delete *IPIt;
    }
}

}  // namespace forgery_logic
