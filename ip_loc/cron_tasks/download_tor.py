from ip_loc.models import *
from ip_loc.helpers import std_to_decimal_ip as parse_ip

import urllib

class DownloadTor():
    """
        TOR IP address database
    """
    def __init__(self):

        self.DEFAULT_TOR_URL = "https://www.dan.me.uk/torlist/"

    def run(self):
        url = self.DEFAULT_TOR_URL
        contents = self.get_data(url)
        if self.check_contents(contents):
            data = self.read_data(contents)
            self.clear_table()
            self.add_data(data)
        else:
            print "Unable to read list"

    def get_data(self, url):
        print "Downloading file"
        try:
            data = urllib.urlopen(url)
        except IOError, e:
            print "Can't retrieve %r: %s" % (url, e)
            return None
        return data.readlines()

    def read_data(self, contents):
        print "Reading data "

        def parseline(line):
            line = line.replace("\"", "").replace("\n","")
            return line

        data = []
        for l in contents:
            ip = parse_ip(parseline(l))
            #append TorNode objects for bulk create
            data.append(TorNode(ip=ip))
        return data

    def check_contents(self, contents):
        return  contents[0].find("Umm...") == -1 #stupid error message

    def clear_table(self):
        print "Clearing old objects"
        TorNode.objects.all().delete()

    def add_data(self, data):
        print "Writing new data"
        TorNode.objects.bulk_create(data)
