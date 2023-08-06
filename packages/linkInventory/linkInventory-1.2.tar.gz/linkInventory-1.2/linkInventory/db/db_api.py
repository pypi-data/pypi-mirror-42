from linkInventory.db.models import NetLink
from linkInventory.db.engine import DataBase
from linkInventory.configs.config_handler import Configs
from linkInventory.db.engine import DataBase
# from linkInventory.app_run import conf  # This gives circular import error
must_have_keys_in_yml = {'host_name',
                             'host_port',
                             'ssl',
                             'ssl_settings',
                             'database',
                             'secrets'
                             }
 
conf = Configs('linkInventory', must_have_keys_in_yml=must_have_keys_in_yml)

# conf_file='linkInventory/tests/test_data/test_linkInventory_configs.yml'
# conf = Configs('linkInventory', conf_file=conf_file, must_have_keys_in_yml=must_have_keys_in_yml)




db = DataBase(conf)

def get_links(db=db):
         ob = []
         s = db.session.query(NetLink).all()
         #result = conn.execute(s)
         for row in s:
             d = row.to_dict()
             ob.append(d)         
         return ob
     
     
def get_link_by_slno(slno, db=db):
    s = db.session.query(NetLink).filter_by(serial_no=slno).first()
    d = s.to_dict()
    return d
     
     
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