from django.db import models

class IPtoLoc(models.Model):
    ip_to = models.CharField(max_length=15)
    ip_fr = models.CharField(max_length=15)
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s | %s : %s" %(ip_to, ip_fr, country_name)

    def checkIP(self,ip_check):
    	def parseip(s):
		    ip = 0
		    c = s.split(".")
		    for i in range (3,-1,-1):
		        p = pow(256,i)
		        ip += int(c[abs(3-i)])*p  
		    return ip

		ip_check = parseip(ip_check)
		if(ip_check >= self.ip_to and ip_check <= self.ip_fr):
		    return self.country_code

	def check_user_IPs(self,ip_old,ip_new):
		return self.checkIP(ip_old) == self.checkIP(ip_new)


class TorNode(models.Model):
    ip = models.CharField(max_length=15)

    def __unicode__(self):
        return "%s is a tor node" %(ip)
