# from sqlalchemy import *
# import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
 
class NetLink(Base):
    
    __tablename__ = 'vw_comm_links'
    
    serial_no = Column(Integer, primary_key=True)
    circuit_id = Column( String(120))
    division_name = Column(String(120))
    fa_end = Column(String(500))
    bandwidth =  Column(String(50))
    link_type = Column(String(50))
 
    def __repr__(self):
        return '<NetLink (serial_no=%r, circuit_id=%s>' % (self.serial_no, self.circuit_id)
    
    def to_dict(self):
        
        d = {"serial_no": self.serial_no, "circuit_ID": self.circuit_id, 
             "division_name": self.division_name, "fa_end": self.fa_end,
             "bandwidth": self.bandwidth,  "link_type": self.link_type}
        return d


 