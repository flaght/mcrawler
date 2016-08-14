//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月14日 Author: kerry
#include  <string>
#include "core/common.h"
#include "basic/native_library.h"
#include "config/config.h"
#include "console/console_logic.h"
#include "net/errno.h"

#define DEFAULT_CONFIG_PATH     "./plugins/console/console_config.xml"

namespace console_logic {

Consolelogic* Consolelogic::instance_ = NULL;

Consolelogic::Consolelogic() {
  if (!Init())
    assert(0);
}

Consolelogic::~Consolelogic() {
}

bool Consolelogic::Init() {
  std::string path = DEFAULT_CONFIG_PATH;
  config::FileConfig* config = config::FileConfig::GetFileConfig();
  if (config == NULL)
    return false;
  bool r = config->LoadConfig(path);

  factory_ = console_logic::ConsoleFactory::GetInstance();
  factory_->InitParam(config);
  factory_->Test();
  return true;
}


Consolelogic*
Consolelogic::GetInstance() {
  if (instance_ == NULL)
    instance_ = new Consolelogic();
  return instance_;
}

void Consolelogic::FreeInstance() {
  delete instance_;
  instance_ = NULL;
}

bool Consolelogic::OnIniTimer(struct server *srv) {
  return true;
}

bool Consolelogic::OnTimeout(struct server *srv, char *id, int opcode,
                             int time) {
  switch (opcode) {
    default:
      break;
  }
  return true;
}

}  // namespace manager_logic

