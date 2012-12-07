from django_cron import cronScheduler

from download_tor import DownloadTor
from download_ip import DownloadIP

cronScheduler.register(DownloadIP)
cronScheduler.register(DownloadTor)