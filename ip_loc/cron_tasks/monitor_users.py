from ip_loc.models import *
from ip_loc.helpers import std_to_decimal_ip as parse_ip
from ip_loc.query_managers import *

from audit_alert.cron_task_base import CronBase

import urllib

TOR_FLAG = 'flagged_tor'
COUNTRY_FLAG = 'flagged_countries'

class MonitorUsers(CronBase):
    """
        Search AuditLogs and build users that might have been compromised.
    """

    def check_users(self, objs):
        """
            Iterates over objects and determines if the country has changed from previous log ons or if the user is using a TOR node.
        """
        objs = self._clean_objects(objs)
        
        user_map = self._get_user_map(objs)

        country_flags = []
        tor_flags = []
        for username, obj_list in user_map.items():
            c_codes = {}
            tor_nodes = []
            for obj in obj_list:
                ip = obj.action_ip

                #convert to country code
                code = ip_to_ccode(ip)
                if c_codes.get(code):
                    c_codes[code].append(ip)
                else:
                    c_codes[code] = [ip]
                #check if a tor node
                if check_tor(ip):
                    tor_nodes.append(ip)
            if len(c_codes) > 1:
                print username
                country_flags.append({username : c_codes})

            if len(tor_nodes):
                tor_flags.append({username : tor_nodes})

        return {
            COUNTRY_FLAG : country_flags,
            TOR_FLAG : tor_flags,
        }
        