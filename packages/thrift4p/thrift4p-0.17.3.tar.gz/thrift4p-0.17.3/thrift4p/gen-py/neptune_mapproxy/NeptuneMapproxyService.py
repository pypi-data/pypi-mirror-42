#
# Autogenerated by Thrift Compiler (0.9.3)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import logging
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Iface:
  def getDistance(self, cityid, slon, slat, elon, elat):
    """
    Parameters:
     - cityid
     - slon
     - slat
     - elon
     - elat
    """
    pass

  def getRoutine(self, cityid, slon, slat, elon, elat):
    """
    Parameters:
     - cityid
     - slon
     - slat
     - elon
     - elat
    """
    pass

  def getBatchDistance(self, cityid, lines):
    """
    Parameters:
     - cityid
     - lines
    """
    pass

  def getServerNodes(self, cityid):
    """
    Parameters:
     - cityid
    """
    pass


class Client(Iface):
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def getDistance(self, cityid, slon, slat, elon, elat):
    """
    Parameters:
     - cityid
     - slon
     - slat
     - elon
     - elat
    """
    self.send_getDistance(cityid, slon, slat, elon, elat)
    return self.recv_getDistance()

  def send_getDistance(self, cityid, slon, slat, elon, elat):
    self._oprot.writeMessageBegin('getDistance', TMessageType.CALL, self._seqid)
    args = getDistance_args()
    args.cityid = cityid
    args.slon = slon
    args.slat = slat
    args.elon = elon
    args.elat = elat
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_getDistance(self):
    iprot = self._iprot
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = getDistance_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "getDistance failed: unknown result")

  def getRoutine(self, cityid, slon, slat, elon, elat):
    """
    Parameters:
     - cityid
     - slon
     - slat
     - elon
     - elat
    """
    self.send_getRoutine(cityid, slon, slat, elon, elat)
    return self.recv_getRoutine()

  def send_getRoutine(self, cityid, slon, slat, elon, elat):
    self._oprot.writeMessageBegin('getRoutine', TMessageType.CALL, self._seqid)
    args = getRoutine_args()
    args.cityid = cityid
    args.slon = slon
    args.slat = slat
    args.elon = elon
    args.elat = elat
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_getRoutine(self):
    iprot = self._iprot
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = getRoutine_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "getRoutine failed: unknown result")

  def getBatchDistance(self, cityid, lines):
    """
    Parameters:
     - cityid
     - lines
    """
    self.send_getBatchDistance(cityid, lines)
    return self.recv_getBatchDistance()

  def send_getBatchDistance(self, cityid, lines):
    self._oprot.writeMessageBegin('getBatchDistance', TMessageType.CALL, self._seqid)
    args = getBatchDistance_args()
    args.cityid = cityid
    args.lines = lines
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_getBatchDistance(self):
    iprot = self._iprot
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = getBatchDistance_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "getBatchDistance failed: unknown result")

  def getServerNodes(self, cityid):
    """
    Parameters:
     - cityid
    """
    self.send_getServerNodes(cityid)
    return self.recv_getServerNodes()

  def send_getServerNodes(self, cityid):
    self._oprot.writeMessageBegin('getServerNodes', TMessageType.CALL, self._seqid)
    args = getServerNodes_args()
    args.cityid = cityid
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_getServerNodes(self):
    iprot = self._iprot
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      raise x
    result = getServerNodes_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    raise TApplicationException(TApplicationException.MISSING_RESULT, "getServerNodes failed: unknown result")


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["getDistance"] = Processor.process_getDistance
    self._processMap["getRoutine"] = Processor.process_getRoutine
    self._processMap["getBatchDistance"] = Processor.process_getBatchDistance
    self._processMap["getServerNodes"] = Processor.process_getServerNodes

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_getDistance(self, seqid, iprot, oprot):
    args = getDistance_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = getDistance_result()
    try:
      result.success = self._handler.getDistance(args.cityid, args.slon, args.slat, args.elon, args.elat)
      msg_type = TMessageType.REPLY
    except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
      raise
    except Exception as ex:
      msg_type = TMessageType.EXCEPTION
      logging.exception(ex)
      result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
    oprot.writeMessageBegin("getDistance", msg_type, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_getRoutine(self, seqid, iprot, oprot):
    args = getRoutine_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = getRoutine_result()
    try:
      result.success = self._handler.getRoutine(args.cityid, args.slon, args.slat, args.elon, args.elat)
      msg_type = TMessageType.REPLY
    except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
      raise
    except Exception as ex:
      msg_type = TMessageType.EXCEPTION
      logging.exception(ex)
      result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
    oprot.writeMessageBegin("getRoutine", msg_type, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_getBatchDistance(self, seqid, iprot, oprot):
    args = getBatchDistance_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = getBatchDistance_result()
    try:
      result.success = self._handler.getBatchDistance(args.cityid, args.lines)
      msg_type = TMessageType.REPLY
    except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
      raise
    except Exception as ex:
      msg_type = TMessageType.EXCEPTION
      logging.exception(ex)
      result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
    oprot.writeMessageBegin("getBatchDistance", msg_type, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_getServerNodes(self, seqid, iprot, oprot):
    args = getServerNodes_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = getServerNodes_result()
    try:
      result.success = self._handler.getServerNodes(args.cityid)
      msg_type = TMessageType.REPLY
    except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
      raise
    except Exception as ex:
      msg_type = TMessageType.EXCEPTION
      logging.exception(ex)
      result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
    oprot.writeMessageBegin("getServerNodes", msg_type, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES

class getDistance_args:
  """
  Attributes:
   - cityid
   - slon
   - slat
   - elon
   - elat
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'cityid', None, None, ), # 1
    (2, TType.DOUBLE, 'slon', None, None, ), # 2
    (3, TType.DOUBLE, 'slat', None, None, ), # 3
    (4, TType.DOUBLE, 'elon', None, None, ), # 4
    (5, TType.DOUBLE, 'elat', None, None, ), # 5
  )

  def __init__(self, cityid=None, slon=None, slat=None, elon=None, elat=None,):
    self.cityid = cityid
    self.slon = slon
    self.slat = slat
    self.elon = elon
    self.elat = elat

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
        if ftype == TType.I32:
          self.cityid = iprot.readI32()
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.DOUBLE:
          self.slon = iprot.readDouble()
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.DOUBLE:
          self.slat = iprot.readDouble()
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.DOUBLE:
          self.elon = iprot.readDouble()
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.DOUBLE:
          self.elat = iprot.readDouble()
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
    oprot.writeStructBegin('getDistance_args')
    if self.cityid is not None:
      oprot.writeFieldBegin('cityid', TType.I32, 1)
      oprot.writeI32(self.cityid)
      oprot.writeFieldEnd()
    if self.slon is not None:
      oprot.writeFieldBegin('slon', TType.DOUBLE, 2)
      oprot.writeDouble(self.slon)
      oprot.writeFieldEnd()
    if self.slat is not None:
      oprot.writeFieldBegin('slat', TType.DOUBLE, 3)
      oprot.writeDouble(self.slat)
      oprot.writeFieldEnd()
    if self.elon is not None:
      oprot.writeFieldBegin('elon', TType.DOUBLE, 4)
      oprot.writeDouble(self.elon)
      oprot.writeFieldEnd()
    if self.elat is not None:
      oprot.writeFieldBegin('elat', TType.DOUBLE, 5)
      oprot.writeDouble(self.elat)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.cityid)
    value = (value * 31) ^ hash(self.slon)
    value = (value * 31) ^ hash(self.slat)
    value = (value * 31) ^ hash(self.elon)
    value = (value * 31) ^ hash(self.elat)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class getDistance_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.I32, 'success', None, None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.I32:
          self.success = iprot.readI32()
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
    oprot.writeStructBegin('getDistance_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.I32, 0)
      oprot.writeI32(self.success)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.success)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class getRoutine_args:
  """
  Attributes:
   - cityid
   - slon
   - slat
   - elon
   - elat
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'cityid', None, None, ), # 1
    (2, TType.DOUBLE, 'slon', None, None, ), # 2
    (3, TType.DOUBLE, 'slat', None, None, ), # 3
    (4, TType.DOUBLE, 'elon', None, None, ), # 4
    (5, TType.DOUBLE, 'elat', None, None, ), # 5
  )

  def __init__(self, cityid=None, slon=None, slat=None, elon=None, elat=None,):
    self.cityid = cityid
    self.slon = slon
    self.slat = slat
    self.elon = elon
    self.elat = elat

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
        if ftype == TType.I32:
          self.cityid = iprot.readI32()
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.DOUBLE:
          self.slon = iprot.readDouble()
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.DOUBLE:
          self.slat = iprot.readDouble()
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.DOUBLE:
          self.elon = iprot.readDouble()
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.DOUBLE:
          self.elat = iprot.readDouble()
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
    oprot.writeStructBegin('getRoutine_args')
    if self.cityid is not None:
      oprot.writeFieldBegin('cityid', TType.I32, 1)
      oprot.writeI32(self.cityid)
      oprot.writeFieldEnd()
    if self.slon is not None:
      oprot.writeFieldBegin('slon', TType.DOUBLE, 2)
      oprot.writeDouble(self.slon)
      oprot.writeFieldEnd()
    if self.slat is not None:
      oprot.writeFieldBegin('slat', TType.DOUBLE, 3)
      oprot.writeDouble(self.slat)
      oprot.writeFieldEnd()
    if self.elon is not None:
      oprot.writeFieldBegin('elon', TType.DOUBLE, 4)
      oprot.writeDouble(self.elon)
      oprot.writeFieldEnd()
    if self.elat is not None:
      oprot.writeFieldBegin('elat', TType.DOUBLE, 5)
      oprot.writeDouble(self.elat)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.cityid)
    value = (value * 31) ^ hash(self.slon)
    value = (value * 31) ^ hash(self.slat)
    value = (value * 31) ^ hash(self.elon)
    value = (value * 31) ^ hash(self.elat)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class getRoutine_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.LIST, 'success', (TType.STRUCT,(TPoint, TPoint.thrift_spec)), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.LIST:
          self.success = []
          (_etype12, _size9) = iprot.readListBegin()
          for _i13 in xrange(_size9):
            _elem14 = TPoint()
            _elem14.read(iprot)
            self.success.append(_elem14)
          iprot.readListEnd()
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
    oprot.writeStructBegin('getRoutine_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.LIST, 0)
      oprot.writeListBegin(TType.STRUCT, len(self.success))
      for iter15 in self.success:
        iter15.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.success)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class getBatchDistance_args:
  """
  Attributes:
   - cityid
   - lines
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'cityid', None, None, ), # 1
    (2, TType.LIST, 'lines', (TType.STRUCT,(TLine, TLine.thrift_spec)), None, ), # 2
  )

  def __init__(self, cityid=None, lines=None,):
    self.cityid = cityid
    self.lines = lines

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
        if ftype == TType.I32:
          self.cityid = iprot.readI32()
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.LIST:
          self.lines = []
          (_etype19, _size16) = iprot.readListBegin()
          for _i20 in xrange(_size16):
            _elem21 = TLine()
            _elem21.read(iprot)
            self.lines.append(_elem21)
          iprot.readListEnd()
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
    oprot.writeStructBegin('getBatchDistance_args')
    if self.cityid is not None:
      oprot.writeFieldBegin('cityid', TType.I32, 1)
      oprot.writeI32(self.cityid)
      oprot.writeFieldEnd()
    if self.lines is not None:
      oprot.writeFieldBegin('lines', TType.LIST, 2)
      oprot.writeListBegin(TType.STRUCT, len(self.lines))
      for iter22 in self.lines:
        iter22.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.cityid)
    value = (value * 31) ^ hash(self.lines)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class getBatchDistance_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.STRUCT, 'success', (TResult, TResult.thrift_spec), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRUCT:
          self.success = TResult()
          self.success.read(iprot)
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
    oprot.writeStructBegin('getBatchDistance_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRUCT, 0)
      self.success.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.success)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class getServerNodes_args:
  """
  Attributes:
   - cityid
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'cityid', None, None, ), # 1
  )

  def __init__(self, cityid=None,):
    self.cityid = cityid

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
        if ftype == TType.I32:
          self.cityid = iprot.readI32()
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
    oprot.writeStructBegin('getServerNodes_args')
    if self.cityid is not None:
      oprot.writeFieldBegin('cityid', TType.I32, 1)
      oprot.writeI32(self.cityid)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.cityid)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class getServerNodes_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.LIST, 'success', (TType.STRING,None), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.LIST:
          self.success = []
          (_etype26, _size23) = iprot.readListBegin()
          for _i27 in xrange(_size23):
            _elem28 = iprot.readString()
            self.success.append(_elem28)
          iprot.readListEnd()
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
    oprot.writeStructBegin('getServerNodes_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.LIST, 0)
      oprot.writeListBegin(TType.STRING, len(self.success))
      for iter29 in self.success:
        oprot.writeString(iter29)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.success)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
