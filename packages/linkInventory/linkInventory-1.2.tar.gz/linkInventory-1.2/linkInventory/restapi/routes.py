from flask import Blueprint
import json
from linkInventory.db.db_api import get_links , get_link_by_slno
 # bp1 is getting it automatically
 
from tokenleaderclient.configs.config_handler import Configs    
from  tokenleaderclient.client.client import Client 
from tokenleaderclient.rbac.enforcer import Enforcer

adminops_bp = Blueprint('adminops_bp', __name__)
auth_config = Configs()
tlclient = Client(auth_config)
enforcer = Enforcer(tlclient)


bp1 = Blueprint('bp1', __name__)

@bp1.route('/list/links', methods=['GET'])
@enforcer.enforce_access_rule_with_token('linkInventory.restapi.routes.get_links_rest')
def get_links_rest(wfc):
         result_from_db_api = get_links()
         concern = ("\n \nThe user belongs to org={}, orgunit={}, dept={}. do you think"
          " that the entire result should be displayed or need filter ?\n".format(
              wfc.org, wfc.orgunit, wfc.department))
         rest_result = json.dumps({"message": result_from_db_api , "concern": concern})
         return rest_result
 

@bp1.route('/list/link/<slno>', methods=['GET'])
@enforcer.enforce_access_rule_with_token('linkInventory.restapi.routes.get_link_by_slno')
def get_link_by_slno_rest(slno, wfc):
    result_from_db_api = get_link_by_slno(slno)
    concern = ("\n \nThe user belongs to org={}, orgunit={}, dept={}. do you think"
          " that the entire result should be displayed or need filter ?\n".format(
              wfc.org, wfc.orgunit, wfc.department))
    rest_result = json.dumps({"message": result_from_db_api , "concern": concern })    
    return rest_result

