
import linkInventory
# from micros1.configs.config_cli import conf, why it is calling argparse ?
from linkInventory.configs.config_handler import Configs
from linkInventory.db.engine import DataBase

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

c = conf.yml

conf_obj = {"conf": conf}
config_list = [conf_obj, c]

#DOn't import bp1 blueprint  it before all  conf and other  objects are initialized 
from linkInventory.restapi.routes import bp1
bp_list = [bp1]

app = linkInventory.create_app(blue_print_list=bp_list , config_map_list = config_list)

host = c.get('host_name')
port = c.get('host_port')
ssl = c.get('ssl')
ssl_settings = c.get('ssl_settings')

def main():   
    if  ssl == 'enabled':
        app.run(ssl_context=ssl_settings, host = host, port=port, )
    else:
        app.run(host = host, port=port, )
        
