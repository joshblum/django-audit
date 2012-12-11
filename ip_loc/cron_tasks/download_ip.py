from ip_loc.models import *

import os
import urllib
import zipfile


class DownloadIP():
    """
        Downloads and updates the IP address database
    """

    def __init__(self, filename=None):
        if not filename:
            filename = "http://software77.net/geo-ip/?DL=2"
        
        self.DEFAULT_IP_URL = filename
        self.DEFAULT_IP_DIRECTORY = "/tmp"

    def run(self):
        url, directory = self.DEFAULT_IP_URL, self.DEFAULT_IP_DIRECTORY
        if not os.path.exists(directory):
            os.makedirs(directory)
        dest = self.get_unzipped(url, directory)
        data = self.read_data(dest)
        self.clear_table()
        self.add_data(data)
        os.removedirs(directory)

    def get_unzipped(self, url, directory):
        print "Downloading IP list file"
        name = os.path.join(directory, 'tmp.zip')
        try:
            name, hdrs = urllib.urlretrieve(url, name)
        except IOError, e:
            print "Can't retrieve %r to %r: %s" % (url, directory, e)
            return
        try:
            z = zipfile.ZipFile(name)
        except zipfile.error, e:
            print "Bad zipfile (from %r): %s" % (url, e)
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
        print "Reading data from %s" % dest

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
        print "Clearing old objects"
        IPtoLoc.objects.all().delete()

    def add_data(self, data):
        print "Writing new data"
        IPtoLoc.objects.bulk_create(data)