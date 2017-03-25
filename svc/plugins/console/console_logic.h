//  Copyright (c) 2015-2015 The autocrawler Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry
#ifndef KID_CONSOLE_CONSOLE_LOGIC_
#define KID_CONSOLE_CONSOLE_LOGIC_
#include "console_logic.h"
#include "console_time_manager.h"
#include "core/common.h"
#include "basic/basictypes.h"
#include "console/console_factory.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"

namespace console_logic {

class Consolelogic {
 public:
  Consolelogic();
  virtual ~Consolelogic();

 private:
  static Consolelogic *instance_;

 public:
  static Consolelogic *GetInstance();
  static void FreeInstance();

  bool OnIniTimer(struct server *srv);

  bool OnTimeout(struct server *srv, char* id, int opcode, int time);
 private:
  bool Init();
  bool ReadConfigXML(const std::string& file);
 private:
  bool ParserKafkaConaddr(base_logic::DictionaryValue* value,
                          console_logic::KafkaInfo& kafka);
 private:
  console_logic::ConsoleFactory* factory_;
  console_logic::ConsoleTimeManager* console_time_mgr_;

};
}  // namespace console_logic

#endif

