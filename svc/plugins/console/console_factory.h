//  Copyright (c) 2016-2016 The KID Authors. All rights reserved.
//  Created on: 2016年8月14日 Author: kerry
#ifndef KID_CONSOLE_FACTORY_H__
#define KID_CONSOLE_FACTORY_H__

#include "config/config.h"
#include "console_db.h"
#include "console_stock_manager.h"
#include "hexun_task_manager.h"

namespace console_logic {

class ConsoleFactory {
 public:
  ConsoleFactory();
  virtual ~ConsoleFactory();
 public:
  void Init();
  void Dest();
 private:
  static ConsoleFactory* instance_;
 public:
  static ConsoleFactory* GetInstance();
  static void FreeInstance();

  void InitParam(config::FileConfig* config);

  void Test();

  void TimeEvent(int opcode, int time);
 private:
  console_logic::ConsoleStockManager*  stock_mgr_;
  console_logic::ConsoleDB* console_db_;
  console_logic::HexunTaskManager*  hexun_task_mgr_;
};
}
#endif