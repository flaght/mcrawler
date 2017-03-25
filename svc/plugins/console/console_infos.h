//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2016.8.14 Author: kerry

#ifndef KID_CONSOLE_INFOS_H__
#define KID_CONSOLE_INFOS_H__

#include "basic/basictypes.h"
#include "logic/base_values.h"
#include <string>

namespace console_logic {

class KafkaInfo {
 public:
  KafkaInfo();

  KafkaInfo(const KafkaInfo& kafka);

  KafkaInfo& operator =(const KafkaInfo& kafka);

  const void set_svc_id(const int32 svc_id){
    data_->svc_id_ = svc_id;
  }

  const void set_host(const std::string& host){
    data_->host_ = host;
  }

  const void set_kafka_name(const std::string& kafka_name){
    data_->kafka_name_ = kafka_name;
  }

  const int32 svc_id() const {
    return data_->svc_id_;
  }

  const std::string& host() const {
    return data_->host_;
  }

  const std::string& kafka_name() const {
    return data_->kafka_name_;
  }
 private:
  class Data {
   public:
    Data()
        : refcount_(1),
          svc_id_(0) {
    }

   public:
    int32        svc_id_;
    std::string  host_;
    std::string  kafka_name_;

    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }
    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }

   private:
    int refcount_;
  };

  Data* data_;
};

class StockInfo {
 public:
  StockInfo();

  StockInfo(const StockInfo& stock);

  StockInfo& operator =(const StockInfo& stock);

  ~StockInfo() {
    if (data_ != NULL) {
      data_->Release();
    }
  }

  void set_stock_id(const int32 stock_id) {
    data_->stock_id_ = stock_id;
  }

  void set_symbol(const std::string& symbol) {
    data_->symbol_ = symbol;
  }

  void set_symbol_ext(const std::string& symbol_ext) {
    data_->symbol_ext_ = symbol_ext;
  }

  void set_flag(const std::string& flag) {
    data_->flag_ = flag;
  }

  const int32 stock_id() const {
    return data_->stock_id_;
  }

  const std::string& symbol() const {
    return data_->symbol_;
  }

  const std::string& symbol_ext() const {
    return data_->symbol_ext_;
  }

  const std::string& flag() const {
    return data_->flag_;
  }

  void ValueSerialization(base_logic::DictionaryValue* dict);
 private:
  class Data {
   public:
    Data()
        : refcount_(1),
          stock_id_(0) {
    }

   public:
    int32 stock_id_;
    std::string symbol_;
    std::string symbol_ext_;
    std::string name_;
    std::string flag_;
    void AddRef() {
      __sync_fetch_and_add(&refcount_, 1);
    }
    void Release() {
      __sync_fetch_and_sub(&refcount_, 1);
      if (!refcount_)
        delete this;
    }

   private:
    int refcount_;
  };

  Data* data_;
};

}
#endif
