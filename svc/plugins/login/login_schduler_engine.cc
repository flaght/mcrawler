//  Copyright (c) 2015-2016 The kid Authors. All rights reserved.
//  Created on: 2016年1月5日 Author: kerry
#include "login/login_schduler_engine.h"
#include "login/create_cookie.h"
#include <string>

#include "logic/logic_comm.h"
#include "logic/logic_unit.h"

namespace login_logic {

LoginSchdulerManager *LoginSchdulerEngine::schduler_mgr_ = NULL;
LoginSchdulerEngine *LoginSchdulerEngine::schduler_engine_ = NULL;

LoginSchdulerManager::LoginSchdulerManager() : login_db_(NULL) {
  login_cache_ = new LoginSchdulerCache();
  InitThreadrw(&lock_);
}

LoginSchdulerManager::~LoginSchdulerManager() {
  DeinitThreadrw(lock_);
  CreateCookieEngine::FreeCookiesInstance();
}

void LoginSchdulerManager::Init() {
  PrintInfo();
  SetBatchCookies();
  PrintInfo();
}

void LoginSchdulerManager::Init(login_logic::LoginDB *login_db) {
  login_db_ = login_db;
  Init();
}

void LoginSchdulerManager::SetBatchCookies() {
  std::list<base_logic::LoginCookie> list;
  base_logic::WLockGd lk(lock_);
  login_db_->GetCookies(&list);
  while (list.size() > 0) {
    base_logic::LoginCookie info = list.front();
    list.pop_front();
    SetCookie(info);
  }
}

void LoginSchdulerManager::CheckBatchCookie(const int64 plat_id) {
  base_logic::WLockGd lk(lock_);
  PrintInfo();
  CookiePlatform platform;
  bool r = false;
  r = base::MapGet<COOKIE_MAP, COOKIE_MAP::iterator, int64, CookiePlatform>(
      login_cache_->cookie_map_, plat_id, platform);
  if (!r) {
    LOG_ERROR2("plat_id error %lld", plat_id);
    return;
  }
  int64 from = platform.list.size() > 0 ? platform.list.size() - 1 : 3000;
  SetBatchCookie(plat_id, from);
  PrintInfo();
}

void LoginSchdulerManager::SetBatchCookie(const int64 plat_id,
                                          const int64 from) {
  std::list<base_logic::LoginCookie> list;
  int64 &plat_update_time = login_cache_->update_time_map_[plat_id];
  login_db_->GetCookie(&list, plat_id, from, 3000, plat_update_time);
  // LOG_DEBUG2("mysql data list size %d", list.size());
  while (list.size() > 0) {
    base_logic::LoginCookie info = list.front();
    list.pop_front();
    SetCookie(info);
  }
}

void LoginSchdulerManager::PrintInfo() {}

bool LoginSchdulerManager::FectchBacthCookies(
    const int64 plat_id, const int64 count,
    std::list<base_logic::LoginCookie> *list) {
  base_logic::WLockGd lk(lock_);
  CookiePlatform &platform = login_cache_->cookie_map_[plat_id];
  if (0 == platform.list.size()) {
    LOG_MSG2("plat_id %lld no cookies", plat_id);
    return false;
  }
  platform.list.sort(base_logic::LoginCookie::cmp);
  FetchAndSortCookies(count, platform.list, list, plat_id);
  return true;
}

void LoginSchdulerManager::SetCookie(const base_logic::LoginCookie &info) {
  CookiePlatform &platform =
      login_cache_->cookie_map_[info.get_cookie_attr_id()];
  COOKIE_LIST &list = platform.list;
  for (COOKIE_LIST::iterator it = list.begin(); it != list.end(); it++) {
    if (info.get_username() == it->get_username() &&
        info.get_passwd() == it->get_passwd()) {
      list.erase(it);
      break;
    }
  }

  platform.list.push_back(info);
  platform.current_pos_ = 0;
  int64 info_update_time = info.get_update_time();
  platform.update_time_ = info_update_time;
  int64 &plat_update_time =
      GetDatabaseUpdateTimeByPlatId(info.get_cookie_attr_id());
  if (plat_update_time < info_update_time)
    plat_update_time = info_update_time;
}

void LoginSchdulerManager::FetchAndSortCookies(
    const int64 count, std::list<base_logic::LoginCookie> &src_list,
    std::list<base_logic::LoginCookie> *dst_list, int64 plat_id) {
  time_t current_time = time(NULL);
  // LOG_DEBUG2("location of src_list %p", &src_list);
  std::list<base_logic::LoginCookie>::iterator it = src_list.begin();
  int32 index = 0;
  for (; it != src_list.end() && index < count; it++) {
    base_logic::LoginCookie &info = (*it);
    // add rule cookie
    if (info.rule() == 1) {
      login_logic::CreateCookieEngine::GetCookiesInstance()->OnCreateCreate(
          info.get_cookie_attr_id(), info, count, (*dst_list));
    } else {
      if (info.is_over_time(current_time)) {
        dst_list->push_back(info);
        info.update_send_time(current_time);
        info.set_is_read(true);
        index++;
      } else {
        break;
      }
    }
  }
  if (0 == dst_list->size() && 1 != plat_id)
    dst_list->push_back(*(src_list.begin()));
}

int64 &
LoginSchdulerManager::GetDatabaseUpdateTimeByPlatId(const int64 plat_id) {
  return login_cache_->update_time_map_[plat_id];
}
void LoginSchdulerManager::SetUpdateTime(const int64 plat_id,
                                         const int64 update_time) {
  login_cache_->update_time_map_[plat_id] = update_time;
}

} //  namespace login_logic
