//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.16 Author: kerry

#ifndef KID_RULE_PARSER_H__
#define KID_RULE_PARSER_H__

#include <string>

namespace console_logic {

class RuleParser {
 public:
  RuleParser();
  virtual ~RuleParser();
 public:
  bool PaserTaskRule(const std::string& task_url);

};

}
#endif
