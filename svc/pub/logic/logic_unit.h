//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015年9月15日 Author: kerry

#ifndef KID_LOGIC_UNIT_H_
#define KID_LOGIC_UNIT_H_

#include <sys/socket.h>
#include <arpa/inet.h>
#include <string>
#include "basic/basictypes.h"
#include "basic/native_library.h"
#include "net/comm_head.h"
#include "net/packet_processing.h"
#include "logic/logic_comm.h"
#include "basic/basic_util.h"

namespace logic {

class SomeUtils {
 public:
  static void* GetLibraryFunction(const std::string& library_name,
                                  const std::string& func_name);

  static void CreateToken(const int64 uid, const std::string& password,
                          std::string* token);

  static bool VerifyToken(const int64 uid, const std::string& password,
                          const std::string& token);

  static inline int8 StringToIntChar(const char* str) {
    int8 intvalue = 0;
    base::BasicUtil::StringUtil::StringToCharInt(std::string(str), &intvalue);
    return intvalue;
  }
  static inline int16 StringToIntShort(const char* str) {
    int16 intvalue = 0;
    base::BasicUtil::StringUtil::StringToShortInt(std::string(str), &intvalue);
    return intvalue;
  }

  static inline std::string StringReplace(std::string& str,
                                          const std::string& old_value,
                                          const std::string& new_value) {
    for (std::string::size_type pos(0); pos != std::string::npos; pos +=
        new_value.length()) {

      if ((pos = str.find(old_value, pos)) != std::string::npos)
        str.replace(pos, old_value.length(), new_value);
      else
        break;
    }
    return str;
  }

  static inline std::string StringReplaceUnit(std::string& str,
                                              const std::string& old_value,
                                              const std::string& new_value) {
    for (std::string::size_type pos(0); pos != std::string::npos; pos +=
        new_value.length()) {

      if ((pos = str.find(old_value, pos)) != std::string::npos) {
        str.replace(pos, old_value.length(), new_value);
        break;
      } else
        break;
    }
    return str;
  }

  static inline bool GetIPAddress(const int socket, std::string& ip,
                                  int& port) {
    struct sockaddr_in sa;
    socklen_t len;
    len = sizeof(sa);
    if (!getpeername(socket, (struct sockaddr *) &sa, &len)) {
      ip = inet_ntoa(sa.sin_addr);
      port = ntohs(sa.sin_port);
      return true;
    }
    return false;
  }

  static int64 GetReadConfigID(const std::string& file);
};

class SendUtils {
 public:
  static int32 SendFull(int socket, const char* buffer, size_t bytes);
  static bool SendBytes(int socket, const void* bytes, int32 len,
                        const char* file, int32 line);
  static bool SendMessage(int socket, struct PacketHead* packet,
                          const char* file, int32 line);
  static bool SendHeadMessage(int socket, int32 operate_code, int32 type,
                              int32 is_zip_encrypt, int64 session,
                              int32 reserved, const char* file, int32 line);

  static bool SendErronMessage(int socket, int32 operate_code, int32 type,
                               int32 is_zip_encrypt, int64 session,
                               int32 reserved, int32 error, const char* file,
                               int32 line);

  static struct threadrw_t* socket_lock_;
};
}  //  namespace logic

#define send_bytes (socket, bytes, len)\
    logic::SomeUtils::SendBytes(socket, bytes, len, __FILE__, __LINE__)\


#define send_message(socket, packet) \
    logic::SendUtils::SendMessage(socket, packet, __FILE__, __LINE__)\


#define send_headmsg(socket, operate_code, type, is_zip_encrypt, \
        reserved, session)\
    logic::SendUtils::SendHeadMessage(socket, operate_code, type, \
            is_zip_encrypt, reserved, session, __FILE__, __LINE__)\


#define send_errnomsg(socket, operate_code, type, is_zip_encrypt, \
        reserved, session, error)\
    logic::SendUtils::SendErronMessage(socket, operate_code, type, \
            is_zip_encrypt, reserved, session, error, __FILE__, __LINE__)\

#define closelockconnect(socket) \
    shutdown(socket, SHUT_RDWR);

#endif /* LOGIC_UNIT_H_ */
