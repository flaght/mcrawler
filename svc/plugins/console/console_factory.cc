//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016年8月14日 Author: kerry

#include "console_factory.h"
#include "basic/template.h"
#include "logic/logic_comm.h"

namespace console_logic {

ConsoleFactory*
ConsoleFactory::instance_ = NULL;

ConsoleFactory*
ConsoleFactory::GetInstance() {
  if (instance_ == NULL)
    instance_ =new ConsoleFactory();
  return instance_;
}

ConsoleFactory::ConsoleFactory() {
  Init();
}

ConsoleFactory::~ConsoleFactory() {

}

void ConsoleFactory::Init() {

}

void ConsoleFactory::InitParam(config::FileConfig* config) {
  console_db_ = new console_logic::ConsoleDB(config);
}

void ConsoleFactory::Dest() {
  if (console_db_) {delete console_db_; console_db_ = NULL;}
}

void ConsoleFactory::Test() {
  std::list<base_logic::TaskInfo> list;
  console_db_->FetchBatchRuleTask(&list);
  LOG_DEBUG2("list size %lld", list.size());
}

void ConsoleFactory::TimeEvent(int opcode, int time) {
  switch (opcode) {
    default:
      break;
  }
}

}
