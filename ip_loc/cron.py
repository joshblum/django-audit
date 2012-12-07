from django_cron import cronScheduler, Job
from ip_loc.models import *

import os
import urllib
import zipfile

DEFAULT_IP_URL = "http://software77.net/geo-ip/?DL=2"
DEFAULT_TOR_URL = "https://www.dan.me.uk/torlist/"
DEFAULT_DIRECTORY = "/tmp"

class DownloadIPList(Job):
    """
        Downloads and updates the IP address database
    """
    run_every = 86400 #24 hours

    def job(self):
        url, directory = DEFAULT_IP_URL, DEFAULT_DIRECTORY
        dest = self.get_unzipped(url, directory)
        data = self.read_data(dest)
        self.clear_table()
        self.add_data(data)

    def get_unzipped(self, url, directory):
        self.stdout.write("Downloading file\n")
        name = os.path.join(directory, 'tmp.zip')
        try:
            name, hdrs = urllib.urlretrieve(url, name)
        except IOError, e:
            self.stdout("Can't retrieve %r to %r: %s\n" % (url, directory, e))
            return
        try:
            z = zipfile.ZipFile(name)
        except zipfile.error, e:
            self.stdout("Bad zipfile (from %r): %s\n" % (url, e))
            return
        for n in z.namelist():
            dest = os.path.join(directory, n)
            destdir = os.path.dirname(dest)
            if not os.path.isdir(destdir):
                os.makedirs(destdir)
            data = z.read(n)
            f = open(dest, 'w')
            f.write(data)
            f.close()
        z.close()
        os.unlink(name)
        return dest

    def read_data(self, dest):
        self.stdout.write("Reading data from %s\n" % dest)
        
        # def parseip(ip):
        #     ip = int(ip)
        #     output = ""
        #     for i in range (3,-1,-1):
        #         div = pow(256,i)
        #         output += str(ip/div) +"."
        #         ip = ip % div        
        #     return output[0:-1]

        def parseline(line):
            line = line.replace("\"", "").replace("\n","")
            params = line.split(",")
            return params[0], params[1], params[4], params[6]

        f = open(dest)

        data = []
        for l in f:
            if l.find('#') == -1:
                ip_to, ip_fr, country_code, country_name = parseline(l)
                #append IPtoLoc objects for bulk create
                data.append(IPtoLoc(ip_to=ip_to, ip_fr=ip_fr, country_code=country_code, country_name=country_name))
        
        f.close()
        os.unlink(dest)

        return data

    def clear_table(self):
        self.stdout.write("Clearing old objects\n")
        IPtoLoc.objects.all().delete()

    def add_data(self, data):
        self.stdout.write("Writing new data\n")
        IPtoLoc.objects.bulk_create(data)

class DownloadTor(Job):
    """
        TOR IP address database
    """

    run_every = 5400 #1.5 hours

    def job(self):
        url = DEFAULT_TOR_URL
        contents = self.get_data(url)
        if(contents != None)
            data = self.read_data(contents)
            self.clear_table()
            self.add_data(data)

    def get_data(self, url):
        self.stdout.write("Downloading file\n")
        try:
            data = urllib.urlopen(url)
        except IOError, e:
            self.stdout("Can't retrieve %r: %s\n" % (url, e))
            return None
        return data

    def read_data(self, contents):
        self.stdout.write("Reading data from %s\n" % dest)
        
        def parseip(s):
            ip = 0
            c = s.split(".")
            for i in range (3,-1,-1):
                p = pow(256,i)
                ip += int(c[abs(3-i)])*p  
            return ip

        def parseline(line):
            line = line.replace("\"", "").replace("\n","")
            return line

        data = []
        for l in contents:
            if l.find('...') == -1:
                ip = parseip(parseline(l))
                #append TorNode objects for bulk create
                data.append(Tor_Node(ip=ip))
        return data

    def clear_table(self):
        self.stdout.write("Clearing old objects\n")
        Tor_Node.objects.all().delete()

    def add_data(self, data):
        self.stdout.write("Writing new data\n")
        Tor_Node.objects.bulk_create(data)

cronScheduler.register(DownloadIPList)
cronScheduler.register(DownloadTor)


