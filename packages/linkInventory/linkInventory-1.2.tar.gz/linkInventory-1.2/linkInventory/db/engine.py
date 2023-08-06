from sqlalchemy import *
from urllib.parse import quote_plus
import pyodbc
from sqlalchemy.orm import mapper, scoped_session, sessionmaker

class DataBase(object):
    
    metadata=MetaData()
    
    def __init__(self, conf):        
        self.yml = conf.yml
        self.dbs = self.yml.get('database')  
        self.driver = self.dbs.get('DRIVER')
        self.server = self.dbs.get('Server')
        self.database = self.dbs.get('Database')
        self.uid = self.dbs.get('UID')
        self.pwd = conf.decrypt_password(self.dbs.get('db_pwd_key_map'))
        self.tds_version = self.dbs.get('TDS_Verson')
        self.port = self.dbs.get('Port')
        self.engine_connect_string = self.dbs.get('engine_connect_string')
        
        self.raw_connection_string = ("DRIVER={};"
                             "Server={};"
                             "Database={};"
                             "UID={};"
                             "PWD={};"
                             "TDS_Version={};"
                             "Port={};").format(self.driver, self.server, self.database, 
                                                self.uid, self.pwd, self.tds_version, self.port)
                             
        self.connection_string = quote_plus(self.raw_connection_string)
        
        self.engine=create_engine(
            'mssql+pyodbc:///?odbc_connect={}'.format(self.connection_string))
        
        self.session=scoped_session(sessionmaker (autocommit=False,
                                                autoflush=False,
                                                bind=self.engine ))         
        self.conn=self.engine.connect()


'''
https://docs.sqlalchemy.org/en/latest/orm/tutorial.html

from linkInventory.db.models  import NetLink
from linkInventory.db.engine import conf, DataBase
db = DataBase(conf)


for instance in db.session.query(NetLink).order_by(NetLink.serial_no):
   print(instance.link_type)
   
query = db.session.query(NetLink).filter_by(serial_no=1)
query.all()
query.first()
query.count()

 

'''