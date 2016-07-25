# -.- coding:utf-8 -.-
'''
Created on 2015年12月26日

@author: chenyitao
'''
import struct


DELTA = 0x9e3779b9L
MAX_INT = 2**23-1
OP = 0xffffffffL

def __str2int(src):
    v = struct.pack('=cccc', src[0], src[1], src[2], src[3])
    v = struct.unpack('=i', v)[0]
    return OP&v

def __encrypt(v1, v2, k, rounds):
    __sum = 0
    a = __str2int(k[0])
    b = __str2int(k[1])
    c = __str2int(k[2])
    d = __str2int(k[3])
    for i in range(0,rounds):  # @UnusedVariable
        __sum = OP&(__sum+DELTA)
        lm = OP&(v2<<4)
        r1 = OP&(lm+a)
        r2 = OP&(v2+__sum)
        rm = OP&(v2>>5)
        r3 = OP&(rm+b)
        n1 = OP&(r1^r2)
        n2 = OP&(n1^r3)
        v1 = OP&(v1+n2)
        
        lm = OP&(v1<<4)
        r1 = OP&(lm+c)
        r2 = OP&(v1+__sum)
        rm = OP&(v1>>5)
        r3 = OP&(rm+d)
        n1 = OP&(r1^r2)
        n2 = OP&(n1^r3)
        v2 = OP&(v2+n2)
#         v2 += ((OP&(OP&(v1<<4)+c)^(OP&(v1+__sum))^(OP&(OP&(v1>>5)+d)))&OP)
    return v1,v2

def __decrypt(v1, v2, k, rounds):
    if rounds==32:
        __sum = 0xc6ef3720L
    else:
        __sum = 0xe3779b90L
    a = __str2int(k[0])
    b = __str2int(k[1])
    c = __str2int(k[2])
    d = __str2int(k[3])
    for i in range(0, rounds):  # @UnusedVariable
        lm = OP&(v1<<4)
        r1 = OP&(lm+c)
        r2 = OP&(v1+__sum)
        rm = OP&(v1>>5)
        r3 = OP&(rm+d)
        n1 = OP&(r1^r2)
        n2 = OP&(n1^r3)
        v2 = OP&(v2-n2)
        
        lm = OP&(v2<<4)
        r1 = OP&(lm+a)
        r2 = OP&(v2+__sum)
        rm = OP&(v2>>5)
        r3 = OP&(rm+b)
        n1 = OP&(r1^r2)
        n2 = OP&(n1^r3)
        v1 = OP&(v1-n2)
#         v2 -= ((v1<<4)+k[2])^(v1+__sum)^((v1>>5)+k[3])
#         v1 -= ((v2<<4)+k[0])^(v2+__sum)^((v2>>5)+k[1])
        __sum = OP&(__sum-DELTA)
    return v1,v2

def __str_en_8byte(msg, key, rounds):
    _len = len(msg)
    n = _len/8
    len1 = (n+1)*8
    s = ''
    for index in range(0,len1):
        if index < _len:
            s += msg[index]
        else:
            s += '\0'
    ret = ''
    i = 0
    while i<len1:
        v1 = struct.pack('=cccc', s[i+0], s[i+1], s[i+2], s[i+3])
        v1 = struct.unpack('=I', v1)[0]
        v2 = struct.pack('=cccc', s[i+4], s[i+5], s[i+6], s[i+7])
        v2 = struct.unpack('=I', v2)[0]
        r1,r2 = __encrypt(v1, v2, key, rounds)
        ret += struct.pack('=I', r1)
        ret += struct.pack('=I', r2)
        i += 8
    return ret

def __str_de_8byte(msg, key, rounds):
    ret = ''
    i = 0
    while i< len(msg):
        v1 = struct.pack('=cccc', msg[i+0], msg[i+1], msg[i+2], msg[i+3])
        v1 = struct.unpack('=I', v1)[0]
        v2 = struct.pack('=cccc', msg[i+4], msg[i+5], msg[i+6], msg[i+7])
        v2 = struct.unpack('=I', v2)[0]
        r1,r2 = __decrypt(v1, v2, key, rounds)
        ret += struct.pack('=I', r1)
        ret += struct.pack('=I', r2)
        i += 8
    return ret

def encrypt(msg, key, rounds=16):
    i=0
    tmp = []
    while i<len(msg):
        if (i+8)>len(msg):
            tmp.append(msg[i:len(msg)])
        else:
            tmp.append(msg[i:i+8])
        i+=8
    ret = ''
    for _str in tmp:
        v = __str_en_8byte(_str, key, rounds)
        ret += v
    return ret

def decrypt(msg, key, rounds=16):
    i=0
    tmp = []
    while i<len(msg):
        if (i+8)>len(msg):
            tmp.append(msg[i:len(msg)])
        else:
            tmp.append(msg[i:i+8])
        i+=8
    ret = ''
    for _str in tmp:
        v = __str_de_8byte(_str, key, rounds)
        ret += v
    return ret

if __name__ == '__main__':
    msg = '133784816481helo'
    en = encrypt(msg, ['1234','5678','90ab','cdek'])
    i = 0
    for c in en:
        print '%d: %x' % (i, ord(c))
        i += 1
    de = decrypt(en, ['1234','5678','90ab','cdek'])
    print de
