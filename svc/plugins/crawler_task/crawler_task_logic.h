//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry

#ifndef KID_CRAWLER_TASK_TASK_LOGIC_
#define KID_CRAWLER_TASK_TASK_LOGIC_

#define DUMP_PACKET 1

#include "basic/basictypes.h"
#include "core/common.h"
#include "crawler_schduler/crawler_schduler_engine.h"
#include "crawler_task/crawler_task_db.h"
#include "crawler_task/crawler_task_kafka.h"
#include "crawler_task/task_schduler_engine.h"
#include "crawler_task/task_time_manager.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"

namespace crawler_task_logic {

class CrawlerTasklogic {
public:
  CrawlerTasklogic();
  virtual ~CrawlerTasklogic();

private:
  static CrawlerTasklogic *instance_;

public:
  static CrawlerTasklogic *GetInstance();
  static void FreeInstance();

public:
  bool OnTaskConnect(struct server *srv, const int socket);

  bool OnTaskMessage(struct server *srv, const int socket, const void *msg,
                     const int len);

  bool OnTaskClose(struct server *srv, const int socket);

  bool OnBroadcastConnect(struct server *srv, const int socket,
                          const void *data, const int len);

  bool OnBroadcastMessage(struct server *srv, const int socket, const void *msg,
                          const int len);

  bool OnBroadcastClose(struct server *srv, const int socket);

  bool OnIniTimer(struct server *srv);

  bool OnTimeout(struct server *srv, char *id, int opcode, int time);

private:
  bool Init();

  void InitTask(crawler_task_logic::TaskSchdulerManager *schduler_mgr);

  void TimeDistributionTask();

  void TimeFetchTask();

private:
  void ReplyTaskState(struct server *srv, int socket, struct PacketHead *packet,
                      const void *msg = NULL, int32 len = 0);

  void RelpyCrawlNum(struct server *srv, int socket, struct PacketHead *packet,
                     const void *msg = NULL, int32 len = 0);

private:
  scoped_ptr<crawler_task_logic::CrawlerTaskDB> task_db_;
  scoped_ptr<crawler_task_logic::TaskTimeManager> task_time_mgr_;
  // crawler_task_logic::TaskTimeManager*                      task_time_mgr_;
  scoped_ptr<crawler_task_logic::CrawlerTaskKafka> task_kafka_;
  crawler_schduler::SchdulerEngine *crawler_schduler_engine_;
  int64 svc_id_;
};

} // // namespace crawler_task_logic

#endif
