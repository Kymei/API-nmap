from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base

class result(Base):

    __tablename__ = 'scan_result'
    id = Column(Integer, primary_key=True)
    id_major = Column(String(32), index=True, unique=False,nullable=False)
    id_scan = Column(String(32), index=True, unique=False,nullable=False)
    host = Column(String(16), index=True, unique=False, nullable=False)
    protocol = Column(String(10), index=False, unique=False, nullable=False)
    port = Column(Integer, index=False, unique=False, nullable=False)
    state = Column(String(6), index=False, unique=False, nullable=True) 
    name = Column(Text, index=False, unique=False, nullable=True)
    product = Column(String(50), index=False, unique=False, nullable=True)
    version = Column(Text, index=False, unique=False, nullable=True)
    extra = Column(Text, index=False, unique=False, nullable=True)
    cpe = Column(Text, index=False, unique=False, nullable=True)
    vulnerable = Column(Text, index=True, unique=False, nullable=False)

    def __init__(self,id_major,id_scan,host,protocol,port,state,name,product,version,extra,cpe,vulnerable):
        self.id_major=id_major
        self.id_scan=id_scan
        self.host = host
        self.protocol = protocol
        self.port=port
        self.state = state
        self.name = name
        self.product = product
        self.version = version
        self.extra = extra
        self.cpe = cpe
        self.vulnerable=vulnerable

class scan_status(Base):
    __tablename__ = 'scan_progress'
    id_scan = Column(String(32), primary_key=True)
    id_cut = Column(String(32), primary_key=True)
    status = Column(String(20), index=False,unique=False,nullable=False)
    email = Column(String(100), index=False,unique=False,nullable=False)
    hosts = Column(Text, index=False, unique=False, nullable=False)
    ports = Column(Text, index=False, unique=False, nullable=False)
    HNO = Column(Boolean, index=False, unique=False, nullable=False)
    initiation_date = Column(DateTime)
    ending_date = Column(Text, index=False, unique=False, nullable=True)

    def __init__(self,id_scan,id_cut,status,email,hosts,ports,HNO,initiation_date,ending_date):
        self.id_scan=id_scan
        self.id_cut=id_cut
        self.status=status
        self.email=email
        self.hosts=hosts
        self.ports=ports
        self.HNO=HNO
        self.initiation_date=initiation_date
        self.ending_date=ending_date