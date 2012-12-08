from ip_loc.models import *
from ip_loc.helpers import std_to_decimal_ip as parse_ip
    
def ip_to_ccode(ip):
    """
        Tries to convert the given ip to a country code. Returns None if no object is found.
    """
    
    try:
        ip = parse_ip(ip) #convert to decimal form
        print ip
        objs = IPtoLoc.objects.filter(ip_to__gte=ip, ip_fr__lte=ip)
        print objs
        if objs.exists():
            return objs[0].country_code
    except Exception as e:
        print str(e)
        return None

def check_tor(ip):
    """
        Returns True if a TorNode matches the given node and False otherwise
    """
    ip = parse_ip(ip)
    try:
        node = TorNode.objects.get(ip=ip)
        return True
    except:
        return False