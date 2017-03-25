//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry
#include "console/console_infos.h"

namespace console_logic {

KafkaInfo::KafkaInfo(void) {
  data_ = new Data();
}

KafkaInfo::KafkaInfo(const KafkaInfo& kafka)
    : data_(kafka.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

KafkaInfo& KafkaInfo::operator =(const KafkaInfo& kafka) {
  if (kafka.data_ != NULL) {
    kafka.data_->AddRef();
  }
  if (data_ != NULL) {
    data_->Release();
  }

  data_ = kafka.data_;
  return (*this);
}

StockInfo::StockInfo(void) {
  data_ = new Data();
}

StockInfo::StockInfo(const StockInfo& stock)
    : data_(stock.data_) {
  if (data_ != NULL) {
    data_->AddRef();
  }
}

StockInfo& StockInfo::operator =(const StockInfo& stock) {
  if (stock.data_ != NULL) {
    stock.data_->AddRef();
  }
  if (data_ != NULL) {
    data_->Release();
  }

  data_ = stock.data_;
  return (*this);
}

void StockInfo::ValueSerialization(base_logic::DictionaryValue* dict) {
  dict->GetString(L"symbol", &data_->symbol_);
  dict->GetString(L"sename", &data_->name_);
  std::string exchange;
  dict->GetString(L"exchange", &exchange);
  if (exchange == "001002")
    data_->flag_ = "SH";
  else if (exchange == "001003")
    data_->flag_ = "SZ";
  else
    return;
  data_->symbol_ext_ = data_->flag_ + data_->symbol_;
}

}
