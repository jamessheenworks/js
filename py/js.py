
from array import array


class tfr(object):

  def __init__(self): 
    self.c=crc('crc32c')
    self.ibc=ibc()

  def enc(self,dd):
    def rev(s):
      ss=list(s)
      ss.reverse()
      return bytes(bytearray(ss))
    ll=rev(self.ibc.i2b(len(dd),16))
    llcrc=self.ibc.b2i(self.c.crc(ll))
    llcrc=self.ibc.i2b(((llcrc >> 15) | (llcrc << 17)) + 0xa282ead8,16)[4:8]
    if issubclass(type(dd),str): dd=dd.encode()
    ddcrc=self.ibc.b2i(self.c.crc(dd))
    ddcrc=self.ibc.i2b(((ddcrc >> 15) | (ddcrc << 17)) + 0xa282ead8,16)[4:8]
    return bytes(bytearray(ll+rev(llcrc)+dd+rev(ddcrc)))


class crc(object): 

  def __init__(self,codec): 
    poly={
      'crc32': 0xEDB88320, 
      'crc32c': 0x82F63B78
    }
    t=array('L')
    for byte in range(256): 
      crc=0 
      for bit in range(8): 
        if (byte^crc)&1: 
          crc=(crc>>1)^poly[codec] 
        else: 
          crc>>=1 
        byte>>=1 
      t.append(crc)
    self.t=t 

  def crc(self,data): 
    value=0xffffffff
    if issubclass(type(data),str): data=data.encode()
    for c in data: 
      value=self.t[(c^value)&0xff]^(value>>8)
    return bytes.fromhex(format((-1-value)&0xffffffff,'08x'))


class ibc(object): 

  def __init__(self,byteorder='big'): 
    self.order=byteorder

  def i2b(self,i,d=0): 
    if d%2: d+=1
    if d==0: d=''
    s=format(i,'0'+str(d)+'x')
    if len(s)%2: s='0'+s
    return bytes.fromhex(s)

  def b2i(self,b): 
    return int.from_bytes(b,byteorder=self.order)


class jsc(): 
  def b2h(b): return b.hex()
  def h2b(h): return bytes.fromhex(h)
  def h2i(h): return int(h,16)
  def i2h(i,d=0): 
    if d%2: d+=1
    if d==0: d=''
    s=format(i,'0'+str(d)+'x')
    if len(s)%2: s='0'+s
    return s
  def s2b(s): return s.encode()
  def b2s(b): return b.decode()
  def b2a(b): return list(b)
  def a2b(a): return bytes(bytearray(a))
  def i2b(i,d=0): return bytes.fromhex(jsc.i2h(i,d))
  def b2i(b,byteorder='big'): return int.from_bytes(b,byteorder=byteorder)

