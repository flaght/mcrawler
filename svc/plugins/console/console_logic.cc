//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月14日 Author: kerry
#include  <string>
#include "core/common.h"
#include "basic/native_library.h"
#include "logic/xml_parser.h"
#include "config/config.h"
#include "console/console_logic.h"
#include "net/errno.h"
#include "basic/basic_util.h"

#define DEFAULT_CONFIG_PATH     "./plugins/console/console_config.xml"
#define CUSTOM_CONFIG_PATH      "./plugins/console/custom_config.xml"

namespace console_logic {

Consolelogic* Consolelogic::instance_ = NULL;

Consolelogic::Consolelogic() {
  if (!Init())
    assert(0);
}

Consolelogic::~Consolelogic() {
  console_logic::ConsoleFactory::FreeInstance();
  if (console_time_mgr_) {
    delete console_time_mgr_;
    console_time_mgr_ = NULL;
  }
}

bool Consolelogic::Init() {
  std::string path = DEFAULT_CONFIG_PATH;
  config::FileConfig* config = config::FileConfig::GetFileConfig();
  if (config == NULL)
    return false;
  bool r = config->LoadConfig(path);
  if (!r)
    return false;
  console_time_mgr_ = new console_logic::ConsoleTimeManager();

  factory_ = console_logic::ConsoleFactory::GetInstance();
  factory_->InitParam(config);
  //读取爬虫服务调度信息
  ReadConfigXML(CUSTOM_CONFIG_PATH);
  //factory_->Test();
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
  if (srv->add_time_task != NULL) {
    srv->add_time_task(srv, "console", TIME_DISTRIBUTION_TASK, 10, -1);
    srv->add_time_task(srv, "console", TIME_FETCH_TASK, 10, -1);
    srv->add_time_task(srv, "console", TIME_UPDATE_STOCK, 3600, -1);
  }
  return true;
}

bool Consolelogic::OnTimeout(struct server *srv, char *id, int opcode,
                             int time) {
  console_time_mgr_->ConsoleTimeEvent(opcode, time);
  return true;
}

bool Consolelogic::ReadConfigXML(const std::string& file) {
  bool r = false;
  logic::XmlParser xml_parser;
  base_logic::DictionaryValue* value = xml_parser.ReadXml(file);
  if (value == NULL) {
    return -1;
  }
  base_logic::DictionaryValue* cluster = NULL;
  //int64 id = 0;
  r = value->GetDictionary(L"cluster", &cluster);
  if (!r) {
    if (value) {
      delete value;
      value = NULL;
    }
    return false;
  }
  //解析kafka信息
  base_logic::DictionaryValue::key_iterator it = cluster->begin_keys();
  for (; it != cluster->end_keys(); ++it) {
    std::string key = base::BasicUtil::StringConversions::WideToASCII((*it));
    base_logic::DictionaryValue* value_t = NULL;
    r = cluster->GetDictionary((*it), &value_t);
    if (!r)
      continue;
    console_logic::KafkaInfo kafka;
    r = ParserKafkaConaddr(value_t,kafka);
    if (r)
      factory_->SetKafkaInfo(kafka);
  }

  return true;
}

bool Consolelogic::ParserKafkaConaddr(base_logic::DictionaryValue* value,
                                      console_logic::KafkaInfo& kafka) {
  std::string host;
  std::string name;
  std::string svc_id;
  std::string valid;
  console_logic::KafkaInfo t_kafka;
  bool r = false;

  r = value->GetString(L"id", &svc_id);
  if (!r)
    return false;
  kafka.set_svc_id(atoi(svc_id.c_str()));
  r = value->GetString(L"valid", &valid);
  if (!r || atoi(valid.c_str()) == 0)
    return false;
  value->GetString(L"host", &host);
  value->GetString(L"name",&name);
  kafka.set_host(host);
  kafka.set_kafka_name(name);
  return true;
}

}  // namespace console_logic

