import math

f = open("iptocountry.csv")

def parseip(ip):
    output = ""
    for i in range (3,-1,-1):
        div = pow(256,i)
        output += str(ip/div) +"."
        ip = ip % div        
    return output[0:-1]

def parseline(line):
    line = line.replace("\"", "").replace("\n","")
    params = line.split(",")
    return int(params[0]), int(params[1]), params[4], params[6]

for l in f:
    to,fr,cncode, cn = parseline(l)
    print parseip(to), parseip(fr),cncode, cn
