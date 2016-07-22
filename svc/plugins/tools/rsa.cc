//  Copyright (c) 2015-2015 The restful Authors. All rights reserved.
//  Created on: 2015/11/24 Author: jiaoyongqing

#include "tools/rsa.h"

RsaOp::RsaOp() {
  pub_key_ = NULL;
  pub_expd_ = NULL;

  module_ = NULL;

  pub_expd_len_ = 0;

  module_len_ = 0;
}

RsaOp::~RsaOp() {
  CloseKey();
  FreeRes();
}

int RsaOp::set_params(const unsigned char *pub_expd, \
                                   int pub_expd_len, \
                        const unsigned char *module, \
                                     int module_len) {
  if (pub_expd) {
    pub_expd_len_ = pub_expd_len;
    pub_expd_ = new unsigned char[pub_expd_len];
    if (!pub_expd_) {
      FreeRes();
      return -1;
    }

    memcpy(pub_expd_, pub_expd, pub_expd_len_);
  }

  if (module) {
    module_len_ = module_len;
    module_ = new unsigned char[module_len];
    if (!module_) {
      FreeRes();
      return -1;
    }
    memcpy(module_, module, module_len);
  }

  return 0;
}

int RsaOp::OpenPubkey() {
  pub_key_ = RSA_new();
  pub_key_->e = BN_bin2bn(pub_expd_, pub_expd_len_, pub_key_->e);
  pub_key_->n = BN_bin2bn(module_, module_len_, pub_key_->n);

  return 0;
}

int RsaOp::PubkeyEncrypt(const unsigned char *in, \
                                      int in_len, \
                             unsigned char **out, \
                             int * const out_len) {
  *out_len =  RSA_size(pub_key_);
  *out =  (unsigned char *)malloc(*out_len);
  if (NULL == *out) {
    printf("pubkey_encrypt:malloc error!\n");
    return -1;
  }
  memset(reinterpret_cast<void *>(*out), 0, *out_len);

  int ret =  RSA_public_encrypt(in_len, in, *out, pub_key_, RSA_PKCS1_PADDING);
  return ret;
}

void RsaOp::FreeRes() {
  if (pub_expd_) {
    delete []pub_expd_;
    pub_expd_ = NULL;
  }

  if (module_) {
    delete []module_;
    module_ = NULL;
  }
}

int RsaOp::CloseKey() {
  if (pub_key_) {
    RSA_free(pub_key_);
    pub_key_ = NULL;
  }

  return 0;
}
