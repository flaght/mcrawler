//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#ifndef KID_CONSOLE_STOCK_MANAGER_H__
#define KID_CONSOLE_STOCK_MANAGER_H__

#include <map>
#include <string>
#include "thread/base_thread_lock.h"
#include "console/console_db.h"
namespace console_logic {

typedef std::map<std::string, console_logic::StockInfo> STOCKINFO_MAP;

class ConsoleStockCache {
 public:
  STOCKINFO_MAP stock_map_;
};

class ConsoleStockManager {
 public:
  ConsoleStockManager();
  virtual ~ConsoleStockManager();
 private:
  void Init();
 public:
  void Init(console_logic::ConsoleDB* console_db);
  void Swap(std::list<console_logic::StockInfo>& list);
  void Test();
 private:
  struct threadrw_t* lock_;
  ConsoleStockCache* stock_cache_;
  console_logic::ConsoleDB* console_db_;
};

class ConsoleStockEngine {
 private:
  static ConsoleStockEngine* console_stock_engine_;
  static ConsoleStockManager* console_stock_manager_;
  ConsoleStockEngine() {
  }
  virtual ~ConsoleStockEngine() {
  }

 public:
  static ConsoleStockEngine* GetConsoleStockEngine() {
    if (console_stock_engine_ == NULL)
      console_stock_engine_ = new ConsoleStockEngine();
    return console_stock_engine_;
  }

  static ConsoleStockManager* GetConsoleStockManager() {
    if (console_stock_manager_ == NULL)
      console_stock_manager_ = new ConsoleStockManager();
    return console_stock_manager_;
  }

  static void FreeConsoleStockEngine(){
    delete console_stock_engine_;
    console_stock_engine_ = NULL;
  }

  static void FreeConsoleStockManager() {
    delete console_stock_manager_;
    console_stock_manager_ = NULL;
  }
};

}

#endif
