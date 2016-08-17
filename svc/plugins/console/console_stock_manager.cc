//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#include "console/console_stock_manager.h"
#include "logic/logic_comm.h"

namespace console_logic {

ConsoleStockManager* ConsoleStockEngine::console_stock_manager_ = NULL;
ConsoleStockEngine* ConsoleStockEngine::console_stock_engine_ = NULL;

ConsoleStockManager::ConsoleStockManager()
    : console_db_(NULL) {
  stock_cache_ = new ConsoleStockCache();
  Init();
}

void ConsoleStockManager::Init() {
  InitThreadrw(&lock_);
}

ConsoleStockManager::~ConsoleStockManager() {
  DeinitThreadrw (lock_);
}

void ConsoleStockManager::Init(console_logic::ConsoleDB* console_db) {
  console_db_ = console_db;
  console_db_->FectchStCode(stock_cache_->stock_map_);
}

void ConsoleStockManager::Test(){
  LOG_DEBUG2("stock_map_ %lld", stock_cache_->stock_map_.size());
}

void ConsoleStockManager::Swap(std::list<console_logic::StockInfo>& list) {
  for(STOCKINFO_MAP::iterator it = stock_cache_->stock_map_.begin();
      it != stock_cache_->stock_map_.end(); it++) {
    list.push_back(it->second);
  }
}

}
