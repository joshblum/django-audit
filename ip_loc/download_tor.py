from django_cron import Job
from ip_loc.models import *

from helpers import std_to_decimal_ip as parse_ip

import urllib

class DownloadTor(Job):
    """
        TOR IP address database
    """

    run_every = 5400 #1.5 hours
    DEFAULT_TOR_URL = "https://www.dan.me.uk/torlist/"

    def job(self):
        url = self.DEFAULT_TOR_URL
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

        def parseline(line):
            line = line.replace("\"", "").replace("\n","")
            return line

        data = []
        for l in contents:
            if l.find('...') == -1:
                ip = parse_p(parseline(l))
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


