//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月16日 Author: kerry

#ifndef KID_TASK_TASK_LOGIC_
#define KID_TASK_TASK_LOGIC_
#include "core/common.h"
#include "task/task_time_manager.h"
#include "task/task_db.h"
#include "task/task_schduler_engine.h"
#include "crawler_schduler/crawler_schduler_engine.h"
#include "analytical_schduler/analytical_schduler.h"
#include "basic/basictypes.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"



namespace task_logic {

class Tasklogic {
 public:
    Tasklogic();
    virtual ~Tasklogic();

 private:
    static Tasklogic    *instance_;

 public:
    static Tasklogic *GetInstance();
    static void FreeInstance();

 public:
    bool OnTaskConnect(struct server *srv, const int socket);

    bool OnTaskMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnTaskClose(struct server *srv, const int socket);

    bool OnBroadcastConnect(struct server *srv, const int socket,
            const void *data, const int len);

    bool OnBroadcastMessage(struct server *srv, const int socket,
            const void *msg, const int len);

    bool OnBroadcastClose(struct server *srv, const int socket);

    bool OnIniTimer(struct server *srv);

    bool OnTimeout(struct server *srv, char* id, int opcode, int time);

 private:
    bool Init();

    void InitTask(task_logic::TaskSchdulerManager* schduler_mgr);

    void TimeDistributionTask();

    void TimeFetchTask();

    void TimeDistributionHBase();

    void TimeFetchHBase();

 private:
    void ReplyTaskState(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg = NULL,
            int32 len = 0);

    void ReplyAnalyticalState(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg = NULL,
            int32 len = 0);

    void RelpyCrawlNum(struct server* srv, int socket,
            struct PacketHead *packet, const void *msg = NULL,
            int32 len = 0);

 private:
    scoped_ptr<task_logic::TaskDB>          task_db_;
    scoped_ptr<task_logic::TaskTimeManager> task_time_mgr_;
    crawler_schduler::SchdulerEngine*       crawler_schduler_engine_;
    analytical_schduler::SchdulerEngine*    analytical_schduler_engine_;
};

}  // // namespace task_logic

#endif

