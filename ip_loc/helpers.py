def std_to_decimal_ip(s):
    """
        Converts IP in standard form: 192.186.1.1. to decimal
    """
    ip = 0
    c = s.split(".")
    for i in range (3,-1,-1):
        p = pow(256,i)
        ip += int(c[abs(3-i)])*p  
    return ip

def decimal_to_std_ip(ip):
    """"
        Converts IP form decimal to standard form
    """
    ip = int(ip)
    output = ""
    for i in range (3,-1,-1):
        div = pow(256,i)
        output += str(ip/div) +"."
        ip = ip % div        
    return output[0:-1]