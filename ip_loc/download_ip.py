from django_cron import Job

from helpers import *

import os
import urllib
import zipfile


class DownloadIP(Job):
    """
        Downloads and updates the IP address database
    """
    run_every = 86400 #24 hours
    DEFAULT_IP_URL = "http://software77.net/geo-ip/?DL=2"
    DEFAULT_IP_DIRECTORY = "/tmp"

    def job(self):
        url, directory = self.DEFAULT_IP_URL, self.DEFAULT_IP_DIRECTORY
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