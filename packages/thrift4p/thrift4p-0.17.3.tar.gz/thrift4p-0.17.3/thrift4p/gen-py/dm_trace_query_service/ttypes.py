#
# Autogenerated by Thrift Compiler (0.9.3)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class Location:
  """
  Attributes:
   - lon
   - lat
   - time
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'lon', None, None, ), # 1
    (2, TType.STRING, 'lat', None, None, ), # 2
    (3, TType.STRING, 'time', None, None, ), # 3
  )

  def __init__(self, lon=None, lat=None, time=None,):
    self.lon = lon
    self.lat = lat
    self.time = time

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.lon = iprot.readString()
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.lat = iprot.readString()
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.time = iprot.readString()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Location')
    if self.lon is not None:
      oprot.writeFieldBegin('lon', TType.STRING, 1)
      oprot.writeString(self.lon)
      oprot.writeFieldEnd()
    if self.lat is not None:
      oprot.writeFieldBegin('lat', TType.STRING, 2)
      oprot.writeString(self.lat)
      oprot.writeFieldEnd()
    if self.time is not None:
      oprot.writeFieldBegin('time', TType.STRING, 3)
      oprot.writeString(self.time)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.lon)
    value = (value * 31) ^ hash(self.lat)
    value = (value * 31) ^ hash(self.time)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
