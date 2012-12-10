import kronos

from xss_detect.cron_tasks.xss_parser import XSSParser, XSS_FLAG

@kronos.register("0 0 * * *")
def xss_daily_cron():
    parser = XSSParser([XSS_FLAG])
    parser.run()