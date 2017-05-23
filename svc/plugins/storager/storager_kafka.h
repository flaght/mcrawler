//  Copyright (c) 2015-2016 The KID Authors. All rights reserved.
//  Created on: 2016.2.18 Author: yangge

#ifndef KID_STORAGER_KAFKA_H_
#define KID_STORAGER_KAFKA_H_

#include <string>
#include <list>
#include "net/comm_head.h"
#include "logic/auto_crawler_infos.h"
#include "basic/basictypes.h"
#include "logic/base_values.h"
#include "basic/scoped_ptr.h"
#include "queue/kafka_producer.h"

namespace storager_logic {

class StroagerKafka {
 public:
    StroagerKafka(config::FileConfig* config);
    StroagerKafka(base::ConnAddr& addr);
    virtual ~StroagerKafka();


 public:
    bool AddStorageInfo(const std::list<struct StorageUnit*>& list,
            const int32 type = 1);

    void Test();
 private:
    kafka_producer kafka_producer_;
};

}  // namespace storager_logic

#endif /* STORAGE_DB_H_ */
