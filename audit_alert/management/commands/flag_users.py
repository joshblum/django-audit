from django.core.management.base import NoArgsCommand

from xss_detect.cron_tasks.xss_parser import XSSParser, XSS_FLAG
from ip_loc.cron_tasks.monitor_users import MonitorUsers, TOR_FLAG, COUNTRY_FLAG

class Command(NoArgsCommand):
    help = 'Run the detection applications'

    def handle(self, *args, **options):
        self.stdout.write('Starting...\n')

        parser = XSSParser([XSS_FLAG])
        parser.run()
        user_monitor = MonitorUsers([COUNTRY_FLAG, TOR_FLAG])
        user_monitor.run()
        
        self.stdout.write('Done \n')




            
