# -.- coding:utf-8 -.-
'''
Created on 2015年9月17日

@author: chenyitao
'''

from random import randint as _randint
from random import seed
from struct import pack as _pack
from struct import unpack as _unpack


__all__ = ['encrypt', 'decrypt']
seed()
op = 0xffffffffL

def xor(a, b):
    a1,a2 = _unpack('>LL', a[0:8])
    b1,b2 = _unpack('>LL', b[0:8])
    r = _pack('>LL', ( a1 ^ b1) & op, ( a2 ^ b2) & op)
    return r

def code(v, k):
    '''
    TEA coder encrypt 64 bits value, by 128 bits key,
    QQ do 16 round TEA.
    To see:
    http://www.ftp.cl.cam.ac.uk/ftp/papers/djw-rmn/djw-rmn-tea.html .
    TEA 加密,  64比特明码, 128比特密钥, qq的TEA算法使用16轮迭代
    具体参看
    http://www.ftp.cl.cam.ac.uk/ftp/papers/djw-rmn/djw-rmn-tea.html
    '''
    n = 16
    delta = 0x9e3779b9L
    k = _unpack('>LLLL', k[0:16])
    y, z = _unpack('>LL', v[0:8])
    s = 0
    for i in xrange(n):
        i
        s += delta
        y += (op &(z<<4))+ k[0] ^ z+ s ^ (op&(z>>5)) + k[1]
        y &= op
        z += (op &(y<<4))+ k[2] ^ y+ s ^ (op&(y>>5)) + k[3]
        z &= op
    r = _pack('>LL',y,z)
    return r

def decipher(v, k):
    '''
    TEA decipher, decrypt  64bits value with 128 bits key.
    TEA 解密程序, 用128比特密钥, 解密64比特值
    it's the inverse function of TEA encrypt.
    他是TEA加密函数的反函数.
   '''
    n = 16
    y, z = _unpack('>LL', v[0:8])
    a, b, c, d = _unpack('>LLLL', k[0:16])
    delta = 0x9E3779B9L
    s = (delta << 4)&op
    for i in xrange(n):
        i
        z -= ((y<<4)+c) ^ (y+s) ^ ((y>>5) + d)
        z &= op 
        y -= ((z<<4)+a) ^ (z+s) ^ ((z>>5) + b)
        y &= op
        s -= delta
        s &= op
    return _pack('>LL', y, z)

def encrypt(v, k):
    '''
    参数 v 是被加密的明文, k是密钥
    填充字符数是随机数, (老的QQ使用0xAD)
    填充字符的个数 n = (8 - (len(v)+2)) %8 + 2
    ( 显然, n至少为2, 取2到9之间)
    然后在填充字符前部插入1字节, 值为 ((n - 2)|0xF8)
    以便标记填充字符的个数.
    在消息尾部添加7字节'\0'
    因此消息总长变为 filln + 8 + len(v),
    他模8余0(被8整除)
    加密这段消息
    每8字节, 
    规则是
    code函数就是QQ 的TEA加密函数.
    v是被加密的8字节数据
    tr是前次加密的结果
    to是前次被加密的数据, 等于 v_pre ^ r_pre_pre
    对头8字节, 'tr' 和 'to' 设为零
    不断循环,
    结束.
    '''
    END_CHAR = '\0'
    FILL_N_OR = 0xF8
    vl = len(v)
    filln = (8-(vl+2))%8 + 2
    fills = ''
    for i in xrange(filln):
        fills = fills + chr(_randint(0, 0xff))
    v = ( chr((filln -2)|FILL_N_OR)
         + fills
         + v
         + END_CHAR * 7)
    tr = '\0'*8
    to = '\0'*8
    r = ''
    o = '\0' * 8
    for i in xrange(0, len(v), 8):
        o = xor(v[i:i+8], tr)
        tr = xor(code(o, k), to)
        to = o
        r += tr
    return r

def decrypt(v, k):
    '''
    DeCrypt Message
    消息解密
    by (*) we can find out follow easyly:
    通过(*)式,我们可以容易得发现(明文等于):
    x  = decipher(v[i:i+8] ^ prePlain, key) ^ preCyrpt
    prePlain is pre 8 byte to be code.
    perPlain 是被加密的前8字节
    Attention! It's v per 8 byte value xor pre 8 byte prePlain,
    注意! 他等于前8字节数据异或上前8字节prePlain,
    not just per 8 byte.
    而不只是前8字节.
    preCrypt is pre 8 byte Cryped.
    perCrypt 是前8字节加密结果.
    In the end of deCrypte the raw message,
    在解密完原始数据后,
    we have to cut the filled bytes which was append in encrypt.
    我们必须去除在加密是添加的填充字节.
    the number of the filling bytes in the front of message is
    填充在消息头部的字节数是
    pos + 1.
    pos is the first byte of deCrypted --- r[0] & 0x07 + 2
    pos等于解密后的第一字节 --- r[0] & 0x07 + 2
    the end of filling aways is 7 zeros.
    尾部填充始终是7字节零.
    we can test the of 7 bytes is zeros, to make sure it is right.
    我们可以通测试最后7字节是零, 来确定它是正确的.
    so return r[pos+1:-7]
    所以返回 r[pos+1:-7]
    '''
    l = len(v)
    prePlain = decipher(v, k)
    pos = (ord(prePlain[0]) & 0x07L) +2
    r = prePlain
    preCrypt = v[0:8]
    for i in xrange(8, l, 8):
        x = xor(decipher(xor(v[i:i+8], prePlain),k ), preCrypt)
        prePlain = xor(x, preCrypt)
        preCrypt = v[i:i+8]
        r += x
    if r[-7:] != '\0'*7:
        return None
    return r[pos+1:-7]

def main():
    v = encrypt('00 00 00 aa 00 00 00 00 00 00 00 00 00 00 00', 'ae 27 0f 52 c9 14 d0 b5 e7 21 b6 1c a8 3b 8a 7c')
    print repr(v)
    print decrypt(v, 'ae 27 0f 52 c9 14 d0 b5 e7 21 b6 1c a8 3b 8a 7c')

if __name__ == "__main__":
#     main()
    x = 2053724225
    y = 0x9e3779b9L
    print x^y
