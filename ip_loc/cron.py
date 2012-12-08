import kronos

from ip_loc.cron_tasks.download_tor import DownloadTor
from ip_loc.cron_tasks.download_ip import DownloadIP
from ip_loc.cron_tasks.monitor_users import MonitorUsers

@kronos.register("0 0 * * *")
def daily_cron():
    ip = DownloadIP()
    ip.run()

    user_monitor = MonitorUsers()
    user_monitor.run()

@kronos.register("0 * * * *")   
def hourly_cron():
    tor = DownloadTor()
    tor.run()
