from django.core.management.base import BaseCommand
from ip_loc.models import *

import urllib

DEFAULT_URL = "https://www.dan.me.uk/torlist/"

class Command(BaseCommand):
    help = 'TOR IP address database'

    def handle(self, *args, **options):
        url = self.get_args(*args)
        contents = self.get_data(url)
        if(contents != None)
            data = self.read_data(contents)
            self.clear_table()
            self.add_data(data)
    
    def get_args(self, *args):
        try:
            url = str(args[0])
        except:
            url = DEFAULT_URL
        self.stdout.write('Assigning url to: %s \n'%(url, directory))
        return url


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
        
        def parseip(ip):
            ip = int(ip)
            output = ""
            for i in range (3,-1,-1):
                div = pow(256,i)
                output += str(ip/div) +"."
                ip = ip % div        
            return output[0:-1]

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

        