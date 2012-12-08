from ip_loc.models import *
from ip_loc.helpers import std_to_decimal_ip as parse_ip
    
def ip_to_ccode(ip):
    """
        Tries to convert the given ip to a country code. Returns None if no object is found.
    """

    ip = int(parse_ip(ip)) #convert to decimal form
    objs = IPtoLoc.objects.filter(ip_to__lte=ip, ip_fr__gte=ip)
    if objs.exists():
        return objs[0].country_code
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