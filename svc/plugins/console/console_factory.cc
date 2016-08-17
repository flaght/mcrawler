//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016年8月14日 Author: kerry

#include "console_factory.h"
#include "basic/template.h"
#include "logic/logic_comm.h"

namespace console_logic {

ConsoleFactory* ConsoleFactory::instance_ = NULL;

ConsoleFactory*
ConsoleFactory::GetInstance() {
  if (instance_ == NULL)
    instance_ = new ConsoleFactory();
  return instance_;
}

ConsoleFactory::ConsoleFactory() {
  Init();
}

ConsoleFactory::~ConsoleFactory() {
  console_logic::ConsoleStockEngine::FreeConsoleStockManager();
  if (hexun_task_mgr_) {delete hexun_task_mgr_; hexun_task_mgr_ = NULL;}
  if (console_db_) {delete console_db_; console_db_ = NULL;}
}

void ConsoleFactory::Init() {
  stock_mgr_ = console_logic::ConsoleStockEngine::GetConsoleStockManager();
  hexun_task_mgr_ = new console_logic::HexunTaskManager();
}

void ConsoleFactory::InitParam(config::FileConfig* config) {
  console_db_ = new console_logic::ConsoleDB(config);
  stock_mgr_->Init(console_db_);
}

void ConsoleFactory::Dest() {
  if (console_db_) {
    delete console_db_;
    console_db_ = NULL;
  }
}

void ConsoleFactory::Test() {
  std::list<base_logic::TaskInfo> list;
  console_db_->FetchBatchRuleTask(&list);
  //LOG_DEBUG2("list size %lld", list.size());
 // stock_mgr_->Test();

  while(list.size() > 0) {
    base_logic::TaskInfo task = list.front();
    list.pop_front();
    if (task.attrid() == 60008)
      hexun_task_mgr_->CreateTask(task);
  }

}

void ConsoleFactory::TimeEvent(int opcode, int time) {
  switch (opcode) {
    default:
      break;
  }
}

}
